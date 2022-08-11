# multiplayer-multi-armed-bandits
This repo contains code for multi-armed bandit algorthm testing and local multiplayer competition. 

To run the application:

1. Clone the repository.
```
git clone https://github.com/Khush-dev/multiplayer-multi-armed-bandits.git
cd multiplayer-multi-armed-bandits
pip install -r requirements.txt
```
2. Populate params.yml  (IMP: Atleast specify SERVER_IP (your own IP, in case you are hosting the server))
4. To start the server: `python game_server.py`
Click "Start" button on the Server window
5. Modify algorithm(tossed,heads) in algorithms.py
6. To start an non-interactive client: `python non_interactive_client.py <USERNAME>`
7. To start a interactive client: `python interactive_client.py <USERNAME>`
You can also compare different algorithms locally
