import pygame as pg
from pygame.math import Vector2

width = 2*600
height = 600
renderWidth = 400
screen = pg.display.set_mode((width , height))
clock = pg.time.Clock() 
running  = True
bgcol = 0,0,0
lcol = 255,255,255
total = 50
pic = pg.image.load("ML/VehiclesDriving/car1.png")
dashboard = pg.image.load("ML/VehiclesDriving/Dashboard.png")
dashboard = pg.transform.rotozoom(dashboard , 0 , .3)
dashboard = dashboard.subsurface((50,40,400,245))
bg = pg.image.load("ML/VehiclesDriving/bg.png")
bg = pg.transform.scale(bg , (renderWidth , 250))
carLength , carWidth = 110 , 55
pic = pg.transform.scale(pic,(carLength , carWidth))
group = pg.sprite.Group()

numWalls = 8
walls = []
botPathWidth = 100
baseHeight = height - botPathWidth
wallGap = width / numWalls
wallWidth = 20
wallHeight = 3*baseHeight/4


savedVehicles = []
n = 1
fittestVehicleRun = False
gen = 0
checkpt1 = Vector2((numWalls-1)*wallGap + wallWidth , baseHeight-wallWidth)
checkpt2 = Vector2(3*width/4 , baseHeight)
showRays = False

allEdges = []
cars = []
render = []  