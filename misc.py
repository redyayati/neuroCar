import pygame as pg 
import pygame.gfxdraw
from pygame.math import Vector2
from allVariables import *
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



def Render(render) : 
    n = len(render)
    w = int(renderWidth / n)
    # screen.blit(bg , (width+wallWidth/2 , 0))
    pg.draw.rect(screen , (100,130,180) , (width+wallWidth/2  , 0 , renderWidth , height/2))
    for i in range(n) : 
        ren = render[i]
        col = 255 - (255*ren/renderWidth)
        if col < 10 : col = 10
        h = (2*height*renderWidth - height*ren) / (3*renderWidth) - 100
        x , y = width+wallWidth/2 + i*w , height/2 - h/2
        pg.draw.rect(screen , (col,col,col) , (x,y,w,h))
        # screen.blit(dashboard , (width+wallWidth/2 , height/2+50))

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
        c = int(x / wallGap) 
        if c%2 == 0 : 
            r = int(height/rowGap) - int(y/rowGap)
        else: 
            r = int(y/rowGap)
        point = numRows*(5**c) + r 
        return point*round