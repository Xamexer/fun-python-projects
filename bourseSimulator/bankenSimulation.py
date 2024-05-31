import random
import socket
import grpc
import pandas as pd
import logging
import re
import time
import os
import urllib.parse
import http.server
from concurrent import futures
from threading import Thread
from connection import *
import transfer_pb2_grpc
import transfer_pb2
import paho.mqtt.client as mqtt

# Constants
MQTT_BROKER = "mqtt.eclipseprojects.io"
LOWER_MONEY_CAP = 1

class Bank:
    def __init__(self, name):
        self.name = name
        self.vaultCash = float(random.randrange(0, 100000))
        self.portfolio = 0
        self.setSecurities()
        self.startingPortfolio()
        self.socket = UdpSocket(socket.gethostbyname(socket.gethostname()), 8080)

    def receive(self):
        msg, addr = self.socket.receive()
        self.updateByBourseTransaction(msg)
        logging.info(f'From {addr}: {msg.decode()}')

    def setSecurities(self):
        self.securities = pd.DataFrame({
            'abbreviation': securitiesList['abbreviation'],
            'currentPrice': securitiesList['currentPrice'],
            'count': [random.randrange(0, 1000) for _ in range(len(securitiesList))]
        })
        print(self.securities)

    def startingPortfolio(self):
        self.portfolio = sum(self.securities['count'] * self.securities['currentPrice'])
        self.portfolio += self.vaultCash
        print(f"Vault value: {self.vaultCash}")
        print(f"Starting portfolio value: {self.portfolio}")

    def updateByBourseTransaction(self, msg: bytes):
        self.portfolio = 0
        parts = msg.decode().split(",")
        security, new_price, change_count = parts[0], float(parts[1]), int(parts[2])

        print(f"The price of {security} security got updated: {self.securities.loc[self.securities['abbreviation'] == security, 'currentPrice'].iloc[0]} -> {new_price}")
        
        if change_count < 0 and self.securities.loc[self.securities['abbreviation'] == security, 'count'].iloc[0] < -change_count:
            print(f"BANK {my_bank} doesn't have enough {security} securities to sell")
            self.updatePortfolioValues(security, new_price)
            return

        if change_count > 0:
            print(f"BANK {my_bank} just bought {change_count} {security} securities.")
        else:
            print(f"BANK {my_bank} just sold {-change_count} {security} securities.")

        self.securities.loc[self.securities['abbreviation'] == security, 'count'] += change_count
        self.updatePortfolioValues(security, new_price)

    def updatePortfolioValues(self, security, new_price):
        self.securities.loc[self.securities['abbreviation'] == security, 'currentPrice'] = new_price
        self.portfolio = sum(self.securities['count'] * self.securities['currentPrice']) + self.vaultCash
        print(self.securities)
        print(f"Vault value: {self.vaultCash}")
        print(f"New portfolio value: {self.portfolio}")
        if self.portfolio < LOWER_MONEY_CAP:
            self.requestMoney(random.randrange(10000, 20000))

    def updateByWorkerTransaction(self, parts):
        security, change_count = parts[0], int(parts[1])
        if change_count < 0 and self.securities.loc[self.securities['abbreviation'] == security, 'count'].iloc[0] < -change_count:
            return False

        print(f"BANK {my_bank} just {'bought' if change_count > 0 else 'sold'} {abs(change_count)} {security} securities via Web-Interface")
        self.securities.loc[self.securities['abbreviation'] == security, 'count'] += change_count
        self.updatePortfolioValues(security, self.securities.loc[self.securities['abbreviation'] == security, 'currentPrice'].iloc[0])
        return True

    def updateByCustomerTransaction(self, cashTransaction):
        if self.portfolio < LOWER_MONEY_CAP or self.portfolio < cashTransaction:
            self.requestMoney(random.randrange(10000, 20000))

        self.vaultCash += cashTransaction
        self.portfolio = sum(self.securities['count'] * self.securities['currentPrice']) + self.vaultCash
        print(f"A Customer just {'deposited' if cashTransaction > 0 else 'withdrew'} {abs(cashTransaction)} $ from BANK {my_bank}")
        print(self.securities)
        print(f"Vault value: {self.vaultCash}")
        print(f"New portfolio value: {self.portfolio}")
        return cashTransaction < 0

    def requestMoney(self, amount):
        for index in range(num_banks):
            if index == my_bank:
                continue
            channel = grpc.insecure_channel(f'{socket.gethostbyname(f"bank_server{index}")}:{50051 + index}')
            client = transfer_pb2_grpc.BankInteractionStub(channel)
            request = transfer_pb2.LendRequest(amount=amount, bank=my_bank)
            response = client.LendMoney(request)
            if response.lendAccept:
                print(f"You just got {request.amount} $ from bank {index}")
                self.vaultCash += request.amount
                return f"You just got {request.amount} $ from bank {index}"
            else:
                print("Lending money rejected")
        return "Unfortunately no bank lends your bank any money"

def run_webserver():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(('', 80))
        server_socket.listen(1)
        print(f'Server running at http://localhost:{my_port - my_bank}')
        
        while True:
            client_socket, client_address = server_socket.accept()
            with client_socket:
                request = client_socket.recv(1024).decode('utf-8')
                response_content = handle_request(request)
                response = create_response(response_content)
                client_socket.sendall(response.encode('utf-8'))

