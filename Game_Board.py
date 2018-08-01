#Here I want to deal some cards.
#let's specify the following:
#1. Game type
#2. How many players
import itertools
from collections import Counter
import pandas as pd
from Basics import Deck, Card

def get_ranks(cards):
    """
    Returns a list of ints containing the rank of each card in cards.
    ex. 
    get_ranks(['2S','3C','5C','4D','6D'])
    returns [2,3,5,4,6]
    """
    #cards = numeric_ranks(cards) # Convert rank letters to numbers (e.g. J to 11)
    return [int(card[0:-1]) for card in cards]


def get_suits(cards):
    """
    Returns a list of strings containing the suit of each card in cards.
    ex. 
    get_ranks(['2S','3C','5C','4D','6D'])
    returns ['S','C','C','D','D']
    """
    return [card[-1] for card in cards]

def isstraight(rank):
    """ 
    Returns True if all numbers in lst can be ordered consecutively, and False otherwise
    """
    #if there's an ACE,  remove it first, and two situations:
    #1. connected? meaning len(set(lst)) == 4 and max(lst) - min(lst) == len(lst) - 1
    #2. is the min a 2 or a max a king? min(lst) == 2 or max(lst) == 13
    #if both true, then it's a straight
    lst = rank.copy()
    if 14 in lst:
        lst.remove(14)
        if len(set(lst)) == 4 and max(lst) - min(lst) == len(lst) - 1:
            if max(lst) == 13 or min(lst) == 2:
                #print('straight')
                return True
    #otherwise, connected? meaning len(set(lst)) == 5 and max(lst) - min(lst) == len(temp_lst) - 1
    elif len(set(lst)) == 5 and max(lst) - min(lst) == len(lst) - 1:
        return True
    return False  

def isflush(suits):
    """ 
    Returns True if all elements of lst are the same, False otherwise 
    ex.
    all_equal(['S,'S','S']) returns True
    """
    return len(set(suits)) == 1
def best_hand(all_hands):
    best = []
    
    for hand, evaluations in all_hands:
        #print(hand, evaluations)
        #if best hand is empty, assign a hand, typically for the first in the loop
        if len(best) == 0:
            #print('initialize')
            best.append((hand, evaluations))
        else:
            #if the overall evaluation is the same, then append
            if evaluations == best[0][1]:
                #print('all the same')
                best.append((hand, evaluations))
            #if the overall hand is better, assign that hand to best
            elif evaluations[0] > best[0][1][0]:
                #print('fundamentally better')
                best = [(hand, evaluations)]
            #if the overall evaulation is the same
            elif evaluations[0] == best[0][1][0]:
                #if the key is better, assign that hand to best
                if evaluations[2] > best[0][1][2]:
                    #print('better key')
                    best = [(hand, evaluations)]
                #if the kickers are better, assign that hand to best
                elif evaluations[2] == best[0][1][2] and evaluations[3] > best[0][1][3]:
                    #print('better kicker')
                    best = [(hand, evaluations)]
            #else:
            #    print('worse')

    return best
    
    
