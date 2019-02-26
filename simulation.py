from random import shuffle
import numpy as np
from tabulate import tabulate

class Card:
    def __init__(self, number, shape):
        self.numbers = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
        self.shapes = ['Diamond','Club','Heart', 'Spade']
        self.number = number
        self.shape = shape
        
    def getNumber(self):
        return self.numbers[self.number]

    def getShape(self):
        return self.shapes[self.shape]

class Deck:
    def __init__(self):
        self.reset()

    def reset(self):
        self.cards = []
        for number in range(13):
            for shape in range(4):
                self.cards.append(Card(number,shape))

    def shuffle(self):
        shuffle(self.cards)

    def draw(self):
        return self.cards.pop()

class Player:
    def __init__(self,money = 0, betAmount = 5):
        self.hand = []
        self.money = money
        self.betAmount = betAmount
        self.value = 0
        self.initialMoney = money
    def cardValue(self,inputCards):
        def takeNumber(card):
            return card.number
        cards = sorted(inputCards, key=takeNumber)
        numOfCards = len(cards)
        value = 0
        #value 0  = exceed21
        #value 21 = 3card21 or 4card21
        #value 22 = 5card
        #value 23 = 5card21
        #value 24 = 2card21
        #value 25 = AA
        #value 26 = 5cardExceed21
        if(numOfCards == 2):
            if(cards[0].number == 0):#firstCard = A
                if(cards[1].number == 0):#secondCard = A
                    value = 25 
                elif(cards[1].number >= 9):#secondCard = 10 J Q K
                    value = 24
                else:#secondCard = 2 3 4 5 6 7 8 9
                    value = 11 + cards[1].number + 1
            else:
                value = 0
                for card in cards:
                    if(card.number >= 9):
                        value = value + 10
                    else:
                        value = value + card.number + 1   
        elif(numOfCards == 3):
            if(cards[0].number != 0):
                value = 0
                for card in cards:
                    if (card.number >= 9):
                        value = value + 10
                    else:
                        value = value + card.number + 1
            else:
                if (cards[1].number == 0):
                    if(cards[2].number ==0):
                        value = 21
                    else:
                        value = 11 + cards[2].number + 1
                else:
                    value = 0
                    for i in range(2):
                        if (cards[i+1].number >= 9):
                            value = value + 10
                        else:
                            value = value + cards[i+1].number + 1
                    if(value + 10 <= 21):
                        value = value + 10
                    else:
                        value = value + 1
            if value > 21:
                value = 0
                
        elif(numOfCards == 4):
            value = 0
            for card in cards:
                if (card.number >= 9):
                    value = value + 10
                else:
                    value = value + card.number + 1
            if value > 21:
                value = 0
        else:
            tempValue = 0
            for card in cards:
                if (card.number >= 9):
                    tempValue = tempValue + 10
                else:
                    tempValue = tempValue + card.number + 1
            if (tempValue) == 21:
                value = 23
            elif(tempValue < 21):
                value = 22
            else:
                value = 26
        return value
    def insertHand(self,card):
        self.hand.append(card)
        self.value = self.cardValue(self.hand)
    def clearHand(self):
        self.hand.clear()
        self.value = 0
    def clearMoney(self):
        self.money = self.initialMoney

    
def drawRule(player, deck, rule = 16):#draw of less than 16
    while True:
        value = player.value
        if(value >= 21 or value == 0):
            break
        else:
            if(value <= 15):
                player.insertHand(deck.draw())
            else:
                if value < rule:
                    player.insertHand(deck.draw())
                else:
                    break



def printPlayerInfo():
    print('=============================')
    for i, player in enumerate(players):
        cardText = ''
        for card in player.hand:
            cardText = cardText + card.getNumber() + card.getShape() + ' '
        print('Player ' + str(i+1) + ': ' + cardText)
        print('Value : ' + str(player.value))
        print('Money : ' + str(player.money))
    print('')
    cardText = ''
    for card in banker.hand:
        cardText = cardText + card.getNumber() + card.getShape() + ' '
    print('Banker : ' + cardText)
    print('Value : ' + str(banker.value))
    print('Money : ' + str(banker.money))
    print('=============================')

def distributeWinLoss(player, banker, multiplier):
    winLoss = multiplier * player.betAmount
    player.money = player.money + winLoss
    banker.money = banker.money - winLoss

