import numpy as np
import PIL
import pyautogui
import cv2
from PokerPlayer import Player
import time
from playsound import playsound
import configMultiplayer

# Globals
twoPlayerMode = True
notifyExtraHands = True
whiteThreshold = 250
sleepTimeShort = 0.25
sleepTimeLong = 1.5


def main():
    # Locals
    programRunning = False
    playerOne = Player('Player One', notifyExtraHands)

    if twoPlayerMode:
        playerTwo = Player('Player Two', notifyExtraHands)
        playerOne, playerTwo = configMultiplayer.configTwoPlayer(playerOne, playerTwo)
        players = [playerOne, playerTwo]
        print('Running in two player mode!')
    else:
        players = [playerOne]
        print('Running in single player mode!')

    print('Move mouse to top of screen to begin')

    # ------------------------
    # Main loop
    # ------------------------
    while True:
        if not programRunning:
            time.sleep(sleepTimeShort)

            # Start program if mouse is moved to top of screen
            currentX, currentY = pyautogui.position()
            if currentY < 10:
                print('Program running! Move mouse to bottom of screen to pause program')
                programRunning = True

        if programRunning:
            time.sleep(sleepTimeLong)

            # Exit if user moves mouse to bottom of screen
            currentX, currentY = pyautogui.position()
            if currentY > 1070:
                print('Program pausing... Move mouse to top of screen to restart')
                programRunning = False
                for player in players:
                    player.cardsActiveOld = False
                continue

            for player in players:
                time.sleep(sleepTimeShort)

                # Grab screenshot of game
                player.screen = np.array(PIL.ImageGrab.grab())
                player.screen = cv2.cvtColor(player.screen, cv2.COLOR_RGB2GRAY)

                # Check if player has cards
                player.cardsActive = player.screen[player.cardActiveRow][player.cardActiveCol] > whiteThreshold

                # Process the cards when they appear
                if player.cardsActive:
                    if not player.cardsActiveOld:
                        player.cardOne, player.cardTwo = player.ProcessCards()
                        print(player.name + ': ' + 'Detected ' + player.cardOne.value + ' of ' + player.cardOne.suit +
                              ', ' + player.cardTwo.value + ' of ' + player.cardTwo.suit)

                        # Check if the cards detected are valid
                        if not player.cardOne.validCard or not player.cardTwo.validCard:
                            print(player.name + ': ' + 'Bad card read, trying to read again')
                            continue

                        # Check if hand is good
                        goodHand = player.IsHandGood(player.cardOne, player.cardTwo)
                        if goodHand:
                            playsound('notification.mp3')
                            print('Good hand detected! Move mouse to top of screen to start program again')
                            programRunning = False
                            continue

                    # If hand is not good, check if the fold box is ticked
                    checkBoxTicked = player.screen[player.checkBoxRow][player.checkBoxCol] > whiteThreshold or \
                                     player.screen[player.checkFoldBoxRow][player.checkFoldBoxCol] > whiteThreshold

                    if not checkBoxTicked:
                        print(player.name + ': ' + 'Attempting to auto fold...')
                        player.AutoFold()

                player.cardsActiveOld = player.cardsActive


if __name__ == '__main__':
    main()
