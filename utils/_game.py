import pygame 
import random
from utils._utils          import stopTimer
from scenes.title          import *
from levels.mapMaker       import *
from levels.MAP_CREATOR    import *
from levels.LOAD_MAP_DATA  import *
from units.player          import *
from levels.levelOne       import *
from levels.levelTwo       import *
from levels.levelThree     import *
from levels.levelFour      import *
from levels.levelFive      import *
from levels.iceWorld       import *
from levels.smallWorld     import *

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
        self.levelSelectMode          = True
        self.selectedLevel        = 'levelOne'


        #------------SCENES
        self.introScene           = introScreen(gui)
        self.mapEditor            = mapEditor(gui,self)

        # ------------LEVEL INIT
        
        self.levelsInitialised    = False
        self.loadingFail          = False
        self.leveltoLoad          = 0
        self.levelLoadComplete    = False
        self.levelScreenMask      = pygame.Surface((gui.w,gui.h))
        self.alphaI               = 100


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


        self.maxRecordedSpeed       = 0




        # -----MAP ITEMS

        self.mapCreator           = mapCreator(gui)
        self.mapSelection         = None
        self.chosenMapName        = None
        self.chosenMapPath        = None
        self.activeL1Data         = [] # LOADED BY LOAD_MAP_DATA
        self.activeL2Data         = []
        self.activeEnemyData      = []
        self.rawL1Data            = []
        self.rawL2Data            = []
        self.rawEnemyData         = []

        # -----TIME

        self.speedTimer            = stopTimer()
        self.stopTimer2            = stopTimer()
        self.stopTimer3            = stopTimer()

        # -------PATH
        self.basePath              = IMAGEASSETPATH

        #--------VISUALS

        self.dynamicBorder        = dynamicBorder(borderColour=(60,60,200),noShadeShifts=10)
        self.buttonIndex          = 0

    def initLevels(self,gui):
        
        # ----------IN GAME
        mandatoryLevels      = ['lv1','lv2','lv3','lv4','lv5','iceWorld','smallWorld']

        if(self.leveltoLoad<=len(mandatoryLevels)-1):
            level = mandatoryLevels[self.leveltoLoad]
            
            if(self.loadingFail ==False):
                try:
                    print("Attempting to load Level : " + str(level))
                    sampleLevel=load_pickle('state/' + str(level) +'.pkl')
                except:
                    print('Load failed')
                    self.loadingFail = True

                if(self.loadingFail == False):
                    print(str(level) + ' : LOADED')
                    if(self.leveltoLoad==len(mandatoryLevels)-1):
                        self.levelLoadComplete = True
                        print('COMPLETE')
                    else:
                        self.leveltoLoad +=1
                        print("Incrementing to next level")


            # CREATE NEW MAP IF FAILED
            if(self.loadingFail):
                complete = self.mapEditor.createNewMap(gui,self,externallyCalled=True,specifiedName=level)
                if(complete):
                    self.loadingFail = False
            
        if(self.levelLoadComplete):
            self.levelOne             = levelOne(gui,self)
            self.levelTwo             = levelTwo(gui,self)
            self.levelThree           = levelThree(gui,self)
            self.levelFour            = levelFour(gui,self)
            self.levelFive            = levelFive(gui,self)
            self.iceWorld             = iceWorld(gui,self)
            self.smallWorld           = smallWorld(gui,self)
            
            self.levelsInitialised    = True
                    

    def coordinateGame(self,gui):

        if(self.state == 'intro'):
            self.introScene.showstartup(gui,self)

        if(self.state == 'editor'):
            self.mapEditor.run(gui,self)

        #------------MAP EDITOR

        if(self.state=='newMapEditor'):

            if(self.mapSelection=='loadMap'):
                self.loadMapMenu(gui,self)

            elif(self.mapSelection=='newMap'):
                self.mapCreator.createMap(gui,self)

            elif(self.mapSelection=='editMap'):
                self.mapCreator.editMap(gui,self)
            else:
                self.mapMenu(gui,self)



        if(self.state == 'start'):
            if(self.levelsInitialised==False):
                self.initLevels(gui)
                return()
            
            # ---RUN THE ACTUAL LEVEL 

            if(self.levelSelectMode==False):

                if(self.selectedLevel=='levelOne'):
                    self.levelOne.run(gui,self)
                elif(self.selectedLevel=='levelTwo'):
                    self.levelTwo.run(gui,self)
                elif(self.selectedLevel=='levelThree'):
                    self.levelThree.run(gui,self)
                elif(self.selectedLevel=='levelFour'):
                    self.levelFour.run(gui,self)
                elif(self.selectedLevel=='levelFive'):
                    self.levelFive.run(gui,self)
                elif(self.selectedLevel=='iceWorld'):
                    self.iceWorld.run(gui,self)
                elif(self.selectedLevel=='smallWorld'):
                    self.smallWorld.run(gui,self)




            # ----CHOSE A LEVEL 
            
            if(self.levelSelectMode):

                # DRAW COVER PICTURE

                drawImage(gui.screen,gui.cover3,(0.5*(gui.w-gui.cover1.get_width()),0.44*(gui.h-gui.cover1.get_height())))
                self.levelScreenMask.set_alpha(self.alphaI)
                self.levelScreenMask.fill((0,0,0))
                gui.screen.blit(self.levelScreenMask,(0,0))

                # DRAW TITLE
                
                chosenFont = gui.largeFont
                borderColour=(60,60,200)
                tw,th   = getTextWidth(chosenFont,'A menu item yep sure.'),getTextHeight(chosenFont,'A menu item yep sure.')
                drawText(gui,gui.bigFont,'Select Level',0.52*(gui.w-tw),0.03*gui.h, colour=(100, 100, 255))

                # GET LEVELS AVAILABLE
                loadPath       = 'state/'
                availableFiles = os.listdir(loadPath)
                availableFiles = [x for x in availableFiles if x[-4:]=='.pkl']
                chosenFont = gui.smallFont
                borderColour=(60,60,200)
                tw,th   = getTextWidth(chosenFont,'A menu item yep sure.'),getTextHeight(chosenFont,'A menu item yep sure.')

                buttonY = 300
                for f in availableFiles:
                    
                    backColour =(0,0,0)
                    if(f[:-4] =='iceWorld'):
                        backColour =(250,20,20)

                    chosenFile,tex,tey  = simpleButton(0.5*(gui.w-tw),buttonY,f,gui,chosenFont,setTw=tw,backColour=backColour,borderColour=borderColour, textColour=(255,255,255))
                    
                    buttonY += 1.5*th
                    # IF FILE SELECTED LOAD FILE 
                    if(chosenFile):
                        if(f[:-4] =='lv1'):
                            self.selectedLevel = 'levelOne'
                            self.levelSelectMode   = False
                        if(f[:-4] =='lv2'):
                            self.selectedLevel = 'levelTwo'
                            self.levelSelectMode   = False
                        if(f[:-4] =='lv3'):
                            self.selectedLevel = 'levelThree'
                            self.levelSelectMode   = False
                        if(f[:-4] =='lv4'):
                            self.selectedLevel = 'levelFour'
                            self.levelSelectMode   = False
                        if(f[:-4] =='lv5'):
                            self.selectedLevel = 'levelFive'
                            self.levelSelectMode   = False
                        if(f[:-4] =='iceWorld'):
                            #self.selectedLevel = 'iceWorld'
                            #self.levelSelectMode   = False
                            pass
                        if(f[:-4] =='smallWorld'):
                            self.selectedLevel = 'smallWorld'
                            self.levelSelectMode   = False
                        


                tw,th             = getTextWidth(chosenFont,'A menu item.'),getTextHeight(chosenFont,'A menu item.')
                back,tex,tey      = simpleButton(100,0.93*gui.h,'Back',gui,chosenFont,setTw=tw,backColour=(0,0,0),borderColour=borderColour, textColour=(255,255,255))
                if(back):
                    self.introScene.state = 'intro'
                    self.state            = 'intro'  

    def mapMenu(self,gui,game):
        
        # DRAW BACKGROUND PIC
        drawImage(gui.screen,gui.madge,[0,0])

        # DRAWS BORDER 
        self.dynamicBorder.animateBorder('menu border',game,gui)

        self.levelScreenMask.set_alpha(self.alphaI)
        self.levelScreenMask.fill((0,0,0))
        gui.screen.blit(self.levelScreenMask,(0,0))

        # GET TEXT VALUES
        chosenFont = gui.largeFont
        borderColour=(60,60,200)
        
        tw,th   = getTextWidth(chosenFont,'A menu item yep sure.'),getTextHeight(chosenFont,'A menu item yep sure.')


        # MANAGE DPAD CONTROL OF BUTTONS 
        buttonColourList = [(0,0,0),(0,0,0)]
        if(gui.input.returnedKey.upper()=='S'): self.buttonIndex  +=1
        if(gui.input.returnedKey.upper()=='W'): self.buttonIndex  -=1
        if(self.buttonIndex<0): self.buttonIndex = len(buttonColourList) -1
        if(self.buttonIndex>len(buttonColourList)-1): self.buttonIndex = 0
        backColour                   = buttonColourList
        backColour[self.buttonIndex] = borderColour



        newMap,tex,tey      = simpleButton(0.15*(gui.w-tw),0.4*gui.h,'New Map',gui,chosenFont,setTw=tw,backColour=backColour[0],borderColour=borderColour, textColour=(255,255,255))

        loadMap,tex,tey     = simpleButton(0.15*(gui.w-tw),tey + 0.8*th,'Load Map',gui,chosenFont,setTw=tw,backColour=backColour[1],borderColour=borderColour, textColour=(255,255,255))

        # KEY SELECTION 
        if(gui.input.returnedKey=='return'):
            newMap = 0==self.buttonIndex
            loadMap = 1==self.buttonIndex
            gui.input.returnedKey       = ''
        
        if(newMap):
            self.mapSelection = 'newMap'
            self.buttonIndex = 0
        if(loadMap):
            self.mapSelection = 'loadMap'
            self.buttonIndex = 0

    def loadMapMenu(self,gui,game):
        borderColour = (153, 204, 255)
        backColour   = (51, 102, 255)
        textColour   = (255,255,255)

        gui.screen.fill((51, 51, 153))
        drawImage(gui.screen,gui.sarah,[0,0])
        
        self.levelScreenMask.set_alpha(self.alphaI)
        self.levelScreenMask.fill((0,0,0))
        gui.screen.blit(self.levelScreenMask,(0,0))

        # ------GET LOADED MAPS 
        loadPath       = game.mapPaths
        availableFiles = os.listdir(loadPath)
        availableFiles = [x for x in availableFiles if x[-4:]=='.txt']
        
        # ------TEXT VALUES
        chosenFont = gui.smallFont
        tw,th   = getTextWidth(chosenFont,'A menu item yep sure.'),getTextHeight(chosenFont,'A menu item yep sure.')

        drawTextWithBackground(gui.screen,gui.bigFont,"Select a Map",0.15*gui.w,80,setWidth=2*tw,setHeight=2*th, textColour=textColour,backColour= backColour,borderColour=borderColour)

        # ------DRAW LOAD OPTION FOR EACH MAP 

        buttonY = 300
        xOption = 0.15*gui.w

        for f in availableFiles:
            chosenFile,tex,tey  = simpleButton(xOption,buttonY,f,gui,chosenFont,setTw=tw,backColour=backColour,borderColour=borderColour, textColour=textColour)
            hoverered, ttx,tty  = drawText(gui,gui.smallFont, 'Delete',tex+10,buttonY+10, colour=(0,200,0),center=False,pos=[gui.mx,gui.my])
            
            buttonY += 1.5*th
            
            # IF FILE SELECTED LOAD FILE 
            
            if(chosenFile):

                raw_map_data,map_l2_data,map_enemy_data,spawn_zones = loadUnconverted(loadPath+f)
                game.rawL1Data         = raw_map_data
                game.rawL2Data         = map_l2_data
                game.rawSpawnData      = spawn_zones
                
                self.chosenMapName = f.replace('.txt','')
                self.chosenMapPath = game.mapPaths + self.chosenMapName + '.txt'
                self.mapSelection = 'editMap'
                break

            # IF DELETE
            if(hoverered and gui.clicked):
                os.remove(loadPath + f)

        tw,th   = getTextWidth(chosenFont,'A menu item.'),getTextHeight(chosenFont,'A menu item.')
        back,tex,tey      = simpleButton(gui.w-300,0.93*gui.h,'Back',gui,chosenFont,setTw=tw,backColour=backColour,borderColour=borderColour, textColour=textColour)
        if(back):
            print('going to intro')
            self.mapSelection = ''
            self.introScene.state = 'intro'
            self.state            = 'intro'  


            


    def calculatePlayerSpeed(self,player):
        # CALCULATING PLAYER SPEED
        printSpeed    = self.speedTimer.stopWatch(1, 'playerSpeed calculator', 'player speed', self,silence=True)
        if(printSpeed):
            speed = player.cumulatedDistance/1
            if(speed>self.maxRecordedSpeed): self.maxRecordedSpeed = speed
            print('Player speed is ' + str(speed))
            print('Max speed is ' + str(self.maxRecordedSpeed))
            print('')
            self.speedTimer.reset()
            player.cumulatedDistance=0






