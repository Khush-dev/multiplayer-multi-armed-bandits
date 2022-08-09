import socket, sys
from time import sleep
import threading
import numpy as np
import random
import matplotlib.pyplot as plt
import json

## PARAMETERS
MAX_ITERS = 100
MAX_RUNS = 1000
NUM_COINS = 3

def algorithm(tossed,heads):
    """
    Enter your Algorithm in this functions.
    tossed[i] contains the number of times the 'i'th coin is tossed/'i'th arm is pulled
    heads[i] contains the number of times the 'i'th coin gave heads/'i'th arm got reward 1
    This data is assumed to be sufficient.
    """
    ## TODO: implement algorithms

    # # EG2
    # for i,num in enumerate(tossed):
    #     if num == 0:
    #         return i
    # eps = 0.3
    # return random.choice(range(NUM_COINS)) if sum(tossed)/MAX_ITERS < eps else np.argmax([float(h)/total for h,total in zip(heads,tossed)])


    # # EG2-corrected
    # for i,num in enumerate(tossed):
    #     if num == 0:
    #         return i
    # eps = 1/np.sqrt(sum(tossed))
    # return random.choice(range(NUM_COINS)) if random.random() < eps else np.argmax([h/total for h,total in zip(heads,tossed)])


    # # EG3
    # for i,num in enumerate(tossed):
    #     if num == 0:
    #         return i
    # eps = 0.3
    # return random.choice(range(NUM_COINS)) if random.random() < eps else np.argmax([h/total for h,total in zip(heads,tossed)])


    # # EG3-corrected
    # for i,num in enumerate(tossed):
    #     if num == 0:
    #         return i
    # eps = 1/(sum(tossed)+1)
    # return random.choice(range(NUM_COINS)) if random.random() < eps else np.argmax([h/total for h,total in zip(heads,tossed)])
    
    # Baseline - random choice
    return random.choice(range(NUM_COINS))



class Player:
    def __init__(self, name, host_addr, host_port):
        self.name = name
        self.client = None
        self.host_port = HOST_PORT
        self.host_addr = HOST_ADDR 
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
        except Exception as e:
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
                self.choose(algorithm(self.tossed,self.heads))
            elif from_server.startswith("out"):
                outcome = int(from_server[3:])
                print(f"Outcome: {outcome}")
                self.update(self.choice,outcome)
                self.choose(algorithm(self.tossed,self.heads))
            elif from_server.startswith("res"):
                score,p_vals = from_server[3:].split('$')
                score = float(score)
                self.p_vals = json.loads(p_vals)
                print(f"Total Score : {score}")
                print(f"p values : {self.p_vals}")
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

    

# network details
if len(sys.argv) != 3:
    print(f"Too less or too many arguments! {len(sys.argv)} != 3")
    assert False
else:
    HOST_ADDR = sys.argv[1]
    name = sys.argv[2]
HOST_PORT = 8080


player = Player(name, HOST_ADDR, HOST_PORT)
player.connect()