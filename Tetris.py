from cmu_graphics import *

import math
import random  

def onAppStart(app):
    # step1
    app.rows = 15
    app.cols = 10
    app.boardLeft = 100
    app.boardTop = 60
    app.boardWidth = 200
    app.boardHeight = 300
    app.cellBorderWidth = 1
    restart(app)
 
def restart(app):
    url1 = 'cmu://1395/127744/OMG+NewJeans.mp3'
    app.sound1 = Sound(url1)
    app.sound1.play(loop=True)
    url2 = 'cmu://1395/127774/01+Ditto.mp3'
    app.sound2 = Sound(url2)
    app.sound2.pause()
    app.board = [([None] * app.cols) for row in range(app.rows)]
    # step2 
    loadTetrisPieces(app)
    # Start with piece 0 (the red I piece) loaded
    app.piece = app.tetrisPieces[0] 
    app.pieceColor = app.tetrisPieceColors[0]
    app.pieceTopRow = 0
    app.pieceLeftCol = 0
    
    # step6
    app.currentPieceIndex = random.randrange(len(app.tetrisPieces))
    loadNextPiece(app)
    app.stepsPerSecond = 1 
    app.paused = False
    app.gameOver = False
    app.displayGameOver = False
    
    # step7
    app.rowsPopped = 0
    app.scores = 0
    app.level = 1
    
    # Plus Score
    app.displayScore = False
    app.timepassed = 0
    app.plusScoreCoordinate = None
    
    # make it pretty
    app.url = 'cmu://1395/127472/Screen+Shot+2023-02-27+at+11.47.15+AM.png'

    

def loadNextPiece(app):
    app.nextPieceIndex = pieceIndex = random.randrange(len(app.tetrisPieces))
    loadPiece(app, app.currentPieceIndex)

def loadTetrisPieces(app):
    # Seven "standard" pieces (tetrominoes)
    iPiece = [[  True,  True,  True,  True ]]
    jPiece = [[  True, False, False ],
              [  True,  True,  True ]]
    lPiece = [[ False, False,  True ],
              [  True,  True,  True ]]
    oPiece = [[  True,  True ],
              [  True,  True ]]
    sPiece = [[ False,  True,  True ],
              [  True,  True, False ]]
    tPiece = [[ False,  True, False ],
              [  True,  True,  True ]]
    zPiece = [[  True,  True, False ],
              [ False,  True,  True ]] 
    app.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece,
                         sPiece, tPiece, zPiece ]
    yellow = rgb(255,235,50)
    pink = rgb(255, 150, 225)
    green = rgb(85, 242, 120)
    aquamarine = rgb(20, 245, 210)
    purple = rgb(151, 115, 255)
    orange = rgb(255, 146, 85)
    blue = rgb(85, 145, 255)
    app.tetrisPieceColors = [ gradient(green,'white'),
                              gradient(yellow,'white'),
                              gradient(orange,'white'),
                              gradient(aquamarine,'white'),
                              gradient(purple,'white'),
                              gradient(pink,'white'),
                              gradient(blue,'white') ]

def loadPiece(app, pieceIndex):
    app.piece = app.tetrisPieces[pieceIndex]
    app.pieceColor = app.tetrisPieceColors[pieceIndex]
    pieceCols = len(app.piece[0])
    app.pieceTopRow = 0
    app.pieceLeftCol = app.cols//2 - math.ceil(pieceCols/2)

def onStep(app):
    if app.pieceTopRow == 0:
            if not pieceIsLegal(app):
                app.gameOver = True
                app.stepsPerSecond = 0
                app.sound1.pause()
                app.displayGameOver = True
                app.sound2.play(loop=True)
    if not app.gameOver:
        if not app.paused:
            takeStep(app)
    # else:
    #     app.stepsPerSecond = 0
    #     app.displayGameOver = True

def takeStep(app):
    if not app.paused:
        if not movePiece(app, +1, 0):
            # We could not move the piece, so place it on the board:
            cellLeft, cellTop = getCellLeftTop(app, 
                                            app.pieceTopRow, app.pieceLeftCol)
            placePieceOnBoard(app)
            app.plusScoreCoordinate = cellLeft, cellTop
            removeFullRows(app)
            loadNextPiece(app)
    if app.rowsPopped >= 5:
        app.stepsPerSecond = 1.5
        app.level = 2
        app.url = 'cmu://1395/127589/IMG_3712.jpg'
    if app.rowsPopped >= 10:
        app.stepsPerSecond = 2
        app.level = 3
        app.url = 'cmu://1395/127557/IMG_3710.jpg'
    if app.rowsPopped >= 20:
        app.stepsPerSecond = 2.5
        app.level = 4
        app.url = 'cmu://1395/127602/IMG_3715.jpg' # Sun
    if app.rowsPopped >= 30:
        app.stepsPerSecond = 3
        app.level = 5
        app.url = 'cmu://1395/127605/IMG_3716.jpg' # sky

