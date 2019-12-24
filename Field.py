import module_manager
module_manager.review()
import random
import pygame
import math
from pygameGame import PygameGame
from Player import Player
from Disc import Disc
from Thrower import Thrower
from team import Team
import os
import string

# from Lukas Peraza, 2015 for 15-112 Pygame Lecture



class Field(PygameGame):
    
    def init(self):
        ###                         Play Screen                              ###
        self.screen= pygame.display.set_mode((self.width, self.height))
        
        self.throwing=False
        self.path=[]
        self.dpath=[]
        self.bgColor = (20, 175, 20)
        
        # regualtion field dimensions
        bounds=[3,120,40]
        endzone=[98,40,25]
        # distance from top of screen
        dist=self.height/5
        # ratio of field to screen size
        ratio=self.width/(bounds[1]+2*bounds[0])
        self.ratio=ratio
        self.brick=[(bounds[2]+bounds[0])*ratio,dist+bounds[2]/2*ratio,bounds[2]*ratio]
        # bounds of field
        self.bounds=((ratio*bounds[0],dist),
        (ratio*bounds[1],ratio*bounds[2]))
        
        self.endzone=[((ratio*bounds[0],dist),
        (ratio*endzone[2],ratio*endzone[1])),
        ((ratio*endzone[0],dist),(ratio*endzone[2],ratio*endzone[1]))]
        
        
        
        disc=Disc(self.brick[0],self.brick[1],3,0,0,0,0)
        self.disc=pygame.sprite.GroupSingle(disc)
        self.catchable=False
        self.turnOver=True
        self.intercepting=False
        
        #taken from stack overflow 
        #https://stackoverflow.com/questions/20842801/how-to-display-text-in-pygame
        pygame.font.init() 
        myfont = pygame.font.SysFont('rockwell', int(ratio*10))
        self.title = myfont.render('Frisbee Game', True, (250,250,250))
        self.windFont = pygame.font.SysFont('rockwell', int(ratio*5))
        self.windTitle= self.windFont.render('Wind:', True, (250,250,250))
        
        
        self.windspeed=(random.randint(0,20))/60
        self.windDir=random.randint(0,360)
        self.windX=math.cos(self.windDir)*self.windspeed
        self.windY=math.sin(self.windDir)*self.windspeed
        self.thrower=pygame.sprite.GroupSingle()
        
        self.playing=False
        
        
        ###                           Open Screen                            ###
        self.opening=True
        self.instructions=False
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
        
        myfont2 = pygame.font.SysFont('rockwell',int(self.width/25))
        self.playTitle=myfont2.render('PLAY',True,(250,250,250))
        
        myfont3 = pygame.font.SysFont('rockwell',int(self.width/40))
        self.instTitle=myfont3.render('INSTRUCTIONS',True,(250,250,250))
        
        self.playBotton=((self.width/2-self.width/10,self.height/3),(self.width/5,self.height/5))
        self.instBotton=((self.width/2-self.width/10,2*self.height/3),(self.width/5,self.height/5))
    
        self.playC=(250,250,250)
        self.playW=3
        self.instW=3
        self.instC=(250,250,250)
        self.n=1
        self.t=0
        self.t2=0
        self.gameTo=5
        ###                         Select Screen                            ###
        self.selecting=False
        self.dir=1
        self.userOffense=True
        self.wak=0
        
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
            self.teamColor+=[(250,250,250)]
            self.teamLst+=[i]
            
        self.uSelect=False
        self.sColor=(250,250,250)
        self.uColor=(250,250,250)
        self.uConfirmed=False
        self.cSelect=False

        
        self.team1="Mr.Yuk"
        self.team2="En Sabah Nur"
        self.team1score=0
        self.team2score=0
        self.team1Color=(200,250,50)
        self.team2Color=(0,0,150)
        
        self.dist=dist
        
        
        ###                        Directions Screen                         ###
        
        self.back=self.windFont.render('BACK',False,(250,250,250))
        df=pygame.font.SysFont('rockwell',int(self.ratio*2))
        self.line1=df.render('Basic rules of Ultimate Frisbee:',False, (250,250,250))
        self.line2=df.render('- The disc is advanced up the field by passing between players',False,(250,250,250))
        self.line3=df.render('- The player holding the disc cannot move until they throw to another player',
        False, (250,250,250))
        self.line4=df.render('- If the defense catches the disc, it hits the ground, or it goes out of bounds,'+\
        'the disc changes possestion',False, (250,250,250))
        self.line5=df.render('- A goal is scored if the offense catches the disc in the opponents endzone',
        False, (250,250,250))
        self.line6=df.render('Basics of the Frisbee Game:',False,(250,250,250))
        self.line7=df.render('-To move players around, right click on a player and then click somewhere within the'+\
        'bounds of the field',False, (250,250,250))
        self.line8=df.render('- Once you have possesion of the disc, left click anywhere on the screen to throw it '+\
        'to that location (keep in mind wind speed)',False, (250,250,250))
        self.line9=df.render('- Cuts will apear automatically from the back of the stack, except for near the endzone'+\
        ' where they will apear from the front',False, (250,250,250))
        self.line10=df.render('Good luck and have fun!',False, (250,250,250))
        
        self.win=False
        self.loose=False
        self.winText=myfont.render("You Win!!!",False, (250,250,250))
        self.looseText=myfont.render("You Lose!!!",False, (250,250,250))
        
    def spawn(self):
        
        self.offense=pygame.sprite.Group()
        self.onList=[]
        #delete when making roster screen
        for players in self.user.roster:
            p=players
        mP=self.user.roster
        # delete when making roster screen
        player=Player(self.endzone[0][1][0],self.dist+self.endzone[0][1][1]/3+self.ratio*15,6,
        self.team1,self.team1Color,p,mP[p][0],mP[p][1],mP[p][2],mP[p][3],mP[p][4],mP[p][5],mP[p][6],2)
        self.offense.add(player)
        for i in range(5):
            player=Player(self.endzone[0][1][0],self.dist+self.endzone[0][1][1]/3+self.ratio*i*3,6,
            self.team1,self.team1Color,p,mP[p][0],mP[p][1],mP[p][2],mP[p][3],mP[p][4],mP[p][5],mP[p][6],1)
            self.offense.add(player)
        self.selectedPlayer=Player(self.endzone[0][1][0],self.dist+self.endzone[0][1][1]/3+self.ratio*18,6,
        self.team1,self.team1Color,p,mP[p][0],mP[p][1],mP[p][2],mP[p][3],mP[p][4],mP[p][5],mP[p][6],2)
        self.offense.add(self.selectedPlayer)
        self.temp=self.selectedPlayer
        for player in self.offense:
            self.onList+=[player]
        
        if self.userOffense==False or self.wak==0:
            disc=Disc(self.brick[0],self.brick[1],3,0,0,0,0)
            self.disc=pygame.sprite.GroupSingle(disc)
            if self.wak==1:
                self.dir=-1
        else:
            disc=Disc(self.brick[0]+self.ratio*40,self.brick[1],3,0,0,0,0)
            self.disc=pygame.sprite.GroupSingle(disc)
            self.dir=1

        
        self.dList=[]
        self.defense=pygame.sprite.Group()
        # delete when making roster
        for players in self.computer.roster:
            p=players
        mP=self.computer.roster
        
        for i in range(2):
            player=Player(self.bounds[1][0]-self.dist,self.dist+self.endzone[0][1][1]/3+self.ratio*(15+i*3),6,
            self.team2,self.team2Color,p,mP[p][0],mP[p][1],mP[p][2],mP[p][3],mP[p][4],mP[p][5],mP[p][6],2)
            self.defense.add(player)
        for i in range(5):
            player=Player(self.bounds[1][0]-self.dist,self.dist+self.endzone[0][1][1]/3+self.ratio*i*3,6,
            self.team2,self.team2Color,p,mP[p][0],mP[p][1],mP[p][2],mP[p][3],mP[p][4],mP[p][5],mP[p][6],1)
            self.defense.add(player)
        for player in self.defense:
            self.dList+=[player]
        
        if self.wak==1:
            if self.userOffense==True: 
                self.changePossesion()
            else: self.userOffense=True
            #else: self.changePossesion()
            
        else: 
            self.wak=1
        
    def redrawAll(self,screen):
        if self.playing==True:
            screen=self.screen
            # draws the field
            pygame.draw.rect(screen, (250,250,250),self.bounds,1)
            pygame.draw.rect(screen, (250,250,250),self.endzone[0],1)
            pygame.draw.rect(screen, (250,250,250),self.endzone[1],1)
            pygame.draw.rect(screen, (250,250,250),(self.brick[0]-2,self.brick[1]-2,
            4,4),1)
            pygame.draw.rect(screen, (250,250,250),(self.bounds[1][0]-self.brick[2]-2+self.bounds[0][0],
            self.brick[1]-2,4,4),1)
            
            # draws players
            self.offense.draw(screen)
            self.defense.draw(screen)
            
            for disc in self.disc:
                if disc.catch==False:
                    pygame.draw.circle(screen,(200,0,0),(int(disc.x+disc.radius/2),int(disc.y+disc.radius/2)),
                    int(disc.radius*3/2))
                    self.catchable=False
                else:
                    self.catchable=True
                # puts the disc in bounds if it turns over
                if disc.turnover==True:
                    if disc.x>self.endzone[1][0][0]:
                        disc.x=self.endzone[1][0][0]
                    elif disc.x<self.endzone[0][1][0]:
                        disc.x=self.endzone[0][1][0]+self.bounds[0][0]
                    if disc.y<self.bounds[0][1]:
                        disc.y=self.bounds[0][1]
                    elif disc.y>self.bounds[1][1]+self.bounds[0][1]:
                        disc.y=self.bounds[1][1]+self.bounds[0][1]
                    self.catchable=False
                    self.turnOver=True
                else:
                    self.turnOver=False
                
            self.disc.draw(screen)
            
            if len(self.path)>1:
                pygame.draw.line(self.screen,(255,0,0),(self.temp.x,self.temp.y),
                (self.path[1][0],self.path[1][1]),2)
                if (self.temp.x<=self.path[1][0]+self.temp.radius and
                self.temp.x>=self.path[1][0]-self.temp.radius and 
                self.temp.y<=self.path[1][1]+self.temp.radius and 
                self.temp.y>=self.path[1][1]-self.temp.radius):
                    self.path=self.path[1:]
            if self.userOffense==True:
                for i in range(1,len(self.path)-1):
                    pygame.draw.line(self.screen,(255,0,0),(self.path[i][0],self.path[i][1]),
                    (self.path[i+1][0],self.path[i+1][1]),2)
            
            
            if len(self.dpath)>1:
                pygame.draw.line(self.screen,(0,0,255),(self.dtemp.x,self.dtemp.y),
                (self.dpath[1][0],self.dpath[1][1]),2)
                if (self.dtemp.x<=self.dpath[1][0]+self.dtemp.radius and
                self.dtemp.x>=self.dpath[1][0]-self.dtemp.radius and 
                self.dtemp.y<=self.dpath[1][1]+self.dtemp.radius and 
                self.dtemp.y>=self.dpath[1][1]-self.dtemp.radius):
                    self.dpath=self.dpath[1:]
            for i in range(1,len(self.dpath)-1):
                pygame.draw.line(self.screen,(0,0,255),(self.dpath[i][0],self.dpath[i][1]),
                (self.dpath[i+1][0],self.dpath[i+1][1]),2)
            
            # draws titles
            screen.blit(self.title,(self.bounds[0][0],self.bounds[0][0]//2))
            screen.blit(self.windTitle,(self.endzone[1][0][0],self.bounds[0][0]//2))
            screen.blit(self.team1report,(self.bounds[0][0],self.bounds[0][1]+self.bounds[1][1]))
            screen.blit(self.team2report,(self.bounds[0][0],self.bounds[0][1]+self.bounds[1][1]+self.ratio*5))
            
            # draws wind direction
            pygame.draw.line(self.screen, (200,200,200),
            (self.endzone[1][0][0]+self.bounds[0][0]*6,self.bounds[0][0]*3/2),
            (self.endzone[1][0][0]+self.bounds[0][0]*6+self.windX*100,
            self.bounds[0][0]*3/2+self.windY*100),3)
            pygame.draw.circle(self.screen,(0,0,255),
            (int(self.endzone[1][0][0]+self.bounds[0][0]*6),int(self.bounds[0][0]*3/2)),3)
            
            if self.throwing==True:
                self.thrower.draw(screen)
                '''pygame.draw.rect(screen,(0,200,200),self.forceSide,2)
                pygame.draw.rect(screen,(200,0,200),self.breakSide,2)
                pygame.draw.rect(screen,(200,200,0),self.deepSpace,2)'''
    
        elif self.opening==True:
            pygame.draw.rect(self.screen,self.playC,self.playBotton,self.playW)
            pygame.draw.rect(self.screen,self.instC,self.instBotton,self.instW)
            
            screen.blit(self.title,(self.width/4,self.width/25))
            screen.blit(self.playTitle,(self.width/2-self.width/20,self.height/3+self.height/17.5))
            screen.blit(self.instTitle,(self.width/2-self.width/11.5,2*self.height/3+self.height/14))
            
            
            screen.blit(self.skyIm,self.skyRect)
            screen.blit(self.layoutIm,self.layoutRect)
            self.win=False
            self.loose=False
            
            
        elif self.instructions==True:
            pygame.draw.rect(screen,(200,200,200),(self.ratio*5,self.ratio*5,self.ratio*20,self.ratio*10),3)
            screen.blit(self.title,(self.width/4,self.width/25))
            screen.blit(self.back,(self.ratio*8,self.ratio*7))
            screen.blit(self.line1,(self.ratio*10,self.ratio*20))
            screen.blit(self.line2,(self.ratio*10,self.ratio*23))
            screen.blit(self.line3,(self.ratio*10,self.ratio*26))
            screen.blit(self.line4,(self.ratio*10,self.ratio*29))
            screen.blit(self.line5,(self.ratio*10,self.ratio*32))
            screen.blit(self.line6,(self.ratio*10,self.ratio*38))
            screen.blit(self.line7,(self.ratio*10,self.ratio*41))
            screen.blit(self.line8,(self.ratio*10,self.ratio*44))
            screen.blit(self.line9,(self.ratio*10,self.ratio*47))
            screen.blit(self.line10,(self.ratio*10,self.ratio*50))
            
        elif self.win==True:
            pygame.draw.rect(screen,(200,200,200),(self.ratio*5,self.ratio*5,self.ratio*20,self.ratio*10),3)
            screen.blit(self.winText,(self.width/3,self.height/3))
            screen.blit(self.back,(self.ratio*8,self.ratio*7))
            
        elif self.loose==True:
            pygame.draw.rect(screen,(200,200,200),(self.ratio*5,self.ratio*5,self.ratio*20,self.ratio*10),3)
            screen.blit(self.looseText,(self.width/3,self.height/3))
            screen.blit(self.back,(self.ratio*8,self.ratio*7))
            
        elif self.selecting==True:
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
                    tIm= pygame.transform.scale(pygame.image.load(self.computer.pic).convert_alpha(),(int(ry*5),
                     int(ry*5)))
                    screen.blit(tIm,(8*self.width/9+self.width/100,self.width/50))
                    screen.blit(self.undo,(self.width/8,self.height*17/20))
                    pygame.draw.rect(screen,self.uColor,
                    (self.width/10,self.height*17/20,self.width/6,2*self.height/20),2)
            
    def timerFired(self, dt):
        if self.playing==True:
            if self.team1score==self.gameTo:
                self.playing=False
                self.win=True
            elif self.team2score==self.gameTo:
                self.playing=False
                self.loose=True
            if self.userOffense==True:
                x,y=self.keyHelper(self.isKeyPressed)
                self.selectedPlayer.move(x,y)
            self.offense.update(self.bounds,0,0)
            self.defense.update(self.bounds,0,0)
            self.disc.update()
            
            # makes the disc change possesion if it hits the ground
            if self.turnOver==True and self.n==0 and self.throwing==False:
                self.changePossesion()
                self.n+=1
            
            # allows for players to catch the disc
            if self.catchable==True or self.turnOver==True:
                for player in pygame.sprite.groupcollide(self.offense, self.disc, True, True,
                        pygame.sprite.collide_circle):
                    self.throwing=True
                    if player.y>self.bounds[0][1]+self.ratio*30:
                        # close to force sideline
                        self.stack=(player.x+self.ratio*5*self.dir,self.bounds[0][1]+self.ratio*25,
                        player.x+self.ratio*30*self.dir)
                        self.forceSide=(self.stack[0],self.stack[1]+player.radius,
                        self.stack[2]-self.stack[0],
                        self.bounds[1][1]+self.bounds[0][1]-self.stack[1]-player.radius)
                        self.breakSide=(self.stack[0],self.bounds[0][1],self.stack[2]-self.stack[0],
                        self.stack[1]-self.bounds[0][1]-player.radius)
                    elif player.y<self.bounds[0][1]+self.ratio*10:
                        # close to break sidline
                        self.stack=(player.x+self.ratio*5*self.dir,self.bounds[0][1],
                        player.x+self.ratio*30*self.dir)
                        self.breakSide=(self.stack[0],self.bounds[0][1],
                        self.stack[2]-self.stack[0],self.stack[1]-self.bounds[0][1]-player.radius)
                        self.forceSide=(self.stack[0],self.stack[1]+player.radius,
                        self.stack[2]-self.stack[0],
                        self.bounds[1][1]+self.bounds[0][1]-self.stack[1]-player.radius)
                    else:
                        self.stack=(player.x+self.ratio*5*self.dir,player.y-self.ratio*5,
                        player.x+self.ratio*30*self.dir)
                        self.forceSide=(self.stack[0],self.stack[1]+player.radius,
                        self.stack[2]-self.stack[0],
                        self.bounds[1][1]+self.bounds[0][1]-self.stack[1]-player.radius)
                        self.breakSide=(self.stack[0],self.bounds[0][1],self.stack[2]-self.stack[0],
                        self.stack[1]-self.bounds[0][1]-player.radius)
                    
                    # sets up deep space
                    if self.dir==1:
                        self.deepSpace=(self.stack[2],self.bounds[0][1],
                        self.bounds[0][0]+self.bounds[1][0]-self.stack[2],
                        self.bounds[1][1])
                    else:
                        self.deepSpace=(self.stack[2],self.bounds[0][1],
                        self.bounds[0][0]-self.stack[2],
                        self.bounds[1][1])
                    if player==self.temp:
                        self.path=[]
                    if self.dir==1:
                        if player.x>self.endzone[1][0][0]+self.ratio and \
                        player.x<self.endzone[1][1][0]+self.endzone[1][0][0]:
                            if player.team==self.team2:self.team2score+=1
                            else:self.team1score+=1
                            self.team1report=self.windFont.render((str(self.team1)+": "+str(self.team1score)),
                            False,(self.team1Color))
                            self.team2report=self.windFont.render((str(self.team2)+": "+str(self.team2score)),
                            False,(self.team2Color))
                            for o in self.offense:
                                self.offense.remove(o)
                            for d in self.defense:
                                self.defense.remove(d)
                            for t in self.thrower:
                                self.thrower.remove(t)
                            self.throwing=False
                            self.spawn()  
                            
                            self.catchable=False
                            self.turnOver=True
                            self.intercepting=False
                            self.dir=1
                            self.n=1
                            self.changePossesion()
                            print ("score for:",player.team)
                    elif self.dir==-1:
                        if player.x>self.endzone[0][0][0] and \
                        player.x<self.endzone[0][1][0]+self.endzone[0][0][0]-self.ratio:
                            if player.team==self.team2:self.team2score+=1
                            else:self.team1score+=1
                            self.team1report=self.windFont.render((str(self.team1)+": "+str(self.team1score)),
                            False,(self.team1Color))
                            self.team2report=self.windFont.render((str(self.team2)+": "+str(self.team2score)),
                            False,(self.team2Color))
                            for o in self.offense:
                                self.offense.remove(o)
                            for d in self.defense:
                                self.defense.remove(d)
                            for t in self.thrower:
                                self.thrower.remove(t)
                            self.throwing=False 
                            self.spawn()
                            
                            self.catchable=False
                            self.turnOver=True
                            self.intercepting=False
                            self.dir=1
                            self.n=1
                            self.changePossesion()
                            print ("score for:",player.team)
                    thrower=Thrower(player.x,player.y,6,self.bounds[1][0],
                    self.bounds[1][1],player.defaltColor)
                    self.thrower.add(thrower)
                    self.thrower.update(player.x,player.y)
                    player.select=False
                    self.intercepting=False
                    self.tempPlayer=player
                    self.n=0
                    for thrower1 in self.thrower:
                        self.tempThrower =thrower1
                        
            # allos for defendes to make interceptions and change the possesion
            if self.catchable ==True:
                for player in pygame.sprite.groupcollide(self.defense, self.disc, False, True,
                        pygame.sprite.collide_circle):
                    thrower=Thrower(player.x,player.y,6,self.bounds[1][0],
                    self.bounds[1][1],player.defaltColor)
                    self.thrower.add(thrower)
                    self.thrower.update(player.x,player.y)
                    self.changePossesion()
                    self.tempPlayer=player
                    newDisc=Disc(player.x-player.radius,player.y-player.radius,3,0,0,0,0)
                    self.disc.add(newDisc)
                    self.turnOver=True
                    self.n=1
                    
            # makes offenders run their paths
            if len(self.path)>1:
                self.runTo(self.runPlayer,self.path[1][0],self.path[1][1])
                
            if len(self.dpath)>1:
                self.runTo(self.drunPlayer,self.dpath[1][0],self.dpath[1][1])
    
            # makes offenders form a stack
            if self.throwing==True:
                n=0
                h=0
                for player in self.offense:
                    if player.cutter==True:
                        if self.dir==1 and self.stack[0]>self.endzone[1][0][0]-self.ratio*15:
                            if len(self.path)>1:
                                if player!=self.runPlayer:
                                    self.runTo(player,self.stack[0]+(n*self.ratio*25/4),self.stack[1])
                                    n+=1
                            else:
                                self.runTo(player,self.stack[0]+(n*self.ratio*25/4),self.stack[1])
                                n+=1
                        elif self.dir==-1 and self.stack[0]<self.endzone[0][0][0]+self.endzone[0][1][0]+self.ratio*15:
                            if len(self.path)>1:
                                if player!=self.runPlayer:
                                    self.runTo(player,self.stack[0]-(n*self.ratio*25/4),self.stack[1])
                                    n+=1
                            else:
                                self.runTo(player,self.stack[0]-(n*self.ratio*25/4),self.stack[1])
                                n+=1
                        else:
                            if len(self.path)>1:
                                if player!=self.runPlayer:
                                    self.runTo(player,self.stack[2]-(n*self.ratio*25/4*self.dir),self.stack[1])
                                    n+=1
                            else:
                                self.jogTo(player,self.stack[2]-(n*self.ratio*25/4*self.dir),self.stack[1])
                                n+=1
                    else:
                        if len(self.path)>1:
                            if player!=self.runPlayer:
                                self.runTo(player,self.stack[0]-(self.ratio*10*self.dir),
                                self.stack[1]+(self.ratio*10*h))
                                h+=1
                        else:
                            self.jogTo(player,self.stack[0]-(self.ratio*10*self.dir),
                            self.stack[1]+(self.ratio*10*h))
                            h+=1
            # makes offenders and defenders intercept discs
            else:
                if self.intercepting==True:
                    for disc in self.disc:
                        x,y=self.intercept(self.interceptP,disc)
                        x1,y1=self.intercept(self.interceptD,disc)
                        if x!=None:
                            self.runTo(self.interceptP,x,y)
                        if x1!=None:
                            self.runTo(self.interceptD,x1,y1)
                if self.userOffense==False:
                    for player in self.offense:
                        if player.cutter==False:
                            for disc in self.disc:
                                self.runTo(player,disc.x,disc.y)
                            break 
                            
            # makes players make cuts
            if self.throwing==True :
                for player in self.offense:
                    if len(self.path)<2 and ((player.x>=self.stack[2]-player.radius and\
                    player.x<=self.stack[2]+player.radius and (self.stack[0]<=self.endzone[1][0][0]-self.ratio*15 or\
                    self.dir==-1) and (self.stack[0]>=self.endzone[0][0][0]+self.endzone[0][1][0]+self.ratio*15 or\
                    self.dir==1)) or (self.dir==1 and self.stack[0]>self.endzone[1][0][0]-self.ratio*15 and \
                    player.x>=self.stack[0]-player.radius and player.x<=self.stack[0]+player.radius) or\
                    (self.dir==-1 and self.stack[0]<self.endzone[0][0][0]+self.endzone[0][1][0]+self.ratio*15 and \
                    player.x>=self.stack[0]-player.radius and player.x<=self.stack[0]+player.radius)):
                        self.t+=1
                        if self.t>60:
                            for player1 in self.offense:
                                player1.select=False
                            self.t=0
                            self.runPlayer=player
                            self.temp=player
                            if self.dir==1:
                                if self.stack[0]>self.endzone[1][0][0]-self.ratio*15:
                                    x=random.randint(0,int(self.ratio*20))-self.stack[2]+self.stack[0]
                                    y=(random.randint(0,int(self.bounds[0][1]+self.bounds[1][1]-self.stack[1])))
                                    x1=random.randint(0,int(self.ratio*5))
                                    y1=random.randint(player.radius*2,
                                    int(self.bounds[0][1]+self.bounds[1][1]-self.stack[1]))
                                else:
                                    x=random.randint(0,int(self.ratio*5))
                                    y=random.randint(0,int(self.bounds[0][1]+self.bounds[1][1]-self.stack[1]))
                                    x1=random.randint(0,int(self.ratio*20))
                                    y1=random.randint(player.radius*2,
                                    int(self.bounds[0][1]+self.bounds[1][1]-self.stack[1]))
                                self.path=[[player.x,player.y],[self.stack[2]+x*self.dir,self.stack[1]+y],
                                [self.stack[0]+x1*self.dir,self.stack[1]+y1]]
                                self.offense.remove(player)
                                self.offense.add(player)
                            else:
                                if self.stack[0]<self.endzone[0][0][0]+self.endzone[0][1][0]+self.ratio*15:
                                    x=random.randint(0,int(self.ratio*5))
                                    y=random.randint(0,int(self.bounds[0][1]+self.bounds[1][1]-self.stack[1]))
                                    x1=random.randint(0,int(self.ratio*20))+self.stack[2]-self.stack[0]
                                    y1=random.randint(player.radius*2,
                                    int(self.bounds[0][1]+self.bounds[1][1]-self.stack[1]))
                                else:
                                    x=random.randint(0,int(self.ratio*5))
                                    y=random.randint(0,int(self.bounds[0][1]+self.bounds[1][1]-self.stack[1]))
                                    x1=random.randint(0,int(self.ratio*20))
                                    y1=random.randint(player.radius*2,
                                    int(self.bounds[0][1]+self.bounds[1][1]-self.stack[1]))
                                self.path=[[player.x,player.y],[self.stack[2]+x1*self.dir,self.stack[1]+y1],
                                [self.stack[0]+x*self.dir,self.stack[1]+y]]
                            self.offense.remove(player)
                            self.offense.add(player)
            
            # makes the defenders gurad offenders
            n=0
            for defender in self.dList:
                if self.intercepting==True and defender==self.interceptD:
                    n+=1
                    continue 
                elif self.userOffense==False and len(self.dpath)>1 and defender==self.dtemp:
                    n+=1
                    continue
                if self.throwing==False:
                    self.jogTo(defender,self.onList[n].x,self.onList[n].y+self.onList[n].radius*2)
                    n+=1
                else:
                    if (defender.x>self.tempThrower.x-self.tempThrower.radius-defender.radius*2 and 
                    defender.x<self.tempThrower.x+self.tempThrower.radius+defender.radius*2 and
                    defender.y>self.tempThrower.y-self.tempThrower.radius-defender.radius*2 and 
                    defender.y<self.tempThrower.y+self.tempThrower.radius+defender.radius*2):
                        self.runTo(defender,self.onList[n].x+self.onList[n].radius*self.dir,
                        self.onList[n].y-self.onList[n].radius*2)
                        n+=1
                    else:
                        self.runTo(defender,self.onList[n].x,self.onList[n].y+self.onList[n].radius*2)
                        n+=1
                        
            # makes the AI throw
            if self.userOffense==False and len(self.path)==2 and self.throwing==True:
                self.t2+=1
                if self.t2>20:
                    for thrower in self.thrower:
                        x=(self.path[1][0]+self.runPlayer.x)/2
                        y=(self.path[1][1]+self.runPlayer.y)/2
                        thrower.update(x,y)
                    n=random.randint(0,1)
                    self.t2=0
                    if n==1:
                        self.mousePressed(x,y)
                        
    def changePossesion(self):
            self.dir*=-1
            tempO=[]
            tempD=[]
            self.onList=[]
            self.dList=[]
            for ofender in self.offense:
                tempO+=[ofender]
                ofender.select=False
                self.offense.remove(ofender)
            for defender in self.defense:
                defender.select=False
                tempD+=[defender]
                self.defense.remove(defender)
            for ofender in tempD:
                self.offense.add(ofender)
                self.onList+=[ofender]
            for defender in tempO:
                self.defense.add(defender)
                self.dList+=[defender]
            self.intercepting=False
            self.path=[]
            self.dpath=[]
            if self.userOffense==True:self.userOffense=False
            else: self.userOffense=True

            
    def getTeams(self,path):
        lst=[]
        for filename in os.listdir(path):
            lst+=[filename]
        return lst
            
            
            
    def mouseMotion(self, x, y):
        if self.playing ==True and  self.throwing==True and self.userOffense==True:
            self.thrower.update(x,y)
        elif self.opening==True:
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
        elif self.selecting==True:
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
            
    def runTo(self,player,x,y):
        xDist=(x-player.x)
        yDist=(y-player.y)
        dist=(xDist**2+yDist**2)**.5
        if dist<(player.vx**2+player.vy**2)**.5/(player.accel*2):
            player.vx*=(1-player.accel)
            player.vy*=(1-player.accel)
            player.percent=0
        else:
            if player.percent>=player.speed:
                player.vx=xDist/dist*player.speed
                player.vy=yDist/dist*player.speed
    
            else:
                player.vx=xDist/dist*player.percent
                player.vy=yDist/dist*player.percent
                player.percent+=player.accel
                
    def jogTo(self,player,x,y):
        xDist=(x-player.x)
        yDist=(y-player.y)
        dist=(xDist**2+yDist**2)**.5
        player.vx=xDist/dist*player.speed/3
        player.vy=yDist/dist*player.speed/3
        
    def intercept(self,player,disc):
        
        if len(self.path)>1 and player==self.runPlayer:
            self.path=[]
        if len(self.dpath)>1 and player==self.drunPlayer:
            self.dpath=[]
        t=disc.totalTime
        tt=disc.totalTime
        vx,vy,x,y=disc.vx,disc.vy,disc.x,disc.y
        while t>-10:
            vx+=disc.windX/20
            vy+=disc.windY/20
            x+=vx
            y+=vy
            vx*=disc.gxy
            vy*=disc.gxy
            xDist,yDist=(x-player.x),(y-player.y)
            dist=(xDist**2+yDist**2)**.5
            yDir=yDist/dist
            xDir=xDist/dist
            if t<150:
                if abs(.5*(tt-t)*(yDir*player.accel*(tt-t)))>=abs(yDist) and \
                abs(.5*(tt-t)**2*xDir*player.accel)>=abs(xDist):
                    xDist2=x-player.x
                    yDist2=y-player.y
                    dist2=(xDist2**2+yDist2**2)**.5
                    return (x+xDist2/dist2*50,y+yDist2/dist2*50)
                startT=player.speed/player.accel
                startGX=.5*(startT)**2*yDir*player.accel
                startGY=.5*(startT)**2*xDir*player.accel
                if (.5*(tt-startT)*yDir*player.speed+startGY>=yDist and
                .5*(tt-startT)*xDir*player.speed+startGX):
                    xDist2=x-player.x
                    yDist2=y-player.y
                    dist2=(xDist2**2+yDist2**2)**.5
                    return (x+xDist2/dist2*50,y+yDist2/dist2*50)
            t-=1
        return (None,None)
        
    
    def leftMouse(self,x,y):
        if self.playing ==True:
            if self.userOffense==True:
                n,w=0,0
                r=False
                for player in self.offense:
                    w+=1
                    if player.select==True:
                        r=True
                        self.temp=player
                    if (x<=player.x+player.radius and x>=player.x-player.radius and 
                    y<=player.y+player.radius and y>=player.y-player.radius):
                        player.select=True
                        self.path=[]
                    else:
                        n+=1
                        player.select=False
                for player in self.offense:
                    if player.select==True:
                        self.offense.remove(player)
                        self.runPlayer=player
                        self.offense.add(player)
        
                if r==True and w-n==0:
                    self.temp.select=True
                    if x>self.bounds[0][0] and x<self.bounds[0][0]+self.bounds[1][0] and y>self.bounds[0][1] and \
                    y<self.bounds[0][1]+self.bounds[1][1]:
                        if len(self.path)==0:
                            self.path+=[[self.temp.x,self.temp.y],[x,y]]
                        else:
                            self.path+=[[x,y]]
            else:
                n,w=0,0
                r=False
                for player in self.defense:
                    w+=1
                    if player.select==True:
                        r=True
                        self.dtemp=player
                    if (x<=player.x+player.radius and x>=player.x-player.radius and 
                    y<=player.y+player.radius and y>=player.y-player.radius):
                        player.select=True
                        self.dpath=[]
                    else:
                        n+=1
                        player.select=False
                for player in self.defense:
                    if player.select==True:
                        self.defense.remove(player)
                        self.drunPlayer=player
                        self.defense.add(player)
        
                if r==True and w-n==0:
                    self.dtemp.select=True
                    if x>self.bounds[0][0] and x<self.bounds[0][0]+self.bounds[1][0] and y>self.bounds[0][1] and \
                    y<self.bounds[0][1]+self.bounds[1][1]:
                        if len(self.dpath)==0:
                            self.dpath+=[[self.dtemp.x,self.dtemp.y],[x,y]]
                        else:
                            self.dpath+=[[x,y]]
                
    def keyHelper(self,key):
        x,y=0,0
        if key(pygame.K_w):
            y-=1

        if key(pygame.K_a):
            x-=1

        if key(pygame.K_s):
            y+=1
            
        if key(pygame.K_d):
            x+=1
        return (x,y)
    
    def mousePressed(self, x, y):
        if self.playing==True and self.throwing==True:
            # impliment if multiple players can move at once
            '''if self.userOffense==True:
                if x>self.forceSide[0] and x<self.forceSide[0]+self.forceSide[2]:
                    if y>self.forceSide[1] and y<self.forceSide[1]+self.forceSide[3]:
                        n=0
                        for player in self.onList:
                            if player.x>self.forceSide[0] and player.x<self.forceSide[0]+self.forceSide[2] and\
                            player.y>self.forceSide[1] and player.y<self.forceSide[1]+self.forceSide[3]:
                                player1=self.dList[n]
                                break
                            n+=1
                    elif y>self.breakSide[1] and y<self.breakSide[1]+self.breakSide[3]:
                        n=0
                        for player in self.onList:
                            if player.x>self.forceSide[0] and player.x<self.forceSide[0]+self.forceSide[2] and\
                            player.y>self.breakSide[1] and player.y<self.breakSide[1]+self.breakSide[3]:
                                player1=self.dList[n]
                                break
                            n+=1
                elif x>self.deepSpace[0] and x<self.deepSpace[0]+self.deepSpace[2] and \
                y>self.deepSpace[1] and y<self.deepSpace[1]+self.deepSpace[3]:
                    n=0
                    for player in self.onList:
                        if player.x>self.deepSpace[0] and player.x<self.deepSpace[0]+self.deepSpace[2] and \
                        player.y>self.deepSpace[1] and player.y<self.deepSpace[1]+self.deepSpace[3]:
                            player1=self.dList[n]
                            break
                        n+=1
                try: 
                    self.interceptD=player1
                    self.interceptP=player
                except:
                    lilDis=1000
                    n=0
                    for player in self.onList:
                        if ((x-player.x)**2+(y-player.y)**2)**.5<lilDis:
                            lilDis=((x-player.x)**2+(y-player.y)**2)**.5
                            self.interceptP=player
                            self.interceptD=self.dList[n]
                        n+=1
            else:'''
            # the player that has a path intercepts the disc
            if len(self.path)>1:
                self.interceptP=self.runPlayer
                n=0
                for player in self.onList:
                    if player==self.runPlayer:
                        self.interceptD=self.dList[n]
                    n+=1
            # if there is no path then the closest player intercepts the disc
            else:
                lilDis=1000
                n=0
                for player in self.onList:
                    if ((x-player.x)**2+(y-player.y)**2)**.5<lilDis:
                        lilDis=((x-player.x)**2+(y-player.y)**2)**.5
                        self.interceptP=player
                        self.interceptD=self.dList[n]
                    n+=1
            
            self.tempPlayer.vx=0
            self.tempPlayer.vy=0
            self.offense.add(self.tempPlayer)
            for throw in self.thrower:
                xDif=random.randint(0,abs(int(throw.throwX*(1-self.tempPlayer.thorws))))
                yDif=random.randint(0,abs(int(throw.throwY*(1-self.tempPlayer.thorws))))
                if random.randint(0,1)==1:xDif*=-1
                if random.randint(0,1)==1:yDif*=-1
                xDist=throw.throwX+xDif
                yDist=throw.throwY+yDif
            if xDist>0: x=10
            else: x=-10
            if yDist>0: y=10
            else: y=-10
            disc=Disc(self.tempPlayer.x+x,self.tempPlayer.y+y,3,xDist,yDist,self.windX,self.windY)
            self.disc.add(disc)
            self.thrower.remove()
            self.throwing=False
            self.intercepting=True
            
            
                
                
        elif self.opening==True:
            if x>self.playBotton[0][0] and x<self.playBotton[0][0]+self.playBotton[1][0]:
                if y>self.playBotton[0][1] and y<self.playBotton[0][1]+self.playBotton[1][1]:
                    self.opening=False
                    self.selecting=True
                elif y>self.instBotton[0][1] and y<self.instBotton[0][1]+self.instBotton[1][1]:
                    self.opening=False
                    self.instructions=True
                
        elif self.instructions==True or self.loose==True or self.win==True:
            if x>self.ratio*5 and x<self.ratio*25 and y>self.ratio*5 and y<self.ratio*15:
                print ("works!")
                self.instructions=False
                self.win=False
                self.loose=False
                self.opening=True 
                self.team1score=0
                self.team2score=0
                
        elif self.selecting==True:
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
                    self.team1Color=self.user.color
                    self.team2Color=self.computer.color
                    self.team1=self.user.name
                    self.team2=self.computer.name
                    self.team1report=self.windFont.render((str(self.team1)+": "+str(self.team1score)),
                    False,(self.team1Color))
                    self.team2report=self.windFont.render((str(self.team2)+": "+str(self.team1score)),
                    False,(self.team2Color))
                    self.spawn()
                    self.selecting=False
                    self.playing=True 
                    
                
            elif self.cSelect==True:
                if (x>self.width/10 and x<self.width/10+self.width/6 and y>self.height*17/20 and \
                y<self.height*17/20+2*self.height/20 and self.cSelect==True):
                    self.uConfirmed=False 
                    self.uSelect==True
                    self.cSelect=False 
                
def main():
    game = Field(1000,600)
    game.run()

if __name__ == '__main__':
    main()
    