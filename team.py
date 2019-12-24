import pygame
import os
import string

class Team(object):
    def __init__(self,team):
        self.name=team
        self.pic="Teams\\"+str(team)+"\\picture.png"
        tAbout=readFile("Teams\\"+str(team)+"\\About.txt")
        tRoster=readFile("Teams\\"+str(team)+"\\Roster.txt")
        self.about=[]
        temp=[]
        for line in tAbout.splitlines():
            if "Color" in line:
                for num in line.split(","):
                    temp1=""
                    for char in num:
                        if char.isdigit():
                            temp1+=char
                    temp+=[temp1]
                self.color=(int(temp[0]),int(temp[1]),int(temp[2]))
            else:
                self.about +=[line]
                
        Roster=dict()
        for line in tRoster.splitlines():
            n=""
            lst=[]
            for element in line.split(","):
                if n=="":
                    n=element
                else:
                    lst+=[float(element)]
            Roster[n]=lst
        self.roster=Roster
        print (self.name,self.roster)
            
            
        
# taken from 112 website
def readFile(path):
    with open(path, "rt") as f:
        return f.read()