from utils._utils import *
from utils._utils import stopTimer
from utils.gameUtils import *
from levels.LOAD_MAP_DATA import *
import random
import math

"""
TODO:

L2: TILELESS
ENEMY PLACEMENT
SPAWN ZONE SELECT
BOX SELECT:




"""

class mapCreator():
    def __init__(self,gui):
        self.textState  = None
        self.fadeState  = None
        self.timer      = stopTimer()
        self.timer2     = stopTimer()
        self.timer3     = stopTimer()
        self.saveTimer  = stopTimer()
        self.loadTimer  = stopTimer()
        self.introY     = None

        # MASK
        self.levelScreenMask      = pygame.Surface((gui.w,gui.h))
        self.alphaI               = 100

        self.dynamicBorder        = dynamicBorder(borderColour=(60,60,200),noShadeShifts=10)

        # alpha overlay
        self.alphaI               = 100      # used on fade out (goes up to 255)
        self.fadeSurface          = pygame.Surface((gui.w,gui.h))

        self.transMaskAlpha   = 100
        self.transMask        = pygame.Surface((0.16*gui.w, 0.18*gui.h))

        # ----drag selector
        self.dragSelect             = dragSelectorScrollable()


        # ----create map variables

        self.initMapQuestions   = True
        self.questionCursor     = 0
        self.questionsComplete  = False
        self.chosenGameMap      = None
        self.answerList         = []



        # EDITOR


        self.mapLoaded          = False
        self.multiSelect        = False
        self.boxCoords          = []
        self.boxSelect          = False

        self.saving             = False
        self.savegame           = False
        self.saves              = 0
        self.loadGame           = False
        self.loading            = False
        self.loads              = 0


        self.toggleWindow       = True
        self.check              = False

        self.tileCursor         = 0
        self.updateTileEnabled   = True
        self.currentLayer        = 'S'


        self.tileReferenceData   = None
        self.selectedTileKey    = 'template'
        self.selectedTileSubKey = 'base100_1'
        
        self.layer2RefData       = None
        self.selectedL2Key      = 'objectTiles'
        self.selectedL2SubKey   = 'obj1'
        self.layer2RefDataScaled = None

        self.animatedRefData        = None
        self.selectedAnimKey        = 'conveyor'
        self.currentAnimRotation    = 0
        
        self.enemyRefData        = None
        self.selectedEnemyKey    = 'air' 
        self.selectedEnemySubKey = 'scout'
        self.enemySelectionState = 'notSelected'
        self.enemyToPlace        = {}
        self.patrolCoords        = []

        self.currentEnemyRotation   = 0
        self.currentObjectiveCursor = None
        self.navEnabled             = True

        self.bonusSpawnTypes = ["None","PowerUp","Missiles","HealthUp"]
        self.bonusSpawn     = 'None'




    def createMap(self,gui,game):
        
        self.dynamicBorder.animateBorder('menu border',game,gui)


        # ASK QUESTIONS ABOUT NEW MAP 
        questionList = ['Name of Map file', 'Map Width', 'Map Height', 'Tile Size']
        sampleAnsers = ['rumble map','30','50','69']
        if(self.initMapQuestions):
            game.input.enteredString = sampleAnsers[self.questionCursor]
            self.initMapQuestions = False


        # QUESTIONS REGARDING MAP DIMENSIONS AND SIZES 
        if(self.questionCursor < len(questionList) and self.questionsComplete==False):
            # ---- display the question 
            drawText(gui,gui.font,questionList[self.questionCursor],500,300, colour=(100, 100, 255))
            game.input.drawTextInputSingleLine(game.input.enteredString,500,400,gui,boxBorder=(50,50,200),boxFill=(0,0,0) ,colour=(80,80,255))
            returnvalue = game.input.processInput()
            
            if(game.input.returnedKey=='ENTER'):
                self.answerList.append(game.input.enteredString)
                self.questionCursor +=1
                game.input.enteredString = ''
                if(self.questionCursor >= len(questionList)):
                    self.questionsComplete = True
                else:
                    game.input.enteredString = sampleAnsers[self.questionCursor]

        
        # CREATE MAP OBJECT 

        if(self.questionsComplete and self.chosenGameMap==None):
            gameMap = {"name": self.answerList[0],
                       "cols": math.floor(int(self.answerList[1])/50),
                       "rows":math.floor(int(self.answerList[2])/50),
                       "tileDims": int(self.answerList[3])
                       }


            # CHOSEN MAP VALUES
            print("CHOSEN MAP VALUES:")
            print(gameMap)


            print("Creating base map....")
            mapfile = '*L1\n'
            odd = True
            for r in range(gameMap['rows']):
                for c in range(gameMap['cols']):
                    if(odd):
                        mapfile += 'template/base100_1,'
                    else:
                        mapfile += 'template/base100_9,'

                mapfile += '\n'

            mapfile += '*L1\n'
            print("Complete\n")

            print("ADDING L2 placeholder ....")
            mapfile += '*L2\n'
            mapfile += '*L2\n'

            print("ADDING ANIMATION placeholder ....")
            mapfile += '*ANIMATED\n'
            mapfile += '*ANIMATED\n'

            print("ADDING ENEMY placeholder ....")
            mapfile += '*ENEMY\n'
            mapfile += '*ENEMY\n'

            print("ADDING SPAWN placeholder ....")
            mapfile += '*SPAWN\n'
            mapfile += '*SPAWN\n'

            print("ADDING QUADRANT placeholder ....")
            mapfile += '*QUADRANT\n'
            mapfile += '*QUADRANT\n'

            print("Mapfile looks like this")
            print(mapfile)





            print("Saving....")
            loadPath       = game.mapPaths
            f = open(loadPath + gameMap['name'] + '.txt','w')
            f.write(mapfile[:-1])

            game.chosenMapName = gameMap['name']
            self.chosenMapPath = game.mapPaths + game.chosenMapName + '.txt'
            game.mapSelection  ='editMap'  # will prevent this being recalled


            # -------NUMBER OF ROWS CALCULATED 
            # --- reset
            self.initMapQuestions   = True
            self.questionCursor     = 0
            self.questionsComplete  = False
            self.chosenGameMap      = None
            self.answerList         = []









    def editMap(self,gui,game):

        #----------------------------SKIRMISH SETUP

        if(self.mapLoaded==False):
            print("LOADING MAP")
            self.chosenMapPath = game.chosenMapPath
            self.chosenMapName = game.chosenMapName
            game.loadMapData(gui,self)
            self.loadLevelData(gui,game)

            self.mapLoaded = True

        #---------------------------CAMERA AND SIZING

        hoveredTile = self.tileReferenceData[self.selectedTileKey][self.selectedTileSubKey]


        startX,startY= 0,0
        gui.moveCamera(game)
        if(self.navEnabled):
            self.nav(gui,game)


        # These get overriden by any layer below
        gui.scrollEnabled      = True
        sampleTile             = self.sampleTile

        #----------------------------MAP RENDERING

        self.renderLayer1Map(gui,game,hoveredTile)
        self.setQuadrants(gui,game)
        self.spawnZones(gui,game)
        self.renderLayer2Map(gui,game,startX,startY)
        self.renderAnimatedObjects(gui,game,startX,startY)
        self.renderEnemyMap(gui,game,startX,startY)

        self.updateTileEnabled = True
        self.showTileListL1(gui,sampleTile)
        self.showTileListL2(gui,sampleTile)
        self.showAnimatedList(gui,game)
        self.showEnemyList(gui,sampleTile)

        self.sideMenu(gui,game,sampleTile)

        self.buttonSelection(gui,game,hoveredTile)

        
        #-------LOAD
        self.loadGameLogic(gui)

        #------------SAVE
        self.saveGameLogic(gui,game)




    def buttonSelection(self,gui,game,hoveredTile):

        #----------------------------MAP OPTIONS
        if(self.currentLayer=='l1'):
            if(gui.input.returnedKey.upper()=='I'):
                self.selectedTileSubKey = get_next_subkey(self.tileReferenceData, self.selectedTileKey, self.selectedTileSubKey)
            if(gui.input.returnedKey.upper()=='K'):
                self.selectedTileSubKey = get_previous_subkey(self.tileReferenceData, self.selectedTileKey, self.selectedTileSubKey)
            if(gui.input.returnedKey.upper()=='L' or gui.input.returnedKey.upper()=='E'):
                self.selectedTileKey = get_next_tile_key(self.tileReferenceData, self.selectedTileKey)
                self.selectedTileSubKey = list(self.tileReferenceData[self.selectedTileKey].keys())[0]
                self.tileCursor =0
            if(gui.input.returnedKey.upper()=='J' or gui.input.returnedKey.upper()=='Q'):
                self.selectedTileKey = get_previous_tile_key(self.tileReferenceData, self.selectedTileKey)
                self.selectedTileSubKey = list(self.tileReferenceData[self.selectedTileKey].keys())[0]
                self.tileCursor =0
        
        if(self.currentLayer=='l2'):
            if(gui.input.returnedKey.upper()=='I'):
                self.selectedL2SubKey = get_next_subkey(self.layer2RefData, self.selectedL2Key, self.selectedL2SubKey)
            if(gui.input.returnedKey.upper()=='K'):
                self.selectedL2SubKey = get_previous_subkey(self.layer2RefData, self.selectedL2Key, self.selectedL2SubKey)
            if(gui.input.returnedKey.upper()=='L' or gui.input.returnedKey.upper()=='E'):
                self.selectedL2Key = get_next_tile_key(self.layer2RefData, self.selectedL2Key)
                self.selectedL2SubKey = list(self.layer2RefData[self.selectedL2Key].keys())[0]
                self.tileCursor =0
            if(gui.input.returnedKey.upper()=='J' or gui.input.returnedKey.upper()=='Q'):
                self.selectedL2Key = get_previous_tile_key(self.layer2RefData, self.selectedL2Key)
                self.selectedL2SubKey = list(self.layer2RefData[self.selectedL2Key].keys())[0]
                self.tileCursor =0

        if(self.currentLayer=='E'):

            if(gui.input.returnedKey.upper()=='L' or gui.input.returnedKey.upper()=='E'):
                self.selectedEnemyKey = get_next_tile_key(self.enemyRefData, self.selectedEnemyKey)
                self.selectedEnemySubKey = list(self.enemyRefData[self.selectedEnemyKey].keys())[0]
                self.tileCursor  =0
            if(gui.input.returnedKey.upper()=='J' or gui.input.returnedKey.upper()=='Q'):
                self.selectedEnemyKey = get_previous_tile_key(self.enemyRefData, self.selectedEnemyKey)
                self.selectedEnemySubKey = list(self.enemyRefData[self.selectedEnemyKey].keys())[0]
                self.tileCursor =0

            if(gui.input.returnedKey.upper()=='I'):
                self.selectedEnemySubKey = get_next_subkey(self.enemyRefData, self.selectedEnemyKey, self.selectedEnemySubKey)
            if(gui.input.returnedKey.upper()=='K'):
                self.selectedEnemySubKey = get_previous_subkey(self.enemyRefData, self.selectedEnemyKey, self.selectedEnemySubKey)




        if(gui.input.returnedKey=='space'):
            self.tileCursor = 0
            if(self.currentLayer=='l1'):
                self.currentLayer = 'l2'
            elif(self.currentLayer=='l2'):
                self.currentLayer = 'A'
            elif(self.currentLayer=='A'):
                self.currentLayer = 'E'
            elif(self.currentLayer=='E'):
                self.currentLayer = 'S'
            elif(self.currentLayer=='S'):
                self.currentLayer = 'Q'
            elif(self.currentLayer=='Q'):
                self.currentLayer = 'l1'


        if(gui.input.returnedKey.upper()=='H'):
            gui.camX = 0
            gui.camY = 0




    def sideMenu(self,gui,game,sampleTile):


        # --------------------------Text Info
        if(self.boxSelect):
            sentence = "Box Selection Enabled"
            setWidth=getTextWidth(gui.font,sentence)
            drawTextWithBackground(gui.screen,gui.font,sentence,0.8*gui.w,0.14*gui.h,setWidth=setWidth ,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))
        else:
            layerInfoRef = {"l1":"Layer 1" ,"l2":"Objects","A":"Animated Objects","E": "Enemy Placement" ,"S":"Set Spawn Zones","Q":"Set Quadrant Zones"}
            sentence = layerInfoRef[self.currentLayer]
            setWidth=getTextWidth(gui.font,sentence)
            drawTextWithBackground(gui.screen,gui.font,sentence,0.8*gui.w,0.14*gui.h,setWidth=setWidth ,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))

        # --------------------------bounding box

        boxX,boxY = 0.8*gui.w, 0.18*gui.h
        boxW,boxH = 0.16*gui.w, 0.18*gui.h
        
        pygame.draw.rect(gui.screen, (180,180,200), [boxX, boxY,boxW, boxH],4)
        self.transMask.set_alpha(self.transMaskAlpha)
        self.transMask.fill((0,0,150))
        gui.screen.blit(self.transMask, (boxX, boxY))

        if(gui.mouseCollides(boxX,boxY,boxW,boxH)):
            gui.scrollEnabled = False  
            self.updateTileEnabled = False

        # -----SAVE MAP
        saveX , saveY = boxX+0.02*gui.w, boxY + 0.02*gui.h
        self.savegame = drawSelectableImage(gui.saveIcon,gui.saveIcon2,[saveX,saveY],gui)
        if(gui.mouseCollides(saveX,saveY,gui.saveIcon.get_width(),gui.saveIcon.get_height())):
            gui.scrollEnabled = False
        
        
        # -----LOAD MAP
        loadX, loadY = boxX+0.06*gui.w, boxY + 0.02*gui.h
        self.loadGame = drawSelectableImage(gui.loadIcon,gui.loadIcon2,[loadX,loadY],gui)
        if(gui.mouseCollides(loadX,loadY,gui.saveIcon.get_width(),gui.saveIcon.get_height())):
            gui.scrollEnabled = False


        # -------TOGGLE TILE
        toggleX, toggleY = boxX+0.02*gui.w, boxY + 0.1*gui.h
        
        if(self.currentLayer=='l1'):
            tile1,tile2 = gui.L1_1,gui.L1_2 
        elif(self.currentLayer=='l2'):
            tile1,tile2 = gui.L2_1,gui.L2_2 
        elif(self.currentLayer=='A'):
            tile1,tile2 = gui.Anim_1,gui.Anim_2 
        elif(self.currentLayer=='E'):
            tile1,tile2 = gui.E_1,gui.E_2 
        elif(self.currentLayer=='S'):
            tile1,tile2 = gui.S_1,gui.S_2
        elif(self.currentLayer=='Q'):
            tile1,tile2 = gui.Q_1,gui.Q_2 

        toggleLayer = drawSelectableImage(tile1,tile2,[toggleX,toggleY],gui)
        if(toggleLayer):
            self.tileCursor = 0
            if(self.currentLayer=='l1'):
                self.currentLayer = 'l2'
            elif(self.currentLayer=='l2'):
                self.currentLayer = 'A'
            elif(self.currentLayer=='A'):
                self.currentLayer = 'E'
            elif(self.currentLayer=='E'):
                self.currentLayer = 'S'
            elif(self.currentLayer=='S'):
                self.currentLayer = 'Q'
            elif(self.currentLayer=='Q'):
                self.currentLayer = 'l1'


        # -------LAYER TOGGLE
        toggleX, toggleY = boxX+0.06*gui.w, boxY + 0.1*gui.h
        toggleWindow = drawSelectableImage(gui.openTileWindow,gui.openTileWindow2,[toggleX,toggleY],gui)
        if(toggleWindow):
            self.toggleWindow = not self.toggleWindow
        

        setWidth=getTextWidth(gui.font,'A menu item yep sure correct.')
        sentence = "Map Size: [" + str(self.mapWidth) + ':' + str(self.mapHeight) +']'
        drawTextWithBackground(gui.screen,gui.font,sentence,50,20,setWidth=setWidth ,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))
        sentence = '(' +str(gui.mx+gui.camX) + ',' + str(gui.my+gui.camY) +')'
        drawTextWithBackground(gui.screen,gui.font,sentence,50,800,setWidth=setWidth ,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))
        

    def showTileListL1(self,gui,sampleTile):

        # TILE/OBJECT WINDOW
        if(self.toggleWindow and self.currentLayer=='l1'):
            windowItemLen = 70
            rows = 3
            cols = int(windowItemLen/rows)
            startX,startY = 0.2*gui.w,0.8*gui.h
            originX,originY  = startX,startY
            tileLen,tileHeight = sampleTile.get_width() ,sampleTile.get_height()
            # self.tileReferenceData is a dict, where the values are lists of filenames that 
            # correspond to a sprite tile
            subkeys = list(self.tileReferenceData[self.selectedTileKey].keys())
            subkeys.reverse()
            tileIndex = self.tileCursor




            for i in range(rows):

                for j in range(cols):

                    # don't draw any more boxes
                    if(tileIndex>=len(subkeys)):
                        break

                    pygame.draw.rect(gui.screen, (80,80,40), [startX, startY,tileLen, tileHeight])
                    
                    if(tileIndex<len(subkeys)):
                        drawImage(gui.screen, self.tileReferenceData[self.selectedTileKey][subkeys[tileIndex]], (startX, startY))

                    # HIGHLIGHT / SELECTED
                    if(gui.mouseCollides(startX,startY,tileLen,tileHeight)):
                        self.updateTileEnabled = False
                        gui.scrollEnabled = False
                        pygame.draw.rect(gui.screen, (180,180,200), [startX, startY,tileLen, tileHeight],4)
                        if(gui.clicked):
                            self.selectedTileSubKey = subkeys[tileIndex]
                    else:
                        pygame.draw.rect(gui.screen, (30,30,200) , [startX, startY,tileLen, tileHeight],4)



                    
                    tileIndex +=1
                    startX+=tileLen-4
                startX = originX
                startY += tileHeight -4

            # -----NEXT TILE TYPE
            nextGroup = drawSelectableImage(gui.smallBase100[4],gui.smallBase100[5],[originX-50,originY],gui)
            if(gui.mouseCollides(originX-50,originY,50,50)):
                gui.scrollEnabled = False
            if(nextGroup):
                self.selectedTileKey = get_next_tile_key(self.tileReferenceData, self.selectedTileKey)
                self.selectedTileSubKey = list(self.tileReferenceData[self.selectedTileKey].keys())[0]
                self.tileCursor =0

            # -----SCROLL TILES 

            nextTile = drawSelectableImage(gui.smallBase100[11],gui.smallBase100[12],[originX-50,originY+50],gui)
            if(gui.mouseCollides(originX-50,originY+50,50,50)):
                gui.scrollEnabled = False
            if(nextTile):
                if(len(subkeys)>tileIndex):
                    self.tileCursor = tileIndex
                elif(self.tileCursor==len(subkeys)-1):
                    self.tileCursor = 0
                else:
                    self.tileCursor = 0



    def showTileListL2(self,gui,sampleTile):

        # TILE/OBJECT WINDOW
        if(self.toggleWindow and self.currentLayer=='l2'):
            windowItemLen = 30
            rows = 3
            cols = int(windowItemLen/rows)
            startX,startY = 0.2*gui.w,0.8*gui.h
            originX,originY  = startX,startY
            tileLen,tileHeight = 70,70
            subkeys = list(self.layer2RefData[self.selectedL2Key].keys())
            subkeys.reverse()
            tileIndex = self.tileCursor

            
            for i in range(rows):

                for j in range(cols):

                    # don't draw any more boxes
                    if(tileIndex>=len(subkeys)):
                        break

                    pygame.draw.rect(gui.screen, (80,80,40), [startX, startY,tileLen, tileHeight])
                    
                    if(tileIndex<len(subkeys)):
                        drawImage(gui.screen, self.layer2RefDataScaled[self.selectedL2Key][subkeys[tileIndex]], (startX, startY))

                    # HIGHLIGHT / SELECTED
                    if(gui.mouseCollides(startX,startY,tileLen,tileHeight)):
                        self.updateTileEnabled = False
                        gui.scrollEnabled = False
                        pygame.draw.rect(gui.screen, (180,180,200), [startX, startY,tileLen, tileHeight],4)
                        if(gui.clicked):
                            self.selectedL2SubKey = subkeys[tileIndex]
                    else:
                        pygame.draw.rect(gui.screen, (30,30,200) , [startX, startY,tileLen, tileHeight],4)



                    
                    tileIndex +=1
                    startX+=tileLen-4
                startX = originX
                startY += tileHeight -4

            # -----NEXT TILE TYPE
            nextGroup = drawSelectableImage(gui.smallBase100[4],gui.smallBase100[5],[originX-50,originY],gui)
            if(gui.mouseCollides(originX-50,originY,50,50)):
                gui.scrollEnabled = False
            if(nextGroup):
                self.selectedL2Key      = get_next_tile_key(self.layer2RefData, self.selectedL2Key)
                self.selectedL2SubKey   = list(self.layer2RefData[self.selectedL2Key].keys())[0]
                self.tileCursor =0

            # -----SCROLL TILES 

            nextTile = drawSelectableImage(gui.smallBase100[11],gui.smallBase100[12],[originX-50,originY+50],gui)
            if(gui.mouseCollides(originX-50,originY+50,50,50)):
                gui.scrollEnabled = False
            if(nextTile):
                if(len(subkeys)>tileIndex):
                    self.tileCursor = tileIndex
                elif(self.tileCursor==len(subkeys)-1):
                    self.tileCursor = 0
                else:
                    self.tileCursor = 0


    def showAnimatedList(self,gui,game):

        # TILE/OBJECT WINDOW
        if(self.toggleWindow and self.currentLayer=='A'):
            windowItemLen = 30
            rows = 3
            cols = int(windowItemLen/rows)
            startX,startY = 0.2*gui.w,0.8*gui.h
            originX,originY  = startX,startY
            tileLen,tileHeight = 70,70
            tileIndex = self.tileCursor
            mainKeys = list(self.animatedRefData.keys())
            mainKeys.reverse()

            
            for i in range(rows):

                for j in range(cols):

                    # don't draw any more boxes
                    if(tileIndex>=len(mainKeys)):
                        break

                    pygame.draw.rect(gui.screen, (80,80,40), [startX, startY,tileLen, tileHeight])
                    
                    if(tileIndex<len(mainKeys)):
                        drawImage(gui.screen, self.animatedRefData[self.selectedAnimKey]['thumbnail'], (startX, startY))

                    # HIGHLIGHT / SELECTED
                    if(gui.mouseCollides(startX,startY,tileLen,tileHeight)):
                        self.updateTileEnabled = False
                        gui.scrollEnabled = False
                        pygame.draw.rect(gui.screen, (180,180,200), [startX, startY,tileLen, tileHeight],4)
                        if(gui.clicked):
                            self.selectedAnimKey = mainKeys[tileIndex]
                    else:
                        pygame.draw.rect(gui.screen, (30,30,200) , [startX, startY,tileLen, tileHeight],4)



                    
                    tileIndex +=1
                    startX+=tileLen-4
                startX = originX
                startY += tileHeight -4

            # -----NEXT TILE TYPE
            # nextGroup = drawSelectableImage(gui.smallBase100[4],gui.smallBase100[5],[originX-50,originY],gui)
            # if(gui.mouseCollides(originX-50,originY,50,50)):
            #     gui.scrollEnabled = False
            # if(nextGroup):
            #     self.selectedEnemyKey      = get_next_tile_key(self.enemyRefData, self.selectedEnemyKey)
            #     self.selectedEnemySubKey   = list(self.enemyRefData[self.selectedEnemyKey].keys())[0]
            #     self.tileCursor =0

            # -----SCROLL TILES 

            nextTile = drawSelectableImage(gui.smallBase100[11],gui.smallBase100[12],[originX-50,originY+50],gui)
            if(gui.mouseCollides(originX-50,originY+50,50,50)):
                gui.scrollEnabled = False
            if(nextTile):
                if(len(mainKeys)>tileIndex):
                    self.tileCursor = tileIndex
                elif(self.tileCursor==len(mainKeys)-1):
                    self.tileCursor = 0
                else:
                    self.tileCursor = 0





    def showEnemyList(self,gui,sampleTile):

        # TILE/OBJECT WINDOW
        if(self.toggleWindow and self.currentLayer=='E'):
            windowItemLen = 30
            rows = 3
            cols = int(windowItemLen/rows)
            startX,startY = 0.2*gui.w,0.8*gui.h
            originX,originY  = startX,startY
            tileLen,tileHeight = 70,70
            subkeys = list(self.enemyRefData[self.selectedEnemyKey].keys())
            subkeys.reverse()
            tileIndex = self.tileCursor

            
            for i in range(rows):

                for j in range(cols):

                    # don't draw any more boxes
                    if(tileIndex>=len(subkeys)):
                        break

                    pygame.draw.rect(gui.screen, (80,80,40), [startX, startY,tileLen, tileHeight])
                    
                    if(tileIndex<len(subkeys)):
                        drawImage(gui.screen, self.enemyRefData[self.selectedEnemyKey][subkeys[tileIndex]]['scaled_image'], (startX, startY))

                    # HIGHLIGHT / SELECTED
                    if(gui.mouseCollides(startX,startY,tileLen,tileHeight)):
                        self.updateTileEnabled = False
                        gui.scrollEnabled = False
                        pygame.draw.rect(gui.screen, (180,180,200), [startX, startY,tileLen, tileHeight],4)
                        if(gui.clicked):
                            self.selectedEnemySubKey = subkeys[tileIndex]
                    else:
                        pygame.draw.rect(gui.screen, (30,30,200) , [startX, startY,tileLen, tileHeight],4)



                    
                    tileIndex +=1
                    startX+=tileLen-4
                startX = originX
                startY += tileHeight -4

            # -----NEXT TILE TYPE
            nextGroup = drawSelectableImage(gui.smallBase100[4],gui.smallBase100[5],[originX-50,originY],gui)
            if(gui.mouseCollides(originX-50,originY,50,50)):
                gui.scrollEnabled = False
                self.updateTileEnabled = False
            if(nextGroup):
                self.selectedEnemyKey      = get_next_tile_key(self.enemyRefData, self.selectedEnemyKey)
                self.selectedEnemySubKey   = list(self.enemyRefData[self.selectedEnemyKey].keys())[0]
                self.tileCursor =0

            # -----SCROLL TILES 

            nextTile = drawSelectableImage(gui.smallBase100[11],gui.smallBase100[12],[originX-50,originY+50],gui)
            if(gui.mouseCollides(originX-50,originY+50,50,50)):
                gui.scrollEnabled = False
                self.updateTileEnabled = False
            if(nextTile):
                if(len(subkeys)>tileIndex):
                    self.tileCursor = tileIndex
                elif(self.tileCursor==len(subkeys)-1):
                    self.tileCursor = 0
                else:
                    self.tileCursor = 0










    def renderLayer1Map(self,gui,game,hoveredTile):
        """
        hoveredTile is a pygame image object it refers to:
        hoveredTile = self.tileReferenceData[self.selectedTileKey][self.selectedTileSubKey]
        """

        if(gui.pressed==False): self.multiSelect = False

        rows = len(self.activeL1Data)    
        cols = len(self.activeL1Data[0])


        startX,startY = 0,0


        for row in range(len(self.activeL1Data)):
            for col in range(len(self.activeL1Data[0])):
                x =  startX + (col * self.tileWidth)  # 50 pixels
                y =  startY + (row * self.tileHeight) # 50 pixels

                if(x<gui.camX-50 or x>gui.camX +gui.camW+50):
                    continue
                if(y<gui.camY-50 or y>gui.camY +gui.camH+50):
                    continue

                # DRAW HOVERED TILE 
                if(gui.mouseCollides(x-gui.camX,y-gui.camY ,self.tileWidth ,self.tileHeight) and self.currentLayer=='l1'):
                    drawImage(gui.screen, hoveredTile, (x -gui.camX,y-gui.camY ))
                    
                    #--------UPDATE TILE 

                    if(self.multiSelect):
                        self.activeL1Data[row][col]            = hoveredTile
                        self.rawL1Data[row][col]               = self.selectedTileKey + '/' + self.selectedTileSubKey
                    
                    if(gui.clicked and self.updateTileEnabled):
                        self.activeL1Data[row][col]            = hoveredTile
                        self.rawL1Data[row][col] = self.selectedTileKey + '/' + self.selectedTileSubKey
                        if(gui.pressed):
                            self.multiSelect = True
                else:
                    # ONLY DRAW INBOUNDS IF CHECK ENABLED 
                    if(self.check):
                        # disabled for now, self.check = False
                        if(x - gui.camX > -100 and x - gui.camX < gui.w  and y - gui.camY > -100 and y - gui.camY < gui.h + 100):
                            drawImage(gui.screen, self.activeL1Data[row][col], (x - gui.camX, y - gui.camY))
                    else:
                        drawImage(gui.screen, self.activeL1Data[row][col], (x - gui.camX, y - gui.camY))

        #------REPLACE ALL TILES
        if(self.currentLayer=='l1'):
            if(gui.input.returnedKey.upper()=='R'):
                for row in range(rows):
                    for col in range(cols):
                        x = startX + (col * self.tileWidth )
                        y = startY + (row* self.tileHeight )
                        self.activeL1Data[row][col]            = hoveredTile
                        self.rawL1Data[row][col] = self.selectedTileKey + '/' + self.selectedTileSubKey
            
            if(gui.input.returnedKey.upper()=='B'):
                self.boxSelect = not self.boxSelect

            if(self.boxSelect):
                self.updateTileEnabled = False
                self.boxSelector(gui,game)
            else:
                self.updateTileEnabled = True


    
        # # RENDER LAYER ONE
        # sampleImage = self.activeL1Data[0][0]

        # # *** SETTING THE INDEX'S GREATLY SPEEDS UP AND REDUCES LAG
        # indexBottom = math.floor((gui.camY)/sampleImage.get_height())
        # indexTop = math.ceil((gui.camY+gui.camH)/sampleImage.get_height())



        # indexTop = clamp(indexTop,rows)
        # indexRight = clamp(indexRight,cols)                


    def renderLayer2Map(self,gui,game,startX,startY):

        if(self.currentLayer=='l1'):
            return()

        # RENDER AND MANAGE LAYER 2

        if(self.currentLayer in ['l2','E','S','Q']):

            if(self.currentLayer in ['l2']):
                # DISPLAY CURRENT SELECTED TILE
                selectedTile = self.layer2RefData[self.selectedL2Key][self.selectedL2SubKey]
                drawImage(gui.screen, selectedTile, (gui.mx,gui.my))

                deleteHover= False

            # DISPLAY FULL MAP
            for i in range(len(self.activeL2Data)-1,-1,-1):
                item = self.activeL2Data[i]
                drawImage(gui.screen, item[2], (item[0]-gui.camX,item[1]-gui.camY))
                
                # DELETE
                if(self.currentLayer in ['l2']):
                    if(gui.mouseCollides(item[0]-gui.camX,item[1]-gui.camY,item[2].get_width(),item[2].get_height())):
                        pygame.draw.rect(gui.screen, (180,180,120), [item[0]-gui.camX,item[1]-gui.camY,item[2].get_width(),item[2].get_height()],4)
                        deleteHover = True
                        if(gui.clicked):    
                            self.activeL2Data.pop(i)

            # ADD TILE TO LIST
            if(self.currentLayer in ['l2']):
                nothingSelected = True
                if(gui.clicked and nothingSelected and not deleteHover and self.updateTileEnabled):
                    self.activeL2Data.append([gui.mx+gui.camX, gui.my+gui.camY, selectedTile, self.selectedL2Key,self.selectedL2SubKey])
                    print("Added: " + str([selectedTile,gui.mx-gui.camX,gui.my-gui.camY,self.selectedL2Key,self.selectedL2SubKey ]))


    def renderAnimatedObjects(self,gui,game,startX,startY):

        if(self.currentLayer in ['l1','l2']):
            return()

        # RENDER AND MANAGE ENEMY LAYER

        
        if(self.currentLayer in ['A','E', 'S','Q']):

            # DISPLAY CURRENT SELECTED TILE AT CURSOR
            if(self.currentLayer in ['A']):
                selectedTile = self.animatedRefData[self.selectedAnimKey]['cursorImage']
            
                selectedTile = pygame.transform.rotate(selectedTile,self.currentAnimRotation)

                drawImage(gui.screen, selectedTile, (gui.mx,gui.my))

            deleteHover= False

            # DISPLAY FULL MAP
            for i in range(len(self.activeAnimatedData)-1,-1,-1):
                currentAnimatedObject = self.activeAnimatedData[i]
                objClass = currentAnimatedObject['classObject']
                objClass.drawSelf(gui,game,self)
                
                # -------------DELETE

                if(self.currentLayer in ['A']):
                    if(gui.mouseCollides(currentAnimatedObject['x']-gui.camX,currentAnimatedObject['y']-gui.camY,objClass.w,objClass.h)):
                        pygame.draw.rect(gui.screen, (180,180,120), [currentAnimatedObject['x']-gui.camX,currentAnimatedObject['y']-gui.camY,objClass.w,objClass.h],4)
                        deleteHover = True
                        if(gui.clicked):    
                            self.activeAnimatedData.pop(i)

        if(self.currentLayer in ['A']):

            #------ROTATE ENEMY

            if(gui.input.returnedKey.upper()=='R'):
                self.currentAnimRotation += 90
                if(self.currentAnimRotation>270):
                    self.currentAnimRotation = 0

            # ADD TILE TO LIST
            nothingSelected = True
            if(gui.clicked and nothingSelected and not deleteHover and self.updateTileEnabled):
                xpos,ypos   = gui.mx+gui.camX, gui.my+gui.camY
                images      = self.animatedRefData[self.selectedAnimKey]['images']
                speed          = 'fast'
                changeDuration = 0.2
                terrainObj  = nonInteractable(int(xpos),int(ypos),images,imageAnimateAdvanced(images,changeDuration),gui)
                if(self.currentAnimRotation in [0,180]):
                    pass
                else:
                    w,h = terrainObj.h,terrainObj.w
                    terrainObj.w = w
                    terrainObj.h = h


                terrainObj.facing = self.currentAnimRotation + 90
                self.activeAnimatedData.append({"x":int(xpos) ,"y": int(ypos),"libraryKey": self.selectedAnimKey,"speed":speed, "classObject": terrainObj})
                print("Added animation object ")




    def renderEnemyMap(self,gui,game,startX,startY):


        if(self.currentLayer in ['l1','l2','A']):
            return()

        # RENDER AND MANAGE ENEMY LAYER

        
        if(self.currentLayer in ['E', 'S','Q']):

            # DISPLAY CURRENT SELECTED TILE
            if(self.currentLayer in ['E']):
                selectedTile = self.enemyRefData[self.selectedEnemyKey][self.selectedEnemySubKey]['image']
            
                selectedTile = pygame.transform.rotate(selectedTile,self.currentEnemyRotation-90)
                print(self.currentEnemyRotation)

                if(self.enemySelectionState=='notSelected'):
                    drawImage(gui.screen, selectedTile, (gui.mx,gui.my))

            deleteHover= False

            # DRAW ALL ENEMIES
            for i in range(len(self.activeEnemyData)-1,-1,-1):
                item = self.activeEnemyData[i]
                ex,ey = item['x']-gui.camX,item['y']-gui.camY
                drawImage(gui.screen, item['image'], (ex,ey))
                
                # DRAW PATROL COORDS
                string = str(item['patrolRoute']).replace('[','').replace(']','').replace("'",'')
                tw= getTextWidth(gui.picoFont,string)
                drawTextWithBackground(gui.screen,gui.picoFont,string,ex-0.5*tw,ey+1.1*item['image'].get_height(),textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))
                # DRAW OBJECTIVES
                if(item['itemDrop']!= 'None'):
                    dropString = "Drops"
                else:
                    dropString = "No Drop"
                string = str(item['assignedObjective']) + " : " + dropString
                tw= getTextWidth(gui.picoFont,string)
                drawTextWithBackground(gui.screen,gui.nanoFont,string,ex-0.5*tw,ey+1.3*item['image'].get_height(),textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))





                # -------------DELETE

                if(self.currentLayer in ['E']):
                    if(gui.mouseCollides(item['x']-gui.camX,item['y']-gui.camY,item['image'].get_width(),item['image'].get_height())):
                        pygame.draw.rect(gui.screen, (180,180,120), [item['x']-gui.camX,item['y']-gui.camY,item['image'].get_width(),item['image'].get_height()],4)
                        deleteHover = True
                        if(gui.clicked):    
                            self.activeEnemyData.pop(i)

            
            if(self.currentLayer in ['E']):

                  

                # --------PLACE ENEMY 

                nothingSelected = True
                if(gui.clicked and nothingSelected and not deleteHover and self.updateTileEnabled):
                    if(self.enemySelectionState=='notSelected'):
                        self.enemyToPlace = {'x':gui.mx+gui.camX ,'y':gui.my+gui.camY ,'image':selectedTile ,'enemyKeyName':self.selectedEnemyKey ,'enemySubKeyName':self.selectedEnemySubKey ,'rotation':wrapAngle(self.currentEnemyRotation),'patrolRoute':[],'itemDrop':'None', 'lv':3}
                        self.enemySelectionState='setObjectives'


                # ----------OBJECTIVE SELECTION

                if(self.enemySelectionState=='setObjectives'):
                    self.navEnabled   = False
                    gui.scrollEnabled = False
                    drawImage(gui.screen, selectedTile, (self.enemyToPlace['x'] - gui.camX,self.enemyToPlace['y']-gui.camY))
                    
                    # initialise objective if not exist
                    if(self.currentObjectiveCursor==None):
                        self.currentObjectiveCursor = self.availableObjectives[0]
                    
                    pressedKey     = gui.input.returnedKey.upper()
                    # GET DIRECTION OF ACCELLERATION
                    if('D' == pressedKey):
                        self.currentObjectiveCursor = self.availableObjectives[(self.availableObjectives.index(self.currentObjectiveCursor) + 1) % len(self.availableObjectives)]
                    if('A' == pressedKey):
                        self.currentObjectiveCursor = self.availableObjectives[(self.availableObjectives.index(self.currentObjectiveCursor) - 1) % len(self.availableObjectives)]
                    if('RETURN' == pressedKey):
                        self.enemyToPlace['assignedObjective'] = self.currentObjectiveCursor
                        self.currentObjectiveCursor = None
                        self.enemySelectionState='itemDrop'
                        gui.input.returnedKey = ''



                    string = str(self.currentObjectiveCursor)
                    tw= getTextWidth(gui.smallFont,string)
                    drawTextWithBackground(gui.screen,gui.smallFont,string,self.enemyToPlace['x']-0.5*tw-gui.camX,self.enemyToPlace['y']+1.2*self.enemyToPlace['image'].get_height()-gui.camY,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))
                
                
                # ----------ENEMY DROP

                if(self.enemySelectionState=='itemDrop'):
                    self.navEnabled   = False
                    gui.scrollEnabled = False
                    drawImage(gui.screen, selectedTile, (self.enemyToPlace['x'] - gui.camX,self.enemyToPlace['y']-gui.camY))
                    
                    
                    pressedKey     = gui.input.returnedKey.upper()

                    # GET DIRECTION OF ACCELLERATION
                    if('D' == pressedKey):
                        self.bonusSpawn = self.bonusSpawnTypes[(self.bonusSpawnTypes.index(self.bonusSpawn) + 1) % len(self.bonusSpawnTypes)]
                    if('A' == pressedKey):
                        self.bonusSpawn = self.bonusSpawnTypes[(self.bonusSpawnTypes.index(self.bonusSpawn) - 1) % len(self.bonusSpawnTypes)]
                    if('RETURN' == pressedKey):
                        self.enemyToPlace['itemDrop'] = self.bonusSpawn
                        self.enemySelectionState='askPatrol'
                        self.bonusSpawn = 'None'
                        gui.input.returnedKey = ''



                    string = str(self.bonusSpawn)
                    tw= getTextWidth(gui.smallFont,string)
                    drawTextWithBackground(gui.screen,gui.smallFont,string,self.enemyToPlace['x']-0.5*tw-gui.camX,self.enemyToPlace['y']+1.2*self.enemyToPlace['image'].get_height()-gui.camY,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))
                
                


                # --------WAYPOINTS

                if(self.enemySelectionState=='askPatrol'):
                    drawImage(gui.screen, selectedTile, (self.enemyToPlace['x'] - gui.camX,self.enemyToPlace['y']-gui.camY))

                    chosenFont       = gui.largeFont
                    borderColour     =(60,60,200)
                    tw= getTextWidth(chosenFont,'Yes.')
                    drawTextWithBackground(gui.screen,chosenFont,'Add Patrol Route?',0.4*gui.w,0.35*gui.h,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))
                    yes,tex,tey      = simpleButton(0.4*gui.w,0.4*gui.h,'Yes',gui,chosenFont,setTw=tw,backColour=(0,0,0),borderColour=borderColour, textColour=(255,255,255))
                    no,tex,tey       = simpleButton(0.45*gui.w,0.4*gui.h,'No',gui,chosenFont,setTw=tw,backColour=(0,0,0),borderColour=borderColour, textColour=(255,255,255))
                    



                    gui.scrollEnabled = False
                    if(yes):
                        self.enemySelectionState='setPatrolCoords'
                        gui.scrollEnabled = True
                    if(no or gui.input.returnedKey.upper()=='RETURN'):
                        self.patrolCoords = [(self.enemyToPlace['x'],self.enemyToPlace['y']),(self.enemyToPlace['x'],self.enemyToPlace['y']),(self.enemyToPlace['x'],self.enemyToPlace['y']),(self.enemyToPlace['x'],self.enemyToPlace['y'])]
                        self.enemySelectionState='complete'
                        gui.scrollEnabled = True
                        gui.input.returnedKey = ''

                # DRAW WAYPOINT INDEXES
                if(self.enemySelectionState=='setPatrolCoords'):
                    drawImage(gui.screen, selectedTile, (self.enemyToPlace['x'] - gui.camX,self.enemyToPlace['y']-gui.camY))

                    for coords in self.patrolCoords:
                        coordIndex = str(self.patrolCoords.index(coords))
                        drawTextWithBackground(gui.screen,gui.hugeFont,coordIndex,coords[0]-gui.camX,coords[1]-gui.camY,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))

                # SET WAYPOINTS
                if(self.enemySelectionState=='setPatrolCoords'):
                    patrolIndex = str(len(self.patrolCoords))
                    #drawTextWithBackground(gui.screen,gui.hugeFont,patrolIndex,x-gui.camX,y-gui.camY,textColour=(20, 50, 200),backColour= (0,0,0),borderColour=(50,50,200))
                    if(gui.clicked):
                        self.patrolCoords.append((gui.mx +gui.camX,gui.my+gui.camY))
            
                    if(len(self.patrolCoords)>3):
                        self.enemySelectionState='complete'
                        


                #-----------COMPLETE


                if(self.enemySelectionState=='complete'):
                    self.enemySelectionState = 'notSelected'
                    self.enemyToPlace['patrolRoute'] = self.patrolCoords
                    self.activeEnemyData.append(self.enemyToPlace) 
                    print("Enemy placed ")
                    print(self.enemyToPlace)
                    self.enemyToPlace = {}
                    self.patrolCoords = []
                    self.currentEnemyRotation = 0

                        

            
            

            #------ROTATE ENEMY

            if(gui.input.returnedKey.upper()=='R'):
                self.currentEnemyRotation =  wrapAngle(self.currentEnemyRotation + 90)









    def saveGameLogic(self,gui,game):
        if(gui.input.returnedKey.upper()=='C' or self.savegame):


            with open(self.chosenMapPath, 'r') as file:
                content = file.read()


            # ----------L1

            # Split the content into sections
            before_l1, l1_data, after_l1 = content.split('*L1', 2)

            # Convert self.rawL1Data back to string format
            new_l1_data = '\n'.join([','.join(row) for row in self.rawL1Data])

            # Combine the sections back together with the updated map_data
            new_content = before_l1 + '*L1\n' + new_l1_data + '\n*L1' + after_l1

            # Write the updated content back to the file
            with open(self.chosenMapPath, 'w') as file:
                file.write(new_content)

            # ----------L2

            with open(self.chosenMapPath, 'r') as file:
                content = file.read()

            # Split the content into sections
            before_l2, l2_data, after_l2 = content.split('*L2', 2)

            # Convert new_l2_data to the desired string format, ignoring the pygame object
            new_l2_data_str = ','.join(['/'.join(map(str, row[:2] + row[3:])) for row in self.activeL2Data])

            # Combine the sections back together with the updated l2_data
            new_content = before_l2 + '*L2\n' + new_l2_data_str + '\n*L2' + after_l2

            # Write the updated content back to the file
            with open(self.chosenMapPath, 'w') as file:
                file.write(new_content)


            # ----------A

            with open(self.chosenMapPath, 'r') as file:
                content = file.read()

            # Split the content into sections
            before_animated, animated_data, after_animated = content.split('*ANIMATED', 2)

            new_animated_data_str = ''

            for anim in self.activeAnimatedData:
                # conveyor/90/200/420/fast
                facing = anim['classObject'].facing 
                changeDurationDict   = { "0.2": "fast", "0.4": "medium","0.6" :"slow"}
                
                new_animated_data_str += anim['libraryKey'] + '/' + str(facing) + '/' + str(anim['x']) + '/' + str(anim['y']) + '/' + anim['speed'] + ','
            

            # Combine the sections back together with the updated animated_data
            new_content = before_animated + '*ANIMATED\n' + new_animated_data_str + '\n*ANIMATED' + after_animated

            # Write the updated content back to the file
            with open(self.chosenMapPath, 'w') as file:
                file.write(new_content)

            
            
            # ----------E

            with open(self.chosenMapPath, 'r') as file:
                content = file.read()

            new_enemy_data_str = []
            for enemy in self.activeEnemyData:
                patrol_route_str = ':'.join(['-'.join(map(str, point)) for point in enemy['patrolRoute']])
                enemy_str = f"{enemy['x']}/{enemy['y']}/{enemy['enemyKeyName']}/{enemy['enemySubKeyName']}/{enemy['rotation']}/{patrol_route_str}/{enemy['lv']}/{enemy['assignedObjective']}/{enemy['itemDrop']}"
                new_enemy_data_str.append(enemy_str)
            new_enemy_data_str = ','.join(new_enemy_data_str)

            # Split the content into sections
            before_enemy, enemy_data, after_enemy = content.split('*ENEMY', 2)

            # Combine the sections back together with the updated enemy data
            new_content = before_enemy + '*ENEMY\n' + new_enemy_data_str + '\n*ENEMY' + after_enemy



            # Write the updated content back to the file
            with open(self.chosenMapPath, 'w') as file:
                file.write(new_content)

            # ----------S

            with open(self.chosenMapPath, 'r') as file:
                content = file.read()

            spawn_data_str = ""
            for s in self.activeSpawnZones:

                spawn_data_str += str(s[0]) + '/' + str(s[1]) + '/' + str(s[2]) + '/' + str(s[3]) + ','


            # Split the content into sections
            before_spawn, spawn_data, after_spawn = content.split('*SPAWN', 2)

            # Combine the sections back together with the updated enemy data
            new_content = before_spawn + '*SPAWN\n' + spawn_data_str + '\n*SPAWN' + after_spawn


            # Write the updated content back to the file
            with open(self.chosenMapPath, 'w') as file:
                file.write(new_content)


            # ----------Q

            with open(self.chosenMapPath, 'r') as file:
                content = file.read()

            quadrant_data_string = ""
            for s in self.activeQuadrants:

                quadrant_data_string += str(s[0]) + '/' + str(s[1]) + '/' + str(s[2]) + '/' + str(s[3]) + ','


            createNew = False
            # Split the content into sections
            try:
                before_quadrant, quandrant_data, after_quadrant = content.split('*QUADRANT', 2)
            except:
                createNew = True
                


            if(not createNew):
                # Combine the sections back together with the updated enemy data
                new_content = before_quadrant + '*QUADRANT\n' + quadrant_data_string + '\n*QUADRANT' + after_quadrant
            else:
                print("Quadrant data doesn't exist - appending")
                new_content = content + '\n' + '*QUADRANT\n' + quadrant_data_string + '\n*QUADRANT'



            # Write the updated content back to the file
            with open(self.chosenMapPath, 'w') as file:
                file.write(new_content)



            self.saving = True
            self.savegame = False







        if(self.saving):
            saveMessageTimeout    = self.saveTimer.stopWatch(3,'SaveMessage',self.saves,game)
            drawText(gui,gui.bigFont, 'Map Saved!',gui.w*0.45,gui.h*0.45,colour=(80, 255, 80))
            if(saveMessageTimeout):
                self.saving = False
                self.saves+=1

        if(self.loading):
            loadMessageTimeout    = self.loadTimer.stopWatch(3,'LoadMessage',self.loads,game)
            drawText(gui,gui.bigFont, 'Map Loaded!',gui.w*0.45,gui.h*0.45,colour=(80, 255, 80))
            if(loadMessageTimeout):
                self.loading = False
                self.loads+=1

    def loadGameLogic(self,gui):
        if(gui.input.returnedKey.upper()=='F' or self.loadGame):
            self.mapLoaded = False
            self.loading  = True
            self.loadGame = False



    def boxSelector(self,gui,game):

        if(gui.rightClicked):
            self.boxCoords = []
        
        if(gui.clicked):
            if(len(self.boxCoords)<4):
                self.boxCoords.append((gui.mx+gui.camX,gui.my+gui.camY))


        # if CURSOR AREA SELECTION
        if(len(self.boxCoords)<4):
            for bc in self.boxCoords:
                drawTextWithBackground(gui.screen,gui.bigFont,str(self.boxCoords.index(bc)),bc[0]-gui.camX,bc[1]-gui.camY ,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))
            
        if(len(self.boxCoords)==4):
            selectedCoords = self.boxCoords
            x_min = min(x for x, y in selectedCoords)
            y_min = min(y for x, y in selectedCoords)
            x_max = max(x for x, y in selectedCoords)
            y_max = max(y for x, y in selectedCoords)
            selectedArea = [x_min, y_min, x_max - x_min, y_max - y_min]


            x,y = 0,0
            # USES THE type and index as keys to gui.layer2Dict
            counter = 0

            for r in range(len(self.activeL1Data)):
                row = self.activeL1Data[r]
                for c in range(len(row)):
                    image = self.activeL1Data[r][c]
                    if(collidesObjectless(x,y,image.get_width(),image.get_height(),selectedArea[0],selectedArea[1],selectedArea[2],selectedArea[3])):
                        self.activeL1Data[r][c]            = self.tileReferenceData[self.selectedTileKey][self.selectedTileSubKey]
                        self.rawL1Data[r][c]               = self.selectedTileKey + '/' + self.selectedTileSubKey     



                    x += image.get_width()
                y+= image.get_height()
                x = 0


            self.boxCoords     = []
            print("Resetting box coords")





    @staticmethod
    def collides_objectless(x, y, w, h, x1, y1, w1, h1):
        return (x >= x1 and x <= x1 + w1 and y >= y1 and y <= y1 + h1) or \
               (x1 >= x and x1 <= x + w and y1 >= y and y1 <= y + h)

    def spawnZones(self, gui, game):
        if self.currentLayer != 'S':
            return

        collides_with_existing = False
        starting_colour = (20, 30, 70)
        collide_index = None
        for idx, spawn_zone in enumerate(self.activeSpawnZones):
            # DELETE EXISTING IF CLICKED
            if gui.mouseCollides(spawn_zone[0] - gui.camX, spawn_zone[1] - gui.camY, spawn_zone[2], spawn_zone[3]):
                collides_with_existing = True
                collide_index = idx

            # MERGE JOINT BOXES
            for other_idx, spawn_zone_two in enumerate(self.activeSpawnZones[idx + 1:], start=idx + 1):
                if self.collides_objectless(*spawn_zone, *spawn_zone_two):
                    new_box = self.merge_boxes(spawn_zone, spawn_zone_two)
                    self.activeSpawnZones.remove(spawn_zone)
                    self.activeSpawnZones.remove(spawn_zone_two)
                    self.activeSpawnZones.append(new_box)
                    return

            # DRAW SPAWN ZONE MARKER
            pygame.draw.rect(gui.screen, starting_colour, (spawn_zone[0] - gui.camX, spawn_zone[1] - gui.camY, spawn_zone[2], spawn_zone[3]))
            starting_colour = lighten(starting_colour)
            drawTextWithBackground(gui.screen, gui.font, str(idx), spawn_zone[0] - gui.camX + 0.4 * spawn_zone[2], spawn_zone[1] - gui.camY + 0.3 * spawn_zone[3], textColour=(255, 255, 255), backColour=(0, 0, 0), borderColour=(50, 50, 200))

        if collides_with_existing and gui.clicked:
            del self.activeSpawnZones[collide_index]
            gui.pressed = False
            gui.clicked = False
            return

        if self.updateTileEnabled and gui.scrollEnabled:
            self.spawn_box_selector(gui, game)

    def setQuadrants(self, gui, game):
        if self.currentLayer != 'Q':
            return

        collides_with_existing = False
        starting_colour = (20, 30, 70)
        collide_index = None

        for idx, currentQuadrant in enumerate(self.activeQuadrants):
            # DELETE EXISTING IF CLICKED
            if gui.mouseCollides(currentQuadrant[0] - gui.camX, currentQuadrant[1] - gui.camY, currentQuadrant[2], currentQuadrant[3]):
                collides_with_existing = True
                collide_index = idx

            # MERGE JOINT BOXES
            for other_idx, currentQuadrant_two in enumerate(self.activeQuadrants[idx + 1:], start=idx + 1):
                if self.collides_objectless(*currentQuadrant, *currentQuadrant_two):
                    new_box = self.merge_boxes(currentQuadrant, currentQuadrant_two)
                    self.activeQuadrants.remove(currentQuadrant)
                    self.activeQuadrants.remove(currentQuadrant_two)
                    self.activeQuadrants.append(new_box)
                    return

            # DRAW SPAWN ZONE MARKER
            pygame.draw.rect(gui.screen, starting_colour, (currentQuadrant[0] - gui.camX, currentQuadrant[1] - gui.camY, currentQuadrant[2], currentQuadrant[3]))
            starting_colour = lighten(starting_colour)
            drawTextWithBackground(gui.screen, gui.font, str(idx), currentQuadrant[0] - gui.camX + 0.4 * currentQuadrant[2], currentQuadrant[1] - gui.camY + 0.3 * currentQuadrant[3], textColour=(255, 255, 255), backColour=(0, 0, 0), borderColour=(50, 50, 200))

        if collides_with_existing and gui.clicked:
            del self.activeQuadrants[collide_index]
            gui.pressed = False
            gui.clicked = False
            return

        if self.updateTileEnabled and gui.scrollEnabled:
            self.quadrant_box_selector(gui, game)

    def merge_boxes(self, box1, box2):
        nbx = min(box1[0], box2[0])
        nby = min(box1[1], box2[1])
        rhs = max(box1[0] + box1[2], box2[0] + box2[2])
        bhs = max(box1[1] + box1[3], box2[1] + box2[3])
        return [nbx, nby, rhs - nbx, bhs - nby]

    def spawn_box_selector(self, gui, game):
        selected_area = self.dragSelect.dragSelect(gui, gui.camX, gui.camY)
        if selected_area and selected_area[2] > 1 and selected_area[3] > 1:
            self.activeSpawnZones.append(selected_area)

    def quadrant_box_selector(self, gui, game):
        selected_area = self.dragSelect.dragSelect(gui, gui.camX, gui.camY)
        if selected_area and selected_area[2] > 1 and selected_area[3] > 1:
            self.activeQuadrants.append(selected_area)


    def nav(self,gui,game):
        # GET PRESSED KEYS

        #self.gameMap['metaTiles']
        pressedKeys     = [x.upper() for x in gui.input.pressedKeys]
        # ACCELELRATION FLAG
        speed = 20
        if('L' in pressedKeys):
            speed = 60
        if(';' in pressedKeys):
            speed = 200
        
        # GET DIRECTION OF ACCELLERATION
        if('W' in pressedKeys ):
            gui.camY -= speed
        if('S' in pressedKeys):
            gui.camY += speed
        if('D' in pressedKeys):
            gui.camX += speed
        if('A' in pressedKeys):
            gui.camX -= speed

        if(gui.camX<0): gui.camX = 0
        if(gui.camY<0): gui.camY = 0

        if(gui.camX+gui.camW>self.mapWidth): gui.camX = self.mapWidth - gui.camW
        if(gui.camY+gui.camH>self.mapHeight): gui.camY = self.mapHeight - gui.camH






    def loadLevelData(self,gui,game):

        if(self.chosenMapName=='Rural Assault'):
            self.activeLevel             = ruralAssault(gui,self)
            self.availableObjectives     = ['no objective'] + list(self.activeLevel.objectives.keys())
            del self.activeLevel


