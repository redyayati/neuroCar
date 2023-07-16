import pygame as pg 
import pygame.gfxdraw
import random 
import numpy as np
from nn import NeuralNetwork
from pygame.math import Vector2
from allVariables import *
from misc import *

class Vehicle(): 
    def __init__(self , brain = None) :
        self.pos = Vector2(3*wallGap/2 , 50)
        self.vel = Vector2(0,8)
        self.turnAngle = 5
        self.rays = []
        for i in range(0,182,45) : 
            ray = Ray(self.pos , i)
            self.rays.append(ray)
        self.castingRays = []
        for i in range(50 , 90+40 ,1 ) : 
            castRay = Ray(self.pos , i)
            self.castingRays.append(castRay)
        self.isDead = False
        self.score = 0
        self.fitness = 0
        self.round = 1
        self.showRays = False
        self.rayDists = []
        self.passedCheckpoint = False 
        if brain : self.brain = brain.copy()
        else : self.brain = NeuralNetwork(5,8,4)
    def lookWalls(self,edges): 
        rayDist = []
        closestPoints = []
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
                # if self.showRays : self.showRay(ray.pos.x,ray.pos.y,closest.x,closest.y)
                rayDist.append(record)
                closestPoints.append(closest)
            else: rayDist.append(2)
        if rayDist[2] < 30 or rayDist[0] < wallWidth or rayDist[4] < wallWidth : self.isDead = True
        self.rayDists = closestPoints
        return rayDist
    def drawRays(self) : 
        if self.showRays : 
            for ray in self.rays : 
                    for closest in self.rayDists : 
                        self.showRay(ray.pos.x,ray.pos.y,closest.x,closest.y)
    def lookForCast(self , edges) : 
        rayDist = []
        for ray in self.castingRays : 
            record = float('inf')   
            closest = None
            for edge in edges : 
                pt = ray.cast(edge)
                if pt : 
                    dist = self.pos.distance_to(pt)
                    angle = ray.dir.angle_to(self.vel)
                    angle = angle*np.pi/180
                    dist = dist * np.cos(angle)
                    if dist < record : 
                        record = dist
                        closest = pt
            if closest : 
                # if self.showRays : self.showRay(ray.pos.x,ray.pos.y,closest.x,closest.y)
                rayDist.append(record)
            else: rayDist.append(2)
        return rayDist
    def showRay(self,x1,y1,x2,y2) :
        pygame.gfxdraw.line(screen,int(x1),int(y1),int(x2),int(y2),(255,255,255,85))
        pg.draw.circle(screen,(180,10,10),(int(x2),int(y2)),3)
    def turnRight(self) : 
        if not self.isDead : 
            self.vel.rotate_ip(-self.turnAngle)
            self.rotateRays(-self.turnAngle)
            self.rotateCastRays(-self.turnAngle)
    def turnLeft(self):
        if not self.isDead : 
            self.vel.rotate_ip(self.turnAngle)
            self.rotateRays(self.turnAngle)
            self.rotateCastRays(self.turnAngle)
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
    def rotateCastRays(self,theta) : 
        for ray in self.castingRays : 
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