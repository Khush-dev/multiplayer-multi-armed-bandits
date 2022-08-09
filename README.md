# multiplayer-multi-armed-bandits
This repo contains code for local multiplayer multi-armed bandit algorthm testing and competition. 

To run the application:

1. Make sure you have python installed and setup on your system. App is tested on Python 2.7
2. Download or clone the repository
3. To start the server: python game_server.py <IP_ADDR>.
Here, <IP_ADDR> is the server ip address(Example: 192.168.0.1)
4. Click "Start" button on the Server window
5. Modify algorithm(tossed,heads) in non_interactive_client.py.
6. To start a client: python non_interactive_client.py <IP_ADDR> <USERNAME>.
You can also compare different algorithms locally
