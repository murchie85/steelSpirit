from utils._utils import drawImage,getTextWidth,getTextHeight,drawTextWithBackground
from utils.gameUtils import *
from units.scout import *
from units.hind import *
from units.tank import *
from units.snowTank import *
from units.greenTank import *
from units.attackBoat import *
from units.aaSmall import *
from units.mlrs import *
from units.frigate import *
from units.powerDrone import *
from buildings.bioLab import *
from buildings.samSite import *
from buildings.barrelRed import *
from buildings.nonInteractable import *
from scenes.cutSceneGui import * 
from units.player import *




class ruralAssault():

    def __init__(self,gui,parent):
        self.name          = 'ruralAssault'
        self.player        = player(gui)
        self.chosenMapName = 'rural Assault'
        self.chosenMapPath = None
        """
        GIVES; GAME .activeL1Data, activeL2Data,activeAnimatedData,activeEnemyData,activeSpawnZones
        self. tileReferenceData, layer2RefData, layer2RefDataScaled,animatedRefData, enemyRefData
        """
        self.gameMap = {}
        
        self.gameMap['l1']               = parent.activeL1Data
        self.gameMap['l2']               = parent.activeL2Data
        self.gameMap['animatedObjects']  = parent.activeAnimatedData
        self.gameMap['enemies']          = parent.activeEnemyData
        self.gameMap['spawnZones']       = parent.activeSpawnZones
        self.gameMap['quadrants']        = parent.activeQuadrants

        self.tileWidth,self.tileHeight   = parent.tileWidth,parent.tileHeight
        self.mapx,self.mapy              = 0,0
        self.mapw,self.maph              = parent.mapWidth,parent.mapHeight



        # -------GUI STUFF

        self.healthBar             = loadingBarClass(80,10,(27,40,55),(220,220,220),(0,0,200))
        self.objectiveArrow        = imageAnimateAdvanced(gui.objectiveArrow,0.2)
        self.displayObjectiveArrow = False 
        self.showObjectiveTimer    = stopTimer()
        self.arrowCount            = 0
        
        # MASK
        self.guiBoxW,self.guiBoxH = 0.15*gui.w, 0.15*gui.h
        self.guiBoxX,self.guiBoxY = 0.01*gui.w, gui.h - 1.1*self.guiBoxH
        self.guiboxMask           = pygame.Surface((self.guiBoxW,self.guiBoxH))
        self.guiboxMaskFill       = 36,69,115
        self.alphaI               = 50
        self.hideGuiBox           = False




        # --------------CORE DATA

        self.bulletList         = []
        self.plumeList          = []
        self.allyList           = []
        self.enemyList          = []
        self.enemyComponentList = [] # THINGS LIKE TURRETS ETC
        self.unfieldedEnemies   = [] # this contains remaining enemies to put on the  board
        self.defaultEnemyList   = [] # This contains a backup
        
        # ENEMIES AND MISSILES ARE ADDED TO THIS
        self.deadList           = []
        self.terrainList        = []
        self.fids               = [1]

        self.log              = []
        self.remainingEnemies = None
        self.holdGame         = False
        self.gamePaused       = False

        self.enemyDestroyed = False


        # i define this 
        expectedLenSpawnZones      = 3
        if(len(self.gameMap['spawnZones'])<expectedLenSpawnZones):
            print("*************WARNING*******************")
            print("not all spawn zones configured")
            for i in range(expectedLenSpawnZones):
                self.gameMap['spawnZones'].append([0,0,100,100])
        expectedQuadrants      = 1
        if(len(self.gameMap['quadrants'])<expectedQuadrants):
            print("*************WARNING*******************")
            print("not all quadrantsconfigured")
            for i in range(expectedQuadrants):
                self.gameMap['quadrants'].append([0,0,100,100])



        # -------SPAWN ZONES
        self.spawn_1           = {'spawnCount': 1,
                                  'spawnIndex':0, 
                                  'spawn' : [{'type': 'hind','count':3, 'direction': 'front','spawnLocation':self.gameMap['spawnZones'][0]}]}
        self.spawn_2           = {'spawnCount': 2,
                                  'spawnIndex':0, 
                                  'spawn' : [{'type': 'hind','count':4, 'direction': 'front','spawnLocation': self.gameMap['spawnZones'][1]}, 
                                             {'type': 'hind','count':7, 'direction': 'front','spawnLocation': self.gameMap['spawnZones'][2]}]}


        self.playerStartPosition = [4167,10786]
        self.objectives        = {'firstWave': {'objective':'eliminate',
                                                'targetObjects':[], 
                                                'status': 'notStarted', 
                                                'nextObjective':'destroyBase',
                                                'holdGame':False, 
                                                'startMessage':'Rookie, clear a path into the base, good luck!', 
                                                'audio':gui.cutsceneAudio['ruralAssault']['scene1'],
                                                'completionMessage': 'Nicely done!',
                                                'activeQuandrant': {'x':self.gameMap['quadrants'][0][0],'w':self.gameMap['quadrants'][0][2] ,'y':self.gameMap['quadrants'][0][1],'h':self.gameMap['quadrants'][0][3]},
                                                'enemySpawn':self.spawn_1},
                                   'destroyBase': {'objective':'eliminate',
                                                    'targetObjects':[], 
                                                    'status': 'notStarted', 
                                                    'nextObjective':'complete',
                                                    'holdGame':False,  
                                                    'startMessage':'Get to the resupply base and take out those siloes.', 
                                                    'completionMessage': 'Great job! Our forces can carry on unimpeded, make your way to the next objective.',
                                                    'activeQuandrant': {'x':self.gameMap['quadrants'][0][0],'w':self.gameMap['quadrants'][0][2] ,'y':self.gameMap['quadrants'][0][1],'h':self.gameMap['quadrants'][0][3]},
                                                    'enemySpawn':self.spawn_2 },
                                  }
        self.objectiveKeyNames       = list(self.objectives.keys())
        
        self.currentObjective    = 'firstWave'
        self.objectiveIntroState = 'notIntroduced'
        self.objectiveTimer      = countUpTimer()
        self.spawnIndex          = 0 # index of the enemy spawn list
        self.spawnDelayTimer     = stopTimer()
        self.spawnDelay          = 3

        # ------ LEVEL TIMER 

        self.levelTimer      = countUpTimer()
        self.alarmTime       = 10
        self.timeRemaining   = 10
        

        # CUTSCENE STUFF

        self.scene      = 'debug'
        self.state      ='NOT_STARTED'
        self.audioState = None
        self.musicDelay = stopTimer()
    def run(self,gui,game):


        # ----- 
        if(self.state=='NOT_STARTED'):
            self.setUpLevel(gui,game)
            return()

        

        # ------MAIN LOOP 
        self.drawMap(gui,game)


        # ----PAUSE GAME 

        self.pauseGame(gui,game)




        if(not self.holdGame):


            #-----Death animations


            for dead in self.deadList:
                if(dead.alive==False):

                    # DRAW STREWN CARCAS
                    if(hasattr(dead,'drawRemains')):
                        dead.drawRemains(gui,self,game)

                    # SHAKE CAMERA ONCE
                    if(dead.name.upper() in ['TANK','MLRS','FRIGATE']):
                        if(not hasattr(dead,'deathShake')):
                            dead.deathShake = False
                        elif(dead.deathShake == False):
                            # Initiates shake and Will be reset by player
                            self.enemyDestroyed = True
                            dead.deathShake = True

                    # DRAW DEATH EXPLOSION
                    dead.animateDestruction(gui,self,game)

                    # SPAWN POWERUP
                    if(hasattr(dead,'itemDrop')):
                        if(dead.itemDrop=='PowerUp'):
                            self.enemyList.append(powerDrone(createFid(self),gui,x=dead.x,y=dead.y))
                            dead.itemDrop = 'None'

                    if(hasattr(dead,'pointsAwarded')):
                        if(dead.pointsAwarded==False):
                            self.player.score += dead.killScore
                            dead.pointsAwarded = True

            # ------DISPLAY OBJECTIVES 


            if('O' in gui.input.returnedKey.upper()):
                print('displaying objective arrow')
                self.displayObjectiveArrow = True


            # ------BULLET MANAGER

            for bullet in self.bulletList:

                # check if bullet hits any enemies
                for enemy in self.enemyList:

                    if(collidesWithHitBox(bullet,enemy)):
                        bullet.bulletCollides(enemy,gui,self)
                
                # check if bullet hits any enemies
                for ally in self.allyList:

                    if(collidesWithHitBox(bullet,ally)):
                        bullet.bulletCollides(ally,gui,self)

                # move bullet
                bullet.drawSelf(gui,game,self)
                bullet.move(gui,self,game)

            
            # ----PLAYER 

            self.player.drawSelf(gui,game,self)
            if(self.player.alive): 
                self.player.actions(gui,game,self)


            # ------MISSILE PLUME


            for plume in self.plumeList:
                plume.drawSelf(gui,game,self)

            # DRAW ANIMATED TERRAIN
            for terrain in self.terrainList:
                terrain.drawSelf(gui,game,self)


            # ENEMY ACTIONS

            for enemy in self.enemyList:
                enemy.drawSelf(gui,game,self)
                enemy.actions(gui,game,self)

                manageCollisions(self,enemy,gui,game)
                # Note: bullet kills the enemy


        if(self.holdGame):
            self.player.drawSelf(gui,game,self)




        # -----DRAW OVERLAYS 

        levelGui(self,gui,game)



        # ------MANAGE GAME SCENES

        self.gameScenes(gui,game)       

        # ------DRAG PLAYER TO REGION

        self.quandrantManager(gui,game) 

        # OBJECTIVE MANAGER  
        self.objectiveManager(gui,game)

        # ENEMY SPAWNER
        #self.enemySpawnManager(gui,game)








    # INIT LEVEL DESIGN 

    def setUpLevel(self,gui,game):


        # ------------SET PLAYER COORDS

        self.player.x = self.playerStartPosition[0]
        self.player.y = self.playerStartPosition[1]

        
        #--------------ADD ENEMIES

        self.addEnemies(self.gameMap['enemies'],gui)


        #--------------ADD TERRAIN

        for a in self.gameMap['animatedObjects']:
            self.terrainList.append(a['classObject'])
        
        #--------------ADD PLAYER

        self.allyList.append(self.player)
        

        # -------------- UPDATE TARGET OBJECTIVES

        for objective in self.objectiveKeyNames:
            for enemy in self.enemyList:
                if(hasattr(enemy,'assignedObjective')):
                    if(objective ==enemy.assignedObjective):
                        print('Appending enemy ' + str(enemy.id) + ' to objective ' + str(objective))
                        self.objectives[objective]['targetObjects'].append(enemy.id)

        self.state= ' start'
        return()




    def addEnemies(self,enemies,gui):


        for e in enemies:

            x,y = e['x'], e['y']
            if(e['enemySubKeyName']=='scout'):
                enemyObject = scout(createFid(self),gui,x=x,y=y)
                enemyObject.killScore =100
            if(e['enemySubKeyName']=='scout'):
                enemyObject = scout(createFid(self),gui,x=x,y=y)
            if(e['enemySubKeyName']=='hind'):
                enemyObject = hind(createFid(self),gui,x=x,y=y)
                enemyObject.killScore =100
            elif(e['enemySubKeyName']=='tank'):
                enemyObject = tank(createFid(self),gui,x=x,y=y)
                enemyObject.killScore = 200
            elif(e['enemySubKeyName']=='snowTank'):
                enemyObject = snowTank(createFid(self),gui,x=x,y=y)
                enemyObject.killScore = 300
            elif(e['enemySubKeyName']=='attackBoat'):
                enemyObject = attackBoat(createFid(self),gui,x=x,y=y)
                enemyObject.killScore =150
            elif(e['enemySubKeyName']=='greenTank'):
                enemyObject = greenTank(createFid(self),gui,x=x,y=y)
                enemyObject.killScore =150
            elif(e['enemySubKeyName']=='aaSmall'):
                enemyObject = aaSmall(createFid(self),gui,x=x,y=y)
                enemyObject.killScore =300
            elif(e['enemySubKeyName']=='mlrs'):
                enemyObject = mlrs(createFid(self),gui,x=x,y=y)
                enemyObject.killScore = 500
            elif(e['enemySubKeyName']=='frigate'):
                enemyObject = frigate(createFid(self),gui,self,x=x,y=y)
                enemyObject.killScore = 1000
            elif(e['enemySubKeyName']=='powerDrone'):
                enemyObject = powerDrone(createFid(self),gui,x=x,y=y)
                enemyObject.killScore = 0

            elif(e['enemySubKeyName']=='bioLab'):
                enemyObject = bioLab(createFid(self),gui,x=x,y=y)
                enemyObject.killScore = 500
            elif(e['enemySubKeyName']=='samSite'):
                enemyObject = samSite(createFid(self),gui,x=x,y=y)
                enemyObject.killScore = 300
            elif(e['enemySubKeyName']=='barrelRed'):
                enemyObject = barrelRed(createFid(self),gui,x=x,y=y)
                enemyObject.killScore = 0
            
            enemyObject.facing            = wrapAngle(e['rotation'])
            
            enemyObject.patrolLocations   = e['patrolRoute']
            
            enemyObject.assignedObjective = e['assignedObjective']

            enemyObject.itemDrop          = e['itemDrop']


            self.enemyList.append(enemyObject)
            print(enemyObject.name + " Added to the board")
            print(enemyObject.patrolLocations)


    def eliminateObjectives(self,currentObjective):
        if(currentObjective['objective']=='eliminate'):
            deadListIDs = [x.id for x in self.deadList]
            
            for targetiD in currentObjective['targetObjects']:
                # if target dead or already removed from the enemy list
                if(targetiD in deadListIDs):
                    currentObjective['targetObjects'].remove(targetiD)


        # -----SIGNAL OBJECTIVE COMPLETE
        if(currentObjective['objective']=='eliminate'):
            if(len(currentObjective['targetObjects'])<=0):
                currentObjective['status'] = 'signalComplete'



    def drawMap(self,gui,game):
        startX,startY = 0,0

        #--------------LAYER ONE
        for row in range(len(self.gameMap['l1'])):
            for col in range(len(self.gameMap['l1'][0])):
                x =  startX + (col * self.tileWidth)  # 50 pixels
                y =  startY + (row * self.tileHeight) # 50 pixels

                if(x<gui.camX-50 or x>gui.camX +gui.camW+50):
                    continue
                if(y<gui.camY-50 or y>gui.camY +gui.camH+50):
                    continue

                drawImage(gui.screen, self.gameMap['l1'][row][col], (x - gui.camX, y - gui.camY))


        #--------------LAYER TWO (TILELESS)

        for i in range(len(self.gameMap['l2'])):
            item = self.gameMap['l2'][i]
            x,y = item[0],item[1]
            if x + item[2].get_width() < gui.camX - 100 or x  > gui.camX + gui.camW + 100:
                continue
            if y + item[2].get_height()  < gui.camY - 100 or y  > gui.camY + gui.camH + 100:
                continue
            drawImage(gui.screen, item[2], (x-gui.camX,y-gui.camY))


        #--------------ANIMATED LAYER

        for i in range(len(self.gameMap['animatedObjects'])):
            currentAnimatedObject = self.gameMap['animatedObjects'][i]
            objClass = currentAnimatedObject['classObject']

            # Assuming the `objClass` has 'x' and 'y' properties. Adjust as needed.
            if objClass.x + objClass.w < gui.camX - 100 or objClass.x  > gui.camX + gui.camW + 100:
                continue
            if objClass.y + objClass.h < gui.camY - 100 or objClass.y > gui.camY + gui.camH + 100:
                continue


            objClass.drawSelf(gui,game)





    def quandrantManager(self,gui,game):

        # ----CLAMP PLAYER IN CURRENT QUADRANT
        if(self.currentObjective!= None and self.currentObjective != 'complete'):
            currentObjective = self.objectives[self.currentObjective]
            activeQuandrant  = currentObjective['activeQuandrant']

            self.player.leftBoundary  = activeQuandrant['x'] 
            self.player.rightBoundary  = activeQuandrant['x'] + activeQuandrant['w']
            self.player.topBoundary    = activeQuandrant['y']
            self.player.bottomBoundary = activeQuandrant['y'] + activeQuandrant['h'] - self.player.h



    def pauseGame(self,gui,game):
        
        # IF GAME PAUSED
        if(self.gamePaused):
            self.holdGame   = True
            drawTextWithBackground(gui.screen,gui.bigFont,str('Paused'),850,400 ,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))
            if(gui.input.returnedKey=='return'):
                gui.input.returnedKey = ''
                self.gamePaused = False
                self.holdGame   = False
            return()

        # PAUSE GAME
        if(gui.input.returnedKey=='return' and self.scene in ['gameUnderway','debug']):
            
            self.gamePaused = True


    def gameScenes(self,gui,game):
        
        # ADDS THE CUTSCENE CLASS TO THIS CLASS
        if(hasattr(self, 'cutScene')==False):
            self.cutScene = cutScene(gui)




        # ------------ INTRO AND EXIT   

        # COUNT INTO SCENE 1
        if(self.scene=='start'):
            alarmTime = 1
            complete,secondsCounted = self.levelTimer.countRealSeconds(alarmTime,game)
            if(complete):
                self.levelTimer.counter = 0
                self.levelTimer.reset(3)
                self.scene ='claire'

    

        if(self.scene=='claire'):
            self.holdGame = True

            # OPEN WINDOW
            self.cutScene.runCutScene(gui,game,scene='ally',underlay=True)


            # ANIMATE ONCE WINDOW OPEN
            if(self.cutScene.pannelOpen):
                gui.claireTalking.animateNoRotation(gui,'claireTalking',[self.cutScene.imageLeftX,self.cutScene.imageY],game)
                self.cutScene.drawMask(gui,game,overlay=False,border='ally',codec=True)
                finished = self.cutScene.dialogue.drawScrollingDialogue(gui,game,self.cutScene.textW,self.cutScene.textH,gui.smallishFont, "Welcome to training rookie, time to learn the ropes. You have a number of air, land and sea targets. Get going, good luck. Remember you will go into automatic lockon mode which changes your button inputs, press y to toggle lockon on and off.", textStartingPos=(self.cutScene.textX ,self.cutScene.textY),colour=(255,255,255),closeOutDelay=True)
                if(finished):
                    self.scene    ='gameUnderway'
                    self.holdGame = False
                    self.cutScene.reset()



        # MOVE INTO FINISH LEVEL CUTCENE 
        ##if(self.scene =='gameUnderway' and self.remainingEnemies <=0): self.scene = 'levelComplete'

        # FINISH NOTIFICATION
        if(self.scene=='levelComplete'):
            complete,secondsCounted = self.levelTimer.countRealSeconds(3,game)
            if(not complete):
                return()
            else:
                self.scene = 'notifyLevelComplete'
                return()
    
        if(self.scene=='notifyLevelComplete'):
            self.cutScene.runCutScene(gui,game,scene='ally',underlay=True)
            if(self.cutScene.pannelOpen):
                gui.claireTalking.animateNoRotation(gui,'claireTalking',[self.cutScene.imageLeftX,self.cutScene.imageY],game)
                self.cutScene.drawMask(gui,game,overlay=False,border='ally',codec=True)
                
                finished = self.cutScene.dialogue.drawScrollingDialogue(gui,game,self.cutScene.textW,self.cutScene.textH,gui.font, "Hah not bad, this is still a Beta game in very early development, but try out level 2 for more of a challenge.", textStartingPos=(self.cutScene.textX ,self.cutScene.textY),colour=(255,255,255),closeOutDelay=True)
                
                if(finished):
                    print('stage complete, not managed closure yet')
                    exit(0)
                    self.cutScene.pannelOpen = False
                    self.cutScene.reset()


    def objectiveManager(self,gui,game):

        # -----DONT PROCEED IF LEVEL COMPLETE 

        if(self.currentObjective==None or self.currentObjective=='complete'):
            if(self.scene!='levelComplete' and self.scene!='notifyLevelComplete'):
                self.scene = 'levelComplete'
            return()

        if(self.scene=='levelComplete' or self.scene=='notifyLevelComplete'):
            return()

    
        currentObjective = self.objectives[self.currentObjective]

        # COUNT IN TIMER FOR EACH OBJECTIVE
        if(self.objectiveIntroState=='notIntroduced' and currentObjective['status']=='notStarted'):
            complete,secondsCounted = self.objectiveTimer.countRealSeconds(1,game)
            if(not complete):
                return()
            if(complete):
                self.objectiveTimer.counter = 0
                self.objectiveIntroState='introduced'





        # ----INTRODUCE NEXT OBJECTIVE 
        
        if(currentObjective['status']=='notStarted'):
            
            if(currentObjective['holdGame']):
                self.holdGame = True
            
            sceneMessage = currentObjective['startMessage']
            # OPEN WINDOW
            self.cutScene.runRHSCutScene(gui,game,scene='ally',underlay=True,orientation='topRight')
            
            # ANIMATE ONCE WINDOW OPEN
            if(self.cutScene.pannelOpen):
                self.displayObjectiveArrow = True
                gui.claireTalking.animateNoRotation(gui,'claireTalking',[self.cutScene.imageLeftX,self.cutScene.imageY],game)
                self.cutScene.drawMask(gui,game,overlay=False,border='ally',codec=True)
                

                if('audio' in currentObjective.keys() and self.audioState==None):
                    playMusic = self.musicDelay.stopWatch(1,'audio  ' + str(currentObjective['audio']), str(currentObjective['audio']),game,silence=True)
                    if(playMusic):
                        gui.musicPlayer.play(currentObjective['audio'])
                        self.audioState = 'playing'

                finished = self.cutScene.dialogue.drawScrollingDialogue(gui,game,self.cutScene.textW,self.cutScene.textH,gui.smallFont, sceneMessage, textStartingPos=(self.cutScene.textX ,self.cutScene.textY),colour=(51,189,251),closeOutDelay=True,maxLines=4,scrollInterval=0.02,pageWait=3)

                if(finished):
                    currentObjective['status'] = 'inProgress'
                    if(currentObjective['holdGame']):
                        self.holdGame = False
                        self.audioState = None
                    
                    self.cutScene.reset()

        # -----REMOVE DEAD ENEMIES FROM TARGET


        self.eliminateObjectives(currentObjective)


        # ----  NEXT OBJECTIVE, CONGRATULATE and POPULATE NEW OBJECTIVE TARGETS

        if(currentObjective['status']=='signalComplete'):
            skipOutro = False
            sceneMessage = currentObjective['completionMessage']
            if('skipme' in sceneMessage): skipOutro = True

            # OPEN WINDOW
            self.cutScene.runRHSCutScene(gui,game,scene='ally',underlay=True,orientation='topRight')
            # ANIMATE ONCE WINDOW OPEN
            if(self.cutScene.pannelOpen):
                gui.clareSmiling.animateNoRotation(gui,'claireTalking',[self.cutScene.imageLeftX,self.cutScene.imageY],game,repeat=False)
                
                self.cutScene.drawMask(gui,game,overlay=False,border='ally',codec=True)
                finished = self.cutScene.dialogue.drawScrollingDialogue(gui,game,self.cutScene.textW,self.cutScene.textH,gui.smallFont, sceneMessage, textStartingPos=(self.cutScene.textX ,self.cutScene.textY),colour=(51,189,251),closeOutDelay=True,maxLines=4,scrollInterval=0.02,pageWait=2)
                
                if(finished or skipOutro):
                    #NEXT OBJECTIVE 
                    currentObjective['status'] = 'complete'
                    self.currentObjective = currentObjective['nextObjective']
                    
                    # UNPAUSE AND RESET CUTSCENE STATE
                    self.cutScene.reset()

                    self.objectiveIntroState='notIntroduced'

                    # IF ALL OBJECTIVES COMPLETE
                    if(self.currentObjective==None or self.currentObjective=='complete'):
                        self.scene = 'levelComplete'
                    else:
                        self.fieldNewObjective(gui,game)

        


    # ------********LEVEL SPECIFIC OBJECTIVE LOADING ******

    def fieldNewObjective(self,gui,game):

        # QUANDRANT AREA AND CURRENT OBJECIVE

        currentObjective = self.objectives[self.currentObjective]
        activeQuandrant  = currentObjective['activeQuandrant']
        

        # MODIFY ENEMY LIST TO ACTIVE ENEMIES ONLY
        for enemy in self.unfieldedEnemies:
            if(inQuandrant(enemy, activeQuandrant)):
                self.enemyList.append(enemy)


        # REBUILDING LIST DUE TO COMPLEXITY WITH HOLDING DICTS

        newList = []
        for u in range(len(self.unfieldedEnemies)):
            uE = self.unfieldedEnemies[u]
            remove= False
            
            for el in self.enemyList:
                if(el.id==uE.id and el.name ==uE.name):
                    remove=True
            if(remove==False):
                newList.append(uE)

        self.unfieldedEnemies = newList



    # MANAGES ENEMY SPAWN
    def enemySpawnManager(self,gui,game):

        # ONLY CALL IF THERE IS AN OBJECTIVE
        if(self.currentObjective!= None and self.currentObjective != 'complete'):
            currentObjective = self.objectives[self.currentObjective]
            # 'enemySpawn':{'spawnCount': 3,  'spawn' : [{'type': 'hind','count':5, 'direction': 'front','spawnLocation': {'x':0 ,'w':self.mapw ,'y':0 ,'h':self.maph-400}}, {'type': 'hind','count':5, 'direction': 'back','spawnLocation': {'x':0 ,'w':self.mapw ,'y':0 ,'h':self.maph-400}},{'type': 'hind','count':5, 'direction': 'any','spawnLocation': {'x':0 ,'w':self.mapw ,'y':0 ,'h':self.maph-400}} ]}
            
            # IF ENEMY SPAWN IS SET
            if('enemySpawn' in currentObjective.keys()):
                enemySpawnDict = currentObjective['enemySpawn']
                
                # IF SPAWN AVAILABLE
                if(enemySpawnDict['spawnIndex']<=enemySpawnDict['spawnCount']-1):
                    
                    # TIMER DELAY - DON'T GO THROUGH ALL SPAWN LIST T ONCE
                    spawnReady = self.spawnDelayTimer.stopWatch(self.spawnDelay,'spawning group ' + str(enemySpawnDict['spawnIndex']), str(enemySpawnDict['spawnIndex']),game,silence=True)

                    if(spawnReady):
                        currentSpawn = enemySpawnDict['spawn'][enemySpawnDict['spawnIndex']]

                        # check player in spawn location 
                        if(collidesWithObjectLess(currentSpawn['spawnLocation'][0],currentSpawn['spawnLocation'][1],currentSpawn['spawnLocation'][2],currentSpawn['spawnLocation'][3],self.player)):
                            print('Spawn number ' + str(enemySpawnDict['spawnIndex']) + 'in grid ' + str(currentSpawn))
                            #print('Spawning ' + str(currentSpawn))
                            if(currentSpawn['direction']=='front'):
                                for i in range(currentSpawn['count']):
                                    enemy = {'kind':currentSpawn['type'],'seekAndStrafe':True}
                                    
                                    # IF IN FRONT, ANYWHERE WITHIN X VALUE AND JUST OUT OF Y RANGE
                                    if(currentSpawn['direction']=='front'):
                                        
                                        xSpawn = self.player.x-0.5*gui.w + random.randrange(0,gui.w)
                                        if(xSpawn<0):xSpawn = 100
                                        if(xSpawn>self.mapw): xSpawn = self.mapw-100
                                        ySpawn = self.player.y - gui.h - random.randrange(0,0.5*gui.h)
                                        if(ySpawn<0): ySpawn = 100
                                        if(ySpawn>self.maph): ySpawn = self.maph - 100
                                        print('Adding enemy ' + str(enemy) + ' spawning at ' + str([xSpawn,ySpawn]))
                                        addEnemy(self,xSpawn,ySpawn,enemy,gui)

                            enemySpawnDict['spawnIndex']+=1


                    # if in spawn, spawn enemies 


                    # pick theirl ocation 

                    #  add to enemy list

                    # increment counter

                    # random timer 1-5 seconds







