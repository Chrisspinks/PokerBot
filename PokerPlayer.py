import numpy as np
import pytesseract
import PIL
import pyautogui
import imageio
import cv2
import time
from PIL import Image
from card import Card
import os


class Player:
    def __init__(self, name, notifyExtraHands):
        self.name = name
        self.notifyExtraHands = notifyExtraHands
        self.cardOne = Card
        self.cardTwo = Card
        self.pauseTime = 0.2
        self.screen = []
        self.cardsActive = False
        self.cardsActiveOld = False

        # Fold buttons
        self.smallFoldRow = 934
        self.smallFoldCol = 970
        self.bigFoldRow = 881
        self.bigFoldCol = 795
        self.checkBoxRow = 935
        self.checkBoxCol = 947
        self.checkFoldBoxRow = 936
        self.checkFoldBoxCol = 933
        self.checkBoxRowButton = 864
        self.checkBoxColButton = 1012

        # Card constants
        self.cardValueWidth = 40
        self.cardValueHeight = 40
        self.cardSuitWidth = 40
        self.cardSuitHeight = 40
        self.cardNumStartRow = 633
        self.cardSuitStartRow = 681
        self.cardActiveRow = 643
        self.cardActiveCol = 935

        # Card one
        self.cardOneNumStartCol = 890
        self.cardOneSuitStartCol = 903

        # Card two
        self.cardTwoNumStartCol = 967
        self.cardTwoSuitStartCol = 981

        # Other
        self.redBlackThreshold = 60
        self.heartDiamondThreshold = 171
        self.clubSpadeThreshold = 148
        self.imgThreshold = 150
        self.fileName = "currentCard.png"
        self.allCards = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        self.allSuits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.goodHandBaseList = ['AKs', 'AQs', 'AJs', 'ATs', 'A9s', 'A8s', 'A7s', 'A6s', 'A5s', 'A4s', 'A3s', 'A2s',
                                 'KQs', 'KJs', 'KTs',
                                 'QJs', 'QTs',
                                 'JTs', 'J9s',
                                 'T9s',
                                 'AKo', 'AQo', 'AJo', 'ATo',
                                 'KQo', 'KJo']
        self.goodHandExtrasList = ['K9s', 'Q9s', 'T9s', '98s', '87s', '76s', '65s', '54s',
                                   'QJo', 'JTo', 'T9o', '98o']

    def AutoFold(self):
        time.sleep(self.pauseTime)
        pyautogui.click(self.bigFoldCol, self.bigFoldRow)
        time.sleep(self.pauseTime)
        pyautogui.click(self.smallFoldCol, self.smallFoldRow)
        time.sleep(self.pauseTime)
        pyautogui.click(self.checkBoxColButton, self.checkBoxRowButton)

    def ProcessCards(self):
        # ---------------------------------------------------
        # Process first card
        # ---------------------------------------------------
        cardOneNumCoords = [self.cardOneNumStartCol, self.cardNumStartRow, self.cardOneNumStartCol + self.cardValueWidth, self.cardNumStartRow
                            + self.cardValueHeight]
        cardOneValueArray = np.array(PIL.ImageGrab.grab(bbox=cardOneNumCoords))
        cardOneValueArray = cv2.cvtColor(cardOneValueArray, cv2.COLOR_RGB2GRAY)
        cardOneValue = self.DetermineValue(cardOneValueArray)

        # Screenshot first card suit
        cardOneSuitCoords = [self.cardOneSuitStartCol, self.cardSuitStartRow, self.cardOneSuitStartCol + self.cardSuitWidth, self.cardSuitStartRow +
                             self.cardSuitHeight]
        cardOneSuitArray = np.array(PIL.ImageGrab.grab(bbox=cardOneSuitCoords))
        cardOneSuitArray = cv2.cvtColor(cardOneSuitArray, cv2.COLOR_RGB2GRAY)
        cardOneSuit = self.DetermineSuit(cardOneSuitArray)

        self.cardOne = Card(cardOneValue, cardOneSuit)

        # ---------------------------------------------------
        # Process second card
        # ---------------------------------------------------
        cardTwoNumCoords = [self.cardTwoNumStartCol, self.cardNumStartRow, self.cardTwoNumStartCol + self.cardValueWidth, self.cardNumStartRow
                            + self.cardValueHeight]
        cardTwoValueArray = np.array(PIL.ImageGrab.grab(bbox=cardTwoNumCoords))
        cardTwoValueArray = cv2.cvtColor(cardTwoValueArray, cv2.COLOR_RGB2GRAY)
        cardTwoValue = self.DetermineValue(cardTwoValueArray)

        # Screenshot second card suit
        cardTwoSuitCoords = [self.cardTwoSuitStartCol, self.cardSuitStartRow, self.cardTwoSuitStartCol + self.cardSuitWidth, self.cardSuitStartRow +
                             self.cardSuitHeight]
        cardTwoSuitArray = np.array(PIL.ImageGrab.grab(bbox=cardTwoSuitCoords))
        cardTwoSuitArray = cv2.cvtColor(cardTwoSuitArray, cv2.COLOR_RGB2GRAY)
        cardTwoSuit = self.DetermineSuit(cardTwoSuitArray)

        self.cardTwo = Card(cardTwoValue, cardTwoSuit)

        # Check the cards are valid
        self.cardOne, self.cardTwo = self.ValidateCards(self.cardOne, self.cardTwo)

        return self.cardOne, self.cardTwo

    def DetermineValue(self, imgArray):
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

        # Duplicate the image (otherwise tesseract can't read it)
        doubleCardImage = np.concatenate((imgArray, imgArray), axis=1)

        # Convert card value to black
        doubleCardImage = self.ConvertToBlack(doubleCardImage)

        # Save image and process
        imageio.imwrite(self.fileName, doubleCardImage)
        img = Image.open(self.fileName)
        result = pytesseract.image_to_string(img, config="--psm 13")
        img.close()

        os.remove(self.fileName)

        cardVal = result[0]
        if cardVal == '1':
            cardVal = 'T'

        return cardVal

    def DetermineSuit(self, suitArray):
        if np.min(suitArray) < self.redBlackThreshold:
            if np.average(suitArray) < self.clubSpadeThreshold:
                suit = 'Spades'
            else:
                suit = 'Clubs'
        else:
            if np.average(suitArray) < self.heartDiamondThreshold:
                suit = 'Hearts'
            else:
                suit = 'Diamonds'

        return suit

    def ConvertToBlack(self, img):
        for r in range(0, img.shape[0]):
            for c in range(0, img.shape[1]):
                if img[r][c] < self.imgThreshold:
                    img[r][c] = 0

        return img

    def ValidateCards(self, cardOne, cardTwo):
        cardOne.validCard = cardOne.value in self.allCards and cardOne.suit in self.allSuits
        cardTwo.validCard = cardTwo.value in self.allCards and cardTwo.suit in self.allSuits

        return cardOne, cardTwo

    def IsHandGood(self, cardOne, cardTwo):
        # Return true if its a pair
        if cardOne.value == cardTwo.value:
            return True

        hand = self.GetHandOrdered(cardOne, cardTwo)

        if hand in self.goodHandBaseList:
            return True

        if self.notifyExtraHands and hand in self.goodHandExtrasList:
            return True

        return False

    def GetHandOrdered(self, cardOne, cardTwo):
        unorderedHand = cardOne.value + cardTwo.value

        if self.allCards.index(unorderedHand[0]) < self.allCards.index(unorderedHand[1]):
            orderedHand = unorderedHand[::-1]
        else:
            orderedHand = unorderedHand

        if cardOne.suit == cardTwo.suit:
            orderedHand += 's'
        else:
            orderedHand += 'o'

        return orderedHand
