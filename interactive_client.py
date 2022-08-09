import tkinter as tk
from tkinter import PhotoImage
from tkinter import messagebox
import socket, sys
from time import sleep
import threading

# MAIN GAME WINDOW
window_main = tk.Tk()
window_main.title("Game Client")
## PARAMETERS
MAX_ITERS = 100
MAX_RUNS = 1000

class Player:
    def __init__(client, HOST_PORT, HOST_ADDR):
        self.name = " "
        self.client = client
        self.host_port = HOST_PORT
        self.host_addr = HOST_ADDR 
        self.iter = 0
        self.runs = 0
        self.score = 0
        self.tossed = np.zeros(NUM_COINS)
        self.heads = np.zeros(NUM_COINS)

    def algorithm(tossed,heads):
        """
        Enter your Algorithm in this functions.
        tossed[i] contains the number of times the 'i'th coin is tossed/'i'th arm is pulled
        heads[i] contains the number of times the 'i'th coin gave heads/'i'th arm got reward 1
        This data is assumed to be sufficient.
        """



        # # EG3
        # eps = 0.3
        # for i,num in enumerate(tossed):
        #     if num == 0:
        #         return i
        # return random.choice(range(NUM_COINS)) if random.random() < eps else argmax([h/total for h,total in zip(heads,total)])
        
        return random.choice(range(NUM_COINS))

    def connect():
        if len(ent_name.get()) < 1:
            tk.messagebox.showerror(
                title="ERROR!!!", message="You MUST enter your first name <e.g. John>"
            )
        else:
            self.name = ent_name.get()
            self.lbl_your_name["text"] = "Your name: " + self.name
            connect_to_server(self.name)


    def count_down(my_timer, nothing):
        if self.runs <= MAX_RUNS and self.iter<= MAX_ITERS:
            self.iter += 1

        self.lbl_game_round["text"] = "Game round " + str(self.iter) + " starts in"

        while my_timer > 0:
            my_timer = my_timer - 1
            print("game timer is: " + str(my_timer))
            self.lbl_timer["text"] = my_timer
            sleep(1)
        # sleep(my_timer)

        enable_disable_buttons("enable")
        self.lbl_round["text"] = "Round - " + str(game_round)
        self.lbl_final_result["text"] = " "


    def choice(arg):
        self.your_choice = arg
        self.lbl_your_choice["text"] = "Your choice: " + self.your_choice

        if self.client:
            dataToSend = self.your_choice
            client.send(dataToSend.encode())
            enable_disable_buttons("disable")


    def connect_to_server(name):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.host_addr, self.host_port))
            client.send(name.encode())  # Send name to server after connecting

            # disable widgets
            btn_connect.config(state=tk.DISABLED)
            ent_name.config(state=tk.DISABLED)
            lbl_name.config(state=tk.DISABLED)
            enable_disable_buttons("disable")

            # start a thread to keep receiving message from server
            # do not block the main thread :)
            threading._start_new_thread(receive_message_from_server, (client, "m"))
        except Exception as e:
            tk.messagebox.showerror(
                title="ERROR!!!",
                message="Cannot connect to host: "
                + self.host_addr
                + " on port: "
                + str(self.host_port)
                + " Server may be Unavailable. Try again later",
            )


    def receive_message_from_server(sck, m):

        while True:
            from_server = str(sck.recv(4096).decode())

            if not from_server:
                break

            if from_server.startswith("welcome"):
                lbl_welcome["text"] = (
                    "Server says: Welcome " + self.name + "!"
                )
                lbl_line_server.pack()
            elif from_server.startswith("out"):
                # get the opponent choice from the server
                outcome = int(from_server[3:])

                # Update GUI
                lbl_opponent_choice["text"] = "Outcome: " + outcome
                lbl_result["text"] = "Result: " + round_result

                # is this the last round e.g. Round 5?
                if game_round == TOTAL_NO_OF_ROUNDS:
                    # compute final result
                    final_result = ""
                    color = ""

                    lbl_final_result["text"] = (
                        "FINAL RESULT: "
                        + str(your_score)
                        + " - "
                        + final_result
                    )
                    lbl_final_result.config(foreground=color)

                    enable_disable_buttons("disable")
                    game_round = 0
                    your_score = 0
                    opponent_score = 0

                # Start the timer
                threading._start_new_thread(count_down, (game_timer, ""))

        sck.close()
# def show_run(self):
    #     """
    #     Shows a graph of average reward over iterations
    #     """
    #     #Empirical Average Lists

    #     fig, ax = plt.subplots()

    #     for i in range(1,self.iters+1):
    #             if(choice == 1):
    #                 ax.axhspan(0, 1, i/self.iters, (i-1)/self.iters, facecolor='#FFCCCC')  #Generates band colors
    #             elif(choice == 2):
    #                 ax.axhspan(0, 1, i/self.iters, (i-1)/self.iters, facecolor='#E5FFCC')
    #             else:
    #                 ax.axhspan(0, 1, i/self.iters, (i-1)/self.iters, facecolor='#CCE5FF')

    #     ## Plots time-evolution of Empirical averages for each coin
    #     ## Also colors the background with colors to indicate periods where each coin was used
    #     # plt.axhline(y=p1, color='r', linestyle='--',alpha=0.3)
    #     # plt.axhline(y=p2, color='g', linestyle='--',alpha=0.3)
    #     # plt.axhline(y=p3, color='b', linestyle='--',alpha=0.3)
    #     plt.plot(t, emp1, "red", label = "Coin 1")
    #     plt.plot(t, emp2, "green", label = "Coin 2")
    #     plt.plot(t, emp3, "blue", label = "Coin 3")
    #     plt.title("Time variation of empirical averages")
    #     plt.legend(loc = "upper left")
    #     plt.grid()
    #     plt.show()
