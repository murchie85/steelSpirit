from utils._utils import *
from utils.gameUtils import *
from oldLevels.mapMakerOptions import *
from oldLevels.mapMakerLoadMap import *
from oldLevels.mapMakerEdit import *
from oldLevels.mapMakerLayer2 import *
from oldLevels.mapMakerUnits import *
from oldLevels.mapMakerTileLessL1 import * 
from oldLevels.mapMakerSpawnZones import *

import os


class mapEditor():
	def __init__(self,gui,game):
		self.state             = 'options'
		self.questionCursor    = 0
		self.answerList        = []
		self.questionsComplete = False
		self.buttonIndex       = 0
		self.buttonsHovered    = False

		self.gameMap           = None

		# CURSOR SELECTION
		self.dragSelect             = dragSelector()


		# TILE SELECTION 
		self.tileModes             = ['layer1','layer2','tilelessL1', 'Enemies','spawnZones']
		self.tileMode              = 'layer1'
		self.editingTile           = False

		self.selectModes           = ['tile','box']
		self.selectMode            = 'tile'
		self.boxCoords             = []


		self.enemyObjectiveModes   = ['Place Enemy', 'Set Objective Number']
		self.enemyObjectiveMode    = self.enemyObjectiveModes[0]
		self.enemyObjectives       = 5
		self.currentEnemyObjective = 0

		# layer 1
		self.tileOptions           = list(gui.tileDict.keys())
		self.tileOptionsIndex      = 0
		self.tileOptionsSubIndex   = 0
		
		# layer 2
		self.l2Options             = list(gui.layer2Dict.keys())
		self.l2OptionsIndex      = 0
		self.l2OptionsSubIndex   = 0
		self.deleteL2Flag		 = False

		# tileLess
		self.t1Options           = list(gui.tilelessL1Dict.keys())
		self.t1OptionsIndex      = 0
		self.t1OptionsSubIndex   = 0
		self.tl1SelectedCoords   = []
		self.tl1SelectionState   = None

		self.tileSelecting         = False
		self.tileSelectionList     = []
		self.tileHovered 		   = False
		self.pagedIndex			   = 0
		self.previousIndex         = 0

		# ENEMY SELECTION 

		self.placingEnemy           = False
		self.enemyOptions          = list(gui.enemyDict.keys())
		self.enemyOptionsIndex     = 0
		self.enemyOptionsSubIndex  = 0
		self.enemySelecting        = False
		self.enemyPatrolCoordList   = []
		self.enemyHovered 		   = False
		self.selectedEnemyCoords   = [] # coordinates of enemy currently being placed
		self.enemyPlacementPhase   ='placingEnemy'
		self.patrolCoords          = []
		self.remove                = False
		self.enemyRotation		   = 0


		self.timer      			= stopTimer()
		self.timer      			= stopTimer()
		self.saving 				= False
		self.saves 					= 0

		self.guiDebugDisplayIndex   = 0

		self.levelScreenMask      = pygame.Surface((gui.w,gui.h))
		self.alphaI               = 100

	def init(self,gui,game):
		self.state             = 'options'
		self.questionCursor    = 0
		self.answerList        = []
		self.questionsComplete = False
		self.buttonIndex       = 0
		self.buttonsHovered    = False

		self.gameMap           = None

		# CURSOR SELECTION
		self.dragSelect             = dragSelector()

		# TILE SELECTION 
		self.tileModes             = ['layer1','layer2','tilelessL1', 'Enemies','spawnZones']
		self.tileMode              = 'layer1'
		self.editingTile           = False
		

		self.selectModes           = ['tile','box']
		self.selectMode            = 'tile'
		self.boxCoords             = []

		# ALLOWS SETTING ENEMY OBJECTIVE NUMBER
		self.enemyObjectiveModes   = ['Place Enemy', 'Set Objective Number']
		self.enemyObjectiveMode    = self.enemyObjectiveModes[0]
		self.enemyObjectives       = 5
		self.currentEnemyObjective = 0


		self.tileOptions           = list(gui.tileDict.keys())
		self.tileOptionsIndex      = 0
		self.tileOptionsSubIndex   =  0
		self.tileSelecting         = False
		self.tileSelectionList     = []
		self.tileHovered 		   = False
		self.pagedIndex			   = 0

		# layer 2
		self.l2Options             = list(gui.layer2Dict.keys())
		self.l2OptionsIndex      = 0
		self.l2OptionsSubIndex   = 0

		# tileLess
		self.t1Options           = list(gui.tilelessL1Dict.keys())
		self.t1OptionsIndex      = 0
		self.t1OptionsSubIndex   = 0
		self.tl1SelectedCoords   = []
		self.tl1SelectionState   = None

		# ENEMY SELECTION 

		self.placingEnemy          = False
		self.enemyOptions          = list(gui.enemyDict.keys())
		self.enemyOptionsIndex     = 0
		self.enemyOptionsSubIndex  = 0
		self.enemySelecting        = False
		self.enemyPatrolCoordList   = []
		self.enemyHovered 		   = False
		self.selectedEnemyCoords   = [] # coordinates of enemy currently being placed
		self.enemyPlacementPhase   ='placingEnemy'
		self.patrolCoords          = []
		self.remove                = False


		self.guiDebugDisplayIndex   = 0


	def run(self,gui,game):


		# LOAD MAP OR CREATE NEW ONE 
		if(self.state=='options'):
			mapMakerOptions(self,gui)

		# ----------CREATE MAP  

		if(self.state=='newMap'):
			self.createNewMap(gui,game)


		if(self.state=='newMapAlpha'):
			self.createNewTxtMap(gui,game)

		# ----------LOAD MAP 

		if(self.state=='loadMap'):
			loadMap(self,gui,game)




		# ----------EDIT MAP (LAYER ONE)

		if(self.state=='editMap'):
			editMap(self,gui,game)

		# ----------EDIT MAP (LAYER TWO)

		if(self.state=='editLayer2'): editLayer2(self,gui,game)

		# ----------EDIT MAP (LAYER TWO)

		if(self.state=='tilelessL1'): tilelessL1(self,gui,game)

		# ----------EDIT ENEMIES

		if(self.state=='enemyPlacement'): placeUnits(self,gui,game)

		# ----------EDIT SPAWN ZONES

		if(self.state=='spawnZones'): spawnZones(self,gui,game)







	def createNewMap(self,gui,game,externallyCalled=False,specifiedName='notSpecified'):

		# ASK QUESTIONS ABOUT NEW MAP 
		questionList = ['Name of Map file', 'Map Width', 'Map Height', 'Tile Size']

		# OVERRIDE
		if(externallyCalled and len(self.answerList)<1):
			self.questionCursor = 1
			self.answerList.append(specifiedName)

		# QUESTIONS REGARDING MAP DIMENSIONS AND SIZES 

		if(self.questionCursor < len(questionList) and self.questionsComplete==False):
			drawText(gui,gui.font,questionList[self.questionCursor],500,300, colour=(100, 100, 255))
			game.input.drawTextInputSingleLine(game.input.enteredString,500,400,gui,boxBorder=(50,50,200),boxFill=(0,0,0) ,colour=(80,80,255))
			returnvalue = game.input.processInput()
			
			if(game.input.returnedKey=='ENTER'):
				self.answerList.append(game.input.enteredString)
				game.input.enteredString = ""
				self.questionCursor +=1
				if(self.questionCursor >= len(questionList)):
					self.questionsComplete = True

		
		# CREATE MAP OBJECT 

		if(self.questionsComplete and self.gameMap==None):
			gameMap = {"name": self.answerList[0],
					   "width": int(self.answerList[1]),
					   "height":int(self.answerList[2]),
					   "tileDims": int(self.answerList[3])
					   }


			# -------NUMBER OF ROWS CALCULATED 

			gameMap['cols'] = int(gameMap['width']/gameMap['tileDims'])
			gameMap['rows'] = int(gameMap['height']/gameMap['tileDims'])


			# ------- INITIALISE TILEMAP WITH DEFAULT DICT FOR EVERY COL AND ROW
			metaTiles = []
			for row in range(gameMap['rows']):
				currentRow = []
				for col in range(gameMap['cols']):
					tileType= 'base'
					currentRow.append({'placed': False, 'animated':False,'type':tileType,'index':0})

				metaTiles.append(currentRow)


			# SAVE MAP OBJECT

			gameMap['metaTiles'] = metaTiles
			gameMap['enemyList'] = []
			self.gameMap = gameMap
			save_dict_as_pickle(self.gameMap, 'state/' + str(self.gameMap['name']) + '.pkl' )
			
			# NOTIFIY EXTERNAL  READY 
			if(externallyCalled):
				self.init(gui,game) 
				return(True)
			self.state='editMap'

		# NOTIFIY EXTERNAL NOT READY YET
		if(externallyCalled): 
			return(False)






















	def guiMenuItems(self,gui,game,showSelectMode=True,enemySelectMode=False):
		# SAVE OR GO BACK

		chosenFont = gui.largeFont
		borderColour=(60,60,200)
		
		tw,th                                = getTextWidth(chosenFont,'A menu item.'),getTextHeight(chosenFont,'A menu item yep sure.')
		save,tex,tey,saveHovered             = simpleButtonHovered(1100,0.93*gui.h,'Save',gui,chosenFont,setTw=tw,backColour=(0,0,0),borderColour=borderColour, textColour=(255,255,255))
		back,ttx,tty,backHovered             = simpleButtonHovered(tex + 0.1*tw,0.93*gui.h,'Back',gui,chosenFont,setTw=tw,backColour=(0,0,0),borderColour=borderColour, textColour=(255,255,255))
		tileMode,tex,tey,tileHovered         = simpleButtonHovered(tex + 0.1*tw,0.05*gui.h,self.tileMode,gui,chosenFont,setTw=tw,backColour=(0,0,0),borderColour=(10,170,80), textColour=(255,255,255))
		

		# ----------MODE: LAYER ONE 

		if(showSelectMode):
			selectMode,tex,tey,selectModeHovered = simpleButtonHovered(0.1*tw,0.07*gui.h,self.selectMode,gui,chosenFont,setTw=tw,backColour=(0,0,0),borderColour=(10,170,80), textColour=(255,255,255))
		else:
			selectMode,selectModeHovered  = False,False

		# -----------MODE:  ENEMY SELECTION 
		if(enemySelectMode):
			# CHANGE TO OBJECTIVE NUMBER SELECTOR
			switchEnemyObjective,tex,tey,enemyObjectiveHovered = simpleButtonHovered(tw,0.07*gui.h,self.enemyObjectiveMode,gui,gui.font,backColour=(0,0,0),borderColour=(10,170,80), textColour=(255,255,255))
			incEnemy,tex,tey,incEnemyHovered = simpleButtonHovered(tex,0.07*gui.h,'+',gui,gui.font,setTw=0.3*tw,backColour=(0,0,0),borderColour=(10,170,80), textColour=(255,255,255))
			ignore,tex,tey,ignoreHovered     = simpleButtonHovered(tex,0.07*gui.h,str(self.currentEnemyObjective),gui,gui.font,setTw=0.3*tw,backColour=(0,0,0),borderColour=(10,170,80), textColour=(255,255,255))
			decEnemy,tex,tey,decEnemyHovered = simpleButtonHovered(tex,0.07*gui.h,'-',gui,gui.font,setTw=0.3*tw,backColour=(0,0,0),borderColour=(10,170,80), textColour=(255,255,255))

		else:
			switchEnemyObjective,enemyObjectiveHovered,incEnemy,decEnemy,incEnemyHovered,decEnemyHovered = False,False,False,False,False,False
	

		self.buttonsHovered            = saveHovered or backHovered or tileHovered or selectModeHovered or enemyObjectiveHovered or incEnemyHovered or decEnemyHovered



		if(save):
			save_dict_as_pickle(self.gameMap, 'state/' + str(self.gameMap['name']) + '.pkl' )
			self.saving = True
		if(self.saving):
			saveMessageTimeout    = self.timer.stopWatch(2,'SaveMessage',self.saves,game)
			drawText(gui,gui.bigFont, 'Saved!',650,350,colour=(80, 255, 80))
			if(saveMessageTimeout):
				self.saving = False
				self.saves+=1
		if(tileMode):
			self.tileMode = self.tileModes[(self.tileModes.index(self.tileMode) + 1) %len(self.tileModes)]
			print('now ' + str(self.tileMode))
			if(self.tileMode =='layer1'):
				self.state='editMap'
			if(self.tileMode =='layer2'):
				self.state='editLayer2'
				gui.clicked = False
			if(self.tileMode =='tilelessL1'):
				self.state='tilelessL1'
				gui.clicked = False
			if(self.tileMode =='Enemies'):
				self.state='enemyPlacement'
			if(self.tileMode =='spawnZones'):
				self.state='spawnZones'


		if(selectMode):
			self.selectMode = self.selectModes[(self.selectModes.index(self.selectMode) + 1) %len(self.selectModes)]

		# TOGGLE MODES
		if(switchEnemyObjective): 
			self.enemyObjectiveMode = self.enemyObjectiveModes[(self.enemyObjectiveModes.index(self.enemyObjectiveMode) + 1) %len(self.enemyObjectiveModes)]

		# INC/DEC CURRENT ENEMY OBJECTIVE NUMBER 
		if(incEnemy): self.currentEnemyObjective +=1
		if(decEnemy): self.currentEnemyObjective -=1
		if(self.currentEnemyObjective<0): self.currentEnemyObjective = 0
		if(self.currentEnemyObjective>self.enemyObjectives): self.currentEnemyObjective = self.enemyObjectives

		# -----PRINT OUT TEXT INFORMATION SUCH AS MAP SIZE

		setWidth=getTextWidth(gui.font,'A menu item yep sure correct.')
		sentence = "Map Size: [" + str(self.gameMap['width']) + ':' + str(self.gameMap['height']) +']'
		drawTextWithBackground(gui.screen,gui.font,sentence,50,20,setWidth=setWidth ,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))
		sentence = '(' +str(gui.mx+gui.camX) + ',' + str(gui.my+gui.camY) +')'
		drawTextWithBackground(gui.screen,gui.font,sentence,50,800,setWidth=setWidth ,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))
		


		dictKeys    = list(self.gameMap.keys())
		currentKey = dictKeys[self.guiDebugDisplayIndex]
		printObj   = str(currentKey) + ': ' + str(self.gameMap[currentKey])
		yDebug = 800
		xDebug = 500
		debugFont = gui.font
		# PIVOT TO GIVE AS MUCH SPACE TO PRINT IF TOO BIG
		if(type(self.gameMap[currentKey]) == list): 
			printObj   = str(currentKey) + ': ' + str(self.gameMap[currentKey][0])
			yDebug = 750
			xDebug = 100
			debugFont = gui.smallFont
			setWidth = getTextWidth(gui.smallFont,printObj)

		drawTextWithBackground(gui.screen,debugFont,printObj,xDebug,yDebug,setWidth=setWidth ,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))
		# NEXT DEBUG ITEM
		if(gui.input.returnedKey.upper()=='N'):
			self.guiDebugDisplayIndex += 1
			if(self.guiDebugDisplayIndex>len(dictKeys)-1):
				self.guiDebugDisplayIndex=0


		#--- always goes at the end
		
		if(back):
			game.state = 'intro'  
			self.init(gui,game)
			print('going to intro')



	def nav(self,gui):
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
		if(gui.camX+gui.camW>self.gameMap['width']): gui.camX = self.gameMap['width'] - gui.camW
		if(gui.camY+gui.camH>self.gameMap['height']): gui.camY = self.gameMap['height'] - gui.camH
