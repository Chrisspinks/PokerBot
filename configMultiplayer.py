
def configTwoPlayer(playerOne, playerTwo):
    playerTwoOffset = 960

    # ------------------------------------
    # Player One
    # ------------------------------------
    # Fold buttons
    playerOne.smallFoldRow = 966
    playerOne.smallFoldCol = 472
    playerOne.bigFoldRow = 924
    playerOne.bigFoldCol = 377
    playerOne.checkBoxRow = 966
    playerOne.checkBoxCol = 472
    playerOne.checkFoldBoxRow = 966
    playerOne.checkFoldBoxCol = 462
    playerOne.checkBoxRowButton = 909
    playerOne.checkBoxColButton = 571

    # Card constants
    playerOne.cardValueWidth = 30
    playerOne.cardValueHeight = 30
    playerOne.cardSuitWidth = 30
    playerOne.cardSuitHeight = 30
    playerOne.cardNumStartRow = 605
    playerOne.cardSuitStartRow = 635
    playerOne.cardActiveRow = 615
    playerOne.cardActiveCol = 469

    # Card one
    playerOne.cardOneNumStartCol = 434
    playerOne.cardOneSuitStartCol = 445

    # Card two
    playerOne.cardTwoNumStartCol = 483
    playerOne.cardTwoSuitStartCol = 491

    # Other
    playerOne.redBlackThreshold = 60
    playerOne.heartDiamondThreshold = 184
    playerOne.clubSpadeThreshold = 166

    # ------------------------------------
    # Player Two
    # ------------------------------------
    # Fold buttons
    playerTwo.smallFoldRow = playerOne.smallFoldRow
    playerTwo.smallFoldCol = playerOne.smallFoldCol + playerTwoOffset
    playerTwo.bigFoldRow = playerOne.bigFoldRow
    playerTwo.bigFoldCol = playerOne.bigFoldCol + playerTwoOffset
    playerTwo.checkBoxRow = playerOne.checkBoxRow
    playerTwo.checkBoxCol = playerOne.checkBoxCol + playerTwoOffset
    playerTwo.checkFoldBoxRow = playerOne.checkFoldBoxRow
    playerTwo.checkFoldBoxCol = playerOne.checkFoldBoxCol + playerTwoOffset
    playerTwo.checkBoxRowButton = playerOne.checkBoxRowButton
    playerTwo.checkBoxColButton = playerOne.checkBoxColButton + playerTwoOffset

    # Card constants
    playerTwo.cardValueWidth = playerOne.cardValueWidth
    playerTwo.cardValueHeight = playerOne.cardValueHeight
    playerTwo.cardSuitWidth = playerOne.cardSuitWidth
    playerTwo.cardSuitHeight = playerOne.cardSuitHeight
    playerTwo.cardNumStartRow = playerOne.cardNumStartRow
    playerTwo.cardSuitStartRow = playerOne.cardSuitStartRow
    playerTwo.cardActiveRow = playerOne.cardActiveRow
    playerTwo.cardActiveCol = playerOne.cardActiveCol + playerTwoOffset

    # Card one
    playerTwo.cardOneNumStartCol = playerOne.cardOneNumStartCol + playerTwoOffset
    playerTwo.cardOneSuitStartCol = playerOne.cardOneSuitStartCol + playerTwoOffset

    # Card two
    playerTwo.cardTwoNumStartCol = playerOne.cardTwoNumStartCol + playerTwoOffset
    playerTwo.cardTwoSuitStartCol = playerOne.cardTwoSuitStartCol + playerTwoOffset

    # Other
    playerTwo.redBlackThreshold = playerOne.redBlackThreshold
    playerTwo.heartDiamondThreshold = playerOne.heartDiamondThreshold
    playerTwo.clubSpadeThreshold = playerOne.clubSpadeThreshold

    return playerOne, playerTwo
