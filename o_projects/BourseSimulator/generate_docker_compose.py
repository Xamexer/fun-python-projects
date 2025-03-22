import os
import random
import yaml
import pandas as pd

num_banks = int(os.getenv("NUM_BANKS", 0))
num_bourses = int(os.getenv("NUM_BOURSES", 0))
securitiesList = pd.read_excel("securities.xlsx")['abbreviation']
bourseSecurities = [[] for _ in range(num_bourses)]

amountOfSecurities = len(securitiesList) // num_bourses
for i in range(num_bourses):
    for j in range(amountOfSecurities):
        cut = random.randrange(0,len(securitiesList))
        bourseSecurities[i].append(securitiesList[cut])
        securitiesList = securitiesList.drop(cut)
        securitiesList.reset_index(drop=True,inplace=True)
       
temp = len(securitiesList)
for i in range(temp):
    cut = random.randrange(0,len(securitiesList))
    bourseSecurities[random.randrange(0,num_bourses)].append(securitiesList[cut])
    securitiesList = securitiesList.drop(cut)
    securitiesList.reset_index(drop=True,inplace=True)

services = {}
container = 0
# Create the Bank services
for i in range(0, num_banks):
    service_name = f"bank_server{i}"
    service = {
        "build": {
            "context": ".",
            "dockerfile": "bank.dockerfile"
        },
        "networks": {
            "mynetwork": {}
        },
        "environment": {
            "PORT_PREFAB": 8081 + num_banks + container  ,
            "NUM_BANKS": num_banks,
            "NUM_BOURSES": num_bourses,
            "MY_BANK": i
        },
        "ports" : [
        f"{8081 + container}:80",f"{50051+i}"
    ],
        "volumes": [
            {
                "type": "bind",
                "source": f"./logs/bank.log",
                "target": "/code/bank.log",
                "read_only": False
            }
        ]
    }
    services[service_name] = service
    container += 1

# Create the Bourse services
for i in range(0, num_bourses):
    service_name = f"bourse_client{i}"
    service = {
        "build": {
            "context": ".",
            "dockerfile": "bourse.dockerfile"
        },
        "networks": {
            "mynetwork": {}
        },
        "environment": {
            "PORT_PREFAB": 8081 + num_banks + container,
            "NUM_BANKS": num_banks,
            "NUM_BOURSES": num_bourses,
            "MY_BOURSE": i,
            "MY_SECURITIES": (','.join(bourseSecurities[i])),
            "LOW_COURSE": random.randrange(0,100),
            "HIGH_COURSE": random.randrange(0,100)
        },
        "depends_on": [f"bank_server{i}" for i in range(0, num_banks)],
        "ports" : [
        f"{8081 + container}:80"
    ],
        "volumes": [
            {
                "type": "bind",
                "source": f"./logs/bourse.log",
                "target": "/code/bourse.log",
                "read_only": False
            }
        ]
    }
    services[service_name] = service
    container += 1
service_name = "broker_client"
service = {
        "build": {
            "context": ".",
            "dockerfile": "broker.dockerfile"
        },
        "networks": {
            "mynetwork": {}
        },
        "environment": {
            "NUM_BANKS": num_banks,
        },
        "depends_on": [f"bank_server{i}" for i in range(0, num_banks)],
        "volumes": [
            {
                "type": "bind",
                "source": f"./logs/bourse.log",
                "target": "/code/bourse.log",
                "read_only": False
            }
        ]
    }
services[service_name] = service

docker_compose = {
    "version": "3",
    "services": services,
    "networks": {
        "mynetwork": {}
    }
}
print(docker_compose)

with open("docker-compose.yml", "w") as f:
    yaml.dump(docker_compose, f)
