from utils._utils import *
from utils._utils import stopTimer
from utils.gameUtils import *
from levels.LOAD_MAP_DATA import *
import random

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
        self.currentLayer        = 'Q'


        self.tileReferenceData   = None
        self.selectedTileKey    = 'template'
        self.selectedTileSubKey = 'base100_1'
        
        self.layer2RefData       = None
        self.selectedL2Key      = 'objectTiles'
        self.selectedL2SubKey   = 'obj1'
        self.layer2RefDataScaled = None
        
        self.enemyRefData        = None
        self.selectedEnemyKey    = 'air' 
        self.selectedEnemySubKey = 'scout'
        self.enemySelectionState = 'notSelected'
        self.enemyToPlace        = {}
        self.patrolCoords        = []

        self.currentEnemyRotation = 90


    def createMap(self,gui,game):
        
        self.dynamicBorder.animateBorder('menu border',game,gui)


        # ASK QUESTIONS ABOUT NEW MAP 
        questionList = ['Name of Map file', 'Tiles per Row', 'Number of Rows', 'Tile Size']
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
                       "cols": int(self.answerList[1]),
                       "rows":int(self.answerList[2]),
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

            print("ADDING ENEMY placeholder ....")
            mapfile += '*ENEMY\n'
            mapfile += '*ENEMY\n'

            print("ADDING SPAWN placeholder ....")
            mapfile += '*SPAWN\n'
            mapfile += '*SPAWN\n'

            print("Mapfile looks like this")
            print(mapfile)





            print("Saving....")
            loadPath       = game.mapPaths
            f = open(loadPath + gameMap['name'] + '.txt','w')
            f.write(mapfile[:-1])

            game.chosenMapName = gameMap['name']
            game.chosenMapPath = game.mapPaths + game.chosenMapName + '.txt'
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
            
            raw_map_data,map_l2_data,map_enemy_data,spawn_zones = loadUnconverted(game.chosenMapPath)
            game.rawL1Data    = raw_map_data
            game.rawL2Data    = map_l2_data
            game.rawEnemyData = map_enemy_data
            game.rawSpawnData = spawn_zones

            # This is the data that matters
            self.tileReferenceData,game.activeL1Data                          = loadMapRefData(gui,game)
            self.layer2RefData, game.activeL2Data,self.layer2RefDataScaled    = loadLayer2RefData(gui,game)
            self.enemyRefData,game.activeEnemyData                            = loadEnemyRefData(gui,game)
            game.activeSpawnZones                                             = loadSpawnZones(gui,game)
            

            self.mapLoaded = True

        #---------------------------CAMERA AND SIZING

        sampleTile = game.activeL1Data[1][2] # A tile representative of the height/width
        self.tileWidth  = sampleTile.get_width()
        self.tileHeight = sampleTile.get_height()
        game.mapWidth, game.mapHeight = len(game.activeL1Data[0])  * self.tileWidth ,len(game.activeL1Data) * self.tileHeight

        hoveredTile = self.tileReferenceData[self.selectedTileKey][self.selectedTileSubKey]


        startX,startY= 0,0
        gui.moveCamera(game)
        self.nav(gui,game)


        # These get overriden by any layer below
        gui.scrollEnabled      = True

        #----------------------------MAP RENDERING

        self.renderLayer1Map(gui,game,hoveredTile)
        self.spawnZones(gui,game)
        self.renderLayer2Map(gui,game,startX,startY)
        self.renderEnemyMap(gui,game,startX,startY)

        self.updateTileEnabled = True
        self.showTileListL1(gui,sampleTile)
        self.showTileListL2(gui,sampleTile)
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
            if(gui.input.returnedKey.upper()=='L'):
                self.selectedTileKey = get_next_tile_key(self.tileReferenceData, self.selectedTileKey)
                self.selectedTileSubKey = list(self.tileReferenceData[self.selectedTileKey].keys())[0]
                self.tileCursor =0
            if(gui.input.returnedKey.upper()=='J'):
                self.selectedTileKey = get_previous_tile_key(self.tileReferenceData, self.selectedTileKey)
                self.selectedTileSubKey = list(self.tileReferenceData[self.selectedTileKey].keys())[0]
                self.tileCursor =0
        
        if(self.currentLayer=='l2'):
            if(gui.input.returnedKey.upper()=='I'):
                self.selectedL2SubKey = get_next_subkey(self.layer2RefData, self.selectedL2Key, self.selectedL2SubKey)
            if(gui.input.returnedKey.upper()=='K'):
                self.selectedL2SubKey = get_previous_subkey(self.layer2RefData, self.selectedL2Key, self.selectedL2SubKey)
            if(gui.input.returnedKey.upper()=='L'):
                self.selectedL2Key = get_next_tile_key(self.layer2RefData, self.selectedL2Key)
                self.selectedL2SubKey = list(self.layer2RefData[self.selectedL2Key].keys())[0]
                self.tileCursor =0
            if(gui.input.returnedKey.upper()=='J'):
                self.selectedL2Key = get_previous_tile_key(self.layer2RefData, self.selectedL2Key)
                self.selectedL2SubKey = list(self.layer2RefData[self.selectedL2Key].keys())[0]
                self.tileCursor =0

        if(self.currentLayer=='E'):
            if(gui.input.returnedKey.upper()=='I'):
                self.selectedEnemySubKey = get_next_subkey(self.enemyRefData, self.selectedEnemyKey, self.selectedEnemySubKey)
            if(gui.input.returnedKey.upper()=='K'):
                self.selectedEnemySubKey = get_previous_subkey(self.enemyRefData, self.selectedEnemyKey, self.selectedEnemySubKey)
            if(gui.input.returnedKey.upper()=='L'):
                self.selectedEnemyKey = get_next_tile_key(self.enemyRefData, self.selectedEnemyKey)
                self.selectedEnemySubKey = list(self.enemyRefData[self.selectedEnemyKey].keys())[0]
                self.tileCursor =0
            if(gui.input.returnedKey.upper()=='J'):
                self.selectedEnemyKey = get_previous_tile_key(self.enemyRefData, self.selectedEnemyKey)
                self.selectedEnemySubKey = list(self.enemyRefData[self.selectedEnemyKey].keys())[0]
                self.tileCursor =0




        if(gui.input.returnedKey=='space'):
            self.tileCursor = 0
            if(self.currentLayer=='l1'):
                self.currentLayer = 'l2'
            elif(self.currentLayer=='l2'):
                self.currentLayer = 'E'
            elif(self.currentLayer=='E'):
                self.currentLayer = 'Q'
            elif(self.currentLayer=='Q'):
                self.currentLayer = 'l1'


        if(gui.input.returnedKey.upper()=='H'):
            gui.camX = 0
            gui.camY = 0




    def sideMenu(self,gui,game,sampleTile):


        

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
        if(self.currentLayer=='l2'):
            tile1,tile2 = gui.L2_1,gui.L2_2 
        if(self.currentLayer=='E'):
            tile1,tile2 = gui.E_1,gui.E_2 
        if(self.currentLayer=='Q'):
            tile1,tile2 = gui.Q_1,gui.Q_2 
        toggleLayer = drawSelectableImage(tile1,tile2,[toggleX,toggleY],gui)
        if(toggleLayer):
            self.tileCursor = 0
            if(self.currentLayer=='l1'):
                self.currentLayer = 'l2'
            elif(self.currentLayer=='l2'):
                self.currentLayer = 'E'
            elif(self.currentLayer=='E'):
                self.currentLayer = 'Q'
            elif(self.currentLayer=='Q'):
                self.currentLayer = 'l1'


        # -------LAYER TOGGLE
        toggleX, toggleY = boxX+0.06*gui.w, boxY + 0.1*gui.h
        toggleWindow = drawSelectableImage(gui.openTileWindow,gui.openTileWindow2,[toggleX,toggleY],gui)
        if(toggleWindow):
            self.toggleWindow = not self.toggleWindow
        

        setWidth=getTextWidth(gui.font,'A menu item yep sure correct.')
        sentence = "Map Size: [" + str(game.mapWidth) + ':' + str(game.mapHeight) +']'
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
            if(nextGroup):
                self.selectedEnemyKey      = get_next_tile_key(self.enemyRefData, self.selectedEnemyKey)
                self.selectedEnemySubKey   = list(self.enemyRefData[self.selectedEnemyKey].keys())[0]
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










    def renderLayer1Map(self,gui,game,hoveredTile):
        """
        hoveredTile is a pygame image object it refers to:
        hoveredTile = self.tileReferenceData[self.selectedTileKey][self.selectedTileSubKey]
        """

        if(gui.pressed==False): self.multiSelect = False

        rows = len(game.activeL1Data)    
        cols = len(game.activeL1Data[0])


        startX,startY = 0,0


        for row in range(len(game.activeL1Data)):
            for col in range(len(game.activeL1Data[0])):
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
                        game.activeL1Data[row][col]            = hoveredTile
                        game.rawL1Data[row][col]               = self.selectedTileKey + '/' + self.selectedTileSubKey
                    
                    if(gui.clicked and self.updateTileEnabled):
                        game.activeL1Data[row][col]            = hoveredTile
                        game.rawL1Data[row][col] = self.selectedTileKey + '/' + self.selectedTileSubKey
                        if(gui.pressed):
                            self.multiSelect = True
                else:
                    # ONLY DRAW INBOUNDS IF CHECK ENABLED 
                    if(self.check):
                        # disabled for now, self.check = False
                        if(x - gui.camX > -100 and x - gui.camX < gui.w  and y - gui.camY > -100 and y - gui.camY < gui.h + 100):
                            drawImage(gui.screen, game.activeL1Data[row][col], (x - gui.camX, y - gui.camY))
                    else:
                        drawImage(gui.screen, game.activeL1Data[row][col], (x - gui.camX, y - gui.camY))

        #------REPLACE ALL TILES
        if(self.currentLayer=='l1'):
            if(gui.input.returnedKey.upper()=='R'):
                for row in range(rows):
                    for col in range(cols):
                        x = startX + (col * self.tileWidth )
                        y = startY + (row* self.tileHeight )
                        game.activeL1Data[row][col]            = hoveredTile
                        game.rawL1Data[row][col] = self.selectedTileKey + '/' + self.selectedTileSubKey
            
            if(gui.input.returnedKey.upper()=='B'):
                self.boxSelect = not self.boxSelect

            if(self.boxSelect):
                self.updateTileEnabled = False
                self.boxSelector(gui,game)
            else:
                self.updateTileEnabled = True


    
        # # RENDER LAYER ONE
        # sampleImage = game.activeL1Data[0][0]

        # # *** SETTING THE INDEX'S GREATLY SPEEDS UP AND REDUCES LAG
        # indexBottom = math.floor((gui.camY)/sampleImage.get_height())
        # indexTop = math.ceil((gui.camY+gui.camH)/sampleImage.get_height())



        # indexTop = clamp(indexTop,rows)
        # indexRight = clamp(indexRight,cols)                


    def renderLayer2Map(self,gui,game,startX,startY):

        if(self.currentLayer=='l1'):
            return()

        # RENDER AND MANAGE LAYER 2

        if(self.currentLayer in ['l2','E','Q']):

            if(self.currentLayer in ['l2']):
                # DISPLAY CURRENT SELECTED TILE
                selectedTile = self.layer2RefData[self.selectedL2Key][self.selectedL2SubKey]
                drawImage(gui.screen, selectedTile, (gui.mx,gui.my))

                deleteHover= False

            # DISPLAY FULL MAP
            for i in range(len(game.activeL2Data)-1,-1,-1):
                item = game.activeL2Data[i]
                drawImage(gui.screen, item[2], (item[0]-gui.camX,item[1]-gui.camY))
                
                # DELETE
                if(self.currentLayer in ['l2']):
                    if(gui.mouseCollides(item[0]-gui.camX,item[1]-gui.camY,item[2].get_width(),item[2].get_height())):
                        pygame.draw.rect(gui.screen, (180,180,120), [item[0]-gui.camX,item[1]-gui.camY,item[2].get_width(),item[2].get_height()],4)
                        deleteHover = True
                        if(gui.clicked):    
                            game.activeL2Data.pop(i)

            # ADD TILE TO LIST
            if(self.currentLayer in ['l2']):
                nothingSelected = True
                if(gui.clicked and nothingSelected and not deleteHover and self.updateTileEnabled):
                    game.activeL2Data.append([gui.mx+gui.camX, gui.my+gui.camY, selectedTile, self.selectedL2Key,self.selectedL2SubKey])
                    print("Added: " + str([selectedTile,gui.mx-gui.camX,gui.my-gui.camY,self.selectedL2Key,self.selectedL2SubKey ]))


    def renderEnemyMap(self,gui,game,startX,startY):

        if(self.currentLayer in ['l1','l2']):
            return()

        # RENDER AND MANAGE ENEMY LAYER

        
        if(self.currentLayer in ['E', 'Q']):

            # DISPLAY CURRENT SELECTED TILE
            if(self.currentLayer in ['E']):
                selectedTile = self.enemyRefData[self.selectedEnemyKey][self.selectedEnemySubKey]['image']
            
                selectedTile = pygame.transform.rotate(selectedTile,self.currentEnemyRotation)

                if(self.enemySelectionState=='notSelected'):
                    drawImage(gui.screen, selectedTile, (gui.mx,gui.my))

            deleteHover= False

            # DISPLAY FULL MAP
            for i in range(len(game.activeEnemyData)-1,-1,-1):
                item = game.activeEnemyData[i]
                drawImage(gui.screen, item['image'], (item['x']-gui.camX,item['y']-gui.camY))
                
                # -------------DELETE

                if(self.currentLayer in ['E']):
                    if(gui.mouseCollides(item['x']-gui.camX,item['y']-gui.camY,item['image'].get_width(),item['image'].get_height())):
                        pygame.draw.rect(gui.screen, (180,180,120), [item['x']-gui.camX,item['y']-gui.camY,item['image'].get_width(),item['image'].get_height()],4)
                        deleteHover = True
                        if(gui.clicked):    
                            game.activeEnemyData.pop(i)

            
            if(self.currentLayer in ['E']):

                  

                # --------PLACE ENEMY 

                nothingSelected = True
                if(gui.clicked and nothingSelected and not deleteHover and self.updateTileEnabled):
                    if(self.enemySelectionState=='notSelected'):
                        self.enemyToPlace = {'x':gui.mx+gui.camX ,'y':gui.my+gui.camY ,'image':selectedTile ,'enemyKeyName':self.selectedEnemyKey ,'enemySubKeyName':self.selectedEnemySubKey ,'rotation':self.currentEnemyRotation ,'patrolRoute':[] ,'lv':3}
                        self.enemySelectionState='setPatrolCoords'

                # --------WAYPOINTS

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
                        
                        self.enemySelectionState = 'notSelected'
                        self.enemyToPlace['patrolRoute'] = self.patrolCoords
                        game.activeEnemyData.append(self.enemyToPlace) 
                        self.enemyToPlace = {}
                        self.patrolCoords = []
                        self.currentEnemyRotation = 0
                        



                #------ROTATE ENEMY

                if(gui.input.returnedKey.upper()=='R'):
                    self.currentEnemyRotation += 90
                    if(self.currentEnemyRotation>270):
                        self.currentEnemyRotation = 0









    def saveGameLogic(self,gui,game):
        if(gui.input.returnedKey.upper()=='C' or self.savegame):


            with open(game.chosenMapPath, 'r') as file:
                content = file.read()


            # ----------L1

            # Split the content into sections
            before_l1, l1_data, after_l1 = content.split('*L1', 2)

            # Convert game.rawL1Data back to string format
            new_l1_data = '\n'.join([','.join(row) for row in game.rawL1Data])

            # Combine the sections back together with the updated map_data
            new_content = before_l1 + '*L1\n' + new_l1_data + '\n*L1' + after_l1

            # Write the updated content back to the file
            with open(game.chosenMapPath, 'w') as file:
                file.write(new_content)

            # ----------L2

            with open(game.chosenMapPath, 'r') as file:
                content = file.read()

            # Split the content into sections
            before_l2, l2_data, after_l2 = content.split('*L2', 2)

            # Convert new_l2_data to the desired string format, ignoring the pygame object
            new_l2_data_str = ','.join(['/'.join(map(str, row[:2] + row[3:])) for row in game.activeL2Data])

            # Combine the sections back together with the updated l2_data
            new_content = before_l2 + '*L2\n' + new_l2_data_str + '\n*L2' + after_l2

            # Write the updated content back to the file
            with open(game.chosenMapPath, 'w') as file:
                file.write(new_content)
            # ----------E

            with open(game.chosenMapPath, 'r') as file:
                content = file.read()

            new_enemy_data_str = []
            for enemy in game.activeEnemyData:
                patrol_route_str = ':'.join(['-'.join(map(str, point)) for point in enemy['patrolRoute']])
                enemy_str = f"{enemy['x']}/{enemy['y']}/{enemy['enemyKeyName']}/{enemy['enemySubKeyName']}/{enemy['rotation']}/{patrol_route_str}/{enemy['lv']}"
                new_enemy_data_str.append(enemy_str)
            new_enemy_data_str = ','.join(new_enemy_data_str)

            # Split the content into sections
            before_enemy, enemy_data, after_enemy = content.split('*ENEMY', 2)

            # Combine the sections back together with the updated enemy data
            new_content = before_enemy + '*ENEMY\n' + new_enemy_data_str + '\n*ENEMY' + after_enemy



            # Write the updated content back to the file
            with open(game.chosenMapPath, 'w') as file:
                file.write(new_content)

            # ----------S

            with open(game.chosenMapPath, 'r') as file:
                content = file.read()

            spawn_data_str = ""
            for s in game.activeSpawnZones:

                spawn_data_str += str(s[0]) + '/' + str(s[1]) + '/' + str(s[2]) + '/' + str(s[3]) + ','


            # Split the content into sections
            before_spawn, spawn_data, after_spawn = content.split('*SPAWN', 2)

            # Combine the sections back together with the updated enemy data
            new_content = before_spawn + '*SPAWN\n' + spawn_data_str + '\n*SPAWN' + after_spawn



            # Write the updated content back to the file
            with open(game.chosenMapPath, 'w') as file:
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

            for r in range(len(game.activeL1Data)):
                row = game.activeL1Data[r]
                for c in range(len(row)):
                    image = game.activeL1Data[r][c]
                    if(collidesObjectless(x,y,image.get_width(),image.get_height(),selectedArea[0],selectedArea[1],selectedArea[2],selectedArea[3])):
                        game.activeL1Data[r][c]            = self.tileReferenceData[self.selectedTileKey][self.selectedTileSubKey]
                        game.rawL1Data[r][c]               = self.selectedTileKey + '/' + self.selectedTileSubKey     



                    x += image.get_width()
                y+= image.get_height()
                x = 0


            self.boxCoords     = []
            print("Resetting box coords")


    def spawnZones(self,gui,game):
        
        if(self.currentLayer!='Q'):
            return()
        # ------ GET MAPTILE LIST
        game.activeSpawnZones

        # ------USES THE type and index as keys to gui.tileDict
        collidesWithExisting = False
        startingColour       = (20,30,70)
        collideIndex = 0
        for sz in range(len(game.activeSpawnZones)):
            spawnZone = game.activeSpawnZones[sz]
            # DELETE EXISTING IF CLICKED
            if(gui.mouseCollides(spawnZone[0]-gui.camX,spawnZone[1]-gui.camY,spawnZone[2],spawnZone[3])):
                collidesWithExisting = True
                collideIndex = sz

            # MERGE JOINT BOXES
            for sz2 in range(len(game.activeSpawnZones)):
                spawnZoneTwo = game.activeSpawnZones[sz2]
                if(sz==sz2):
                    pass
                elif(collidesObjectless(spawnZone[0],spawnZone[1],spawnZone[2],spawnZone[3], spawnZoneTwo[0],spawnZoneTwo[1],spawnZoneTwo[2],spawnZoneTwo[3])):
                    rhs = max((spawnZone[0] + spawnZone[2]),(spawnZoneTwo[0] + spawnZoneTwo[2]))
                    bhs = max((spawnZone[1] + spawnZone[3]),(spawnZoneTwo[1] + spawnZoneTwo[3]))
                    nbx = min(spawnZone[0],spawnZoneTwo[0])
                    nby = min(spawnZone[1],spawnZoneTwo[1])
                    
                    newBox = [nbx,nby,rhs-nbx,bhs-nby]
                    print([sz,sz2])
                    print("{} and {} collide".format(str(spawnZone),str(spawnZone)))
                    # DELETE OLD BOXES
                    game.activeSpawnZones.remove(spawnZone)
                    game.activeSpawnZones.remove(spawnZoneTwo)
                    game.activeSpawnZones.append(newBox)
                    return()


            # DRAW SPAWN ZONE
            pygame.draw.rect(gui.screen,startingColour,(spawnZone[0]-gui.camX,spawnZone[1]-gui.camY,spawnZone[2],spawnZone[3]))
            startingColour  = lighten(startingColour)
            drawTextWithBackground(gui.screen,gui.font,str(sz),spawnZone[0]-gui.camX + 0.4*spawnZone[2],spawnZone[1]-gui.camY + 0.3*spawnZone[3],textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))



        # ------MAKE A SPAWN ZONE BY DRAGGING MOUSE


        if(collidesWithExisting and gui.clicked):
            print('deleting ' + str(collideIndex))
            del game.activeSpawnZones[collideIndex]
            gui.pressed=False
            gui.clicked = False
            return()
        elif(self.updateTileEnabled==True and gui.scrollEnabled):
            self.spawnBoxSelector(gui,game)


    def spawnBoxSelector(self,gui,game):

        # SELECTING UNITS 
        selectedArea = self.dragSelect.dragSelect(gui,gui.camX,gui.camY)
        if(selectedArea!=None):
            if(selectedArea[2] > 1 and selectedArea[3] > 1):
                game.activeSpawnZones.append(selectedArea)


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

        if(gui.camX+gui.camW>game.mapWidth): gui.camX = game.mapWidth - gui.camW
        if(gui.camY+gui.camH>game.mapHeight): gui.camY = game.mapHeight - gui.camH

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




