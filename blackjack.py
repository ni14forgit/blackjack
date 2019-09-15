import curses
from card import Card
from player import Player
import time

''' BlackJack class handles main flow of the game, and is called after the player buy-in screen'''


class BlackJack:

    def __init__(self, player_count, screen, amountStartedWith):
        self.stdscr = screen
        self.table = "______________"
        self.screen_height, self.screen_width = self.stdscr.getmaxyx()
        self.card = Card()
        self.bettingOptions = ["$1", "$10", '$50', "$100"]
        self.playerOptions = ["Hit me", "Pass"]
        self.bettingCol = 0
        self.actionCol = 0
        self.mydict = {1: 'ONE', 2: "TWO", 3: "THREE"}
        self.gameDidEnd = False
        self.players = [Player(i+1, [], [], 0, amountStartedWith[i])
                        for i in range(player_count)]
        self.dealer = Player(0, [], [], 0, 0)

    '''each round is an iteration of the mainloop'''

    def mainloop(self):

        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        while not self.gameDidEnd:
            self.setCardState()
            while 1:
                self.makeBetsBeforeCard()
                self.drawTableAndCards(False)
                self.drawScore()
                self.hitMeOrPass()
                self.awardWinLoss()
                self.checkAndRemovePlayers()
                self.gameDidEnd = self.checkIfGameEnded()
                break
        return True

    '''generate and deal cards to players'''

    def setCardState(self):

        lenOfPlayersWithDealer = len(self.players) + 1
        self.refreshCardsAndPlayers()
        self.card.deal_cards(lenOfPlayersWithDealer)

        playerIndex = 0
        counter = 0
        for card in self.card.generated:

            if counter < 2:
                self.dealer.setUp(card)
                counter += 1
                continue

            self.players[playerIndex % len(self.players)].setUp(card)
            playerIndex += 1

    '''clear the cards of existing players from the previous round'''

    def refreshCardsAndPlayers(self):
        self.card.clear_cardset()

        self.dealer.cardList = []
        self.dealer.countList = []
        self.dealer.bet = 0

        for idx, i in enumerate(self.players):
            self.players[idx].cardList = []
            self.players[idx].countList = []
            self.players[idx].bet = 0

    def drawTableAndCards(self, bool):
        self.stdscr.clear()

        x = self.x = self.screen_width // 2 - len(self.table) // 2
        y = self.screen_height // 4

        self.stdscr.addstr(y, x, "Dealer", curses.A_BOLD)
        for i in self.dealer.cardList:
            y += 1
            cardText = str(i)
            if bool:
                self.stdscr.addstr(y, x, cardText)
            else:
                self.stdscr.addstr(y, x, 'Hidden Card')
        y += 1
        self.stdscr.addstr(y, x, self.table)

        space = (self.screen_width - len(self.players) *
                 len(self.table)) / (len(self.players) + 1)

        x = space

        for player in self.players:
            y = self.screen_height * 2 // 4
            self.stdscr.addstr(y, x, "Player " + str(player.id), curses.A_BOLD)
            for i in player.cardList:
                y += 1
                cardText = str(i)
                self.stdscr.addstr(y, x, cardText)
            y += 1
            self.stdscr.addstr(y, x, self.table)
            x += len(self.table) + space

        self.drawScore()
        self.stdscr.refresh()

    '''draw the amount of money each player has in the top left corner'''

    def drawScore(self):

        for idx, player in enumerate(self.players):

            text = "Player " + str(player.id) + " money: $" + str(player.money)

            scorex = self.screen_width // 7 - len(text) // 2
            scorey = self.screen_height // 10 - len(self.players) // 2 + idx

            self.stdscr.addstr(scorey, scorex, text)

        self.stdscr.refresh()

    '''the logic behind a user choosing his/her amount to bet'''

    def makeBetsBeforeCard(self):
        for player in self.players:
            self.bettingCol = 0
            self.drawPlayerBettingOptions(player.id)

            while 1:
                key = self.stdscr.getch()

                if key == curses.KEY_LEFT and self.bettingCol > 0:
                    self.bettingCol -= 1
                elif key == curses.KEY_RIGHT and self.bettingCol < len(self.bettingOptions) - 1:
                    self.bettingCol += 1
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    player.bet = int(self.bettingOptions[self.bettingCol][1:])
                    break

                self.drawPlayerBettingOptions(player.id)

    '''place a white background on select text to show current user option'''

    def colorPrint(self, y, x, text, pair_num):
        self.stdscr.attron(curses.color_pair(pair_num))
        self.stdscr.addstr(y, x, text)
        self.stdscr.attroff(curses.color_pair(pair_num))

    '''logic behind a player choosing another take another card or passing'''

    def hitMeOrPass(self):
        for idx, player in enumerate(self.players):
            self.drawPlayerPlayingOptions(player.id)
            while 1:
                key = self.stdscr.getch()

                if key == curses.KEY_LEFT and self.actionCol > 0:
                    self.actionCol -= 1
                elif key == curses.KEY_RIGHT and self.actionCol < len(self.playerOptions) - 1:
                    self.actionCol += 1
                elif key == curses.KEY_ENTER or key in [10, 13]:
                    if self.actionCol == 0:
                        self.addCardandUpdateScore(idx)
                    else:
                        self.actionCol = 0
                    break
                self.drawPlayerPlayingOptions(player.id)
        self.updateDealer()

    def drawPlayerPlayingOptions(self, player_id):
        self.stdscr.clear()
        self.drawTableAndCards(False)

        title = "Player " + str(player_id) + \
            ": Do you want another card, or passing?"

        x = self.x = self.screen_width // 2 - len(title) // 2
        y = self.screen_height - 6

        self.stdscr.addstr(y, x, title, curses.A_BOLD)

        for idx, row in enumerate(self.playerOptions):
            x = self.screen_width // 2 - len(self.playerOptions)*3 + (8)*idx
            y = self.screen_height - 2 - len(self.playerOptions) // 2
            if idx == self.actionCol:
                self.colorPrint(y, x, row, 1)
            else:
                self.stdscr.addstr(y, x, row)
        self.stdscr.refresh()

    def drawPlayerBettingOptions(self, player_id):
        self.stdscr.clear()

        title = "Player " + self.mydict[player_id] + \
            ": How much are you betting?"

        x = self.x = self.screen_width // 2 - len(title) // 2
        y = self.screen_height // 2

        self.stdscr.addstr(y, x, title, curses.A_BOLD)

        y = self.screen_height // 2 + 2

        for idx, row in enumerate(self.bettingOptions):
            x = self.screen_width // 2 - len(self.bettingOptions)*3 + (8)*idx

            if idx == self.bettingCol:
                self.colorPrint(y, x, row, 1)
            else:
                self.stdscr.addstr(y, x, row)
        self.stdscr.refresh()

    '''if a player chooses to take another card, add to his/her count'''

    def addCardandUpdateScore(self, playerIndex):
        card = self.card.addCard()
        self.players[playerIndex].setUp(card)

    '''check to see if the player beats the dealer, and award money accordingly'''

    def awardWinLoss(self):
        self.drawTableAndCards(True)
        self.drawKeyToContinue()
        dealerCardCount = self.dealer.calculateScore()
        for player in self.players:
            player.winOrLoseMoney(dealerCardCount)
        self.drawTableAndCards(True)

    '''if dealer count is less than 17, then the dealer must add another card'''

    def updateDealer(self):
        if self.dealer.calculateScore() < 17:
            card = self.card.addCard()
            self.dealer.setUp(card)

    '''allow user to view the screen right after cards are revealed'''

    def drawKeyToContinue(self):
        title = "Press any key to bet again, and view updated money amounts."

        x = self.x = self.screen_width // 2 - len(title) // 2
        y = self.screen_height - 3

        self.stdscr.addstr(y, x, title, curses.A_BOLD)
        self.stdscr.refresh()
        self.stdscr.getch()

    '''once a player runs out of money, display a screen before removing the player from the game'''

    def drawPlayerLostPage(self, playerNumber):
        self.stdscr.clear()

        title = "Player " + str(playerNumber) + " lost and is out of the game."
        x = self.x = self.screen_width // 2 - len(title) // 2
        y = self.y = self.screen_height // 2

        self.stdscr.addstr(y, x, title, curses.A_BOLD)

        anotherText = "Press any key to continue."
        x = self.x = self.screen_width // 2 - len(anotherText) // 2
        y = self.y = self.screen_height // 2 + 2

        self.stdscr.addstr(y, x, anotherText, curses.A_BOLD)

        self.stdscr.refresh()
        self.stdscr.getch()

    def checkAndRemovePlayers(self):
        for player in self.players:
            if player.money <= 0:
                self.drawPlayerLostPage(player.id)

        self.players = [x for x in self.players if x.money > 0]

    def checkIfGameEnded(self):
        if (len(self.players) == 0):
            return True
        return False
