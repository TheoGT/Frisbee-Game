import pygame

class Player(pygame.sprite.Sprite):
    
    # idea taken from Lukas Peraza, 2015 for 15-112 Pygame Lecture
    def __init__(self, x, y, radius,team,color,name,number,skill,throws,air,stamina,speed,accel,position):
        super(Player, self).__init__()
        # x, y define the center of the object
        self.x, self.y, self.radius = x, y, radius
        if position==1:
            self.cutter=True
        else:
            self.cutter=False
        self.vx,self.vy=0,0
        self.team,self.skill,self.thorws,self.air=team,skill,throws,air
        self.name,self.number,self.stamina,self.accel=name,number,stamina,accel
        self.speed=speed
        self.moveable=True
        self.select=False
        
        self.image = pygame.Surface((2 * self.radius, 2 * self.radius),
        pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        
        self.percent=0
        self.defaltColor=color
        self.selectC=(255,0,0)
        
        
        self.updateRect()   
        
    def init():pass

        
    def move(self,x,y):
        if (self.vx**2+self.vy**2)**2<self.speed:
            #print (self.vx,self.vy)
            self.vx+=x*self.accel
            self.vy+=y*self.accel
            
    def stop(self):
        print("hi")
        self.moveable=False

        
    # from Lukas Peraza, 2015 for 15-112 Pygame Lecture
    def updateRect(self):
        # update the object's rect attribute with the new x,y coordinates
        if self.select==False:
            pygame.draw.circle(self.image, self.defaltColor,
                            (self.radius, self.radius), self.radius)
        elif self.select==True:
            pygame.draw.circle(self.image, self.selectC,
                            (self.radius, self.radius), self.radius)
        w,h = self.radius,self.radius
        self.rect = pygame.Rect(self.x - w / 2, self.y - h / 2, w, h)

    # ideas form Lukas Peraza, 2015 for 15-112 Pygame Lecture
    def update(self,bounds,x,y):
        if self.moveable==True:
            self.move(x,y)
            slower=.5
        
        self.x+=self.vx
        self.y+=self.vy
        if self.vx>0:
            self.vx-=slower*self.accel
        elif self.vx<0:
            self.vx+=slower*self.accel
        if self.vy>0:
            self.vy-=slower*self.accel
        elif self.vy<0:
            self.vy+=slower*self.accel
        if self.x<=bounds[0][0]:
            self.vx=0
            self.x=bounds[0][0]
        elif self.x>bounds[0][0]+bounds[1][0]:
            self.vx=0
            self.x=bounds[0][0]+bounds[1][0]
        if self.y<bounds[0][1]:
            self.vy=0
            self.y=bounds[0][1]
        elif self.y>bounds[0][1]+bounds[1][1]:
            self.vy=0
            self.y=bounds[0][1]+bounds[1][1]
        self.updateRect()
            