# network client
client = None
if len(sys.argv) == 1:
    HOST_ADDR ="0.0.0.0"
else:
    HOST_ADDR = sys.argv[1]
HOST_PORT = 8080

player = Player()

top_welcome_frame = tk.Frame(window_main)
lbl_name = tk.Label(top_welcome_frame, text="Name:")
lbl_name.pack(side=tk.LEFT)
ent_name = tk.Entry(top_welcome_frame)
ent_name.pack(side=tk.LEFT)
btn_connect = tk.Button(top_welcome_frame, text="Connect", command=lambda: connect())
btn_connect.pack(side=tk.LEFT)
top_welcome_frame.pack(side=tk.TOP)

top_message_frame = tk.Frame(window_main)
lbl_line = tk.Label(
    top_message_frame,
    text="***********************************************************",
).pack()
lbl_welcome = tk.Label(top_message_frame, text="")
lbl_welcome.pack()
lbl_line_server = tk.Label(
    top_message_frame,
    text="***********************************************************",
)
lbl_line_server.pack_forget()
top_message_frame.pack(side=tk.TOP)


top_frame = tk.Frame(window_main)
top_left_frame = tk.Frame(
    top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1
)
lbl_your_name = tk.Label(
    top_left_frame, text="Your name: " + your_name, font="Helvetica 13 bold"
)
lbl_opponent_name = tk.Label(top_left_frame, text="Opponent: " + opponent_name)
lbl_your_name.grid(row=0, column=0, padx=5, pady=8)
lbl_opponent_name.grid(row=1, column=0, padx=5, pady=8)
top_left_frame.pack(side=tk.LEFT, padx=(10, 10))


top_right_frame = tk.Frame(
    top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1
)
lbl_game_round = tk.Label(
    top_right_frame,
    text="Game round (x) starts in",
    foreground="blue",
    font="Helvetica 14 bold",
)
lbl_timer = tk.Label(
    top_right_frame, text=" ", font="Helvetica 24 bold", foreground="blue"
)
lbl_game_round.grid(row=0, column=0, padx=5, pady=5)
lbl_timer.grid(row=1, column=0, padx=5, pady=5)
top_right_frame.pack(side=tk.RIGHT, padx=(10, 10))

top_frame.pack_forget()

middle_frame = tk.Frame(window_main)

lbl_line = tk.Label(
    middle_frame, text="***********************************************************"
).pack()
lbl_line = tk.Label(
    middle_frame, text="**** GAME LOG ****", font="Helvetica 13 bold", foreground="blue"
).pack()
lbl_line = tk.Label(
    middle_frame, text="***********************************************************"
).pack()

round_frame = tk.Frame(middle_frame)
lbl_round = tk.Label(round_frame, text="Round")
lbl_round.pack()
lbl_your_choice = tk.Label(
    round_frame, text="Your choice: " + "None", font="Helvetica 13 bold"
)
lbl_your_choice.pack()
lbl_opponent_choice = tk.Label(round_frame, text="Opponent choice: " + "None")
lbl_opponent_choice.pack()
lbl_result = tk.Label(
    round_frame, text=" ", foreground="blue", font="Helvetica 14 bold"
)
lbl_result.pack()
round_frame.pack(side=tk.TOP)

final_frame = tk.Frame(middle_frame)
lbl_line = tk.Label(
    final_frame, text="***********************************************************"
).pack()
lbl_final_result = tk.Label(
    final_frame, text=" ", font="Helvetica 13 bold", foreground="blue"
)
lbl_final_result.pack()
lbl_line = tk.Label(
    final_frame, text="***********************************************************"
).pack()
final_frame.pack(side=tk.TOP)

middle_frame.pack_forget()

button_frame = tk.Frame(window_main)
photo_tick = PhotoImage(file=r"tick-mark-icon.png")
input_txt = tk.Text(button_frame, height=5, width=20)
btn_submit = tk.Button(
    button_frame,
    text="Submit",
    command=lambda: choice(input_txt.get(1.0, "end-1c")),
    state=tk.DISABLED,
    image=photo_tick,
)
input_txt.grid(row=0, column=0)
btn_submit.grid(row=0, column=1)
button_frame.pack(side=tk.BOTTOM)

def enable_disable_buttons(todo):
    if todo == "disable":
        btn_submit.config(state=tk.DISABLED)
    else:
        btn_submit.config(state=tk.NORMAL)





window_main.mainloop()
