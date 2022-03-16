import json
import requests
import random
#import numpy as np

url = "https://24zl01u3ff.execute-api.us-west-1.amazonaws.com/beta"

def get_data(url)->list:
    url = requests.get(url)
    text = url.text

    data = json.loads(text)
    
    try:
        d = data['body']
        temp = list()
        for i in d:
            if i == '0': temp.append(0)
            elif i == '1': temp.append(1)
        return temp
        
    except:
        get_data(url)


def create_dataset(url, iterations = 30)->dict:
    data = dict()
    for _ in range(iterations):
        data[_] = get_data(url)
    return data

def expectation_step(data, thetaA, thetaB)->(float, float, float, float):
    
    headsA, headsB, tailsA, tailsB = 0,0,0,0

    for i in range(len(data)):
        probA = likelihood(i, data, thetaA)
        probB = likelihood(i, data, thetaB)
        #normalization for probabilities
        pA = probA/(probA+probB)
        pB = probB/(probA+ probB)

        headsA += pA*data[i].count(1)
        tailsA += pA*data[i].count(0)
        headsB += pB*data[i].count(1)
        tailsB += pB*data[i].count(0)

    return headsA, tailsA, headsB, tailsB

def maximization_step(headsA, headsB, tailsA, tailsB)->(float, float):
    
    thetaA = headsA/(headsA+tailsA)
    thetaB = headsB/(headsB+tailsB)
    
    return thetaA, thetaB

def likelihood(i, data, theta)->float:
    return pow(theta, data[i].count(1))* pow(1-theta, data[i].count(0))


def find_theta(data, iterations = 30)->(float, float):
    thetaA, thetaB = random.random(), random.random()

    for _ in range(iterations):
        headsA, tailsA, headsB, tailsB = expectation_step(data, thetaA, thetaB)
        thetaA, thetaB = maximization_step(headsA, headsB, tailsA, tailsB)

    print("The probalities of heads for coin A: %0.3f , coin B: %0.3f" %(thetaA, thetaB))
    return (thetaA, thetaB)

X = create_dataset(url)
find_theta(X)