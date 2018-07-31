import pickle
import pandas as pd
import numpy as np
from Basics import Deck
from win_lose import evaluate_5cards
from time import time
import itertools
import pickle
import os.path

def evaulate_hand(board, whole):
    #this function takes in account of what's dealt, namely what's on the board, and what's whole
    #and determine what's possible, and how many outs there are to those
    #returns a dictionary of possible hands, and the out cards

    #
    #is royal flush possible
    #is straight flush possible
    #is four of a kind possible
    pass

    


# Store my data
file_name = 'Data/all_possible_5cards_eval.pickle'

if os.path.isfile(file_name):
    print('Have file already.')
    with open(file_name, 'rb') as handle:
        df = pickle.load(handle)
    print('File loaded')
else:
    print('Don\'t have necessary file, please wait...')
    somedeck = Deck()
    
    t0 = time()
    df = pd.DataFrame()
    df['all_possible_5cards'] = list(itertools.combinations(somedeck.cards, 5))
    #all_possible_5cards = itertools.combinations(somedeck.cards, 5)

    df['eval'] = df['all_possible_5cards'].apply(evaluate_5cards)

    t1 = time()
    print('took {} seconds to initialize the deck...'.format(t1 - t0))
    #dictionary size is 86101kb, took 36 seconds
    #dataframe size is 93503kb, took 32 seconds
    with open(file_name, 'wb') as handle: 
        pickle.dump(df, handle, protocol=pickle.HIGHEST_PROTOCOL)


