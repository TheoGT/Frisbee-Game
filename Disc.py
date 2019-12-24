import random
import pygame

class Disc(pygame.sprite.Sprite):
    
    
    def __init__(self, x, y, radius,xDist,yDist,windX,windY):
        super(Disc, self).__init__()
        # x, y define the center of the object
        self.x, self.y, self.radius = x, y, radius
        self.vx=xDist//35
        self.vy=yDist//35
        self.gxy=.98
        self.windX=windX
        self.windY=windY
        self.totalTime=10+((xDist**2+yDist**2)**.5)/1.5
        self.catch=False
        self.turnover=False
        # taken from Lukas Peraza
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, (255, 255, 255),
                           (self.radius, self.radius), self.radius)
        
        self.updateRect()
        
    def update(self):
        if self.totalTime>-10:
            self.vx+=self.windX/20
            self.vy+=self.windY/20
            self.x+=self.vx
            self.y+=self.vy
            self.vx*=self.gxy
            self.vy*=self.gxy
            self.totalTime-=1
            if self.totalTime<150:
                self.catch=True
        else:
            self.catch=False
            self.turnover=True
        self.updateRect()

       
    # form Lukas Peraza
    def updateRect(self):
        w,h = self.radius,self.radius
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)