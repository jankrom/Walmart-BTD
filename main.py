import sys
from cmu_112_graphics import *
import math

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
    def __init__(self):
        pass
    

class Bat(Enemy):
    def __init__(self):
        url = "https://i.pinimg.com/originals/05/98/df/0598dfb167a45c5ffdeef6ff6f644102.png"
        self.img = self.loadImage(url)
        self.speed = 20
        self.camo = False
        self.health = 100
        self.radius = 20
        self.destruct = 2

class Skeleton(Enemy):
    def __init__(self):
        self.speed = 10
        self.camo = False
        self.health = 200
        self.radius = 20
        self.destruct = 5

class Spider(Enemy):
    def __init__(self):
        self.speed = 40
        self.camo = True
        self.health = 150
        self.radius = 20
        self.destruct = 3

class Boss(Enemy):
    def __init__(self):
        self.speed = 50
        self.camo = False
        self.health = 1000
        self.radius = 50
        self.destruct = 20


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
    app.turrets = [ ]

def timerFired(app):
    pass

def keyPressed(app, event):
    pass

def mousePressed(app, event):
    pass

def drawEnemy(app, canvas):
    pass

def drawTurret(app, canvas):
    pass

def redrawAll(app, canvas):
    canvas.create_rectangle(0,0, app.width, app.height, fill = "black")
    drawEnemy(app, canvas)
    drawTurret(app, canvas)



runApp(width = 800, height = 600)

        