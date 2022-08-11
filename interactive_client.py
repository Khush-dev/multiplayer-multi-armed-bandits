import sys
from client_utils import Player
from algorithms import interactive
import yaml

with open('params.yml', 'rb') as f:
    params = yaml.safe_load(f.read())

HOST_PORT = params['SERVER_PORT']
HOST_ADDR = params['SERVER_IP']

# override MAX_ITERS and/or NUM_COINS with sys.argv
if len(sys.argv) < 2:
    print(f"Too less arguments! {len(sys.argv)-1} < 1. Please enter username")
    assert False
else:
    name = sys.argv[1]

player = Player(name, interactive)
player.connect()