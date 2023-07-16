import pygame as pg 
import pygame.gfxdraw
import random 
import numpy as np
from nn import NeuralNetwork
from pygame.math import Vector2
import pickle

pg.init()
width = 2*600
height = 600

screen = pg.display.set_mode((width, height))
pg.display.set_caption('Self driving vehicles')
clock = pg.time.Clock() 
running  = True
bgcol = 0,0,0
lcol = 255,255,255
total = 10


class Edge():
    def __init__(self,a,b) : 
        self.a = a
        self.b = b
class Wall():
    def __init__(self,x,y,w,h) : 
        self.a = Vector2(x,y)
        self.b = Vector2(x + w , y)
        self.c = Vector2(x + w , y + h)
        self.d = Vector2(x , y + h)
        self.w = w
        self.h = h
    def show(self) : 
        col = 100
        # pg.draw.line(screen , (lcol) , (self.a.x,self.a.y),(self.b.x,self.b.y),2)
        pg.draw.rect(screen , (col,col,col) , (self.a.x,self.a.y,self.w,self.h))
    def edges(self) : 
        edges = []
        edges.append(Edge(self.a,self.b))
        edges.append(Edge(self.b,self.c))
        edges.append(Edge(self.c,self.d))
        edges.append(Edge(self.d,self.a))
        return edges
    def reset(self): 
        self.a.x = random.randint(0,width)
        self.a.y = random.randint(0,height)
        self.b.x = random.randint(0,width)
        self.b.y = random.randint(0,height)
        
class Ray():
    def __init__(self,pos,deg) : 
        self.pos = pos
        self.dir = Vector2(1,0)
        self.dir.rotate_ip(deg)
    def show(self):
        pygame.gfxdraw.line(screen,int(self.pos.x),int(self.pos.y),int(self.pos.x+self.dir.x*10),int(self.pos.y+self.dir.y*10),(255,255,255,255))
    def cast(self,wall) : 
        x1 = wall.a.x
        y1 = wall.a.y
        x2 = wall.b.x 
        y2 = wall.b.y
        
        x3 = self.pos.x
        y3 = self.pos.y
        x4 = self.pos.x + self.dir.x
        y4 = self.pos.y + self.dir.y

        den = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
        if den == 0 : return 
        t = ((x1-x3)*(y3-y4) - (y1-y3)*(x3-x4)) / den
        u = -1*((x1-x2)*(y1-y3) - (y1-y2)*(x1-x3)) / den
        if t > 0 and t < 1 and u > 0 : 
            pt = Vector2()
            pt.x = x1 + t * (x2-x1)
            pt.y = y1 + t * (y2-y1)
            return pt
        else : return 

