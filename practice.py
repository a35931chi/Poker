import pickle
import pandas as pd
import numpy as np
from Basics import Deck
from win_lose import evaluate_5cards
from time import time
import itertools
import pickle
import os.path
from collections import Counter

def contains(some_tuple, availhand):
    #this function takes in account of what's dealt, namely what's on the board, and what's whole
    #and determine what's possible, and how many outs there are to those
    #returns a dictionary of possible hands, and the out cards

    #
    #is royal flush possible
    #is straight flush possible
    #is four of a kind possible

    #1. count the number of blanks
    blank_counts = 5 - len(availhand)
    cards_needed = list(set(some_tuple) - set(availhand))

    if len(cards_needed) > blank_counts:
        return False
    else:
        return cards_needed


# Store my data
file_name = 'Data/all_possible_5cards_eval.pickle'

if os.path.isfile(file_name):
    print('Have file already.')
    with open(file_name, 'rb') as handle:
        bible = pickle.load(handle)
    print('File loaded')
else:
    print('Don\'t have necessary file, please wait...')
    somedeck = Deck()
    
    t0 = time()
    bible = pd.DataFrame()
    bible['all_possible_5cards'] = list(itertools.combinations(somedeck.cards, 5))
    #all_possible_5cards = itertools.combinations(somedeck.cards, 5)

    bible['eval'] = bible['all_possible_5cards'].apply(evaluate_5cards)

    t1 = time()
    print('took {} seconds to initialize the deck...'.format(t1 - t0))
    #dictionary size is 86101kb, took 36 seconds
    #dataframe size is 93503kb, took 32 seconds
    with open(file_name, 'wb') as handle: 
        pickle.dump(bible, handle, protocol=pickle.HIGHEST_PROTOCOL)


#temp = df.copy()
#availhand = ['14C', '13C', '', '', '']
#temp['outs'] = temp.apply(lambda x: contains(x['all_possible_5cards'], availhand), axis = 1)

mydeck = Deck()
mydeck.shuffle()
#1. when whole cards are dealt
myhand = [mydeck.deal() for _ in range(2)]
#1a. evaluate for best possible hands with past experience

#2. add flop (3 cards)
myhand += [mydeck.deal() for _ in range(3)]
#2a. evaluate for best possible hands, should return all the cards needed to improve
tempbible = bible.copy()
current_eval = evaluate_5cards(myhand)
#tempbible['outs'] = tempbible.apply(lambda x: contains(x['all_possible_5cards'], my_whole), axis = 1)
#tempbible = tempbible[tempbible['outs'] != False]

#3. add turn (1 card)
#3a. evaluate for best possible hands, should return all the cards needed to improve
#4. add river (1 card)
#4a. evaluate for best possible hands, should return all the cards needed to improve