def calculateWinLoss(players, banker):
    if banker.value == 25:
        for player in players:
            if player.value != 25:
                distributeWinLoss(player, banker, -3)
    elif banker.value == 24:
        for player in players:
            if player.value == 25:
                distributeWinLoss(player, banker, 3)
            elif player.value <= 23:
                distributeWinLoss(player, banker, -2)
            else:
                distributeWinLoss(player, banker, 0)
    else:
        for player in players:
            if player.value == 26:
                distributeWinLoss(player, banker, -2)
            elif player.value == 25:
                distributeWinLoss(player, banker, 3)
            elif player.value == 24:
                distributeWinLoss(player, banker, 2)
            elif player.value == 23:
                distributeWinLoss(player, banker, 3)
            elif player.value == 22:
                distributeWinLoss(player, banker, 2)
            else:
                if banker.value == 21:
                    if player.value != 21:
                        distributeWinLoss(player, banker, -2)
                elif player.value == 21:
                    distributeWinLoss(player, banker, 2)
                elif banker.value == 22:
                    distributeWinLoss(player, banker, -2)
                elif banker.value == 26:
                    distributeWinLoss(player, banker, 2)
                else:
                    if banker.value > player.value:
                        distributeWinLoss(player, banker, -1)
                    elif banker.value < player.value:
                        distributeWinLoss(player, banker, 1)
                    else:
                        distributeWinLoss(player,banker,0)        



deck = Deck()
banker = Player()
players = []
numberOfPlayer = 5          #INPUT HERE
numberOfRound = 10000       #INPUT HERE
playerData = []
bankerData= []

for i in range(numberOfPlayer):
    players.append(Player())
##########################################################
bankerLowest = 16
while True:
    #print('----------------------------------------------------------------------------------')
    if bankerLowest == 21:
        break
    else:
        playerLowest = 16
        while True:
            if playerLowest == 21:
                break
            else:
                bankerTotal = 0
                playerTotal = 0
                bankerAve = 0
                playerAve = 0
                for people in players + [banker]:
                    people.clearMoney()
                
                for game in range(numberOfRound):
##                    if game%10000 ==0:
##                        print(game)
                    deck.reset()
                    deck.shuffle()

                    for player in players:
                        player.insertHand(deck.draw())
                        player.insertHand(deck.draw())
                    banker.insertHand(deck.draw())
                    banker.insertHand(deck.draw())

                    #print('\n------------------------------------------------\n')
                    #print('GAME : ' + str(game + 1) + '\nBanker lowest:' + str(bankerLowest) + '\nPlayer lowest: ' + str(playerLowest))

                    for player in players:
                        drawRule(player, deck, playerLowest)
                    drawRule(banker, deck,playerLowest)
                    calculateWinLoss(players, banker)

                    #printPlayerInfo()

                    for people in players + [banker]:
                        people.clearHand()

                bankerTotal = banker.money
                for player in players:
                    playerTotal = playerTotal + player.money

                bankerAve = bankerTotal
                playerAve = playerTotal/numberOfPlayer

                playerData.append(playerAve)
                bankerData.append(bankerAve)

                
##                print('Banker Average Money(draw if less than ' + str(bankerLowest) + '): ' + str(bankerAve))
##                print('Player Average Money(draw if less than ' + str(playerLowest) + '): ' + str(playerAve))
##                print('')
            playerLowest = playerLowest + 1
        bankerLowest = bankerLowest + 1



playerDataNP = np.array_split(np.array(playerData), 5)
playerHeader = ['Player draw\nif <16','Player draw\nif <17','Player draw\nif <18','Player draw\nif <19','Player draw\nif <20']
bankerHeader = ['Banker draw\nif <16','Banker draw\nif <17','Banker draw\nif <18','Banker draw\nif <19','Banker draw\nif <20']
playerTable = tabulate(playerDataNP, playerHeader, tablefmt="fancy_grid",showindex=bankerHeader)
print('Player Earning Matrix Table')
print(playerTable)
print('')

bankerDataNP = np.array_split(np.array(bankerData), 5)
playerHeader = ['Player draw\nif <16','Player draw\nif <17','Player draw\nif <18','Player draw\nif <19','Player draw\nif <20']
bankerHeader = ['Banker draw\nif <16','Banker draw\nif <17','Banker draw\nif <18','Banker draw\nif <19','Banker draw\nif <20']
bankerTable = tabulate(bankerDataNP, playerHeader, tablefmt="fancy_grid",showindex=bankerHeader)
print('Banker Earning Matrix Table')
print(bankerTable)
print('')
    



##for game in range(50):
##    deck.reset()
##    deck.shuffle()
##
##    for player in players:
##        player.insertHand(deck.draw())
##        player.insertHand(deck.draw())
##    banker.insertHand(deck.draw())
##    banker.insertHand(deck.draw())
##
##    #print('\n------------------------- GAME ' + str(game + 1) +'-------------------------\n')
##
##    for player in players:
##        drawRule(player, deck, 19)
##    drawRule(banker, deck,17)
##    calculateWinLoss(players, banker)
##
##    #printPlayerInfo()
##
##    for people in players + [banker]:
##        people.clearHand()
##
##    bankerTotal = bankerTotal + banker.money
##    playerTotal = playerTotal + player.money
##
##bankerAve = bankerTotal/50
##playerAve = (playerTotal/50)/4
##
##print('Banker Average: ' + str(bankerAve))
##print('Player Average: ' + str(playerAve))





