import tkinter as tk
import socket, sys
import threading
import matplotlib.pyplot as plt
import numpy as np
from time import sleep, time
import random
import yaml

with open('params.yml', 'rb') as f:
    params = yaml.safe_load(f.read())

MAX_ITERS = params['MAX_ITERS']
NUM_COINS = params['NUM_COINS']
MAX_RUNS = params['MAX_RUNS']

HOST_PORT = params['SERVER_PORT']
HOST_ADDR = params['SERVER_IP']

print(params)

class Player:
    def __init__(self,addr):
        self.name = ' '
        self.iter = 0
        self.run = 0
        self.addr = addr
        self.score = 0
        self.coins = np.zeros(NUM_COINS)
        self.coin_map = list(range(NUM_COINS))
        random.shuffle(self.coin_map)

    def shuffle(self,choice):
        try:
            choice = int(choice)
        except:
            print(f"wrong choice by user {self.name}: {choice}")
            return 0
        if choice >= NUM_COINS or choice < 0:
            print(f"out of range choice by user {self.name}: {choice}")
            return 0
        return self.coin_map[choice]


## You can safely ignore Tkinter stuff

window = tk.Tk()
window.title("Server")

# Top frame consisting of two buttons widgets (i.e. btnStart, btnStop)
topFrame = tk.Frame(window)
btnStart = tk.Button(topFrame, text="Start", command=lambda: start_server())
btnStart.pack(side=tk.LEFT)
btnStop = tk.Button(
    topFrame, text="Stop", command=lambda: stop_server(), state=tk.DISABLED
)
btnStop.pack(side=tk.LEFT)
topFrame.pack(side=tk.TOP, pady=(5, 0))

# Middle frame consisting of two labels for displaying the host and port info
middleFrame = tk.Frame(window)
lblHost = tk.Label(middleFrame, text="Address: X.X.X.X")
lblHost.pack(side=tk.LEFT)
lblPort = tk.Label(middleFrame, text="Port:XXXX")
lblPort.pack(side=tk.LEFT)
middleFrame.pack(side=tk.TOP, pady=(5, 0))

# The client frame shows the client area
clientFrame = tk.Frame(window)
lblLine = tk.Label(clientFrame, text="**********Client List**********").pack()
scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
tkDisplay = tk.Text(clientFrame, height=10, width=30)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
scrollBar.config(command=tkDisplay.yview)
tkDisplay.config(
    yscrollcommand=scrollBar.set,
    background="#F4F6F7",
    highlightbackground="grey",
    state="disabled",
)
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))


server = None
clients = []
clients_names = [] #stores client names
leaderboard = [] #stores the leaderboard


## Random Number Generation
outcome = []
p = []
for i in range(NUM_COINS):
    p.append(random.random()*0.8 + 0.1)
    # p ~ uniform(0.1,0.9)
    # tried to avoid to high or low values; change accordingly
print(p)
# Pre-compute outcome
outcome = np.random.binomial(size=[MAX_ITERS,MAX_RUNS,NUM_COINS], n=1, p=p)

# Start server function
def start_server():
    global server, HOST_ADDR, HOST_PORT
    btnStart.config(state=tk.DISABLED)
    btnStop.config(state=tk.NORMAL)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(socket.AF_INET)
    print(socket.SOCK_STREAM)

    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(5)  # server is listening for client connection

    threading._start_new_thread(accept_clients, (server, " "))

    lblHost["text"] = "Address: " + HOST_ADDR
    lblPort["text"] = "Port: " + str(HOST_PORT)


# Stop server function
def stop_server():
    global server,leaderboard
    leaderboard.sort(reverse=True)
    print(leaderboard)
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)


def accept_clients(the_server, y):
    while True:
        if len(clients) < 400: # Limit the number of players here
            client, addr = the_server.accept()
            clients.append(client)
            player = Player(addr)
            # use a thread so as not to clog the gui thread
            threading._start_new_thread(send_receive_client_message, (client, addr, player))


# Function to receive message from current clients
def send_receive_client_message(client_connection, client_ip_addr, player):
    global server, clients

    client_msg = " "

    # send welcome message to client
    client_name = client_connection.recv(4096).decode()
    client_connection.send("welcome".encode())

    player.name = client_name
    clients_names.append(client_name)
    update_client_names_display(clients_names)  # update client names display

    while (player.run < MAX_RUNS):
        data = client_connection.recv(4096).decode()
        if not data:
            break

        # get the player choice from received data
        player_choice = data

        # send the outcome of the player's choice
        reward = outcome[player.iter][player.run][player.shuffle(player_choice)]
        player.score += reward
        dataToSend = "out" + str(reward)

        #Update iter count
        player.iter += 1
        if player.iter == MAX_ITERS:
            player.iter = 0
            player.run += 1
            # random.shuffle(player.coin_map)
            ## Uncomment above to shuffle after each run
        client_connection.send(dataToSend.encode())

    # send the final result and clean-up
    shuffled_p = []
    for i in range(NUM_COINS):
        shuffled_p.append(p[player.coin_map[i]])
        # p values according to player's coin_map
    client_connection.send(f"res{player.score/MAX_RUNS}${shuffled_p}".encode())

    print([player.name,player.score/MAX_RUNS])
    global leaderboard
    leaderboard.append([player.score/MAX_RUNS,player.name])

    # find the client index then remove from both lists(client name list and connection list)
    idx = get_client_index(clients, client_connection)
    del clients_names[idx]
    del clients[idx]
    client_connection.close()

    update_client_names_display(clients_names)  # update client names display


# Return the index of the current client in the list of clients
def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx


# Update client name display when a new client connects OR
# When a connected client disconnects
def update_client_names_display(name_list):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete("1.0", tk.END)

    for c in name_list:
        tkDisplay.insert(tk.END, c + "\n")
    tkDisplay.config(state=tk.DISABLED)


window.mainloop()
