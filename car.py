import pygame as pg
from allVariables import *
from pygame.math import Vector2

class Car(pg.sprite.Sprite) : 
    def __init__(self , vehicle , carLength = carLength , carWidth = carWidth) : 
        super().__init__() 
        self.vehicle = vehicle
        self.carLength = carLength
        self.carWidth = carWidth
        self.pic = pic
        self.image = self.pic
        self.rect = self.image.get_rect()
    def drawCar(self) : 
        theta = Vector2(1,0).angle_to(self.vehicle.vel)
        # theta = np.pi * theta / 180
        self.image = pg.transform.scale(self.pic,(self.carLength,self.carWidth))
        self.image = pg.transform.rotate(self.image,180-theta)
        self.rect = self.image.get_rect()
        self.rect.center = self.vehicle.pos.x , self.vehicle.pos.y