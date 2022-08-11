import socket
from time import sleep
import threading
import numpy as np
import random
import matplotlib.pyplot as plt
import json
import yaml

with open('params.yml', 'rb') as f:
    params = yaml.safe_load(f.read())

MAX_ITERS = params['MAX_ITERS']
NUM_COINS = params['NUM_COINS']
MAX_RUNS = params['MAX_RUNS']

HOST_PORT = params['SERVER_PORT']
HOST_ADDR = params['SERVER_IP']


class Player:
    def __init__(self, name, algorithm):
        self.name = name
        self.client = None
        self.host_port = HOST_PORT
        self.host_addr = HOST_ADDR
        self.algorithm = algorithm
        self.iter = 0
        self.run = 0
        self.score = 0
        self.tossed = np.zeros(NUM_COINS)
        self.heads = np.zeros(NUM_COINS)
        self.em = [[[0.0 for j in range(NUM_COINS)]] for i in range(MAX_RUNS)] #final shape MAX_RUNS,MAX_ITERS+1,NUM_COINS

    def connect(self):
        # self.name = #input("Enter your username: ")
        print( f"Your name: {self.name}")
        self.connect_to_server(self.name)

    def choose(self,arg):
        if NUM_COINS <= arg or 0 > arg:
            print("Choice out of range!")
            assert False
        self.choice = arg
        print(f"Your choice: {self.choice}")

        if self.client:
            dataToSend = str(self.choice)
            self.client.send(dataToSend.encode())

    def update(self,choice,outcome):
        self.tossed[choice] += 1
        self.heads[choice] += outcome
        curr_em = self.em[self.run][self.iter].copy()
        curr_em[choice] = float(self.heads[choice])/self.tossed[choice]
        self.em[self.run].append(curr_em)
        self.iter += 1
        if self.iter == MAX_ITERS:
            self.iter = 0
            self.run += 1
            self.tossed = np.zeros(NUM_COINS)
            self.heads = np.zeros(NUM_COINS)

    def connect_to_server(self,name):
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((str(self.host_addr), int(self.host_port)))
            self.client.send(self.name.encode())  # Send name to server after connecting

            # # start a thread to keep receiving message from server
            # # do not block the main thread :)
            # threading._start_new_thread(self.receive_message_from_server, (self.client, "m"))
            self.receive_message_from_server(self.client, "m")
        except ConnectionRefusedError as e:
            print(f"Cannot connect to host: {self.host_addr} on port: {str(self.host_port)} Server may be Unavailable. Try again later")
            print(f"LOG: {e}")

    def receive_message_from_server(self, sck, m):
        print("Connection Established")
        while True:
            from_server = str(sck.recv(4096).decode())

            if not from_server:
                break

            if from_server.startswith("welcome"):
                print(
                    f"Server says: Welcome {self.name} !"
                )
                self.choose(self.algorithm(self.tossed,self.heads))
            elif from_server.startswith("out"):
                outcome = int(from_server[3:].split('$')[0])
                print(f"Outcome: {outcome}")
                self.update(self.choice,outcome)
                if self.run < MAX_RUNS :
                    self.choose(self.algorithm(self.tossed,self.heads))
            elif from_server.startswith("res"):
                score,p_vals = from_server[3:].split('$')
                score = float(score)
                self.p_vals = json.loads(p_vals)
                print(f"Total Score : {score}")
                print(f"p values : {self.p_vals}")
                if MAX_RUNS > 1:
                    self.show_avg_run()
                self.show_first_run()

        sck.close()

    def show_avg_run(self):
        """
        Shows a graph of average reward over iterations
        """
        #Empirical Average Lists
        em = np.array(self.em)
        fig, ax = plt.subplots()
        t = np.linspace(1,MAX_ITERS,num = MAX_ITERS)

        em_avg = np.mean(em[:,1:], axis = 0).T # shape: NUM_COINS, MAX_ITERS+1

        for p in self.p_vals:
            plt.axhline(y=p, linestyle='--',alpha=0.3)
        # plt.axhline(y=p2, color='g', linestyle='--',alpha=0.3)
        # plt.axhline(y=p3, color='b', linestyle='--',alpha=0.3)

        # print(em_avg,em.shape)
        for i in range(NUM_COINS):
            plt.plot(t, em_avg[i], label = f"Coin {i+1}")
        plt.title("Time variation of empirical averages (averaged over all runs)")
        plt.legend(loc = "upper left")
        plt.grid()
        plt.show()

    def show_first_run(self):
        """
        Shows a graph of average reward over iterations
        """
        #Empirical Average Lists
        em = np.array(self.em)[0,1:].T
        fig, ax = plt.subplots()
        t = np.linspace(1,MAX_ITERS,num = MAX_ITERS)

        for p in self.p_vals:
            plt.axhline(y=p, linestyle='--',alpha=0.3)
        # plt.axhline(y=p2, color='g', linestyle='--',alpha=0.3)
        # plt.axhline(y=p3, color='b', linestyle='--',alpha=0.3)

        for i in range(NUM_COINS):
            plt.plot(t, em[i], label = f"Coin {i+1}")
        plt.title("Time variation of empirical averages (in the first run)")
        plt.legend(loc = "upper left")
        plt.grid()
        plt.show()