class Vehicle(): 
    def __init__(self , brain = None) : 
        self.pos = Vector2(3*wallGap/2 , 50)
        self.vel = Vector2(0,5)
        self.turnAngle = 5
        self.rays = []
        for i in range(0,182,45) : 
            ray = Ray(self.pos , i)
            self.rays.append(ray)
        self.isDead = False
        self.score = 0
        self.fitness = 0
        self.round = 1
        self.showRays = False
        self.passedCheckpoint = False 
        if brain : self.brain = brain.copy()
        else : self.brain = NeuralNetwork(5,8,4)
    def lookWalls(self,edges): 
        rayDist = []
        for ray in self.rays : 
            record = float('inf')   
            closest = None
            for edge in edges : 
                pt = ray.cast(edge)
                if pt : 
                    dist = self.pos.distance_to(pt)
                    if dist < record : 
                        record = dist
                        closest = pt
            if closest : 
                if self.showRays : self.showRay(ray.pos.x,ray.pos.y,closest.x,closest.y)
                rayDist.append(record)
            else: rayDist.append(2)
        if rayDist[2] < 25 or rayDist[0] < 5 or rayDist[4] < 5 : self.isDead = True
        return rayDist
    def showRay(self,x1,y1,x2,y2) :
        pygame.gfxdraw.line(screen,int(x1),int(y1),int(x2),int(y2),(255,255,255,85))
        pg.draw.circle(screen,(180,10,10),(int(x2),int(y2)),3)
    def turnRight(self) : 
        if not self.isDead : 
            self.vel.rotate_ip(-self.turnAngle)
            self.rotateRays(-self.turnAngle)
    def turnLeft(self):
        if not self.isDead : 
            self.vel.rotate_ip(self.turnAngle)
            self.rotateRays(self.turnAngle)
    def forward(self) : 
        if not self.isDead : 
            self.pos += self.vel
    def think(self,edges) : 
        inputs = self.lookWalls(edges)
        for i in range(len(inputs)) : inputs[i] = inputs[i] / height
        output = self.brain.predict(inputs)
        if output[0] > output[1] : self.turnRight()
        if output[1] > output[2] : self.turnLeft()
        # if output[3] > .5 : self.forward()
    def printDead(self) : 
        print(self.isDead)
    def checkPass(self, checkpt1, checkpt2) : 
        if self.pos.x > checkpt1.x :
            if self.pos.y > checkpt1.y : self.passedCheckpoint = True 
        if self.passedCheckpoint : 
            if self.pos.x < checkpt2.x : 
                # print("passed " ,self.round )
                self.passedCheckpoint = False 
                self.round += 1

    def run(self) : 
        if not self.isDead : self.pos += self.vel
        self.score = points(self.pos.x , self.pos.y,self.round)
        # self.score += 2
    def mutate(self) : 
        self.brain.mutate(.1)
    def update(self) : 
        if not self.isDead : 
            keys = pg.key.get_pressed()
            # for key in keys : 
            #     if key==1 : print(keys.index(key))
            rKey = 275
            lKey = 276
            dKey = 274 
            uKey = 273
            delta = 3
            theta = 0 
            if keys[lKey] : 
                theta -= delta
                self.vel.rotate_ip(-delta)
            if keys[rKey] : 
                theta += delta
                self.vel.rotate_ip(delta)
            # if keys[uKey] | keys[119]: 
            self.pos += self.vel
            if keys[dKey] | keys[115] : 
                self.pos -= self.vel
            if keys[100] : 
                strafLeft = Vector2(-self.vel.y , self.vel.x)
                self.pos += strafLeft
            if keys[97] : 
                strafRight = Vector2(self.vel.y , -self.vel.x)
                self.pos += strafRight
            self.rotateRays(theta)
            self.boundary()
    def rotateRays(self,theta) :         
        for ray in self.rays : 
            ray.pos = self.pos
            ray.dir.rotate_ip(theta)
    def boundary(self) : 
        margin = 3
        if self.pos.x > width - margin : self.pos.x = width-margin 
        if self.pos.x < margin : self.pos.x = margin 
        if self.pos.y > height-margin : self.pos.y = height-margin
        if self.pos.y < margin : self.pos.y = margin 
    def show(self) : 
        theta = Vector2(1,0).angle_to(self.vel)
        # theta = self.vel.angle_to(Vector2(2,0))
        theta = np.pi * theta / 180
        self.drawVehicle(self.pos.x , self.pos.y,theta,20)
        # pg.draw.circle(screen,(150,150,150) , (int(self.pos.x),int(self.pos.y)),10)
        # pg.draw.line(screen, (255,255,255), (int(self.pos.x),int(self.pos.y)), (int(self.pos.x+self.vel.x*20), int(self.pos.y+self.vel.y*20)),2)
        # for ray in self.rays : 
        #     ray.show()
    def drawVehicle(self,xpos,ypos,theta,l) : 
        x1,y1 = xpos+(5*l/4)*np.cos(theta), ypos+(5*l/4)*np.sin(theta)
        x2,y2 = xpos+l*np.cos(theta-(3.2*np.pi/4)), ypos+l*np.sin(theta-(3.2*np.pi/4))
        xt,yt = xpos+(l/2)*np.cos(theta+(-np.pi)), ypos+(l/2)*np.sin(theta+(-np.pi))
        x3,y3 = xpos+l*np.cos(theta+(3.2*np.pi/4)), ypos+l*np.sin(theta+(3.2*np.pi/4))
        # pg.draw.polygon(screen, (20,220,20),[(x1,y1), (x2,y2),(xt,yt),(x3,y3)], 0) 
        pg.draw.polygon(screen, (0,255,255),[(x1,y1), (x2,y2),(xt,yt),(x3,y3)], 2) 
        pygame.gfxdraw.filled_polygon(screen, ((x1,y1), (x2,y2),(xt,yt),(x3,y3)), (200,200,50,200))
    

def nextGeneration() :
    calculateFitness()
    for i in range(total) :
        newVehicle = pickOne()
        vehicles.append(newVehicle)
    del savedVehicles[:]
def pickOne(): 
    index = 0 
    r = random.random()
    while r > 0 :
        r = r - savedVehicles[index].fitness
        index += 1
    index -= 1 
    theChoosenOne = savedVehicles[index]
    child = Vehicle(theChoosenOne.brain)
    child.mutate()
    return child
def calculateFitness() : 
    sum = 0
    for vehicle in savedVehicles : 
        sum += vehicle.score
    for vehicle in savedVehicles : 
        vehicle.fitness = vehicle.score / sum
def saveVehicle(fitVehicle) : 
    with open('ML/VehiclesDriving/vehicle.obj' , 'wb') as f : 
        pickle.dump(fitVehicle , f)
def loadVehicle() : 
    with open('ML/VehiclesDriving/vehicleCar.obj' , 'rb') as f : 
        fitVehicle = pickle.load(f)
    return fitVehicle
