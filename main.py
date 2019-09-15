import curses
from blackjack import BlackJack

''' curses library from python is used to build terminal based applications '''


class MenuDisplay:

    def __init__(self):
        self.menu = ['1 Player', '2 Players', '3 Players', 'Exit']
        self.money = ["$500", "$300", "$200", "$100"]
        self.playerChoices = ['1 Player', '2 Players', '3 Players', 'Exit']
        self.title = "Welcome to KP Blackjack - Choose Number of Players"
        self.currentRow = 0
        self.mydict = {'1': 'ONE', "2": "TWO", "3": "THREE"}
        self.players = 0
        self.bettingAmounts = []
        self.numOfChosenPlayers = 0
        curses.wrapper(self.mainloop)

    '''loop that lets user choose number of players, and amount of money to buy in for'''

    def mainloop(self, stdscr):
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.stdscr = stdscr
        self.screen_height, self.screen_width = self.stdscr.getmaxyx()
        self.printMenu(self.title, self.playerChoices)

        while 1:
            if self.takeKeyInput(self.printChosen):

                if self.currentRow == len(self.menu) - 1:
                    if self.confirm("Are you sure you want to exit?"):
                        break
                else:
                    for i in range(self.currentRow+1):
                        self.currentRow = 0

                        buyInTitle = "Player " + \
                            self.mydict[str(i+1)] + \
                            ": How much are you buying in for?"

                        self.printMenu(buyInTitle, self.money)

                        while 1:
                            if self.takeKeyInput(self.addBetValues):
                                break

                            self.printMenu(buyInTitle, self.money)

                    blackjack = BlackJack(
                        self.numOfChosenPlayers, self.stdscr, self.bettingAmounts)
                    if blackjack.mainloop():
                        self.bettingAmounts = []
                        pass

            self.printMenu(self.title, self.playerChoices)

    '''show a screen to alert the user of his/her decision before moving on'''

    def printChosen(self):
        self.printCenter(
            "You selected '{}'".format(self.menu[self.currentRow] + " Press any key."))
        self.numOfChosenPlayers = self.currentRow + 1
        self.stdscr.getch()

    '''print options of choosing number of players, and also amount to buy in'''

    def printMenu(self, title_text, mymenu):
        self.stdscr.clear()

        x = self.x = self.screen_width // 2 - len(title_text) // 2
        y = self.screen_height // 4

        self.stdscr.addstr(y, x, title_text, curses.A_BOLD)

        for idx, row in enumerate(mymenu):
            x = self.screen_width // 2 - len(row) // 2
            y = self.screen_height // 2 - len(mymenu) // 2 + idx
            if idx == self.currentRow:
                self.colorPrint(y, x, row, 1)
            else:
                self.stdscr.addstr(y, x, row)
        self.stdscr.refresh()

    '''place a white background on select text to show current user option'''

    def colorPrint(self, y, x, text, pair_num):
        self.stdscr.attron(curses.color_pair(pair_num))
        self.stdscr.addstr(y, x, text)
        self.stdscr.attroff(curses.color_pair(pair_num))

    '''part of confirm function'''

    def printConfirm(self, selected="yes"):

        y = self.screen_height // 2 + 1
        options_width = 10

        option = "yes"
        x = self.screen_width // 2 - options_width // 2 + len(option)
        if selected == option:
            self.colorPrint(y, x, option, 1)
        else:
            self.stdscr.addstr(y, x, option)

        option = "no"
        x = self.screen_width // 2 + options_width // 2 - len(option)
        if selected == option:
            self.colorPrint(y, x, option, 1)
        else:
            self.stdscr.addstr(y, x, option)

        self.stdscr.refresh()

    '''logic for when the user chooses to manually exit the game'''

    def confirm(self, confirmation_text):
        self.printCenter(confirmation_text)

        current_option = "yes"
        self.printConfirm(current_option)

        while 1:
            key = self.stdscr.getch()

            if key == curses.KEY_RIGHT and current_option == "yes":
                current_option = "no"
            elif key == curses.KEY_LEFT and current_option == "no":
                current_option = "yes"
            elif key == curses.KEY_ENTER or key in [10, 13]:
                return True if current_option == "yes" else False

            self.printConfirm(current_option)

    def printCenter(self, text):
        self.stdscr.clear()
        x = self.screen_width // 2 - len(text) // 2
        y = self.screen_height // 2
        self.stdscr.addstr(y, x, text)
        self.stdscr.refresh()

    '''logic for allowing users to select through menu option'''

    def takeKeyInput(self, functionArg):
        key = self.stdscr.getch()
        if key == curses.KEY_UP and self.currentRow > 0:
            self.currentRow -= 1
        elif key == curses.KEY_DOWN and self.currentRow < len(self.menu) - 1:
            self.currentRow += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            functionArg()
            return True

    def addBetValues(self):
        self.bettingAmounts.append(int(self.money[self.currentRow][1:]))


if __name__ == "__main__":
    MenuDisplay()
