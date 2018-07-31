import random
from random import shuffle
import matplotlib.pyplot
import pandas as pd
import numpy as np

class Card:
    def __init__(self, ranksuit):
        self.ranksuit = ranksuit

    '''
    def __str__(self):
        return self.rank + ' of ' +self.suit
        #return self.rank[0] + " of " + self.suit[0]
    '''


class Deck:
    def __init__(self):
        self.cards = []
        self.all_ranks = ['14', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
        self.all_suits = ['C', 'D', 'H', 'S']
        self.cards = [rank+suit for suit in self.all_suits for rank in self.all_ranks]

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
