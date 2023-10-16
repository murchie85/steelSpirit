from utils._utils import *
from utils._utils import stopTimer
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


        # ----create map variables

        self.initMapQuestions   = True
        self.questionCursor     = 0
        self.questionsComplete  = False
        self.chosenGameMap      = None
        self.answerList         = []



        # EDITOR


        self.mapLoaded          = False
        self.selectedTileKey    = 'template'
        self.selectedTileSubKey = 'base100_1'
        self.multiSelect        = False

        self.selectedL2Key      = 'objectTiles'
        self.selectedL2SubKey   = 'obj1'

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
        self.currentLayer        = 'l1'


        self.tileReferenceData   = None
        self.selectedTileKey     = None
        self.selectedTileSubKey  = None
        
        self.layer2RefData       = None
        self.layer2RefDataScaled = None
        self.selectedL2Key       = None
        self.selectedL2SubKey    = None
        
        self.enemyRefData        = None
        self.selectedEnemyKey    = None 
        self.selectedEnemySubKey = None


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
            
            raw_map_data,map_l2_data,map_enemy_data = loadUnconverted(game.chosenMapPath)
            game.rawL1Data    = raw_map_data
            game.rawL2Data    = map_l2_data
            game.rawEnemyData = map_enemy_data
            
            # This is the data that matters
            self.tileReferenceData,game.activeL1Data                          = loadMapRefData(gui,game)
            self.layer2RefData, game.activeL2Data,self.layer2RefDataScaled    = loadLayer2RefData(gui,game)
            self.enemyRefData,game.activeEnemyData                            = loadEnemyRefData(gui,game)



            self.mapLoaded = True

        #---------------------------CAMERA AND SIZING

        hoveredTile = self.tileReferenceData[self.selectedTileKey][self.selectedTileSubKey]

        sampleTile = game.activeL1Data[1][2] # A tile representative of the height/width

        self.tileWidth  = sampleTile.get_width()
        self.tileHeight = sampleTile.get_height()

        startX,startY= 0,0
        gui.moveCamera(game)


        # These get overriden by any layer below
        gui.scrollEnabled      = True

        #----------------------------MAP RENDERING

        self.renderLayer1Map(gui,game,startX,startY,hoveredTile)
        self.renderLayer2Map(gui,game,startX,startY)

        self.updateTileEnabled = True
        self.showTileListL1(gui,sampleTile)
        self.showTileListL2(gui,sampleTile)
        self.showEnemyList(gui,sampleTile)

        self.sideMenu(gui,sampleTile)

        self.buttonSelection(gui,game,hoveredTile)

        
        #-------LOAD
        self.loadGameLogic(gui)

        #------------SAVE
        self.saveGameLogic(gui,game)




    def buttonSelection(self,gui,game,hoveredTile):

        #----------------------------MAP OPTIONS
        if(self.currentLayer=='l1'):
            if(gui.input.returnedKey.upper()=='W'):
                self.selectedTileSubKey = get_next_subkey(self.tileReferenceData, self.selectedTileKey, self.selectedTileSubKey)
            if(gui.input.returnedKey.upper()=='S'):
                self.selectedTileSubKey = get_previous_subkey(self.tileReferenceData, self.selectedTileKey, self.selectedTileSubKey)
            if(gui.input.returnedKey.upper()=='D'):
                self.selectedTileKey = get_next_tile_key(self.tileReferenceData, self.selectedTileKey)
                self.selectedTileSubKey = list(self.tileReferenceData[self.selectedTileKey].keys())[0]
                self.tileCursor =0
            if(gui.input.returnedKey.upper()=='A'):
                self.selectedTileKey = get_previous_tile_key(self.tileReferenceData, self.selectedTileKey)
                self.selectedTileSubKey = list(self.tileReferenceData[self.selectedTileKey].keys())[0]
                self.tileCursor =0
        
        if(self.currentLayer=='l2'):
            if(gui.input.returnedKey.upper()=='W'):
                self.selectedL2SubKey = get_next_subkey(self.layer2RefData, self.selectedL2Key, self.selectedL2SubKey)
            if(gui.input.returnedKey.upper()=='S'):
                self.selectedL2SubKey = get_previous_subkey(self.layer2RefData, self.selectedL2Key, self.selectedL2SubKey)
            if(gui.input.returnedKey.upper()=='D'):
                self.selectedL2Key = get_next_tile_key(self.layer2RefData, self.selectedL2Key)
                self.selectedL2SubKey = list(self.layer2RefData[self.selectedL2Key].keys())[0]
                self.tileCursor =0
            if(gui.input.returnedKey.upper()=='A'):
                self.selectedL2Key = get_previous_tile_key(self.layer2RefData, self.selectedL2Key)
                self.selectedL2SubKey = list(self.layer2RefData[self.selectedL2Key].keys())[0]
                self.tileCursor =0

        if(self.currentLayer=='E'):
            if(gui.input.returnedKey.upper()=='W'):
                self.selectedEnemySubKey = get_next_subkey(self.enemyRefData, self.selectedEnemyKey, self.selectedEnemySubKey)
            if(gui.input.returnedKey.upper()=='S'):
                self.selectedEnemySubKey = get_previous_subkey(self.enemyRefData, self.selectedEnemyKey, self.selectedEnemySubKey)
            if(gui.input.returnedKey.upper()=='D'):
                self.selectedEnemyKey = get_next_tile_key(self.enemyRefData, self.selectedEnemyKey)
                self.selectedEnemySubKey = list(self.enemyRefData[self.selectedEnemyKey].keys())[0]
                self.tileCursor =0
            if(gui.input.returnedKey.upper()=='A'):
                self.selectedEnemyKey = get_previous_tile_key(self.enemyRefData, self.selectedEnemyKey)
                self.selectedEnemySubKey = list(self.enemyRefData[self.selectedEnemyKey].keys())[0]
                self.tileCursor =0





        if(gui.input.returnedKey.upper()=='H'):
            gui.camX = 0
            gui.camY = 0




    def sideMenu(self,gui,sampleTile):


        

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
                        drawImage(gui.screen, self.enemyRefData[self.selectedEnemyKey][subkeys[tileIndex]]['image'], (startX, startY))

                    # HIGHLIGHT / SELECTED
                    if(gui.mouseCollides(startX,startY,tileLen,tileHeight)):
                        self.updateTileEnabled = False
                        gui.scrollEnabled = False
                        pygame.draw.rect(gui.screen, (180,180,200), [startX, startY,tileLen, tileHeight],4)
                        if(gui.clicked):
                            self.selectedEnemyKey = subkeys[tileIndex]
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










    def renderLayer1Map(self,gui,game,startX,startY,hoveredTile):

        if(gui.pressed==False): self.multiSelect = False

        rows = len(game.activeL1Data)    
        cols = len(game.activeL1Data[0]) 

        # RENDER LAYER ONE  

        for row in range(rows):
            for col in range(cols):
                x = startX + (col * self.tileWidth )  # 50 pixels
                y = startY + (row * self.tileHeight) # 50 pixels

                # DRAW HOVERED TILE 
                if(gui.mouseCollides(x-gui.camX,y-gui.camY ,self.tileWidth ,self.tileHeight) and self.currentLayer=='l1'):
                    drawImage(gui.screen, hoveredTile, (x -gui.camX,y-gui.camY ))
                    
                    #--------UPDATE TILE 

                    if(self.multiSelect):
                        game.activeL1Data[row][col]            = hoveredTile
                        game.rawL1Data[row][col] = self.selectedTileKey + '/' + self.selectedTileSubKey
                    
                    if(gui.clicked and self.updateTileEnabled):
                        game.activeL1Data[row][col]            = hoveredTile
                        game.rawL1Data[row][col] = self.selectedTileKey + '/' + self.selectedTileSubKey
                        if(gui.pressed):
                            self.multiSelect = True
                else:
                    # ONLY DRAW INBOUNDS IF CHECK ENABLED 
                    if(self.check):
                        if(x - gui.camX > -100 and x - gui.camX < gui.w  and y - gui.camY > -100 and y - gui.camY < gui.h + 100):
                            drawImage(gui.screen, game.activeL1Data[row][col], (x - gui.camX, y - gui.camY))
                    else:
                        drawImage(gui.screen, game.activeL1Data[row][col], (x - gui.camX, y - gui.camY))

            #------REPLACE ALL TILES
            if(gui.input.returnedKey.upper()=='R'):
                for row in range(rows):
                    for col in range(cols):
                        x = startX + (col * self.tileWidth )
                        y = startY + (row* self.tileHeight )
                        game.activeL1Data[row][col]            = hoveredTile
                        game.rawL1Data[row][col] = self.selectedTileKey + '/' + self.selectedTileSubKey

                


    def renderLayer2Map(self,gui,game,startX,startY):

        if(self.currentLayer=='l1'):
            return()

        # RENDER LAYER 2

        if(self.currentLayer in ['l2','E','Q']):
            for item in game.activeL2Data:
                pass

        
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
                if(gui.mouseCollides(item[0]-gui.camX,item[1]-gui.camY,item[2].get_width(),item[2].get_height())):
                    pygame.draw.rect(gui.screen, (180,180,120), [item[0]-gui.camX,item[1]-gui.camY,item[2].get_width(),item[2].get_height()],4)
                    deleteHover = True
                    if(gui.clicked):    
                        game.activeL2Data.pop(i)

            # ADD TILE TO LIST
            nothingSelected = True
            if(gui.clicked and nothingSelected and not deleteHover and self.updateTileEnabled):
                game.activeL2Data.append([gui.mx+gui.camX, gui.my+gui.camY, selectedTile, self.selectedL2Key,self.selectedL2SubKey])
                print("Added: " + str([selectedTile,gui.mx-gui.camX,gui.my-gui.camY,self.selectedL2Key,self.selectedL2SubKey ]))





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


            # ----------L2

            # Split the content into sections
            before_l2, l2_data, after_l2 = content.split('*L2', 2)

            # Convert new_l2_data to the desired string format, ignoring the pygame object
            new_l2_data_str = ','.join(['/'.join(map(str, row[:2] + row[3:])) for row in game.activeL2Data])

            # Combine the sections back together with the updated l2_data
            new_content = before_l2 + '*L2\n' + new_l2_data_str + '\n*L2' + after_l2




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




