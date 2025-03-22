import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import logging
import sys
import time
from connection import *

# Configure logging
logging.basicConfig(
    filename='bourse.log',
    level=logging.DEBUG,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)

class Bourse:
    def __init__(self, name, securities):
        self.name = name
        self.ownSecurities = securities
        self.sockets = self.initialize_sockets()

    def initialize_sockets(self):
        sockets = []
        for index in range(num_banks):
            bank_address = socket.gethostbyname(f"bank_server{index}")
            sockets.append(UdpSocket(bank_address, 8080))
        return sockets

    def conv_string(self, security):
        return f'{security["abbreviation"]},{security["currentPrice"]}'

    def fluctuate(self):
        """Fluctuate the price of each security."""
        for index in range(len(self.ownSecurities)):
            random_fluctuation = random.uniform(1 - low_course/100000, 1 + high_course/100000)
            self.ownSecurities.at[index, 'currentPrice'] *= random_fluctuation

    def send(self):
        security = self.ownSecurities.sample().iloc[0]
        conv_string = self.conv_string(security)
        amount = random.choice([i for i in range(-5, 6) if i != 0])
        conv_string += f",{amount},{self.name}"
        logging.info(conv_string)
        self.sockets[random.randrange(num_banks)].send(conv_string.encode())

def load_securities():
    securities_list = pd.read_excel("securities.xlsx")
    chosen_securities = os.getenv("MY_SECURITIES", "").split(",")
    securities = pd.DataFrame({'abbreviation': chosen_securities, 'name': '', 'currentPrice': 0.0})

    for index, abbreviation in enumerate(chosen_securities):
        security = securities_list[securities_list['abbreviation'] == abbreviation].iloc[0]
        securities.at[index, 'name'] = security['name']
        securities.at[index, 'currentPrice'] = security['currentPrice']
    
    return securities

def main():
    global num_banks, low_course, high_course
    num_banks = int(os.getenv("NUM_BANKS", "1"))
    low_course = int(os.getenv("LOW_COURSE", "200"))
    high_course = int(os.getenv("HIGH_COURSE", "200"))
    bourse_number = int(os.getenv("MY_BOURSE", "1"))
    port_prefab = int(os.getenv("PORT_PREFAB", "8080"))

    securities = load_securities()
    bourse = Bourse(f"BOURSE {bourse_number}", securities)

    age = 0
    plt.ion()
    fig, ax = plt.subplots()
    colors = ['r', 'g', 'b', 'k', 'm', 'y']
    prev_price = []
    prev_age = 0

    while True:
        bourse.fluctuate()
        bourse.send()
        time.sleep(0.5)

        if True:
            price = bourse.ownSecurities['currentPrice']
            age += 1

            if age > 1:
                for i in range(len(price)):
                    ax.plot([prev_age, age], [prev_price[i], price[i]], colors[i % len(colors)])

            ax.legend(bourse.ownSecurities['name'], loc='upper right')
            prev_price = price.copy()
            prev_age = age

            plt.draw()
            plt.pause(0.0001)

if __name__ == "__main__":
    main()