import pygame
from pygameGame import PygameGame







class openScreen(PygameGame):
    
    def init(self):
        self.screen= pygame.display.set_mode((self.width, self.height))
        self.bgColor = (20, 175, 20)
        
        self.skyIm= pygame.transform.scale(
        pygame.image.load('Pictures/Sky.jpg').convert_alpha(),(int(5*self.height/10), int(7*self.height/10)))
        # image taken from Daniel Tjioe with Ultiphotos
        # https://ultiworld.com/2014/03/11/1-unc-beat-2-colorado-video-breakdown/
        self.skyRect = (0,int(self.height*3/10))
        
        self.layoutIm= pygame.transform.scale(
        pygame.image.load('Pictures/layout2.jpg').convert_alpha(),(int(5*self.height/10), int(7*self.height/10)))
        # image taken from Hannah Frey on Pintrest
        # https://www.pinterest.com/pin/196399233721470387/
        self.layoutRect=(int(self.width-(5*self.height/10)),int(self.height*3/10))
    
        pygame.font.init() 
        myfont = pygame.font.SysFont('rockwell', int(self.width/10))
        self.title = myfont.render('Frisbee Game', False, (250,250,250))
        
        myfont2 = pygame.font.SysFont('rockwell',int(self.width/25))
        self.playTitle=myfont2.render('PLAY',False,(250,250,250))
        
        myfont3 = pygame.font.SysFont('rockwell',int(self.width/40))
        self.instTitle=myfont3.render('INSTRUCTIONS',False,(250,250,250))
        
        self.playBotton=((self.width/2-self.width/10,self.height/3),(self.width/5,self.height/5))
        self.instBotton=((self.width/2-self.width/10,2*self.height/3),(self.width/5,self.height/5))
    
        self.playC=(250,250,250)
        self.playW=3
        self.instW=3
        self.instC=(250,250,250)
    
        
    def redrawAll(self, screen):
        pygame.draw.rect(self.screen,self.playC,self.playBotton,self.playW)
        pygame.draw.rect(self.screen,self.instC,self.instBotton,self.instW)
        
        screen.blit(self.title,(self.width/6,self.width/1000))
        screen.blit(self.playTitle,(self.width/2-self.width/20,self.height/3+self.height/17.5))
        screen.blit(self.instTitle,(self.width/2-self.width/11.5,2*self.height/3+self.height/14))
        
        
        screen.blit(self.skyIm,self.skyRect)
        screen.blit(self.layoutIm,self.layoutRect)
        
        
        
    def mousePressed(self,x,y):
        if x>self.playBotton[0][0] and x<self.playBotton[0][0]+self.playBotton[1][0]:
            if y>self.playBotton[0][1] and y<self.playBotton[0][1]+self.playBotton[1][1]:
                print("play")
            elif y>self.instBotton[0][1] and y<self.instBotton[0][1]+self.instBotton[1][1]:
                print ("instructions")
                pygame.QUIT

    def mouseMotion(self,x,y):
        if x>self.playBotton[0][0] and x<self.playBotton[0][0]+self.playBotton[1][0]:
            if y>self.playBotton[0][1] and y<self.playBotton[0][1]+self.playBotton[1][1]:
                self.playW=7
                self.playC=(250,250,0)
            elif y>self.instBotton[0][1] and y<self.instBotton[0][1]+self.instBotton[1][1]:
                self.instW=7
                self.instC=(250,250,0)
            else:
                self.playW=3
                self.instW=3
                self.playC=(250,250,250)
                self.instC=(250,250,250)
        else:
            self.playW=3
            self.instW=3
            self.playC=(250,250,250)
            self.instC=(250,250,250)

def main():
    game = openScreen(1000,600)
    game.run()

if __name__ == '__main__':
    main()