from cmu_112_graphics import *
import math
import random
import time

#############################################################################
# Splash Screen 
#############################################################################   

def splashScreenMode_redrawAll(app, canvas):
    canvas.create_image(0, 0, image=ImageTk.PhotoImage(app.scaleImage(app.image1, 2.5)), anchor = 'nw')
    canvas.create_text(150, app.height // 2, text = 'Press P to play', font = 'Arial 26 bold')
    canvas.create_text(150, (app.height // 2) + 50, text = 'Press H for help', font = 'Arial 26 bold')
    canvas.create_text(50, 50, text = 'Walmart', font = 'Arial 23 bold')

def splashScreenMode_keyPressed(app, event):
    if event.key == 'p':
        app.mode = "gameMode" 
    elif event.key == 'h':
        app.mode = 'helpMode'

#############################################################################
# Help Screen 
############################################################################# 

def helpMode_redrawAll(app, canvas):
    canvas.create_image(0, 0, image=ImageTk.PhotoImage(app.scaleImage(app.image1, 2.5)), anchor = 'nw')
    canvas.create_text(app.width // 2, 200, text = 'HELP', font = 'Arial 80 bold')
    canvas.create_text(50, 50, text = 'Walmart', font = 'Arial 23 bold')
    canvas.create_text(150, app.height // 2, text = '''
        Tower defense game. 
        Buy turrets from the shop, 
        place them down, 
        and destroy all the balloons. 
        Don't destroy all the baloons
        and you lose. 
        That's no fun so don't lose''', font = 'Arial 12 bold')
    canvas.create_text(170, (app.height // 2) + 100, text = 'Press P to play', font = 'Arial 26 bold')

def helpMode_keyPressed(app, event):
    if event.key == 'p':
        app.mode = "gameMode"

#############################################################################
# Pause Screen 
############################################################################# 

def pauseMode_redrawAll(app, canvas):
    canvas.create_image(0, 0, image=ImageTk.PhotoImage(app.scaleImage(app.image1, 2.5)), anchor = 'nw')
    canvas.create_oval(100, 150, 200, 250, fill = 'turquoise')
    canvas.create_text(150, 200, text = 'Continue')
    canvas.create_oval(100, 350, 200, 450, fill = 'turquoise')
    canvas.create_text(150, 400, text = 'Main Menu')

def pauseMode_mousePressed(app, event):
    x = event.x
    y = event.y
    if (x >= 100 and x <= 200 and y >= 150 and y <= 250):
        app.pause = not app.pause
        app.mode = "gameMode"
    elif (x >= 100 and x <= 200 and y >= 350 and y <= 450):
        app.pause = not app.pause
        app.mode = "splashScreenMode"

#############################################################################
# Enemies
#############################################################################
# enemies class
# each enemy should have:
    # speed
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
        if (self.x-self.r >= app.gridWidth or self.x+self.r <= 0 or 
            self.y-self.r >= app.height or self.y+self.r <= 0):
            app.health -= self.destruct
            app.enemies.remove(self)
        else:
            (row, col) = getCell(app, self.x, self.y)
            if row == app.rows:
                row = app.rows-1
            if col == app.cols:
                col = app.cols-1
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
    if (col+1 < app.cols and (row, col+1) not in self.seenPath and 
            app.board[row][col+1] == app.pathColor):
        self.speedx = abs(self.speedx)
        return True
    elif (col-1 >= 0 and (row, col-1) not in self.seenPath and
             app.board[row][col-1] == app.pathColor):
        self.speedx = -abs(self.speedx)
        return True
    return False

# checks if a y direction move is legal
def moveEnemyLegalY(self, app, row, col):
    if row+1 < app.rows and (row+1, col) not in self.seenPath and app.board[row+1][col] == app.pathColor:
        self.speedy = abs(self.speedy)
        return True
    elif row-1 >= 0 and (row-1, col) not in self.seenPath and app.board[row-1][col] == app.pathColor:
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
        self.health = 200
        self.r = 20
        self.destruct = 2
        self.color = 'red'
        self.seenPath = set()
        self.count = 0
        self.worth = 5
        self.slowed = False

# sane as red but with more HP
class Blue(Enemy):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speedx = 4
        self.speedy = 4
        self.lastMovement = 0
        self.health = 400
        self.r = 20
        self.destruct = 5
        self.color = 'blue'
        self.seenPath = set()
        self.count = 0
        self.worth = 8
        self.slowed = False

# faster than blue and yellow, but with less HP
class Yellow(Enemy):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speedx = 10
        self.speedy = 10
        self.lastMovement = 0
        self.health = 300
        self.r = 20
        self.destruct = 3
        self.color = 'yellow'
        self.seenPath = set()
        self.count = 0
        self.worth = 10
        self.slowed = False

# much slower but has a lot more HP
class Boss(Enemy):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speedx = 2
        self.speedy = 2
        self.lastMovement = 0
        self.health = 2500
        self.r = 50
        self.destruct = 20
        self.color = 'brown'
        self.seenPath = set()
        self.count = 0
        self.worth = 200
        self.slowed = False

#############################################################################
# Turrets
#############################################################################
# turrets class
# each turret should have:
    # range
    # radius/size
    # fire rate
    # type of shots (single enemy, multi enemy, splash)
    # dmg / shot
class Turret(object):
    def __init__(self, x , y):
        self.x = x
        self.y = y

# every turret shoots the closest enemy
    def shootEnemy(self, app):
        currTime = time.time()
        self.elapsedTime = currTime - self.initialTime
        if isinstance(self, Cannon):
            if self.elapsedTime >= 0.5:
                self.closeE = closestEnemy(app, self)
                self.initialTime = currTime
                if self.closeE == None:
                    return
                if distance(self.closeE.x, self.closeE.y, self.x, self.y) <= self.range:
                    if self.closeE.health > 0:
                        app.shots.append(Shot(self.x, self.y, self.closeE.x, self.closeE.y, self))
                        self.closeE.health -= self.damage
        elif isinstance(self, Dart):
            if self.elapsedTime >= 0.1:
                self.closeE = closestEnemy(app, self)
                self.initialTime = currTime
                if self.closeE == None:
                    return
                if distance(self.closeE.x, self.closeE.y, self.x, self.y) <= self.range:
                    if self.closeE.health > 0:
                        if self.closeE.slowed == False:
                                self.closeE.slowed = True
                                self.closeE.speedx = self.closeE.speedx//2
                                self.closeE.speedy = self.closeE.speedy//2
                                self.closeE.color = 'cyan'
                        app.shots.append(Shot(self.x, self.y, self.closeE.x, self.closeE.y, self))
                        self.closeE.health -= self.damage
                    for enemy in app.enemies:
                        if self.closeE == enemy:
                            continue
                        if distance(self.closeE.x, self.closeE.y, enemy.x, enemy.y) <= self.shotRadius:
                            if enemy.slowed == False:
                                enemy.slowed = True
                                enemy.speedx = enemy.speedx//2
                                enemy.speedy = enemy.speedy//2
                                enemy.color = 'cyan'
        elif isinstance(self, Bomber):
            if self.elapsedTime >= 2:
                self.closeE = closestEnemy(app, self)
                self.initialTime = currTime
                if self.closeE == None:
                    return
                if distance(self.closeE.x, self.closeE.y, self.x, self.y) <= self.range:
                    if self.closeE.health > 0:
                        self.closeE.health -= self.damage
                        app.shots.append(Shot(self.x, self.y, self.closeE.x, self.closeE.y, self))
                    for enemy in app.enemies:
                        if self.closeE == enemy:
                            continue
                        if distance(self.closeE.x, self.closeE.y, enemy.x, enemy.y) <= self.shotRadius:
                            if enemy.health > 0:
                                enemy.health -= self.damage

    def drawRadius(self, canvas):
        canvas.create_oval(self.x-self.range, self.y-self.range, self.x+self.range, 
                           self.y+self.range, fill = '')

# slower attack speed but more dmg
class Cannon(Turret):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 100
        self.r = 20
        self.attackSpeed = 30
        self.damage = 100
        self.price = 100
        self.color = 'black'
        self.initialTime = time.time()
        self.elapsedTime = 0
        self.shooting = False
        self.closeE = None
        self.shotx = x
        self.shoty = y

#draws the cannons
    def drawTurret(self, canvas):
        canvas.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, 
                           self.y+self.r, fill = self.color)
        canvas.create_rectangle(self.x-2*self.r, self.y-self.r//2, self.x, 
                           self.y+self.r//2, fill = self.color)

# faster attack speed but less damage
class Dart(Turret):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 200
        self.r = 20
        self.attackSpeed = 30
        self.shotRadius = 100
        self.damage = 2
        self.price = 300
        self.color = 'red'
        self.initialTime = time.time()
        self.elapsedTime = 0
        self.shooting = False
        self.closeE = None
        self.shotx = x
        self.shoty = y

#draws the darter turrets
    def drawTurret(self, canvas):
        canvas.create_rectangle(self.x-self.r, self.y-self.r, self.x+self.r, 
                           self.y+self.r, fill = self.color)
        canvas.create_polygon(self.x, self.y-self.r, self.x, 
                           self.y+self.r, self.x - 2*self.r, self.y, fill = self.color)

# does low damage but has splash damage
class Bomber(Turret):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 100
        self.r = 30
        self.attackSpeed = 5
        self.shotRadius = 100
        self.damage = 50
        self.price = 250
        self.color = 'grey'
        self.initialTime = time.time()
        self.elapsedTime = 0
        self.shooting = False
        self.closeE = None
        self.shotx = x
        self.shoty = y

# draws the bombers  
    def drawTurret(self, canvas):
        canvas.create_rectangle(self.x-self.r, self.y-self.r, self.x+self.r, 
                           self.y+self.r, fill = self.color)
        canvas.create_oval(self.x-self.r//2, self.y-self.r//2, self.x+self.r//2, 
                           self.y+self.r//2, fill = 'black')

#############################################################################
# Shots
#############################################################################   
#shots from turrets
class Shot(object):
    def __init__(self, turretX, turretY, enemyX, enemyY, turret):
        self.tX = turretX
        self.tY = turretY
        self.eX = enemyX
        self.eY = enemyY
        self.tType = turret
        self.shotx = turretX
        self.shoty = turretY
        self.dx = self.tX - self.eX
        self.dy = self.tY - self.eY
        self.cannonR = turret.r
        self.dartR = turret.r
        self.bomberR = turret.r

#draws the shots
    def drawShot(self, canvas, app):
        if isinstance(self.tType, Cannon):
            canvas.create_oval(self.shotx-2*self.cannonR, self.shoty-self.cannonR//2, self.shotx-self.cannonR, 
                           self.shoty+self.cannonR//2, fill = 'red')
            self.shotx -= self.dx//2
            self.shoty -= self.dy//2
        elif isinstance(self.tType, Dart):
            canvas.create_polygon(self.shotx - self.dartR, self.shoty-self.dartR//2, self.shotx - self.dartR, 
                           self.shoty+self.dartR//2, self.shotx - 2*self.dartR, self.shoty, fill = 'black')
            self.shotx -= self.dx//4
            self.shoty -= self.dy//4
        elif isinstance(self.tType, Bomber):
            canvas.create_oval(self.shotx-self.bomberR//2, self.shoty-self.bomberR//2, self.shotx+self.bomberR//2, 
                           self.shoty+self.bomberR//2, fill = 'black', outline = 'red')
            self.shotx -= self.dx//6
            self.shoty -= self.dy//6


#############################################################################
# Drawing
#############################################################################


def appStarted(app):
    app.mode = 'splashScreenMode'
    url = 'https://upload.wikimedia.org/wikipedia/en/e/e6/Bloons_TD_iOS_Logo.jpg'
    app.image1 = app.loadImage(url)
    app.rows = app.height // 30
    app.cols = app.width // 40
    app.cellWidth = (app.width-200) // app.cols
    app.cellHeight = app.cellWidth
    app.shopMargin = app.width // 4
    app.gridWidth = app.width - app.shopMargin
    app.boardColor = 'green'
    app.pathColor = 'goldenrod3'
    (app.startX, app.startY, app.board) = boardGenerator(app)
    app.cellCount = 0
    app.enemies = [ ] 
    app.turrets = [ ]
    app.wave = 1
    app.health = 100
    app.currency = 100
    app.pause = True
    app.gameOver = False
    app.cannonPrice = 100
    app.dartPrice = 300
    app.bombTowerPrice = 250
    app.selectedTurret = None
    app.selectedTurretX = None
    app.selectedTurretY = None
    app.enemySpawnCounter = 0
    app.enemyCounter = 0
    app.red = 0
    app.blue = 0
    app.yellow = 0
    app.boss = 0
    app.enemyRedCounter = 0
    app.enemyBlueCounter = 0
    app.enemyYellowCounter = 0
    app.enemyBossCounter = 0
    app.initialTimeCurrency = time.time()
    app.initialTimeWave = time.time()
    app.waveFinished = False
    app.shots = [ ]

# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
# return True if (x, y) is inside the grid defined by app.
def pointInGrid(app, x, y):
    return ((app.margin <= x <= app.width-app.margin) and
            (app.margin <= y <= app.height-app.margin))

# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
# return (row, col) in which (x, y) occurred or (-1, -1) if outside grid
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

#randomly generates a starting location and then a map from it
def boardGenerator(app):
    start = random.randint(0,3)
    if start == 0: #start on left side
        startRow = random.randint(0,app.rows-1)
        startCol = 0
        (x0, y0, x1, y1) = getCellBounds(app, startRow, startCol)
        startX = 0
        startY = (y0 + y1)//2
    elif start == 1: #start on top
        startRow = 0
        startCol = random.randint(0,app.cols-1)
        (x0, y0, x1, y1) = getCellBounds(app, startRow, startCol)
        startX = (x0+x1)//2
        startY = 0
    elif start == 2: #start on right side
        startRow = random.randint(0,app.rows-1)
        startCol = app.cols-1
        (x0, y0, x1, y1) = getCellBounds(app, startRow, startCol)
        startX = app.gridWidth
        startY = (y0 + y1)//2
    elif start == 3: #start on bottom side
        startRow = app.rows-1
        startCol = random.randint(0,app.cols-1)
        (x0, y0, x1, y1) = getCellBounds(app, startRow, startCol)
        startX = (x0+x1)//2
        startY = app.height
    board = [ [app.boardColor] * app.cols for row in range(app.rows)]
    minimumPath = 20
    return (startX, startY, randomMapGenerator(app, board, startRow, startCol, minimumPath, set()))

# randomly generates a map
def randomMapGenerator(app, board, row, col, minimumPath, seenPath, count = 0):
    if (row == 0 or row == app.rows - 1 or col == 0 or col == app.cols - 1) and count >= minimumPath:
        return board
    else:
        list = [(0,1), (0,-1), (1,0), (-1, 0)]
        random.shuffle(list)
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
            if isPathLegal(app, newRow, newCol, newRow1, newCol1, newRow2, newCol2, seenPath):
                board[newRow][newCol] = app.pathColor
                board[newRow1][newCol1] = app.pathColor
                board[newRow2][newCol2] = app.pathColor
                solution = randomMapGenerator(app, board, newRow2, newCol2, 
                                            minimumPath, seenPath, count + 1)
                if solution != None:
                    return board
                board[newRow][newCol] = app.boardColor
                board[newRow1][newCol1] = app.boardColor
                board[newRow2][newCol2] = app.boardColor
                seenPath.remove((newRow, newCol))
                seenPath.remove((newRow1, newCol1))
                seenPath.remove((newRow2, newCol2))
        return None

# checks to see if a path is legal when making a board
def isPathLegal(app, newRow, newCol, newRow1, newCol1, newRow2, newCol2, seenPath):
    if (newRow >= app.rows or newRow < 0 or newCol >= app.cols or newCol < 0 or 
        newRow1 >= app.rows or newRow1 < 0 or newCol1 >= app.cols or newCol1 < 0
        or newRow2 >= app.rows or newRow2 < 0 or newCol2 >= app.cols or newCol2 < 0):
        return False
    elif ((newRow, newCol) not in seenPath and 
            (newRow1, newCol1) not in seenPath and 
            (newRow2, newCol2) not in seenPath):
        seenPath.add((newRow, newCol))
        seenPath.add((newRow1, newCol1))
        seenPath.add((newRow2, newCol2))
        return True
    return False

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
    canvas.create_oval(w-m//4-10, h//4+20, w-m*3//4+30, h//4+100-20, fill = 'black')
    canvas.create_rectangle(w-m//4-40, h//4+35,w-m*3//4+10, h//4+55, fill = 'black')
    canvas.create_text(w - m//2, h//4+110, text = f"Cannon -- {app.cannonPrice}", font = "Arial 15 bold")
    # creates darter shop
    canvas.create_rectangle(w-m//4, h//4+150, w-m*3//4, h//4+250, fill = 'white')
    canvas.create_rectangle(w-m//4-20, h//4+150+20, w-m*3//4+20, h//4+250-20, fill = 'red')
    canvas.create_polygon(w-m//4-100, h//4+200,w-m*3//4+50, h//4+180, w-m*3//4+50, h//4+220, fill = 'red')
    canvas.create_text(w - m//2, h//4+260, text = f"Darter -- {app.dartPrice}", font = "Arial 15 bold")
    # creates bomb tower shop
    canvas.create_rectangle(w-m//4, h//4+300, w-m*3//4, h//4+400, fill = 'white')
    canvas.create_rectangle(w-m//4-20, h//4+300+20, w-m*3//4+20, h//4+400-20, fill = 'grey')
    canvas.create_oval(w-m//4-35, h//4+300+35, w-m*3//4+35, h//4+400-35, fill = 'black')
    canvas.create_text(w - m//2, h//4+410, text = f"Bomb Tower -- {app.bombTowerPrice}", font = "Arial 15 bold")

# spawns enemies
def spawnEnemy(app):
    currTime = time.time()
    elapsedTime = currTime - app.initialTimeWave
    if app.wave == 1:
        if elapsedTime >= 1:
            if app.enemySpawnCounter < 10:
                app.enemies.append(Red(app.startX, app.startY))
                app.initialTimeWave = time.time()
                app.enemySpawnCounter += 1
                app.enemyCounter += 1
            else:
                app.waveFinished = True
    elif app.wave == 2:
        if elapsedTime >= 1:
            if app.enemySpawnCounter < 10:
                app.enemies.append(Red(app.startX, app.startY))
                app.initialTimeWave = time.time()
                app.enemySpawnCounter += 1
                app.enemyCounter += 1
            elif 9 < app.enemySpawnCounter < 15:
                app.enemies.append(Blue(app.startX, app.startY))
                app.initialTimeWave = time.time()
                app.enemySpawnCounter += 1
                app.enemyCounter += 1
            else:
                app.waveFinished = True
    elif app.wave == 3:
        if elapsedTime >= 1:
            if app.enemySpawnCounter < 15:
                app.enemies.append(Red(app.startX, app.startY))
                app.initialTimeWave = time.time()
                app.enemySpawnCounter += 1
                app.enemyCounter += 1
            elif 14 < app.enemySpawnCounter < 30:
                app.enemies.append(Blue(app.startX, app.startY))
                app.initialTimeWave = time.time()
                app.enemySpawnCounter += 1
                app.enemyCounter += 1
            else:
                app.waveFinished = True
    elif app.wave == 4:
        if elapsedTime >= 1:
            if app.enemySpawnCounter < 30:
                app.enemies.append(Blue(app.startX, app.startY))
                app.initialTimeWave = time.time()
                app.enemySpawnCounter += 1
                app.enemyCounter += 1
            else:
                app.waveFinished = True
    elif app.wave == 5:
        if elapsedTime >= 1:
            if app.enemySpawnCounter < 10:
                app.enemies.append(Red(app.startX, app.startY))
                app.initialTimeWave = time.time()
                app.enemySpawnCounter += 1
                app.enemyCounter += 1
            if app.enemySpawnCounter < 30:
                app.enemies.append(Blue(app.startX, app.startY))
                app.initialTimeWave = time.time()
                app.enemySpawnCounter += 1
                app.enemyCounter += 1
            if app.enemySpawnCounter == 20:
                app.enemies.append(Boss(app.startX, app.startY))
                app.initialTimeWave = time.time()
                app.enemySpawnCounter += 1
                app.enemyCounter += 1
            else:
                app.waveFinished = True
    elif app.wave >= 6:
        if elapsedTime >= 1:
            if app.enemyYellowCounter <= app.yellow:
                app.enemies.append(Yellow(app.startX, app.startY))
                app.enemyYellowCounter += 1
                app.enemyCounter += 1
            if app.enemyRedCounter <= app.red:
                app.enemies.append(Red(app.startX, app.startY))
                app.enemyRedCounter += 1
                app.enemyCounter += 1
            if app.enemyBlueCounter <= app.blue:
                app.enemies.append(Blue(app.startX, app.startY))
                app.enemyBlueCounter += 1
                app.enemyCounter += 1
            if app.enemyBossCounter <= app.boss:
                app.enemies.append(Boss(app.startX, app.startY))
                app.enemyBossCounter += 1
                app.enemyCounter += 1
            else:
                app.waveFinished = True


# moves each enemy
def moveEnemy(app):
    if len(app.enemies) >= 1:
        for enemy in app.enemies:
            enemy.moveEnemy(app)
                
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

# changes the wave
def waveChanger(app):
    if app.waveFinished == True and len(app.enemies) == 0:
        app.wave += 1
        if app.wave % 2 == 0:
            app.red += 5
            app.blue += 10
            app.yellow += 15
        if app.wave % 3 == 0:
            app.boss += 1
        if app.wave >= 20:
            app.boss += 5
            app.yellow += 30
        if app.currency >= 1000:
            app.boss += 5
        if len(app.turrets) >= 5:
            app.yellow += 15
            app.blue += 5
            app.boss += 1
            if len(app.turrets) % 2 == 0:
                app.red += random.randint(1,15)
                app.blue += random.randint(1,10)
                app.yellow += random.randint(1,8)
                app.boss += random.randint(1,3)
        app.enemySpawnCounter = 0
        app.enemyRedCounter = 0
        app.enemyBlueCounter = 0
        app.enemyYellowCounter = 0
        app.enemyBossCounter = 0
        app.waveFinished = False

# checks how much health the player is at
def checkHealth(app):
    for enemy in app.enemies:
        if enemy.health <= 0:
            app.enemies.remove(enemy)
            app.currency += enemy.worth

# checks to see if a shot is still on the screen
def checkShot(app):
    for shot in app.shots:
        if (shot.shotx >= app.gridWidth or shot.shotx <= 0 or 
                shot.shoty >= app.height or shot.shoty <= 0):
            app.shots.remove(shot)

# timer fired while playing
def gameMode_timerFired(app):
    currTime = time.time()
    elapsedTime = currTime - app.initialTimeCurrency
    if app.health <= 0 :
        app.gameOver = True
        app.pause = False
    if app.pause == True:
        spawnEnemy(app)
        moveEnemy(app)
        checkHealth(app)
        checkShot(app)
        for turret in app.turrets:
            turret.shootEnemy(app)
        waveChanger(app)
        if elapsedTime >= 5:
            app.currency += 1
            app.initialTimeCurrency = currTime

def gameMode_keyPressed(app, event):
    if event.key == 'Escape':
        app.pause = not app.pause
        app.mode = 'pauseMode'

def gameMode_mousePressed(app, event):
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
                row3 >= app.rows or
                row4 <= 0 or 
                col2 <= 0 or
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

# checks to see what is clicked in the shop
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

def gameMode_mouseMoved(app, event):
    x = event.x
    y = event.y
    if app.selectedTurret != None:
        app.selectedTurretX = x
        app.selectedTurretY = y

# draws the selected turret
def drawSelectedTurret(app, canvas):
    if app.selectedTurret != None:
        if app.selectedTurretX != None and app.selectedTurretY != None:
            x = app.selectedTurretX
            y = app.selectedTurretY
            t = app.selectedTurret(x,y)
            t.drawTurret(canvas)
            t.drawRadius(canvas)


#draws when gave is over
def drawGameOver(app, canvas):
    canvas.create_text(app.width // 2, app.height // 2, text = "GAME OVER",
                        font = 'Arial 80 bold')

#draws how much health player has left and current wave
def drawHealthAndWave(app, canvas):
    margin = 35
    canvas.create_text((app.width - app.shopMargin) // 2, margin, 
                    text = f"Health: {app.health}", font = "Arial 26 bold")
    canvas.create_text((app.width - app.shopMargin) // 2, app.height - 15, 
                        text = f"Wave {app.wave}", font = "Arial 16 bold")

def gameMode_redrawAll(app, canvas):
    drawBoard(app, canvas)
    for turret in app.turrets:
        turret.drawTurret(canvas)
    for enemy in app.enemies:
        enemy.drawEnemy(canvas, app)
    for shot in app.shots:
        shot.drawShot(canvas, app)
    drawShop(app, canvas)
    drawSelectedTurret(app, canvas)
    drawHealthAndWave(app, canvas)
    if app.health <= 0:
        drawGameOver(app, canvas)


runApp(width = 800, height = 600)

