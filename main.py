#GroceryStoreSim.py
#Name: Tim Weixelman
#Date: 4/27
#Assignment:Lab 11

import simpy
import random
eventLog = []
waitingShoppers = []
idleTime = 0

def shopper(env, id):
    arrive = env.now
    items = random.randint(5, 40)
    shoppingTime = items // 2 # shopping takes 1/2 a minute per item.
    yield env.timeout(shoppingTime)
    # join the queue of waiting shoppers
    waitingShoppers.append((id, items, arrive, env.now))

def checker(env):
    global idleTime
    while True:
        while len(waitingShoppers) == 0:
            idleTime += 1
            yield env.timeout(1) # wait a minute and check again

        customer = waitingShoppers.pop(0)
        items = customer[1]
        checkoutTime = items // 10 + 1
        yield env.timeout(checkoutTime)

        eventLog.append((customer[0], customer[1], customer[2], customer[3], env.now))

def customerArrival(env):
    customerNumber = 0
    while True:
        customerNumber += 1
        env.process(shopper(env, customerNumber))
        yield env.timeout(1) #New shopper every two minutes

def processResults():
    totalWait = 0
    totalShoppers = 0

    for e in eventLog:
        waitTime = e[4] - e[3] #depart time - done shopping time
        totalWait += waitTime
        totalShoppers += 1

    avgWait = totalWait / totalShoppers

    print("The average wait time was %.2f minutes." % avgWait)
    print("The total idle time was %d minutes" % idleTime)

def main():
    numberCheckers = 8

    env = simpy.Environment()

    env.process(customerArrival(env))
    for i in range(numberCheckers):
        env.process(checker(env))

    env.run(until=180 )
    print(len(waitingShoppers))
    processResults()

if __name__ == '__main__':
    main()