def evaluate_5cards(hand):
    #identify the hands
    ranks = get_ranks(hand)
    suits = get_suits(hand)
    
    if len(set(hand)) < len(hand) or max(ranks) > 14 or min(ranks) < 1:
        # There is a duplicate
        return 0, 'Invalid hand', 0, 0
    
    counter = dict(Counter(ranks))

    #if there's two unique type of ranks
    if len(counter) == 2:
        #Four of a kind - All four cards of the same rank.
        if 4 in counter.values():
            key = list(counter.keys())[list(counter.values()).index(4)]
            indices = [i for i, x in enumerate(counter.values()) if x == 1]
            kicker = [list(counter.keys())[i] for i in indices]
            kicker.sort(reverse = True)
            return 8, '4 of a Kind', key, kicker
        #Full house - Three of a kind with a pair.
        elif 2 in counter.values():
            key = list(counter.keys())[list(counter.values()).index(3)]
            return 7, 'Full House', key, 0
    #if there's three unique type of ranks
    elif len(counter) == 3:
        #Three of a kind - Three cards of the same rank.
        if 3 in counter.values():
            key = list(counter.keys())[list(counter.values()).index(3)]
            indices = [i for i, x in enumerate(counter.values()) if x == 1]
            kicker = [list(counter.keys())[i] for i in indices]
            kicker.sort(reverse = True)
            return 4, '3 of a Kind', key, kicker
            
        #Two pair - Two different pairs.
        else:
            indices = [i for i, x in enumerate(counter.values()) if x == 2]
            key = [list(counter.keys())[i] for i in indices]
            key.sort(reverse = True)
            kicker = list(counter.keys())[list(counter.values()).index(1)]
            return 3, '2 Pairs', key, kicker
    #Pair - Two cards of the same rank.
    elif len(counter) == 4:
        key = list(counter.keys())[list(counter.values()).index(2)]
        indices = [i for i, x in enumerate(counter.values()) if x == 1]
        kicker = [list(counter.keys())[i] for i in indices]
        kicker.sort(reverse = True)
        return 2, '1 Pair', key, kicker
    # The hand is a type of straight
    elif isstraight(ranks):
        # Hand is a flush
        if isflush(suits):
            #Royal flush - A, K, Q, J, 10, all the same suit.
            if 10 == min(ranks):
                # Lowest card is an ace
                key = 14
                return 10, 'Royal flush', key, 0
            #Straight flush - Five cards in a sequence, all in the same suit. but not royal flush
            else:
                try:
                    ranks.remove(14)
                except:
                    pass
                key = max(ranks)
                return 9, 'Straight flush', key, 0
        #Straight - Five cards in a sequence, but not of the same suit.
        else:
            if 10 == min(ranks):
                key = 14
            else:
                try:
                    ranks.remove(14)
                except:
                    pass
                key = max(ranks)
            return 5, 'Straight', key, 0
    #Flush - Any five cards of the same suit, but not in a sequence.
    elif isflush(suits):
        ranks.sort(reverse = True)
        return 6, 'Flush', ranks, 0
    #High Card - When you don't have anything else
    else:
        ranks.sort(reverse = True)
        return 1, 'High', ranks, 0


#for now, I just want to write a function that check which hand wins
def evaluate_7cards(combined_hand):
    #check for the total number of cards
    if len(combined_hand) != 7:
        print('something\'s wrong')
        pass

    # All combinations of 5 cards from the larger list
    all_hand_combo = itertools.combinations(combined_hand, 5)
    all_hands_evaluate = []
    for hand in all_hand_combo:
        all_hands_evaluate.append((hand, evaluate_5cards(hand)))
    #print(all_hands_evaluate)
    best = best_hand(all_hands_evaluate)
    
    #print(best)
    return best

def Test_Game(game_type, num_players):
    #initialize the number of players
    #players will be a dictionary
    players_hands = dict()

    #initialize a deck, then shuffle the deck
    mydeck = Deck()
    #print('pre-shuffled')
    #print(mydeck.order)
    mydeck.shuffle()
    #print('shuffled')
    #print(mydeck.order)

    
    if game_type == 'HOLDEM':
        #for holdem, each player is dealt 2 cards
        for i in range(num_players):
            hands = [mydeck.deal() for _ in range(2)]
            players_hands[i] = hands

    #now for the community cards
    hands = [mydeck.deal() for _ in range(5)] 
    comm = hands
       
    #I wanna see the cards that are being dealt
    show = False
    if show:
        for key in players_hands.keys():
            print('Player {} with: '.format(key))
            for card in players_hands[key]:
                print(card.rank, card.suit)
        print('On the Board: ')
        for card in comm:
            print(card.rank, card.suit)
        #I wanna see what's left with the dealer
        print(len(mydeck.cards))
        print(mydeck.show())

    #It will also be interesting to see if cards are dealt per rule have a different winning percentage

    return players_hands, comm

if __name__ == '__main__':
    game_info = []
    whole_cards, comm = Test_Game('HOLDEM', 3)
    for player in whole_cards:
        player_cards = whole_cards[player]

        game_info.append([player, player_cards, comm])
