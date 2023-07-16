import pygame as pg 
import pygame.gfxdraw
import random 
import numpy as np
from pygame.math import Vector2
pg.init()
width = 2*600
height = 600

screen = pg.display.set_mode((width, height))
pg.display.set_caption('Driving vehicles')
clock = pg.time.Clock() 
running  = True
bgcol = 0,0,0
lcol = 255,255,255
pic = pg.image.load("car1.png")
group = pg.sprite.Group()
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

class Vehicle(pg.sprite.Sprite): 
    def __init__(self,pic) : 
        super().__init__()
        self.pos = Vector2(wallGap/2 , height-50)
        self.vel = Vector2(0,-8)
        self.rays = []
        for i in range(-180,2,45) : 
            ray = Ray(self.pos , i)
            self.rays.append(ray)
        self.isDead = False
        self.pic = pic
        self.image = pg.transform.scale(self.pic,(100,50))
        # self.image = pg.transform.rotate(self.image,-90)
        # self.image.set_alpha(self.trans)
        # self.rect = self.image.get_rect()
    def drawCar(self) : 
        theta = Vector2(1,0).angle_to(self.vel)
        # theta = np.pi * theta / 180
        self.image = pg.transform.scale(self.pic,(100,50))
        self.image = pg.transform.rotate(self.image,180-theta)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos.x , self.pos.y
    def lookWalls(self,edges): 
        render = []
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
                # pygame.gfxdraw.line(screen,int(ray.pos.x),int(ray.pos.y),int(closest.x),int(closest.y),(255,255,255,85))
                # pg.draw.circle(screen,(180,10,10),(int(closest.x),int(closest.y)),3)
                render.append(record)
            else: render.append(2)
        if render[2] < 25  : self.isDead = True
        return render
    
    def update(self) : 
        if not self.isDead : 
            keys = pg.key.get_pressed()
            # for key in keys : 
            #     if key==1 : print(keys.index(key))
            rKey = 275
            lKey = 276
            dKey = 274 
            uKey = 273
            delta = 10
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
            for ray in self.rays : 
                ray.pos = self.pos
                ray.dir.rotate_ip(theta)
            self.boundary()
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
        # pg.draw.polygon(screen, (255,255,255),[(x1,y1), (x2,y2),(xt,yt),(x3,y3)], 2) 
        pygame.gfxdraw.filled_polygon(screen, ((x1,y1), (x2,y2),(xt,yt),(x3,y3)), (200,200,50,200))
    

numWalls = 6
walls = []
for i in range(numWalls) : 
    wallGap = width / numWalls
    wallWidth = 10
    wallHeight = 3*height/4
    x = i*wallGap
    if i%2 == 0 : y = 0
    else : y = height - wallHeight
    walls.append(Wall(x,y,wallWidth,wallHeight))
walls.append(Wall(0,0,width,wallWidth))
walls.append(Wall(width-wallWidth,0,wallWidth,height))
walls.append(Wall(0,height-wallWidth,width,wallWidth))
walls.append(Wall(0,0,wallWidth,height))

allEdges = []
for wall in walls : 
    edges = wall.edges()
    for edge in edges : 
        allEdges.append(edge)





particle = Vehicle(pic)
group.add(particle)

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

def points(x,y) : 
        rowGap = 10
        numRows = height/rowGap
        c = int(x / wallGap) 
        if c%2 == 0 : 
            r = int(height/rowGap) - int(y/rowGap)
        else: 
            r = int(y/rowGap)
        point = c*numRows + r 
        return point

while running : 
    screen.fill(bgcol)
    for wall in walls : wall.show()
    # drawGrid()
    particle.update()
    particle.drawCar()
    particle.show()
    # particle.look(walls[1])
    render = particle.lookWalls(allEdges)    # Render(render)
    p = points(particle.pos.x,particle.pos.y)

    for event in pg.event.get() : 
        if event.type == pg.QUIT : 
            running = False 
        elif event.type == pg.KEYDOWN : 
            if event.key == pg.K_ESCAPE : 
                running = False 
            if event.key == pg.K_SPACE : 
                particle.pos = Vector2(wallGap/2 , height-50)
                particle.vel = Vector2(0,-4)
                particle.isDead = False
                particle.rays = []
                for i in range(-180,2,45) : 
                    ray = Ray(particle.pos , i)
                    particle.rays.append(ray)
    group.draw(screen)
    group.update()
    pg.display.flip()
    clock.tick(30)
pg.quit()
