import sys
from cmu_112_graphics import *
import math
import random
import time

'''
Content:
    Towers
    Minions
    Map
'''

'''
Ideas:
    Randomly generated path or let player make own path
    Gets progressively harder as the rounds go by
'''


#############################################################################
# Splash Screen 
#############################################################################   


#############################################################################
# Enemies
#############################################################################
# enemies class
# each enemy should have:
    # speed
    # camouflage or none
            # True = camo, False = none
    # health
    # radius/size
    # damage it causes at the end
    # color
class Enemy(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.seenPath = set()
    
    def drawEnemy(self, canvas, app):
        margin = 10
        if len(app.enemies) >= 1:
            canvas.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, 
                           self.y+self.r, fill = self.color, width = 2)
            canvas.create_text(self.x, self.y - margin, text = f"{self.health}")
    
    def moveEnemy(self, app):
        if (self.x-self.r >= app.width or self.x+self.r <= 0 or 
            self.y-self.r >= app.height or self.y+self.r <= 0):
            app.health -= self.destruct
            app.enemies.remove(self)
        else:
            (row, col) = getCell(app, self.x, self.y)
            (x0, y0, x1, y1) = getCellBounds(app, row, col) 
            self.seenPath.add((row, col))
            if moveEnemyLegalX(self, app, row, col):
                self.lastMovement = 0
                if self.speedy > 0 and ((y0 + y1)//2 > self.y):
                    self.y += self.speedy
                elif self.speedy < 0 and ((y0 + y1)//2 > self.y):
                    self.y += self.speedy
                else:
                    self.x += self.speedx
            elif moveEnemyLegalY(self, app, row, col):
                self.lastMovement = 1
                if self.speedx < 0 and (self.x < (x0 + x1)//2):
                    self.x += self.speedx
                elif self.speedx > 0 and (self.x < (x0 + x1)//2):
                    self.x += self.speedx
                else:
                    self.y += self.speedy
            else:
                if self.lastMovement == 0:
                    self.x += self.speedx
                else:
                    self.y += self.speedy


# checks if a x direction move is legal
def moveEnemyLegalX(self, app, row, col):
    if (row, col+1) not in self.seenPath and app.board[row][col+1] == app.pathColor:
        self.speedx = abs(self.speedx)
        return True
    elif (row, col-1) not in self.seenPath and app.board[row][col-1] == app.pathColor:
        self.speedx = -abs(self.speedx)
        return True
    return False

# checks if a y direction move is legal
def moveEnemyLegalY(self, app, row, col):
    if (row+1, col) not in self.seenPath and app.board[row+1][col] == app.pathColor:
        self.speedy = abs(self.speedy)
        return True
    elif (row-1, col) not in self.seenPath and app.board[row-1][col] == app.pathColor:
        self.speedy = -abs(self.speedy)
        return True
    return False


# basic balloon
class Red(Enemy):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speedx = 4
        self.speedy = 4
        self.lastMovement = 0
        self.camo = False
        self.health = 100
        self.r = 20
        self.destruct = 2
        self.color = 'red'
        self.seenPath = set()
        self.count = 0
        self.worth = 30

# sane as red but with more HP
class Blue(Enemy):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speedx = 4
        self.speedy = 4
        self.lastMovement = 0
        self.camo = False
        self.health = 200
        self.r = 20
        self.destruct = 5
        self.color = 'blue'
        self.seenPath = set()
        self.count = 0
        self.worth = 50

# faster than blue and yellow, but with less HP
class Yellow(Enemy):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speedx = 7
        self.speedy = 7
        self.lastMovement = 0
        self.camo = True
        self.health = 150
        self.r = 20
        self.destruct = 3
        self.color = 'yellow'
        self.seenPath = set()
        self.count = 0
        self.worth = 100

# much slower but has a lot more HP
class Boss(Enemy):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speedx = 2
        self.speedy = 2
        self.lastMovement = 0
        self.camo = False
        self.health = 1000
        self.r = 50
        self.destruct = 20
        self.color = 'brown'
        self.seenPath = set()
        self.count = 0
        self.worth = 1000


#############################################################################
# Turrets
#############################################################################
# turrets class
# each turret should have:
    # range
    # radius/size
    # fire rate
    # type of shots (single enemy, multi enemy, splash)
            # False = Single, True = Multi / Splash
    # dmg / shot
class Turret(object):
    def __init__(self, x , y):
        self.x = x
        self.y = y

    def drawTurret(self, canvas):
        canvas.create_rectangle(self.x-self.r, self.y-self.r, self.x+self.r, 
                           self.y+self.r, fill = self.color)
                

# slower attack speed but more dmg
class Cannon(Turret):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 200
        self.r = 20
        self.attackSpeed = 30
        self.typeShot = False 
        self.damage = 50
        self.price = 100
        self.color = 'black'

# faster attack speed but less damage
class Dart(Turret):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 200
        self.r = 20
        self.attackSpeed = 30
        self.typeShot = False 
        self.damage = 50
        self.price = 100
        self.color = 'red'

# does low damage but has splash damage
class Bomber(Turret):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 200
        self.r = 30
        self.attackSpeed = 5
        self.typeShot = True
        self.shotRadius = 100
        self.damage = 50
        self.price = 50
        self.color = 'grey'

#############################################################################
# Drawing
#############################################################################


def appStarted(app):
    app.rows = app.height // 20
    app.cols = app.width // 40
    app.cellWidth = (app.width-200) // app.cols
    app.cellHeight = app.cellWidth
    app.shopMargin = app.width // 4
    app.gridWidth = app.width - app.shopMargin
    app.boardColor = 'green'
    app.pathColor = 'goldenrod3'
    #app.board = [ [app.boardColor] * app.cols for row in range(app.rows)]
    (app.startX, app.startY, app.board) = boardGenerator(app)
    app.cellCount = 0
    app.enemies = [ ] 
    app.turrets = [ ]
    app.wave = 1
    app.health = 100
    app.currency = 10000
    app.pause = True
    app.gameOver = False
    app.cannonPrice = 100
    app.dartPrice = 150
    app.bombTowerPrice = 50
    app.selectedTurret = None
    app.selectedTurretX = None
    app.selectedTurretY = None
    app.enemySpawnCounter = 0
    app.initialTime = time.time()
    app.waveFinished = False

# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
# return True if (x, y) is inside the grid defined by app.
def pointInGrid(app, x, y):
    return ((app.margin <= x <= app.width-app.margin) and
            (app.margin <= y <= app.height-app.margin))

# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
# return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
def getCell(app, x, y):
    row = int(y / app.cellHeight)
    col = int(x / app.cellWidth)
    return (row, col)

# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
# returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
def getCellBounds(app, row, col):
    x0 = col * app.cellWidth
    x1 = (col+1) * app.cellWidth
    y0 = row * app.cellHeight
    y1 = (row+1) * app.cellHeight
    return (x0, y0, x1, y1)

def boardGenerator(app):
    start = random.randint(0,3)
    end = random.randint(0,3)
    if start == 0: #start on left side
        startRow = random.randint(0,app.rows-1)
        startCol = 0
        endRow = random.randint(0,app.rows-1)
        endCol = 0
        (x0, y0, x1, y1) = getCellBounds(app, startRow, startCol)
        startX = 0
        startY = (y0 + y1)//2
    elif start == 1: #start on top
        startRow = 0
        startCol = random.randint(0,app.cols-1)
        endRow = 0
        endCol = random.randint(0,app.cols-1)
        (x0, y0, x1, y1) = getCellBounds(app, startRow, startCol)
        startX = (x0+x1)//2
        startY = 0
    elif start == 2: #start on right side
        startRow = random.randint(0,app.rows-1)
        startCol = app.cols-1
        endRow = random.randint(0,app.rows-1)
        endCol = app.cols-1
        (x0, y0, x1, y1) = getCellBounds(app, startRow, startCol)
        startX = app.gridWidth
        startY = (y0 + y1)//2
    elif start == 3: #start on bottom side
        startRow = app.rows-1
        startCol = random.randint(0,app.cols-1)
        endRow = app.rows-1
        endCol = random.randint(0,app.cols-1)
        (x0, y0, x1, y1) = getCellBounds(app, startRow, startCol)
        startX = (x0+x1)//2
        startY = app.height
    elif end == 0: #end on left side
        endRow = random.randint(0,app.rows-1)
        endCol = 0
    elif end == 1: #end on top
        endRow = 0
        endCol = random.randint(0,app.cols-1)
    elif end == 2: #end on right side
        endRow = random.randint(0,app.rows-1)
        endCol = app.cols-1
    elif end == 3: #end on bottom side
        endRow = app.rows-1
        endCol = random.randint(0,app.cols-1)
    board = [ [app.boardColor] * app.cols for row in range(app.rows)]
    minimumPath = 20
    startRow = 0
    startCol = 0
    endRow = 4
    endCol = 0
    return (startX, startY, randomMapGenerator(app, board, startRow, startCol, endRow, endCol, minimumPath, set()))

def randomMapGenerator(app, board, row, col, endRow, endCol, minimumPath, seenPath, count = 0):
    if row == endRow and col == endCol and count >= minimumPath:
        return board
    else:
        list = [(0,1), (0,-1), (1,0), (-1, 0)]
        #random.shuffle(list)
        for (drow, dcol) in list:
            newRow = drow + row
            newCol = dcol + col
            newRow1 = drow + newRow
            newCol1 = dcol + newCol
            newRow2 = drow + newRow1
            newCol2 = dcol + newCol1
            if count == 0:
                newRow = row
                newCol = col
                newRow1 = drow + newRow
                newCol1 = dcol + newCol
                newRow2 = drow + newRow1
                newCol2 = dcol + newCol1
            if isPathLegal(app, board, newRow, newCol, newRow1, newCol1, newRow2, newCol2, endRow, endCol, seenPath):
                board[newRow][newCol] = app.pathColor
                board[newRow1][newCol1] = app.pathColor
                board[newRow2][newCol2] = app.pathColor
                solution = randomMapGenerator(app, board, newRow2, newCol2, 
                                            endRow, endCol, minimumPath, seenPath, count + 1)
                if solution != None:
                    return board
                board[newRow][newCol] = app.boardColor
                board[newRow1][newCol1] = app.boardColor
                board[newRow2][newCol2] = app.boardColor
                seenPath.remove((newRow, newCol))
                seenPath.remove((newRow1, newCol1))
                seenPath.remove((newRow2, newCol2))
        return None


def isPathLegal(app, board, newRow, newCol, newRow1, newCol1, newRow2, newCol2, endRow, endCol, seenPath):
    if (newRow >= app.rows or newRow < 0 or newCol >= app.cols or newCol < 0 or 
        newRow1 >= app.rows or newRow1 < 0 or newCol1 >= app.cols or newCol1 < 0
        or newRow2 >= app.rows or newRow2 < 0 or newCol2 >= app.cols or newCol2 < 0):
        return False
    # elif (board[newRow][newCol] == app.pathColor or 
    #     board[newRow1][newCol1] == app.pathColor or 
    #     board[newRow2][newCol2] == app.pathColor):
    #     return False
    elif ((newRow, newCol) not in seenPath and 
            (newRow1, newCol1) not in seenPath and 
            (newRow2, newCol2) not in seenPath):
        seenPath.add((newRow, newCol))
        seenPath.add((newRow1, newCol1))
        seenPath.add((newRow2, newCol2))
        return True
    return False


# creates a hardcoded map
def hardCodedPath(app):
    board = [ [app.boardColor] * app.cols for row in range(app.rows)]
    for row in range(app.rows):
        for col in range(app.cols):
            if row == 2 and col < 18:
                board[row][col] = app.pathColor
            elif col == 17 and row > 2 and row < 13:
                board[row][col] = app.pathColor
            elif row == 13 and col < 18 and col > 12:
                board[row][col] = app.pathColor
            elif col == 12 and row < 14 and row > 5:
                board[row][col] = app.pathColor
            elif row == 6 and col < 12 and col > 6:
                board[row][col] = app.pathColor
            elif col == 7 and row < 14 and row > 5:
                board[row][col] = app.pathColor
            elif row == 13 and col < 8:
                board[row][col] = app.pathColor
    return board

# from HW 6 (Tetris)
# draws the cells of the board using the given dimensions and color
def drawCell(app, canvas, row, col, color):
    canvas.create_rectangle(col*app.cellWidth, row*app.cellHeight, 
    (col+1)*app.cellWidth,(row+1)*app.cellHeight,fill = color, outline = '')

# from HW 6 (Tetris)
# draws the board by drawing the cells using the drawCell function
def drawBoard(app, canvas):
    for row in range(app.rows):
        for col in range(app.cols):
            color = app.board[row][col]
            drawCell(app, canvas, row, col, color)

# draws the shop
def drawShop(app, canvas):
    w = app.width
    h = app.height
    m = app.shopMargin
    canvas.create_rectangle(w-m, 0, w, h, fill = 'grey')
    canvas.create_text(w - m//2, 75, text = "SHOP", font = "Arial 26 bold")
    canvas.create_text(w - m//2, 100, text = f"Currency -- {app.currency}", font = "Arial 15 bold")
    # creates cannon shop
    canvas.create_rectangle(w-m//4, h//4, w-m*3//4, h//4+100, fill = 'white')
    canvas.create_rectangle(w-m//4-20, h//4+20, w-m*3//4+20, h//4+100-20, fill = 'black')
    canvas.create_text(w - m//2, h//4+110, text = f"Cannon -- {app.cannonPrice}", font = "Arial 15 bold")
    # creates darter shop
    canvas.create_rectangle(w-m//4, h//4+150, w-m*3//4, h//4+250, fill = 'white')
    canvas.create_rectangle(w-m//4-20, h//4+150+20, w-m*3//4+20, h//4+250-20, fill = 'red')
    canvas.create_text(w - m//2, h//4+260, text = f"Darter -- {app.dartPrice}", font = "Arial 15 bold")
    # creates bomb tower shop
    canvas.create_rectangle(w-m//4, h//4+300, w-m*3//4, h//4+400, fill = 'white')
    canvas.create_rectangle(w-m//4-20, h//4+300+20, w-m*3//4+20, h//4+400-20, fill = 'grey')
    canvas.create_text(w - m//2, h//4+410, text = f"Bomb Tower -- {app.bombTowerPrice}", font = "Arial 15 bold")

# spawns enemies
def spawnEnemy(app):
    currTime = time.time()
    elapsedTime = currTime - app.initialTime
    if app.wave == 1:
        if elapsedTime >= 1:
            if app.enemySpawnCounter < 10:
                #app.enemies.append(Red(app.startX, app.startY))
                app.enemies.append(Red(0, app.cellHeight//2))
                app.initialTime = time.time()
                app.enemySpawnCounter += 1
            else:
                app.waveFinished = True
    elif app.wave == 2:
        if elapsedTime >= 1:
            if app.enemySpawnCounter < 10:
                app.enemies.append(Red(0, 75))
                app.initialTime = time.time()
                app.enemySpawnCounter += 1
            elif 9 < app.enemySpawnCounter < 15:
                app.enemies.append(Blue(0, 75))
                app.initialTime = time.time()
                app.enemySpawnCounter += 1
            else:
                app.waveFinished = True
    elif app.wave == 3:
        if elapsedTime >= 1:
            if app.enemySpawnCounter < 10:
                app.enemies.append(Red(0, 75))
                app.initialTime = time.time()
                app.enemySpawnCounter += 1
            else:
                app.waveFinished = True
    elif app.wave == 4:
        if elapsedTime >= 1:
            if app.enemySpawnCounter < 10:
                app.enemies.append(Red(0, 75))
                app.initialTime = time.time()
                app.enemySpawnCounter += 1
            elif 9 < app.enemySpawnCounter < 15:
                app.enemies.append(Blue(0, 75))
                app.initialTime = time.time()
                app.enemySpawnCounter += 1
            else:
                app.waveFinished = True
    elif app.wave == 5:
        if elapsedTime >= 1:
            if app.enemySpawnCounter < 10:
                app.enemies.append(Red(0, 75))
                app.initialTime = time.time()
                app.enemySpawnCounter += 1
            else:
                app.waveFinished = True

# moves each enemy
def moveEnemy(app):
    if len(app.enemies) >= 1:
        for enemy in app.enemies:
            enemy.moveEnemy(app)

# every turret shoots the closest enemy
def shootEnemy(app):
    for turret in app.turrets:
        closeE = closestEnemy(app, turret)
        if closeE == None:
            return
        if distance(closeE.x, closeE.y, turret.x, turret.y) <= turret.range:
            if closeE.health > 0:
                closeE.health -= turret.damage
            else:
                app.currency += closeE.worth
                app.enemies.remove(closeE)
            if isinstance(turret, Bomber):
                for enemy in app.enemies:
                    if closeE == enemy:
                        continue
                    if distance(closeE.x, closeE.y, enemy.x, enemy.y) <= turret.shotRadius:
                        if enemy.health > 0:
                            enemy.health -= turret.damage
                        else:
                            app.currency += enemy.worth
                            app.enemies.remove(enemy)
                        
                
# distance formula
def distance(x0, y0, x1, y1):
    return math.sqrt((x1-x0)**2 + (y1-y0)**2)

# finds the closest enemy to a given turret
def closestEnemy(app, turret):
    closestD = None
    if len(app.enemies) < 1:
        return None
    for enemy in app.enemies:
        d = distance(turret.x, turret.y, enemy.x, enemy.y)
        if closestD == None or d < closestD:
            closestD = d
            closeE = enemy
    return closeE

def waveChanger(app):
    if app.waveFinished == True and len(app.enemies) == 0:
        app.wave += 1
        app.enemySpawnCounter = 0
        app.waveFinished = False


def timerFired(app):
    # currTime = time.time()
    # elapsedTime = currTime - app.initialTime
    if app.health <= 0 :
        app.gameOver = True
        app.pause = False
    if app.pause == True:
        #if elapsedTime >= 5:
        spawnEnemy(app)
        moveEnemy(app)
        shootEnemy(app)
        waveChanger(app)
        #app.currency += 1

def keyPressed(app, event):
    if event.key == 'Escape':
        app.pause = not app.pause
    elif event.key == 'Space':
        spawnEnemy(app)
        

def mousePressed(app, event):
    w = app.width
    h = app.height
    m = app.shopMargin
    x = event.x
    y = event.y
    if app.selectedTurret == None:
        pass
    else:
        if x < (app.width - app.shopMargin):
            t = app.selectedTurret(x,y)
            (row, col) = getCell(app, x, y)
            (row1, col1) = getCell(app, x+t.r, y)
            (row2, col2) = getCell(app, x-t.r, y)
            (row3, col3) = getCell(app, x, y+t.r)
            (row4, col4) = getCell(app, x, y-t.r)
            if (t.x + t.r > (app.width - app.shopMargin) or 
                app.board[row][col] == app.pathColor or
                app.board[row1][col1] == app.pathColor or 
                app.board[row2][col2] == app.pathColor or 
                app.board[row3][col3] == app.pathColor or 
                app.board[row4][col4] == app.pathColor):
                return
            for turret in app.turrets:
                if distance(t.x, t.y, turret.x, turret.y) < (t.r + turret.r)+2:
                    return
            if app.currency - t.price >= 0:
                app.turrets.append(t)
                app.currency -= t.price
        app.selectedTurret = None
    whatIsClicked(app, x, y)

def whatIsClicked(app, x, y):
    w = app.width
    h = app.height
    m = app.shopMargin
    if (x >= w-m*3//4 and x <= w-m//4 and y >= h//4 and y <= h//4+100):
        app.selectedTurret = Cannon
    elif (x >= w-m*3//4 and x <= w-m//4 and y >= h//4+150 and y <= h//4+250):
        app.selectedTurret = Dart
    elif (x >= w-m*3//4 and x <= w-m//4 and y >= h//4+300 and y <= h//4+400):
        app.selectedTurret = Bomber


def mouseMoved(app, event):
    x = event.x
    y = event.y
    if app.selectedTurret != None:
        app.selectedTurretX = x
        app.selectedTurretY = y

def drawSelectedTurret(app, canvas):
    if app.selectedTurret != None:
        if app.selectedTurretX != None and app.selectedTurretY != None:
            x = app.selectedTurretX
            y = app.selectedTurretY
            t = app.selectedTurret(x,y)
            t.drawTurret(canvas)


#draws when gave is over
def drawGameOver(app, canvas):
    canvas.create_text(app.width // 2, app.height // 2, text = "GAME OVER",
                        font = '100')

#draws how much health player has left and current wave
def drawHealthAndWave(app, canvas):
    margin = 35
    canvas.create_text((app.width - app.shopMargin) // 2, margin, 
                    text = f"Health: {app.health}", font = "Arial 26 bold")
    canvas.create_text((app.width - app.shopMargin) // 2, app.height - 15, 
                        text = f"Wave {app.wave}", font = "Arial 16 bold")

def redrawAll(app, canvas):
    #canvas.create_rectangle(0,0, app.width, app.height, fill = "green")
    drawBoard(app, canvas)
    drawShop(app, canvas)
    drawSelectedTurret(app, canvas)
    drawHealthAndWave(app, canvas)
    if app.health <= 0:
        drawGameOver(app, canvas)
    if len(app.turrets) >= 1:
        for turret in app.turrets:
            turret.drawTurret(canvas)
    if len(app.enemies) >= 1:
        for enemy in app.enemies:
            enemy.drawEnemy(canvas, app)


runApp(width = 800, height = 600)