def runFittestVehicle() : 
    fitVehicle = loadVehicle()
    fitVehicle.pos = Vector2(3*wallGap/2 , 50)
    # fitVehicle.passedCheckpoint = False
    # fitVehicle.round = 1
    del vehicles[:]
    vehicles.append(fitVehicle)




numWalls = 10
walls = []
botPathWidth = 100
baseHeight = height - botPathWidth
wallGap = width / numWalls
wallWidth = 20
wallHeight = 3*baseHeight/4
for i in range(numWalls) : 
    x = i*wallGap
    if i%2 == 0 : y = 0
    else : y = baseHeight - wallHeight
    walls.append(Wall(x,y,wallWidth,wallHeight))
walls.append(Wall(0,0,width,wallWidth))
walls.append(Wall(width-wallWidth/2,0,wallWidth,height))
# walls.append(Wall(0,baseHeight-wallWidth,width,wallWidth))
walls.append(Wall(wallGap,baseHeight-wallWidth,width-(2*wallGap),wallWidth))
walls.append(Wall(0,0,wallWidth,height))
walls.append(Wall(0,height-wallWidth/2,width,wallWidth))

allEdges = []
for wall in walls : 
    edges = wall.edges()
    for edge in edges : 
        allEdges.append(edge)

particle = Vehicle()

vehicles = []
for i in range(total) : 
    vehicles.append(Vehicle())

render = []  

def Render(render) : 
    n = len(render)
    w = int(width / n)
    for i in range(n) : 
        ren = render[i]
        col = 255 - (255*ren/width)
        if col < 0 : col = 0
        h = (2*height*width - height*ren) / (3*width)
        x , y = width + i*w , height/2 - h/2
        pg.draw.rect(screen , (col,col,col) , (x,y,w,h))
        # pg.draw.rect(screen , (150,150,150) , (x,y,w,h),1)

def drawGrid() : 
    rowGap = 10
    col = 100,100,100
    numRows = int(height/rowGap)
    rowGap = int(height/numRows)
    for i in range(numWalls) : 
        pg.draw.line(screen,(col), (i*wallGap,0),(i*wallGap,height),1)
    for j in range(numRows) : 
        pg.draw.line(screen,(col), (0,j*rowGap),(width,j*rowGap),1)

def points(x,y,round) : 
        rowGap = 5
        numRows = height/rowGap
        c = 2 + int(x / wallGap) 
        if c%2 == 0 : 
            r = int(height/rowGap) - int(y/rowGap)
        else: 
            r = int(y/rowGap)
        point = numRows*(c**2) + r 
        return point*round

savedVehicles = []
n = 1
fittestVehicleRun = False
gen = 0
checkpt1 = Vector2((numWalls-1)*wallGap + wallWidth , baseHeight-wallWidth)
checkpt2 = Vector2(3*width/4 , baseHeight)
showRays = False
while running : 
    screen.fill(bgcol)
    # mx,my = pg.mouse.get_pos()
    # print(points(mx,my))
    # drawGrid()
    for i in range(n) : 
        for vehicle in vehicles : 
            vehicle.run()
            vehicle.checkPass(checkpt1,checkpt2)
            vehicle.think(allEdges)
            

        for i in range(len(vehicles)-1, -1, -1) : 
            if vehicles[i].isDead : savedVehicles.append(vehicles.pop(i))
        # print(len(vehicles) , len(savedVehicles))

        if len(vehicles) == 0 : 
            nextGeneration()
            for veh in vehicles : veh.showRays = showRays
            gen += 1
            print("generation No : " , gen)

    pg.draw.line(screen,(0,255,0), (int(checkpt2.x),int(checkpt2.y)),(int(checkpt2.x),height),3)
    for wall in walls : wall.show()
    for vehicle in vehicles : vehicle.show()

    for event in pg.event.get() : 
        if event.type == pg.QUIT : 
            running = False 
        elif event.type == pg.KEYDOWN : 
            if event.key == pg.K_ESCAPE : 
                running = False 
            if event.key == pg.K_SPACE : 
                showRays = not showRays
                for veh in vehicles : veh.showRays = showRays
            if event.key == pg.K_r : 
                for i in range(len(vehicles)-1, -1, -1) : 
                    savedVehicles.append(vehicles.pop(i))
            if event.key == pg.K_UP : 
                n += 2
                if n >= 30 : n = 30
                print(n)
            if event.key == pg.K_p : 
                for veh in vehicles : print(veh.score)
            if event.key == pg.K_DOWN : 
                n -= 2
                if  n <= 0 : n = 1
                print(n)
            if event.key == pg.K_s : 
                fittestVehicle = vehicles[0]
                saveVehicle(fittestVehicle)
            if event.key == pg.K_l : 
                fittestVehicleRun = True
                runFittestVehicle()
    pg.display.flip()
    clock.tick(60)
pg.quit()