#------STAND ALONE FUNCTION BUT USES SELF

def levelGui(self,gui,game):



    # -------------GUI BOX

    
    if(self.hideGuiBox==False):
        
        # -------------GUI BOUNDING BOX

        self.guiboxMask.set_alpha(self.alphaI)
        self.guiboxMask.fill((self.guiboxMaskFill))
        gui.screen.blit(self.guiboxMask, (self.guiBoxX, self.guiBoxY))
        pygame.draw.rect(gui.screen, self.guiboxMaskFill, [self.guiBoxX, self.guiBoxY,self.guiBoxW, self.guiBoxH],4)


        # -------------PLAYER  SHIP ICON 

        shipImage = gui.shipHealthDisplay['100']
        x,y = self.guiBoxX + 0.07*self.guiBoxW, self.guiBoxY + 0.2*self.guiBoxH
        drawImage(gui.screen, shipImage, (x , y))

        # -------------DAMAGE PERCENT

        string = str(self.player.hp/self.player.defaultHp*100) + '%'
        tw= getTextWidth(gui.squareFontSmall,string)
        drawTextWithBackground(gui.screen,gui.squareFontSmall,string,x + 0.05*self.guiBoxW,y+ 1.1 * shipImage.get_height(),textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))

        # -------------RENDER WEAPONS LOADOUT

        loadout = self.player.loadOutCurrentImage
        x,y = self.guiBoxX + 0.43*self.guiBoxW, self.guiBoxY + 0.2*self.guiBoxH
        drawImage(gui.screen, loadout, (x , y))

        # -------------RENDER BOMBS

        bombicon = gui.bombIcons['nuke']
        x,y = self.guiBoxX + 0.97*self.guiBoxW - bombicon.get_width(), self.guiBoxY + 0.9*self.guiBoxH - 2* bombicon.get_height()
        drawImage(gui.screen, bombicon, (x , y))

        string = '3'
        tw= getTextWidth(gui.squareFontSmall,string)
        drawTextWithBackground(gui.screen,gui.squareFontSmall,string,x + 0.4 * bombicon.get_width(),y + 1.4*bombicon.get_height(),textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))


        # -------------HEALTH BAR 

        x,y = self.guiBoxX + 0.43*self.guiBoxW, self.guiBoxY + 0.8*self.guiBoxH
        if(hasattr(self,'healthBar')):
            self.healthBar.load(x,y,gui,self.player.hp/self.player.defaultHp,borderThickness=2)


        if(gui.mouseCollides(self.guiBoxX,self.guiBoxY,self.guiBoxW, self.guiBoxH)):
            self.hideGuiBox = True



     
    # -------------ENEMIES REMAINING / SCORE

    setWidth=getTextWidth(gui.hugeFont,'ENEMIES.')   
    
    self.remainingEnemies = len([x for x in self.enemyList if(x.alive)])
    renderString = str(self.remainingEnemies)
    renderString = str(self.player.score)
    drawTextWithBackground(gui.screen,gui.hugeFont,renderString,50,20, setWidth=setWidth,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))


    # ------------------OBJECTIVE ARROW 

    if(self.displayObjectiveArrow):
        displayObjectiveComplete = self.showObjectiveTimer.stopWatch(4,'showing objectives' + str(self.currentObjective) + str(self.arrowCount), 'objective ' + str(self.objectives[self.currentObjective]), game,silence=True)
        if(not displayObjectiveComplete):
            if(hasattr(self, 'objectives')):
                if(self.currentObjective!=None and self.currentObjective!='complete'):
                    targetObjectives = self.objectives[self.currentObjective]['targetObjects']
                    if(len(targetObjectives)>0):
                        
                        target=None
                        # get the target CLASS object for the first one in the list
                        for i in self.enemyList:
                            if(i.id==targetObjectives[0]):
                                target = i
                        if(target!=None):

                            angleDiffToEnemy,DistanceToEnemy,enemyTargetAngle = angleToTarget(self.player,self.player.x,self.player.y, target.x + (0.5*target.w) , target.y + (0.5*target.h))

                            vel_x = 300 * math.cos(math.radians(360-enemyTargetAngle)) 
                            vel_y = 300 * math.sin(math.radians(360-enemyTargetAngle))
                            #ox,oy = 0.5*gui.w + vel_x, 0.5*gui.h+vel_y
                            ox,oy = self.player.x + vel_x - gui.camX, self.player.y +vel_y - gui.camY
                            self.objectiveArrow.animate(gui,str(self.currentObjective),[ox,oy],game,rotation=enemyTargetAngle-90) 
        else:
            self.displayObjectiveArrow = False
            self.arrowCount +=1



