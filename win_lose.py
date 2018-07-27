import itertools
from collections import Counter
from Basics import Deck

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

def evaluate_5cards(hand):
    #identify the hands
    ranks = get_ranks(hand)
    suits = get_suits(hand)
    
    if len(set(hand)) < len(hand) or max(ranks) > 14 or min(ranks) < 1:
        # There is a duplicate
        return 'Invalid hand', None, None
    
    counter = dict(Counter(ranks))

    #if there's two unique type of ranks
    if len(counter) == 2:
        #Four of a kind - All four cards of the same rank.
        if 4 in counter.values():
            key = list(counter.keys())[list(counter.values()).index(4)]
            return '4 of a Kind', key, None
        #Full house - Three of a kind with a pair.
        elif 2 in counter.values():
            key = list(counter.keys())[list(counter.values()).index(3)]
            return 'Full House', key, None
    #if there's three unique type of ranks
    elif len(counter) == 3:
        #Three of a kind - Three cards of the same rank.
        if 3 in counter.values():
            key = list(counter.keys())[list(counter.values()).index(3)]
            return '3 of a Kind', key, None
            
        #Two pair - Two different pairs.
        else:
            indices = [i for i, x in enumerate(counter.values()) if x == 2]
            key = [list(counter.keys())[i] for i in indices]
            key.sort(reverse = True)
            kicker = list(counter.keys())[list(counter.values()).index(1)]
            return '2 Pairs', key, kicker
    #Pair - Two cards of the same rank.
    elif len(counter) == 4:
        key = list(counter.keys())[list(counter.values()).index(2)]
        indices = [i for i, x in enumerate(counter.values()) if x == 1]
        kicker = [list(counter.keys())[i] for i in indices]
        kicker.sort(reverse = True)
        return '1 Pair', key, kicker
    # The hand is a type of straight
    elif isstraight(ranks):
        # Hand is a flush
        if isflush(suits):
            #Royal flush - A, K, Q, J, 10, all the same suit.
            if 10 == min(ranks):
                # Lowest card is an ace
                key = 14
                return 'Royal flush', key, None
            #Straight flush - Five cards in a sequence, all in the same suit. but not royal flush
            else:
                try:
                    ranks.remove(14)
                except:
                    pass
                key = max(ranks)
                return 'Straight flush', key, None
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
            return 'Straight', key, None
    #Flush - Any five cards of the same suit, but not in a sequence.
    elif isflush(suits):
        key = max(ranks)
        return 'Flush', key, None
    #High Card - When you don't have anything else
    else:
        ranks.sort(reverse = True)
        return 'High', ranks, None


#for now, I just want to write a function that check which hand wins
def check_hand(combined_hand):
    #check for the total number of cards
    if len(combined_hand) != 7:
        print('something\'s wrong')
        pass



    """
    Returns a string containing the name of the hand in poker.
    Input hand must be a list of 5 strings.
    ex. 
    evaluate_hand(['2S','3C','5C','4D','6D'])
    returns 'Straight'
    """
    # All combinations of 5 cards from the larger list
    all_hand_combos = itertools.combinations(combined_hand, 5)
    hand_name_list = ['Invalid hand', 'High card', 'One pair', 'Two pair',
                      'Three of a kind', 'Straight', 'Flush', 'Full house',
                      'Four of a kind','Straight flush', 'Royal flush']
    num_hand_names = len(hand_name_list)
    max_value = 0
    best_hands = {x: [] for x in range(num_hand_names)}


    
    for combo in all_hand_combos:
        hand = list(combo)
        hand_name = evaluate_hand(hand) # Get the type of hand (e.g., one pair)
        hand_value = hand_name_list.index(hand_name)
        if hand_value >= max_value:
            # Stronger or equal hand has been found
            max_value = hand_value
            best_hands[hand_value].append(hand) # Store hand in dictionary
            
    
    ranks = get_ranks(hand)
    suits = get_suits(hand)
    
    if len(set(hand)) < len(hand) or max(ranks) > 13 or min(ranks) < 1:
        # There is a duplicate
        return 'Invalid hand'
    if isconsecutive(ranks):
        # The hand is a type of straight
        if all_equal(suits):
            # Hand is a flush
            if max(ranks) == 14:
                # Highest card is an ace
                return 'Royal flush'
            return 'Straight flush'
        return 'Straight'
    if all_equal(suits):
        return 'Flush'
    total = sum([ranks.count(x) for x in ranks])
    hand_names = {
        17: 'Four of a kind',
        13: 'Full house',
        11: 'Three of a kind',
        9: 'Two pair',
        7: 'One pair',
        5: 'High card'
        }
    return hand_names[total]


def check_F(hand):
    suits = [h[1] for h in hand]
    if len(set(suits)) == 1:
      return True
    else:
      return False


#later on, need to write a function that analyzes how many cards are missing from the most ideal hands with the whole cards and what's available on the board


if __name__ == '__main__':
    
    Testing_evaluate_5cards = False
    #poker hands probabilities:
    #royal flush: 0.000154%
    #straight flush: 0.00139%
    #four of a kind: 0.0240% 
    #full house: 0.1441% 
    #flush: 0.1965%
    #straight: 0.3925%
    #three of a kind: 2.1128%
    #two pair: 4.7539%
    #one pair: 42.2569%
    #high card: 50.1177% 
    
    Testing_common_occur = True
    
    if Testing_evaluate_5cards:
        for i in range(10):
            mydeck = Deck()
            mydeck.shuffle()
            
            hand = []
            print('\n')
            print('hand {}'.format(i))
            for _ in range(5):
                card = mydeck.deal()
                hand.append(card.rank[1]+card.suit[1])
            print(hand)
            print('evaluation result: ', evaluate_5cards(hand))

    if Testing_common_occur:
        occur = []
        for _ in range(1000000):
            mydeck = Deck()
            mydeck.shuffle()
            hand = []

            for _ in range(5):
                card = mydeck.deal()
                hand.append(card.rank[1]+card.suit[1])
            decision = evaluate_5cards(hand)[0]
            #print(hand, decision)
            occur.append(decision)
        outcome = dict(Counter(occur))
        print(outcome)