def removeFullRows(app):
    # app.timepassed = 0
    row, col = 0, 0
    while row < app.rows:
        fillCount = 0
        rowsRemoved = 0
        for col in range (app.cols):
            if app.board[row][col] != None:
                fillCount += 1
        if fillCount == app.cols:
            app.board.pop(row)
            app.rowsPopped += 1
            app.board.insert(0, ([None] * app.cols))
            rowsRemoved += 1
        else:
            row += 1
        if rowsRemoved == 1:
            app.score = 40*app.level
            app.scores += app.score
            # timePassed(app)
        elif rowsRemoved == 2:
            app.score = 100*app.level
            app.scores += app.score
        elif rowsRemoved == 3:
            app.scores = 300*app.level
            app.scores += app.score
        elif rowsRemoved == 4:
            app.scores = 1200*app.level
            app.scores += app.score
            
# def timePassed(app):
#     app.timepassed += 1
#     while app.timepassed < 3:
#         app.displayScore=True
#     # app.displayScore = False
#     # app.plusScoreCoordinate = None
  
def onMousePress(app, mouseX, mouseY):
    if (360-10 <= mouseX <= 360+10 and
        30-10 <= mouseY <= 30+10):
        app.paused = not app.paused
        if app.paused:
            app.sound1.pause()
        else:
            app.sound1.play(loop=True)

def onKeyPress(app, key):
    if not app.gameOver:
        if key == 'p':
            app.paused = not app.paused
            if app.paused:
                app.sound1.pause()
            else:
                app.sound1.play(loop=True)
        elif key == 'left':
            movePiece(app, 0, -1)
        elif key == 'right':
            movePiece(app, 0, +1)
        elif key == 'down':
            movePiece(app, +1, 0)
        elif key == 'space': 
            hardDropPiece(app)
        elif key == 'up': 
            rotatePieceClockwise(app)
        elif key == 's': takeStep(app)
    else:
        if key == 'enter':
            app.sound2.pause()
            restart(app)

def placePieceOnBoard(app):
    rows, cols = len(app.piece), len(app.piece[0])
    for row in range (rows):
        for col in range (cols):
            if app.piece[row][col]:
                # boardRow = row + (app.rows-rows)
                # boardCol = col + (app.cols-cols)
                boardRow = app.pieceTopRow+row
                boardCol = app.pieceLeftCol+col
                app.board[boardRow][boardCol] = app.pieceColor
                app.currentPieceIndex = app.nextPieceIndex

def rotatePieceClockwise(app):
    oldPiece = app.piece
    oldTopRow = app.pieceTopRow
    oldLeftCol = app.pieceLeftCol
    oldRows, oldCols = len(app.piece), len(app.piece[0])
    app.piece = rotate2dListClockwise(oldPiece)
    
    # adjust the top row of the new piece
    centerRow = oldTopRow + oldRows//2
    newRows = oldCols
    app.pieceTopRow = centerRow - newRows//2
    
    # adjust the left column of the new piece
    centerCol = oldLeftCol + oldCols//2
    newCols = oldRows
    app.pieceLeftCol = centerCol - newCols//2
    
    # check if it is legal, restore to orginal position if not legal
    if not pieceIsLegal(app):
        app.piece = oldPiece
        app.pieceTopRow = oldTopRow
        app.pieceLeftCol = oldLeftCol

def movePiece(app, drow, dcol):
    app.pieceTopRow += drow
    app.pieceLeftCol += dcol
    if not pieceIsLegal(app):
        app.pieceTopRow -= drow
        app.pieceLeftCol -= dcol
        return False
    return True
    
def hardDropPiece(app):
    while movePiece(app, +1, 0):
        pass
        
def pieceIsLegal(app):
    # check if it is over bound
    if not (0 <= app.pieceTopRow <= app.rows-len(app.piece) and 
            0 <= app.pieceLeftCol <= app.cols-len(app.piece[0])):
        return False
    rows, cols = len(app.piece), len(app.piece[0])
    for row in range (rows):
        for col in range (cols):
            if app.piece[row][col] == True:
                pieceRow = app.pieceTopRow + row
                pieceCol = app.pieceLeftCol + col
                if app.board[pieceRow][pieceCol] != None:
                    return False 
    return True
        
def redrawAll(app):
    imageWidth, imageHeight = getImageSize(app.url)
    drawImage(app.url, 0, 0, 
              width=imageWidth/2.5, height=imageHeight/2.5)
    drawBoard(app)
    drawPiece(app)
    drawBoardBorder(app)
    drawScore(app)
    if app.displayGameOver:
        drawGameOver(app)
        
    # if app.displayScore:
    #     drawPlusedScore(app)
    if not app.gameOver:
        drawPause(app)
    
def drawPause(app):
    if app.paused:
        drawPolygon(360, 21, 360, 39, 377, 30, fill='white')
    else:
        drawRect(360, 20, 5, 17, fill='white')
        drawRect(370, 20, 5, 17, fill='white')

def drawPlusedScore(app):
    if app.plusScoreCoordinate != None:
        left, top = app.plusScoreCoordinate
        drawLabel(f'+{app.score}', 350, top, fill='white', 
              font='montserrat', bold=True, size=25)
    
