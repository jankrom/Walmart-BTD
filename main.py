import sys
from cmu_112_graphics import *
import math
import random

'''
Content:
    Towers
    Minions
    Map
'''

'''
Ideas:
    Dungeon Themed
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

    def drawTurret(self, canvas, app):
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
        self.r = 50
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
    app.boardColor = 'green'
    app.pathColor = 'goldenrod3'
    #app.board = [ [app.boardColor] * app.cols for row in range(app.rows)]
    app.board = hardCodedPath(app)
    app.enemies = [ ] 
    app.turrets = [ ]
    app.wave = 1
    app.health = 100
    app.currency = 100
    app.pause = True
    app.gameOver = False
    app.cannonPrice = 100
    app.dartPrice = 150
    app.bombTowerPrice = 50
    app.selectedTurret = 0

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
    enemyList = [ Red, Blue, Yellow, Boss ]
    randEnemy = random.randint(0, len(enemyList) - 1)
    app.enemies.append(enemyList[randEnemy](0, 75))

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

def timerFired(app):
    if app.health <= 0 :
        app.gameOver = True
        app.pause = False
    if app.pause == True:
        #spawnEnemy(app)
        moveEnemy(app)
        shootEnemy(app)
        #app.currency += 1

def keyPressed(app, event):
    if event.key == 'Escape':
        app.pause = not app.pause
    elif event.key == 'Space':
        spawnEnemy(app)
        
    # elif event.key == '1':
    #     spikeTrap.spawnTurret()
    # elif event.key == '2':
    #     Cannon.spawnTurret()
    # elif event.key == '3':
    #     Bomber.spawnTurret()

def mousePressed(app, event):
    # using this to debug as i can spawn wherever I want

    # x = event.x
    # y = event.y
    # enemyList = [ Red, Blue, Yellow, Boss ]
    # randEnemy = random.randint(0, len(enemyList) - 1)
    # app.enemies.append(enemyList[randEnemy](x, y))

    # x = event.x
    # y = event.y
    # t = Dart(x,y)
    # if len(app.turrets) >= 2:
    #     for turret in app.turrets:
    #         if distance(t.x, t.y, turret.x, turret.y) < (t.r + turret.r):
    #             return
    # app.turrets.append(Dart(x,y))

    w = app.width
    h = app.height
    m = app.shopMargin
    x = event.x
    y = event.y
    if (x >= w-m*3//4 and x <= w-m//4 and y >= h//4 and y <= h//4+100):
        app.selectedTurret = Cannon
    if (x >= w-m*3//4 and x <= w-m//4 and y >= h//4+150 and y <= h//4+250):
        app.selectedTurret = Dart
    if (x >= w-m*3//4 and x <= w-m//4 and y >= h//4+300 and y <= h//4+400):
        app.selectedTurret = Bomber

def mouseMoved(app, event):
    x = event.x
    y = event.y

def mouseReleased(app, event):
    x = event.x
    y = event.y
    t = app.selectedTurret(x,y)
    if len(app.turrets) >= 2:
        for turret in app.turrets:
            if distance(t.x, t.y, turret.x, turret.y) < (t.r + turret.r):
                return
    if app.currency - t.price >= 0:
        app.turrets.append(t)
        app.currency -= t.price


#draws when gave is over
def drawGameOver(app, canvas):
    canvas.create_text(app.width // 2, app.height // 2, text = "GAME OVER",
                        font = '100')

#draws how much health player has left
def drawHealth(app, canvas):
    margin = 35
    canvas.create_text((app.width - app.shopMargin) // 2, margin, 
                    text = f"Health: {app.health}", font = "Arial 26 bold")


def redrawAll(app, canvas):
    #canvas.create_rectangle(0,0, app.width, app.height, fill = "green")
    if app.health <= 0:
        drawGameOver(app, canvas)
    drawBoard(app, canvas)
    drawShop(app, canvas)
    drawHealth(app, canvas)
    if len(app.turrets) >= 1:
        for turret in app.turrets:
            turret.drawTurret(canvas, app)
    if len(app.enemies) >= 1:
        for enemy in app.enemies:
            enemy.drawEnemy(canvas, app)


runApp(width = 800, height = 600)

        