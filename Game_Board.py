#Here I want to deal some cards.
#let's specify the following:
#1. Game type
#2. How many players
from Basics import Deck, Card 

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
    Test_Game('HOLDEM', 3)