def handle_request(request):
    if request.startswith('GET / ') or request.startswith('GET /index.html'):
        return open('index.html', 'r').read()
    if request.startswith('GET'):
        return handle_get_request(request)
    if request.startswith('POST'):
        return handle_post_request(request)
    return 'Invalid POST request.'

def create_response(content):
    backButton = '<form action="/index.html" method="get"><input type="submit" value="Back"></form>'
    response = 'HTTP/1.1 200 OK\r\n'
    response += 'Content-Type: text/html\r\n'
    response += f'Content-Length: {len(content) + len(backButton)}\r\n'
    response += '\r\n'
    response += content
    response += backButton
    return response

def handle_post_request(request):
    params = re.findall(r'\w+=([\w-]+)', request.split('\r\n\r\n')[-1])
    if request.startswith('POST /workerAction'):
        return process_worker_action(params)
    if request.startswith('POST /customerAction'):
        return process_customer_action(params)
    return 'Invalid POST request.'

def process_worker_action(params):
    if len(params) != 2 or not params[1].isdigit():
        return 'Invalid POST request.'
    security, count = params[0], int(params[1])
    if security in activeBank.securities['abbreviation'].values and count != 0:
        if activeBank.updateByWorkerTransaction([security, count]):
            action = 'got' if count > 0 else 'lost'
            return f'BANK {my_bank} {action} {abs(count)} {security} security'
        return f'Your bank doesn\'t have enough {security} securities'
    return 'Please fill out all boxes'

def process_customer_action(params):
    if len(params) != 1 or not params[0].isdigit():
        return 'Invalid POST request.'
    cashTransaction = int(params[0])
    if cashTransaction == 0:
        return 'Please enter a value'
    if cashTransaction < activeBank.portfolio:
        if activeBank.updateByCustomerTransaction(-cashTransaction):
            return f'You just paid out {cashTransaction} $ from BANK {my_bank}'
        return f'You just deposited {-cashTransaction} $ to BANK {my_bank}'
    return 'Your bank is broke'

def handle_get_request(request):
    if request.startswith('GET /portfolio'):
        return f'The result is: {activeBank.portfolio} $'
    if request.startswith('GET /request'):
        return activeBank.requestMoney(random.randrange(10000, 20000))
    return 'Invalid GET request.'

class TransferServicer(transfer_pb2_grpc.BankInteractionServicer):
    def LendMoney(self, request, context):
        lend_accept = request.amount * 2.5 <= activeBank.portfolio
        if lend_accept:
            activeBank.vaultCash -= request.amount
            print(f"You just lent {request.amount}€ to bank {request.bank}")
        return transfer_pb2.LendResponse(lendAccept=lend_accept)

def lend_server():
    server = grpc.server(futures.ThreadPoolExecutor())
    transfer_pb2_grpc.add_BankInteractionServicer_to_server(TransferServicer(), server)
    server.add_insecure_port(f'[::]:{50051 + my_bank}')
    server.start()
    print(f"Server started on port {50051 + my_bank}...")
    server.wait_for_termination()

def mqtt_send():
    while True:
        client.publish(f"portfolio/{my_bank}", activeBank.portfolio)
        print(f"Just published bank{my_bank} portfolio")
        global start_time
        start_time = time.time()
        time.sleep(4)

def mqtt_receive():
    client.loop_start()
    for index in range(num_banks):
        if index == my_bank:
            client.subscribe(f"portfoliohelper/{index}")
            continue
        client.subscribe(f"portfolio/{index}")
    client.on_message = on_message

def on_message(client, userdata, message):
    topic = message.topic.split("/")
    payload = message.payload.decode("utf-8")
    if topic[0] == "portfoliohelper":
        process_portfoliohelper_message(topic, int(payload))
    elif topic[0] == "portfolio":
        process_portfolio_message(topic, float(payload))

def process_portfoliohelper_message(topic, payload):
    if payload > 1:
        if my_bank == int(topic[1]):
            print(f"{payload}x banks lent you 20000$ in total")
            activeBank.vaultCash += 20000
            print(f"--- {time.time() - start_time} seconds ---")
        elif help[int(topic[1])] == 1:
            activeBank.vaultCash -= 20000 / payload
            print(f"You lent bank {int(topic[1])} about {20000 / payload}$")
    elif my_bank == int(topic[1]):
        print("Not enough banks found for lending")
    help[int(topic[1])] = 0

def process_portfolio_message(topic, payload):
    if payload < 20000:
        help[int(topic[1])] = 0
        if payload * 2 < activeBank.portfolio:
            help[int(topic[1])] = 1
        client.publish(f"help/{int(topic[1])}", help[int(topic[1])])

# Initialization and startup
securitiesList = pd.read_excel("securities.xlsx")
my_bank = int(os.getenv("MY_BANK", 0))
num_banks = int(os.getenv("NUM_BANKS", 0))
my_port = int(os.getenv("PORT_PREFAB", 0))
activeBank = Bank(f"BANK {my_bank}")
help = [0] * num_banks
print("Bank got created")
activeBank.socket.bind()

client = mqtt.Client(f"bankqueue{my_bank}")
client.connect(MQTT_BROKER)

t1 = Thread(target=lend_server)
t1.start()

t2 = Thread(target=run_webserver)
t2.start()

t3 = Thread(target=mqtt_send)
t3.start()

t4 = Thread(target=mqtt_receive)
t4.start()

while True:
    activeBank.receive()
