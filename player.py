'''Player class called within the BlackJack'''


class Player():
    def __init__(self, id, countList, cardList, bet, money):
        self.id = id
        self.countList = countList
        self.cardList = cardList
        self.bet = bet
        self.money = money

    '''convert a card to a point value'''

    def determineValToAdd(self, cardRank):
        if cardRank not in set(['A', 'J', 'K', 'Q']):
            valToAdd = int(cardRank)
        elif cardRank == 'A':
            valToAdd = 'A'
        else:
            valToAdd = 10
        return valToAdd

    '''add card to player's hand'''

    def setUp(self, card):
        self.cardList += [card]
        valtoAdd = self.determineValToAdd(card[0])
        self.countList.append(valtoAdd)

    '''given a hand, calculate the best possible count'''

    def calculateScore(self):
        score = [0]
        for cardRank in self.countList:
            if cardRank == 'A':
                score1 = [num + 1 for num in score]
                score11 = [num + 11 for num in score]
                score = score1 + score11
            else:
                score = [cardRank + num for num in score]
        count = 0
        for num in score:
            if num > count and num <= 21:
                count = num
        if count == 0:
            return 22
        else:
            return count

    '''compare counts between players and dealer, and add/subtract money accordingly'''

    def winOrLoseMoney(self, dealerCount):
        myCount = self.calculateScore()
        if myCount == 21 and dealerCount != 21:
            self.money += (3/2)*self.bet
        elif myCount <= 21:
            if dealerCount > 21:
                self.money += self.bet
            else:
                if dealerCount < myCount:
                    self.money += self.bet
                elif dealerCount > myCount:
                    self.money -= self.bet
        else:
            self.money -= self.bet
