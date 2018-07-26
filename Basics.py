import random
from random import shuffle
import matplotlib.pyplot
import pandas as pd
import numpy as np

def RANKS():
    return ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

def SUITS():
    return ['Clubs', 'Diamonds', 'Hearts', 'Spades']

class Card:
    def __init__(self, suit, rank):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:
    def __init__(self):
        self.cards = []
        self.cards = [Card(suit, rank) for suit in SUITS() for rank in RANKS()]
        self.order = [str(card.rank) + ' of ' + str(card.suit) for card in self.cards]

    def shuffle(self):
        random.shuffle(self.cards)
        self.order = [str(card.rank) + ' of ' + str(card.suit) for card in self.cards]

    def deal(self):
        if len(self.cards) == 0:
            print('no more to deal')
            pass
        else:
            card = self.cards.pop()
            self.order = [str(card.rank) + ' of ' + str(card.suit) for card in self.cards]
            return card


def test_shuffle(somedeck, shuffle_times = 10000):
    #test the shuffle function. if shuffled a thousand times, let's look at what position each card would get
    
    unshuffled_order = somedeck.order


    orders = []
    for _ in range(shuffle_times):
        somedeck.shuffle()
        orders.append([somedeck.order.index(card) for card in unshuffled_order])

    df_orders = pd.DataFrame(orders, columns = unshuffled_order)
    return df_orders
