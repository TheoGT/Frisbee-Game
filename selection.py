import pygame
from pygameGame import PygameGame
import os
from team import Team


class selection(PygameGame):
    def init(self):
        self.screen= pygame.display.set_mode((self.width, self.height))
        self.bgColor = (20, 175, 20)
        self.myfont5 = pygame.font.SysFont('rockwell', int(self.width/25))
        self.myfont52 = pygame.font.SysFont('rockwell', int(self.width/50))
        myfont3 = pygame.font.SysFont('rockwell', int(self.width/20))
        self.title2=myfont3.render("Team Selection: User:        Computer:", True, (250,250,250))
        self.cont=myfont3.render("Confirm",True,(250,250,250))
        self.undo=myfont3.render("Undo",True,(250,250,250))
        lst=self.getTeams("Teams")
        self.teamLst=[]
        self.teamColor=[]
        for team1 in lst:
            i=Team(team1)
            self.teamColor+=[i.color]
            self.teamLst+=[i]
            
        self.uSelect=False
        self.sColor=(250,250,250)
        self.uColor=(250,250,250)
        self.uConfirmed=False
        self.cSelect=False

            
    def redrawAll(self,screen):
        ry=self.height/50
        n=1
        screen.blit(self.title2,(self.width/25,self.width/50))
        for team in self.teamLst:
            pygame.draw.rect(screen,self.teamColor[n-1],(self.width/25,ry*7*n,23*self.width/25,ry*6),2)
            teamIm= pygame.transform.scale(pygame.image.load(team.pic).convert_alpha(),(int(ry*6), int(ry*6)))
            screen.blit(teamIm,(self.width/25,ry*7*n))
            
            name = self.myfont5.render(team.name, True, (250,250,250))
            screen.blit(name,(self.width/8,ry*7*n+ry))
            
            n1=0
            for line in team.about:
                about = self.myfont52.render(line, True, (250,250,250))
                screen.blit(about,(4*self.width/10,ry*7*n+2*n1*ry+ry))
                n1+=1
                
            pygame.draw.circle(screen,team.color,(int(9*self.width/10),int(ry*7*n+ry*3)),int(ry*2))
            
            n+=1
          
        if self.uSelect==True:
            screen.blit(self.cont,(2*self.width/3,self.height*17/20))
            pygame.draw.rect(screen,self.sColor,
            (2*self.width/3-self.width/40,self.height*17/20,self.width/4,2*self.height/20),2)
            tIm= pygame.transform.scale(pygame.image.load(self.user.pic).convert_alpha(),(int(ry*5), int(ry*5)))
            screen.blit(tIm,(5*self.width/9,self.width/50))
            
            
            if self.cSelect==True:
                tIm= pygame.transform.scale(pygame.image.load(self.computer.pic).convert_alpha(),(int(ry*5), int(ry*5)))
                screen.blit(tIm,(8*self.width/9+self.width/100,self.width/50))
                screen.blit(self.undo,(self.width/8,self.height*17/20))
                pygame.draw.rect(screen,self.uColor,(self.width/10,self.height*17/20,self.width/6,2*self.height/20),2)
                
    def drawTeams(self,screen):
        ry=self.height/50
        n=1
        for team in self.teamLst:
            pygame.draw.rect(screen,self.teamColor[n-1],(self.width/25,ry*7*n,23*self.width/25,ry*6),2)
            teamIm= pygame.transform.scale(pygame.image.load(team.pic).convert_alpha(),(int(ry*6), int(ry*6)))
            screen.blit(teamIm,(self.width/25,ry*7*n))
            
            name = self.myfont5.render(team.name, True, (250,250,250))
            screen.blit(name,(self.width/8,ry*7*n+ry))
            
            n1=0
            for line in team.about:
                about = self.myfont52.render(line, True, (250,250,250))
                screen.blit(about,(4*self.width/10,ry*7*n+2*n1*ry+ry))
                n1+=1
                
            pygame.draw.circle(screen,team.color,(int(9*self.width/10),int(ry*7*n+ry*3)),int(ry*2))
            
            n+=1
        if self.uSelect==True:
            screen.blit(self.cont,(2*self.width/3,self.height*17/20))
            pygame.draw.rect(screen,self.sColor,
            (2*self.width/3-self.width/40,self.height*17/20,self.width/4,2*self.height/20),2)
            tIm= pygame.transform.scale(pygame.image.load(self.user.pic).convert_alpha(),(int(ry*5), int(ry*5)))
            screen.blit(tIm,(5*self.width/9,self.width/50))
            
            
            if self.cSelect==True:
                tIm= pygame.transform.scale(pygame.image.load(self.computer.pic).convert_alpha(),(int(ry*5), int(ry*5)))
                screen.blit(tIm,(8*self.width/9+self.width/100,self.width/50))
                screen.blit(self.undo,(self.width/8,self.height*17/20))
                pygame.draw.rect(screen,self.uColor,(self.width/10,self.height*17/20,self.width/6,2*self.height/20),2)
            
    def mouseMotion(self, x, y):
        ry=self.height/50
        if x>self.width/25 and x<24*self.width/25:
            n=1
            for team in self.teamLst:
                if self.uSelect==False:
                    if y<ry*7*n+ry*6 and y>ry*7*n:
                        self.teamColor[n-1]=(250,250,0)
                    else:
                        self.teamColor[n-1]=(250,250,250)
                    n+=1
                elif self.cSelect==True:
                    if y<ry*7*n+ry*6 and y>ry*7*n and self.user!=team and self.computer!=team:
                        self.teamColor[n-1]=(250,250,0)
                    elif self.user!= team and self.computer!=team:
                        self.teamColor[n-1]=(250,250,250)
                    n+=1
                else:
                    if y<ry*7*n+ry*6 and y>ry*7*n and self.user!=team:
                        self.teamColor[n-1]=(250,250,0)
                    elif self.user!= team:
                        self.teamColor[n-1]=(250,250,250)
                    n+=1
        if self.uSelect==True:
            if (x>2*self.width/3-self.width/40 and x<2*self.width/3-self.width/40+self.width/4 and\
            y>self.height*17/20 and y< self.height*17/20+2*self.height/20):
                self.sColor=(250,250,0)
            else:
                self.sColor=(250,250,250)
            
                
        if self.cSelect==True:
            if (x>self.width/10 and x<self.width/10+self.width/6 and y>self.height*17/20 and \
            y<self.height*17/20+2*self.height/20):
                self.uColor=(250,250,0)
            else:
                self.uColor=(250,250,250)
            
            
            
            
    def mousePressed(self, x, y):
        ry=self.height/50
        if x>self.width/25 and x<24*self.width/25 and self.uConfirmed==False:
            n=1
            for team in self.teamLst:
                if y<ry*7*n+ry*6 and y>ry*7*n:
                    self.uSelect=True
                    self.user=team
                    self.teamColor[n-1]=(0,0,250)
                n+=1
                
        if x>self.width/25 and x<24*self.width/25 and self.uConfirmed==True:
            n=1
            for team in self.teamLst:
                if y<ry*7*n+ry*6 and y>ry*7*n and team!=self.user:
                    self.cSelect=True
                    self.computer=team
                    self.teamColor[n-1]=(250,0,0)
                n+=1        
                
        
        if (x>2*self.width/3-self.width/40 and x<2*self.width/3-self.width/40+self.width/4 and\
            y>self.height*17/20 and y< self.height*17/20+2*self.height/20):
            if self.uSelect==True:
                self.uConfirmed=True 
            if self.cSelect==True:
                print ("hi")
            
        elif self.cSelect==True:
            if (x>self.width/10 and x<self.width/10+self.width/6 and y>self.height*17/20 and \
            y<self.height*17/20+2*self.height/20 and self.cSelect==True):
                self.uConfirmed=False 
                self.uSelect==True
                self.cSelect=False 
        
        
    def getTeams(self,path):
        lst=[]
        for filename in os.listdir(path):
            lst+=[filename]
        return lst
        
    
    
    
    
    
    
        
  
        
        
        
        
        
        
        
        
        
        
        
def main():
    game = selection(1000,600)
    game.run()

if __name__ == '__main__':
    main()