def get_next_subkey(tile_data, tile_key, tile_subkey):
    subkeys = list(tile_data[tile_key].keys())
    
    # If there's no next subkey, return the current subkey
    if not subkeys:
        return tile_subkey
    
    # Find the index of the current subkey
    current_index = subkeys.index(tile_subkey)
    
    # Get the next index
    next_index = (current_index + 1) % len(subkeys)
    
    return subkeys[next_index]

def get_previous_subkey(tile_data, tile_key, tile_subkey):
    subkeys = list(tile_data[tile_key].keys())


    # If there's no previous subkey, return the current subkey
    if not subkeys:
        return tile_subkey
    
    # Find the index of the current subkey
    current_index = subkeys.index(tile_subkey)
    
    # Get the previous index
    previous_index = (current_index - 1) % len(subkeys)
    
    return subkeys[previous_index]

def get_next_tile_key(tile_data, current_tile_key):
    keys = list(tile_data.keys())
    
    # If there are no keys, return the current tile key
    if not keys:
        return current_tile_key
    
    # Find the index of the current tile key
    current_index = keys.index(current_tile_key)
    
    # Get the next index
    next_index = (current_index + 1) % len(keys)
    
    return keys[next_index]
def get_previous_tile_key(tile_data, current_tile_key):
    keys = list(tile_data.keys())
    
    # If there are no keys, return the current tile key
    if not keys:
        return current_tile_key
    
    # Find the index of the current tile key
    current_index = keys.index(current_tile_key)
    
    # Get the next index
    previous_index = (current_index - 1) % len(keys)
    
    return keys[previous_index]


def sortKeys(tileList):
    sortedList = []
    
    for i in tileList:
        tileNumber = int(''.join([char for char in i if char.isdigit()]))
        if(len(sortedList)==0):
            sortedList.append(i)
        else:
            for s in sortedList:
                currentTileNumber = int(''.join([char for char in s if char.isdigit()]))
                # check greater/ less than