def drawGameOver(app):
    # drawRect(0, 118, app.width, 164, fill='black')
    # drawLabel(f'GAME OVER', app.width//2, 180, fill='white', 
    #           font='montserrat', bold=True, size=30)
    # drawLabel(f'Press Enter to restart', app.width//2, 220, fill='white', 
    #           font='montserrat', bold=True, size=22)
    url = 'cmu://1395/127837/Screen+Shot+2023-02-27+at+4.56.06+PM.png'
    imageWidth, imageHeight = getImageSize(url)
    drawImage(url, 0, 0, 
              width=400, height=400)

def drawScore(app):
    drawLabel(f'LEVEL {app.level}', 50, 30, fill='white', 
              font='montserrat', bold=True, size=16)
    drawLabel(f'{app.scores}', app.width//2, 30, fill='white', 
              font='montserrat', bold=True, size=25)

def drawPiece(app):
    if app.piece != None:
        rows, cols = len(app.piece), len(app.piece[0])
        for row in range (rows):
            for col in range (cols):
                if app.piece[row][col] == True:
                    drawPieceCube(app, app.pieceTopRow+row, 
                             app.pieceLeftCol+col, app.pieceColor)
    nextPiece = app.tetrisPieces[app.nextPieceIndex]
    color = app.tetrisPieceColors[app.nextPieceIndex]
    if nextPiece != None:
        rows, cols = len(nextPiece), len(nextPiece[0])
        for row in range (rows):
            for col in range (cols):
                if nextPiece[row][col] == True:
                    drawLabel('NEXT UP', 50, 80, font='montserrat', 
                              fill='white', size=14)
                    drawPreviewPieceCube(app, 0+row, -4+col, color)

def drawPreviewPieceCube(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    left, top = cellLeft*0.8+3, cellTop*0.8+52
    cellWidth, cellHeight = getCellSize(app)
    cellWidth *= 0.8
    # transfer the color if placed
    drawRect(left, top, cellWidth, cellWidth,
             fill=color, border='white', 
             borderWidth=app.cellBorderWidth)
    # Draw Cube Highlights
    drawRect(left+2, top+2, cellWidth//3, cellWidth//3,
             fill='white',
             borderWidth=app.cellBorderWidth)
    drawRect(left+8, top+2, cellWidth//3, cellWidth//3,
             fill='white', opacity=50, 
             borderWidth=app.cellBorderWidth)
    drawRect(left+2, top+8, cellWidth//3, cellWidth//3,
             fill='white', opacity=50, 
             borderWidth=app.cellBorderWidth)

def drawPieceCube(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    # transfer the color if placed
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='white', 
             borderWidth=app.cellBorderWidth)
    # Draw Cube Highlights
    drawRect(cellLeft+2, cellTop+2, cellWidth//3, cellHeight//3,
             fill='white',
             borderWidth=app.cellBorderWidth)
    drawRect(cellLeft+8, cellTop+2, cellWidth//3, cellHeight//3,
             fill='white', opacity=50, 
             borderWidth=app.cellBorderWidth)
    drawRect(cellLeft+2, cellTop+8, cellWidth//3, cellHeight//3,
             fill='white', opacity=50, 
             borderWidth=app.cellBorderWidth)

def drawBoard(app):
    # background color
    # drawRect(0, 0, app.width, app.height, fill=app.pieceColor, opacity=50)
    # draw board
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
             fill='black', opacity=70)
    # draw Next Up board
    color = app.tetrisPieceColors[app.nextPieceIndex]
    drawRect(10, 60, 80, 90,
             fill=color, opacity=25)
    for row in range(app.rows):
        for col in range(app.cols):
            color = app.board[row][col]
            drawCell(app, row, col, color)
    cellWidth, cellHeight = getCellSize(app)
    for i in range (9):
        for j in range (14):
            drawCircle(120+i*cellWidth, 80+j*cellWidth, 1.5, 
                       fill=app.pieceColor, opacity=80)

def drawBoardBorder(app):
    color = gradient('gold', 'white', 'gold')
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
               fill=None, border=app.pieceColor, opacity=70,
               borderWidth=2*app.cellBorderWidth)
    drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
               fill=None, border=app.pieceColor, opacity=70,
               borderWidth=2*app.cellBorderWidth)
    # draw preview border
    color = app.tetrisPieceColors[app.nextPieceIndex]
    drawRect(10, 60, 80, 90, fill=None, 
             border=color, borderWidth=2, opacity=80)
  

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border=None, opacity=70,
             borderWidth=app.cellBorderWidth)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    # cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellWidth)
    
def rotate2dListClockwise(L):
    # if L is RxC
    oldRows, oldCols = len(L), len(L[0])
    # then M is CxR
    newRows, newCols = len(L[0]), len(L)
    M = make2dList(newRows, newCols)
    for oldRow in range (oldRows):
        for oldCol in range (oldCols):
            M[oldCol][(oldRows-1)-oldRow] = L[oldRow][oldCol]
    return M
    
def make2dList(rows, cols):
    return [ [None]*cols for row in range (rows)]
    
def main():
    runApp()

main()
