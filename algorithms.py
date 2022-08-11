import numpy as np
import random
import yaml
import os

with open('params.yml', 'rb') as f:
    params = yaml.safe_load(f.read())

MAX_ITERS = params['MAX_ITERS']
NUM_COINS = params['NUM_COINS']

def interactive(tossed,heads):
    os.system('clear')
    for i,(h,tot) in enumerate(zip(heads,tossed)):
        print(f"Coin {i+1}: {h}/{tot}")
    print(f"Tosses left = {MAX_ITERS - sum(tossed)}")
    print("------------------------------------")

    choice = input(f"Enter Choice (1/2/3...{NUM_COINS}) to toss: ")
    try:
        choice = int(choice)
    except:
        print(f"Enter a number from 1 to {NUM_COINS}(both inclusive)")
        return 0
    if NUM_COINS < choice or 0 >= choice:
        print(f"Enter a number from 1 to {NUM_COINS}(both inclusive)")
        return 0
    return choice-1

def algorithm(tossed,heads):
    """
    Enter your Algorithm in this functions.
    tossed[i] contains the number of times the 'i'th coin is tossed/'i'th arm is pulled
    heads[i] contains the number of times the 'i'th coin gave heads/'i'th arm got reward 1
    This data is assumed to be sufficient.
    """

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

