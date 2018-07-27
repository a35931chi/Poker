import random
from random import shuffle
import matplotlib.pyplot
import pandas as pd
import numpy as np

def RANKS():
    return [('Ace', '14'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'),
            ('8', '8'), ('9', '9'), ('10', '10'), ('Jack', '11'), ('Queen', '12'), ('King', '13')]

def SUITS():
    return [('Clubs', 'C'), ('Diamonds', 'D'), ('Hearts', 'H'), ('Spades', 'S')]

class Card:
    def __init__(self, suit, rank):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return self.rank[0] + " of " + self.suit[0]


class Deck:
    def __init__(self):
        self.cards = []
        self.cards = [Card(suit, rank) for suit in SUITS() for rank in RANKS()]

    def show(self):
        return [str(card.rank[0]) + ' of ' + str(card.suit[0]) for card in self.cards]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) == 0:
            print('no more to deal')
            pass
        else:
            card = self.cards.pop()
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

if __name__ == '__main__':
    mydeck = Deck()
