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
        if len(app.enemies) >= 1:
            canvas.create_oval(self.x-self.r, self.y-self.r, self.x+self.r, 
                           self.y+self.r, fill = self.color, width = 2)
    
    def moveEnemy(self, app):
        self.x += self.speed
        self.y += 0
        if (self.x-self.r >= app.width or self.x+self.r <= 0 or 
            self.y-self.r >= app.height or self.y+self.r <= 0):
            app.health -= self.destruct
            app.enemies.remove(self)

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
    def __init__(self):
        pass

# melee spiketrap class
class spikeTrap(Turret):
    def __init__(self):
        self.range = 10
        self.radius = 30
        self.fireRate = 10
        self.typeShot = False 
        self.damage = 100

class Cannon(Turret):
    def __init__(self):
        self.range = 50
        self.radius = 40
        self.fireRate = 30
        self.typeShot = False 
        self.damage = 50

class Bomber(Turret):
    def __init__(self):
        self.range = 30
        self.radius = 30
        self.fireRate = 5
        self.typeShot = True
        self.damage = 70

#############################################################################
# Drawing
#############################################################################

def appStarted(app):
    app.height = 600
    app.width = 800
    app.enemies = [ ] 
    #app.enemyList [ Red, Blue, Yellow, Boss ]
    app.turrets = [ ]
    app.wave = 1
    app.health = 100
    app.pause = True
    app.gameOver = False

def spawnEnemy(app):
    enemyList = [ Red, Blue, Yellow, Boss ]
    randEnemy = random.randint(0, len(enemyList) - 1)
    app.enemies.append(enemyList[randEnemy](0, 300))
    if len(app.enemies) >= 1:
        for enemy in app.enemies:
            enemy.moveEnemy(app)

def timerFired(app):
    if app.health <= 0 :
        app.gameOver = True
        app.pause = False
    if app.pause == True:
        spawnEnemy(app)


def keyPressed(app, event):
    if event.key == 'Escape':
        app.pause = not app.pause


def mousePressed(app, event):
    # using this to debug as i can spawn wherever I want

    x = event.x
    y = event.y
    enemyList = [ Red, Blue, Yellow, Boss ]
    randEnemy = random.randint(0, len(enemyList) - 1)
    app.enemies.append(enemyList[randEnemy](x, y))

    pass

def drawTurret(app, canvas):
    pass

def drawGameOver(app, canvas):
    canvas.create_text(app.width // 2, app.height // 2, text = "GAME OVER",
                        font = '100')

def drawHealth(app, canvas):
    margin = 50
    canvas.create_text(app.width // 2, margin, 
                    text = f"Health: {app.health}", font = "Arial 26 bold")


def redrawAll(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = "green")
    if app.health <= 0:
        drawGameOver(app, canvas)
    drawHealth(app, canvas)
    if len(app.enemies) >= 1:
        for enemy in app.enemies:
            enemy.drawEnemy(canvas, app)
    #drawTurret(app, canvas)


runApp(width = 600, height = 600)

        