from random import randint


class Card():
    def __init__(self):
        self.rank = ['A', '2', '3', '4', '5', '6',
                     '7', '8', '9', '10', 'J', 'Q', 'K']
        self.suit = ['Hearts', 'Diamond', 'Clubs', 'Spades']
        self.generated = set()

    '''create the necessary number of unique cards to play a round of blackjack'''

    def deal_cards(self, numPlayers):

        cardsDealt = 0

        while cardsDealt < numPlayers * 2:

            mycard = (self.rank[randint(0, 12)], self.suit[randint(0, 3)])

            if mycard not in self.generated:
                self.generated.add(mycard)
                cardsDealt += 1

    def clear_cardset(self):
        self.generated = set()
        self.playerCards = {}

    '''create an additional unique card in the middle of a round'''

    def addCard(self):
        while True:
            mycard = (self.rank[randint(0, 12)], self.suit[randint(0, 3)])
            if mycard not in self.generated:
                self.generated.add(mycard)
                return mycard
