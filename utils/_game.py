import pygame 
import random
from utils._utils              import stopTimer
from scenes.title              import *

from levels.MAP_CREATOR        import *
from levels.LOAD_MAP_DATA      import *
from levels.level_ruralAssault import *
from units.player              import *

from oldLevels.mapMaker           import *
from oldLevels.old_levelOne       import *
from oldLevels.old_levelTwo       import *
from oldLevels.old_levelThree     import *
from oldLevels.old_levelFour      import *
from oldLevels.old_levelFive      import *
from oldLevels.old_iceWorld       import *
from oldLevels.old_smallWorld     import *


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
        self.activeLevel          = None


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
        self.activeAnimatedData   = []
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

        self.levelMenuIndex      = 0

     

    def coordinateGame(self,gui):

        self.newLevels         = ['Rural Assault', 'sandbox']
        self.chosenLevels      = self.newLevels + ['osmallWorld', 'olv5','olv4','olv3','olv2','olv1','oiceWorld']


        if(self.state == 'intro'):
            self.introScene.mainMenu_and_startup(gui,self)

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


        # -----------LOAD GAME


        if(self.state == 'start'):

            self.levelSelectMenu(gui)

            


            # ---RUN THE ACTUAL LEVEL 

            if(self.levelSelectMode==False):

                if(self.activeLevel==None):

                    if(self.selectedLevel in self.newLevels):
                        self.chosenMapPath = self.mapPaths + self.selectedLevel + '.txt'
                        self.loadMapData(gui,self)
                        




                    if(self.selectedLevel=='Rural Assault'):
                        self.activeLevel             = ruralAssault(gui,self)
                    if(self.selectedLevel=='sandbox'):
                        self.activeLevel             = sandbox(gui,self)


                    # OLD LEVELS
                    elif(self.selectedLevel=='olv1'):
                        self.activeLevel             = old_levelOne(gui,self,'state/old/' + 'olv1.pkl')
                    elif(self.selectedLevel=='olv2'):
                        self.activeLevel             = old_levelTwo(gui,self,'state/old/' + 'olv2.pkl')
                    elif(self.selectedLevel=='olv3'):
                        self.activeLevel           = old_levelThree(gui,self,'state/old/' + 'olv3.pkl')
                    elif(self.selectedLevel=='olv4'):
                        self.activeLevel            = old_levelFour(gui,self,'state/old/' + 'olv4.pkl')
                    elif(self.selectedLevel=='olv5'):
                        self.activeLevel            = old_levelFive(gui,self,'state/old/' + 'olv5.pkl')
                    elif(self.selectedLevel=='oiceWorld'):
                        self.activeLevel             = old_iceWorld(gui,self,'state/old/' + 'oiceWorld.pkl')
                    elif(self.selectedLevel=='osmallWorld'):
                        self.activeLevel           = old_smallWorld(gui,self,'state/old/' + 'osmallWorld.pkl')


                self.activeLevel.run(gui,self)




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

                raw_map_data,map_l2_data,animated_data,map_enemy_data,spawn_zones,quadrants = loadUnconverted(loadPath+f)
                game.rawL1Data         = raw_map_data
                game.rawL2Data         = map_l2_data
                game.rawAnimData       = animated_data
                game.rawEnemyData      = map_enemy_data
                game.rawSpawnData      = spawn_zones
                game.rawQuadrantData   = quadrants
                
                self.chosenMapName = f.replace('.txt','')
                self.chosenMapPath = self.mapPaths + self.chosenMapName + '.txt'
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






    def levelSelectMenu(self,gui):
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

            # SET LEVEL FONT
            chosenFont = gui.smallFont
            borderColour=(60,60,200)
            tw,th   = getTextWidth(chosenFont,'A menu item yep sure.'),getTextHeight(chosenFont,'A menu item yep sure.')


            # MANAGE DPAD CONTROL OF BUTTONS 
            buttonColourList = []
            for x in self.chosenLevels:
                buttonColourList.append((0,0,0))

            if(gui.input.returnedKey.upper()=='S'): self.levelMenuIndex  +=1
            if(gui.input.returnedKey.upper()=='W'): self.levelMenuIndex  -=1
            if(self.levelMenuIndex<0): self.levelMenuIndex = len(buttonColourList) -1
            if(self.levelMenuIndex>len(buttonColourList)-1): self.levelMenuIndex = 0
            backColour                   = buttonColourList
            backColour[self.levelMenuIndex] = darken(borderColour,darkenAmount=60)

            # GET LEVELS AVAILABLE
            buttonY = 300
            for l in range(len(self.chosenLevels)):
                level = self.chosenLevels[l]
                
                # MOUSE CLICK SELECTION OF LEVEL

                chosenFile,tex,tey  = simpleButton(0.5*(gui.w-tw),buttonY,level,gui,chosenFont,setTw=tw,backColour=backColour[l],borderColour=borderColour, textColour=(255,255,255))
                
                buttonY += 1.5*th
                # IF FILE SELECTED LOAD FILE 
                if(chosenFile):
                    self.selectedLevel = level
                    self.levelSelectMode   = False
                    
            # BUTTON SELECTION OF LEVEL 
            if(gui.input.returnedKey=='return'):
                self.selectedLevel        = self.chosenLevels[self.levelMenuIndex]
                self.levelSelectMode      = False
                gui.input.returnedKey     = ''


            # GO BACK
            tw,th             = getTextWidth(chosenFont,'A menu item.'),getTextHeight(chosenFont,'A menu item.')
            back,tex,tey      = simpleButton(100,0.93*gui.h,'Back',gui,chosenFont,setTw=tw,backColour=(0,0,0),borderColour=borderColour, textColour=(255,255,255))
            if(back):
                self.introScene.state = 'intro'
                self.state            = 'intro'

    
    
    def loadMapData(self,gui,parent):
        raw_map_data,map_l2_data,animated_data,map_enemy_data,spawn_zones,quadrants               = loadUnconverted(parent.chosenMapPath)
        parent.rawL1Data       = raw_map_data
        parent.rawL2Data       = map_l2_data
        parent.rawAnimData     = animated_data
        parent.rawEnemyData    = map_enemy_data
        parent.rawSpawnData    = spawn_zones
        parent.rawQuadrantData = quadrants



        # This is the data that matters
        parent.tileReferenceData,parent.activeL1Data                          = loadMapRefData(gui,parent)
        parent.layer2RefData, parent.activeL2Data,parent.layer2RefDataScaled  = loadLayer2RefData(gui,parent)
        parent.animatedRefData, parent.activeAnimatedData                     = loadAnimatedData(gui,parent)
        parent.enemyRefData,parent.activeEnemyData                            = loadEnemyRefData(gui,parent)
        parent.activeSpawnZones                                               = loadSpawnZones(gui,parent)
        parent.activeQuadrants                                                = loadQuadrants(gui,parent)

        parent.sampleTile                 = parent.activeL1Data[1][2] # A tile representative of the height/width
        parent.tileWidth                  = parent.sampleTile.get_width()
        parent.tileHeight                 = parent.sampleTile.get_height()
        parent.mapWidth, parent.mapHeight = len(parent.activeL1Data[0])  * parent.tileWidth ,len(parent.activeL1Data) * parent.tileHeight




               