import pygame


class Thrower(pygame.sprite.Sprite):
    def init(self):
        self.image = pygame.Surface((self.width*2,self.height*2),pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, (255, 255, 255),(self.width+3, self.height+3), 
        self.radius//2)
        self.throwX=0
        self.throwY=0
    
    def __init__(self, x, y, radius,width,height,color):
        super(Thrower, self).__init__()
        self.width,self.height=int(width),int(height)
        self.x, self.y, self.radius = x, y, radius
        self.init()
        self.color=color
        self.updateRect()
        self.velocity = (0, 0)

    def updateRect(self):
        # update the object's rect attribute with the new x,y coordinates
        w, h = self.image.get_size()
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)

    def update(self,x,y):
        dist=((self.x-x)**2+(self.y-y)**2)**.5
        
        self.init()
        pygame.draw.line(self.image, (200,0,0), (self.width//2,self.height//2),
        (x+self.width//2-self.x,y+self.height//2-self.y),1)
        pygame.draw.circle(self.image, self.color,(self.width//2, self.height//2), 
        self.radius)
        pygame.draw.circle(self.image, (255, 255, 255),(self.width//2+3, self.height//2+3), 
        self.radius//2)
        self.throwX=x-self.x
        self.throwY=y-self.y