# ---- Applies to enemies 
def manageCollisions(self,enemy,gui,game):

    # GET PLAYER OUT OF SELF SPACE
    if(collidesWith(self.player,enemy) and self.player.invincible==False and enemy.kind in ['air']):

        # IF POWERUP 
        if(enemy.name in ['powerDrone']):
            enemy.collideCollected = True
            return()


        self.player.hp         -= int(0.1*self.player.defaultHp)
        self.player.hit        = True
        self.player.invincible = True

        if self.player.x < enemy.x:
            # Player is to the left of enemy, move player to the right
            self.player.x = enemy.x - 0.2*self.player.w
        elif self.player.x > enemy.x:
            # Player is to the right of enemy, move player to the left
            self.player.x = enemy.x + 0.2*enemy.w
        elif self.player.y < enemy.y:
            # Player is above enemy, move player down
            self.player.y = enemy.y - 0.2*self.player.h
        elif self.player.y > enemy.y:
            # Player is below enemy, move player up
            self.player.y = enemy.y + 0.2*enemy.h
    

    if(onScreen(enemy.x,enemy.y,enemy.w,enemy.h,gui)):
        
        for otherEnemy in self.enemyList:
            if(collidesWith(otherEnemy,enemy)):
                if((enemy.kind =='air' and otherEnemy.kind =='air') or 
                    # if bump into me
                   (enemy.kind in ['structure','vechicle']  and otherEnemy.kind in['vechicle','boat']) or 
                   (enemy.kind =='boat' and otherEnemy.kind =='boat') or 
                   (enemy.kind =='bigBoat' and otherEnemy.kind =='boat')):
                    # MOVE OUT WAY
                    if otherEnemy.x < enemy.x:
                        # Player is to the left of enemy, move player to the right
                        otherEnemy.x = enemy.x - otherEnemy.w
                    elif otherEnemy.x > enemy.x:
                        # Player is to the right of enemy, move player to the left
                        otherEnemy.x = enemy.x + enemy.w
                    elif otherEnemy.y < enemy.y:
                        # Player is above enemy, move player down
                        otherEnemy.y = enemy.y - otherEnemy.h
                    elif otherEnemy.y > enemy.y:
                        # Player is below enemy, move player up
                        otherEnemy.y = enemy.y + enemy.h




#------STAND ALONE FUNCTION 




def inQuandrant(unit, quandrant):
    if((unit.x > quandrant['x']) and (unit.x) < (quandrant['x'] + quandrant['w']) ):
        if(unit.y > quandrant['y'] and (unit.y+unit.h) < (quandrant['y'] + quandrant['h']) ):
            return(True)

    #print('{} {} {} failed '.format(str(unit.x),str(unit.y),str(unit.name)))
    return(False)

