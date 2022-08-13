import sys
from client_utils import Player
from algorithms import algorithm
import yaml

with open('params.yml', 'rb') as f:
    params = yaml.safe_load(f.read())

HOST_PORT = params['SERVER_PORT']
HOST_ADDR = params['SERVER_IP']

if len(sys.argv) < 2:
    print(f"Too less arguments! {len(sys.argv)-1} < 1. Please enter username")
    assert False
else:
    name = sys.argv[1]

player = Player(name, algorithm)
player.connect()