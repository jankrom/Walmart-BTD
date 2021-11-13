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
class Enemy(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def drawEnemy(self, canvas, app):
        margin = 10
        if len(app.enemies) >= 1:
            canvas.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, 
                           self.y+self.r, fill = self.color, width = 2)
            canvas.create_text(self.x, self.y - margin, text = f"{self.health}")
    
    def moveEnemy(self, app):
        self.x += self.speed
        self.y += 0
        if (self.x-self.r >= app.width or self.x+self.r <= 0 or 
            self.y-self.r >= app.height or self.y+self.r <= 0):
            app.health -= self.destruct
            app.enemies.remove(self)

# basic balloon
class Red(Enemy):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 4
        self.camo = False
        self.health = 100
        self.r = 20
        self.destruct = 2
        self.color = 'red'

# sane as red but with more HP
class Blue(Enemy):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 4
        self.camo = False
        self.health = 200
        self.r = 20
        self.destruct = 5
        self.color = 'blue'

# faster than blue and yellow, but with less HP
class Yellow(Enemy):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 7
        self.camo = True
        self.health = 150
        self.r = 20
        self.destruct = 3
        self.color = 'yellow'

# much slower but has a lot more HP
class Boss(Enemy):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2
        self.camo = False
        self.health = 1000
        self.r = 50
        self.destruct = 20
        self.color = 'brown'


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
                           self.y+self.r, fill = 'black')
                

# melee spiketrap class
class spikeTrap(Turret):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 10
        self.r = 30
        self.fireRate = 10
        self.typeShot = False 
        self.damage = 100
        self.price = 150

class Cannon(Turret):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 200
        self.r = 20
        self.fireRate = 30
        self.typeShot = False 
        self.damage = 50
        self.price = 100

class Bomber(Turret):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.range = 30
        self.r = 30
        self.fireRate = 5
        self.typeShot = True
        self.damage = 70
        self.price = 300

#############################################################################
# Drawing
#############################################################################

def appStarted(app):
    app.height = 600
    app.width = 800
    app.enemies = [ ] 
    app.turrets = [ ]
    app.wave = 1
    app.health = 100
    app.money = 100
    app.pause = True
    app.gameOver = False

def spawnEnemy(app):
    enemyList = [ Red, Blue, Yellow, Boss ]
    randEnemy = random.randint(0, len(enemyList) - 1)
    app.enemies.append(enemyList[randEnemy](0, 300))

def moveEnemy(app):
    if len(app.enemies) >= 1:
        for enemy in app.enemies:
            enemy.moveEnemy(app)

def shootEnemy(app):
    for turret in app.turrets:
        closeE = closestEnemy(app, turret)
        if closeE == None:
            return
        if distance(closeE.x, closeE.y, turret.x, turret.y) <= turret.range:
            if closeE.health > 0:
                closeE.health -= turret.damage
            else:
                app.enemies.remove(closeE)

def timerFired(app):
    if app.health <= 0 :
        app.gameOver = True
        app.pause = False
    if app.pause == True:
        #spawnEnemy(app)
        moveEnemy(app)
        shootEnemy(app)

def distance(x0, y0, x1, y1):
    return math.sqrt((x1-x0)**2 + (y1-y0)**2)

def closestEnemy(app, turret):
    closest = None
    if len(app.enemies) < 1:
        return None
    for enemy in app.enemies:
        d = distance(turret.x, turret.y, enemy.x, enemy.y)
        if closest == None or d < closest:
            closest = d
    return enemy

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

    x = event.x
    y = event.y
    t = Cannon(x,y)
    if len(app.turrets) >= 2:
        for turret in app.turrets:
            if distance(t.x, t.y, turret.x, turret.y) < (t.r + turret.r):
                return
    app.turrets.append(Cannon(x,y))


#draws when gave is over
def drawGameOver(app, canvas):
    canvas.create_text(app.width // 2, app.height // 2, text = "GAME OVER",
                        font = '100')

#draws how much health player has left
def drawHealth(app, canvas):
    margin = 50
    canvas.create_text(app.width // 2, margin, 
                    text = f"Health: {app.health}", font = "Arial 26 bold")


def redrawAll(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = "green")
    if app.health <= 0:
        drawGameOver(app, canvas)
    drawHealth(app, canvas)
    if len(app.turrets) >= 1:
        for turret in app.turrets:
            turret.drawTurret(canvas, app)
    if len(app.enemies) >= 1:
        for enemy in app.enemies:
            enemy.drawEnemy(canvas, app)
    #drawTurret(app, canvas)


runApp(width = 600, height = 600)

        