import itertools
from collections import Counter
from Basics import Deck
from Game_Board import Test_Game

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
                elif evaluations[3] > best[0][1][3]:
                    #print('better kicker')
                    best = [(hand, evaluations)]
            #else:
                #print('worse')

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

    best = best_hand(all_hands_evaluate)
    
    #print(best)
    return best


#later on, need to write a function that analyzes how many cards are missing from the most ideal hands with the whole cards and what's available on the board


if __name__ == '__main__':
    
    Test_evaluate_5cards = False

    Test_common_occur = False
    #. poker hands probabilities:
    #10. royal flush: 0.000154%, 'Royal flush': 0.0001%
    #9. straight flush: 0.00139%, 'Straight flush': 0.0011%
    #8. four of a kind: 0.0240%, '4 of a Kind': 0.0230%
    #7. full house: 0.1441%, 'Full House': 0.1347%
    #6. flush: 0.1965%, 'Flush': 0.1998%
    #5. straight: 0.3925%, 'Straight': 0.3976%
    #4. three of a kind: 2.1128%, '3 of a Kind': 2.1141%
    #3. two pair: 4.7539%, '2 Pairs': 4.7731%
    #2. one pair: 42.2569%, '1 Pair': 42.2529%
    #1. high card: 50.1177%, 'High': 50.1036%
    
    Test_combined_hands = False

    Test_best_hand = False

    Test_1000000_hands_sim = True

    
    if Test_evaluate_5cards:
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

    if Test_common_occur:
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

    if Test_combined_hands:
        combined = dict()
        whole_cards, comm = Test_Game('HOLDEM', 3)
        print('community cards: ')
        comm_cards = []
        for card in comm:
            comm_cards.append(card.rank[1] + card.suit[1])
            print(card.rank[1] + card.suit[1])
                
        for player in whole_cards:
            player_cards = []
            
            print('player: {}'.format(player))
            for card in whole_cards[player]:
                player_cards.append(card.rank[1] + card.suit[1])
                print(card.rank[1] + card.suit[1])
            combined[player] = player_cards + comm_cards
 
        #getting player's best hands
        players_bests = dict()
        all_hands = []
        for player in combined:
            hand, evaluation = evaluate_7cards(combined[player])[0]
            print('Player {}: '.format(player))
            print(hand, evaluation)
            all_hands.append((hand, evaluation))
            players_bests[hand] = player

        best_hands = best_hand(all_hands)
        print('number of best hands: {}'.format(len(best_hands)))
        print('best hands is/are: {}'.format(best_hands[0]))

        print('winner is player {}!'.format([players_bests[hand[0]] for hand in best_hands]))
        

        
    if Test_best_hand:
        #hand6 = ('14H', '3S', '10H', '6C', '11S')
        #hand5 = ('9D', '9H', '10H', '7D', '6C')
        #hand9 = ('9D', '9H', '10H', '10D', '6C')
        #hand3 = ('9D', '9H', '10H', '10D', '14C')
        hand1 = ('9D', '7H', '10H', '2H', '14H')
        hand2 = ('9D', '7H', '10H', '2H', '14D')
        #hand2 = ('9H', '7H', '10H', '4H', '14H')
        #hand7 = ('9H', '9D', '9C', '9S', '14H')
        #hand8 = ('8H', '8D', '8C', '8S', '14H')
        #hand4 = ('14H', '2H', '3H', '4H', '5H')
        
        evaluation = {hand1: evaluate_5cards(hand1),
                      hand2: evaluate_5cards(hand2)}
    
        best_hand(evaluation)

    if Test_1000000_hands_sim:
        for _ in range(10):
            


