import pygame 
import random
from utils._utils import stopTimer
from scenes.title import *
from scenes.mapMaker import *
from units.player import *
from levelOne import *

"""
GAME OBJECT STORES SAVE STATE
AND ALL USER STATS

FUNCTIONS FOR PROCESSING PYGAME LOOP
FUNCTIONS FOR PROCESSING NEXT DAY
"""




class gameObject():

    def __init__(self,IMAGEASSETPATH,gui):

        #---------STATES
        
        self.state                = 'intro'  
        self.FPS                  = 90
        self.eventState           = None
        self.running              = True
        self.itercount            = 0
        self.elapsed              = 0  
        self.dt                   = 0



        # ----------IN GAME 
        self.levelOne             = levelOne(gui)


        self.player               = player(gui)

        #------------SCENES
        self.introScene           = introScreen(gui)
        self.mapEditor            = mapEditor(gui,self)


        # ---------USER STATS

        self.userName               = "Straker"
        self.level                  = 1
        self.status                 = "Rookie"
        self.money                  = 25.60
        self.xp                     = 250
        self.items                  = [('cigs',4),('old condom',1),('rusty spanner',1),('cough medicine',1)]
        self.ranks                  = ['Rookie','Junior','Generalist','Specialist','Squadron Leader','Drone Commander']
        self.levelThresholds        = [99,299,499,699,899,1999,2999,3999,5000]
        self.nextXpThresholdIndex   = 0
        self.levelUp                = False



        # -----TIME

        self.stopTimer             = stopTimer()
        self.stopTimer2            = stopTimer()
        self.stopTimer3            = stopTimer()

        # -------PATH
        self.basePath              = IMAGEASSETPATH

 
                

    def coordinateGame(self,gui):

        if(self.state == 'intro'):
            self.introScene.showstartup(gui,self)

        if(self.state == 'editor'):
            self.mapEditor.run(gui,self)

        if(self.state == 'start'):
            self.levelOne.run(gui,self)


