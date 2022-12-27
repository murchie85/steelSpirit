from utils._utils import *
from utils.gameUtils import *
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

		# TILE SELECTION 
		self.tileModes             = ['layer1','Enemies']
		self.tileMode              = 'layer1'
		self.editingTile           = False
		self.tileOptions           = list(gui.tileDict.keys())
		self.tileOptionsIndex      = 0
		self.tileOptionsSubIndex   = 0
		self.tileSelecting         = False
		self.tileSelectionList     = []
		self.tileHovered 		   = False

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

		# TILE SELECTION 
		self.tileModes             = ['layer1','Enemies']
		self.tileMode              = 'layer1'
		self.editingTile           = False
		self.tileOptions           = list(gui.tileDict.keys())
		self.tileOptionsIndex      = 0
		self.tileOptionsSubIndex   =  0
		self.tileSelecting         = False
		self.tileSelectionList     = []
		self.tileHovered 		   = False

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
			# DRAW BACKGROUND PIC
			drawImage(gui.screen,gui.cherry,[0,0])
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

			loadMap,tex,tey    = simpleButton(0.15*(gui.w-tw),tey + 0.8*th,'Load Map',gui,chosenFont,setTw=tw,backColour=backColour[1],borderColour=borderColour, textColour=(255,255,255))

			# KEY SELECTION 
			if(gui.input.returnedKey=='return'):
				newMap = 0==self.buttonIndex
				loadMap = 1==self.buttonIndex
				gui.input.returnedKey       = ''
			
			if(newMap):
				self.state = 'newMap'
			if(loadMap):
				self.state = 'loadMap'
		
		






		if(self.state=='newMap'):
			self.createNewMap(gui,game)


		if(self.state=='loadMap'):

			borderColour = (153, 204, 255)
			backColour   = (51, 102, 255)
			textColour   = (255,255,255)

			gui.screen.fill((51, 51, 153))
			drawImage(gui.screen,gui.madge,[0,0])
			
			self.levelScreenMask.set_alpha(self.alphaI)
			self.levelScreenMask.fill((0,0,0))
			gui.screen.blit(self.levelScreenMask,(0,0))

			# ------GET LOADED MAPS 
			loadPath       = 'state/'
			availableFiles = os.listdir(loadPath)
			availableFiles = [x for x in availableFiles if x[-4:]=='.pkl']
			
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
					self.gameMap = load_pickle(loadPath + f)
					self.gameMap['cols'] = int(self.gameMap['width']/self.gameMap['tileDims'])
					self.gameMap['rows'] = int(self.gameMap['height']/self.gameMap['tileDims'])
					self.state = 'editMap'
					break

				# IF DELETE
				if(hoverered and gui.clicked):
					os.remove(loadPath + f)

			tw,th   = getTextWidth(chosenFont,'A menu item.'),getTextHeight(chosenFont,'A menu item.')
			back,tex,tey      = simpleButton(gui.w-300,0.93*gui.h,'Back',gui,chosenFont,setTw=tw,backColour=backColour,borderColour=borderColour, textColour=textColour)
			if(back):
				game.state = 'intro'  
				self.init(gui,game)
				print('going to intro')


		# ----------EDIT MAP (LAYER ONE)

		if(self.state=='editMap'):

			# GET MAPTILE LIST
			mapTiles = self.gameMap['metaTiles']


			x = 0
			y = 0
			
			# USES THE type and index as keys to gui.tileDict

			# MANAGES STATE
			
			if(gui.clicked and self.tileHovered and self.buttonsHovered!=True):
				if(self.tileSelecting==False and self.editingTile==False):
					self.tileSelecting = True
					gui.clicked        = False
				elif(self.tileSelecting==True and self.editingTile==False):
					self.editingTile = True
					self.tileSelecting = False
					gui.clicked = False
				


			self.tileHovered = False
			for r in range(len(mapTiles)):
				row = mapTiles[r]
				
				for c in range(len(row)):
					col = row[c]

					if(col['animated']==False ):
						image = gui.tileDict[col['type']][col['index']]


						# IF HOVERED, CHANGE TILE TO SELECT ME 
						if(gui.mouseCollides(x-gui.camX,y-gui.camY,image.get_width(),image.get_height())):
							self.tileHovered = True
							if(self.tileSelecting):
								# ADD TO EDIT LIST
								selectedCoords = [r,c]
								if(selectedCoords not in self.tileSelectionList): 
									self.tileSelectionList.append(selectedCoords)

						# IF SELECTED, SHOW THE CURRENT BROWSED IMAGE
						if([r,c] in self.tileSelectionList and self.tileSelecting):
							drawImage(gui.screen,gui.base100[2],(x-gui.camX,y-gui.camY))
					
						# IF SELECTED, SHOW THE CURRENT BROWSED IMAGE
						elif([r,c] in self.tileSelectionList and self.editingTile):
							drawImage(gui.screen, gui.tileDict[self.tileOptions[self.tileOptionsIndex]][self.tileOptionsSubIndex],(x-gui.camX,y-gui.camY))


						# DRAW THE CURRENT TILE
						else:
							drawImage(gui.screen,image,(x-gui.camX,y-gui.camY))



					

					x += image.get_width()

				y+= image.get_height()
				x = 0






			# SELECT TILES OR NAVIGATE MODE 

			if(self.editingTile):
				self.selectTile(gui)
			else:
				self.nav(gui)


			self.guiMenuItems(gui,game)
		


		# ----------EDIT MAP (LAYER ONE)

		if(self.state=='enemyPlacement'):

			if('enemyList' not in self.gameMap):
				print("****Initializing Enemy list on gameMap as does not exist")
				self.gameMap['enemyList'] = []


			# GET MAPTILE LIST
			mapTiles = self.gameMap['metaTiles']
			x,y = 0,0

			self.tileHovered = False
			for r in range(len(mapTiles)):
				row = mapTiles[r]
				
				for c in range(len(row)):
					col = row[c]

					if(col['animated']==False ):
						image = gui.tileDict[col['type']][col['index']]

						# ----IF HOVERED, CHANGE TILE TO SELECT ME 

						if(self.placingEnemy == False and gui.mouseCollides(x-gui.camX,y-gui.camY,image.get_width(),image.get_height())):
							drawImage(gui.screen,gui.base100[2],(x-gui.camX,y-gui.camY))
							
							# ------PLACING ENEMY

							if(gui.clicked and self.buttonsHovered!=True):
								self.placingEnemy = True
								self.selectedEnemyCoords  = [r,c]
								gui.clicked = False
						
						# --------DRAW THE CURRENT TILE

						else:
							drawImage(gui.screen,image,(x-gui.camX,y-gui.camY))

						

						# --------SHOW ALL PLACED ENEMIES

						for enemy in self.gameMap['enemyList']:
							if(r == enemy['row'] and c== enemy['col']):

								name = enemy['kind']
								drawImage(gui.screen,gui.enemyDict[name]['image'],(x-gui.camX,y-gui.camY))


						# --------DISPLAY SELECTED ENEMY

						if(self.placingEnemy):
							if(r==self.selectedEnemyCoords[0] and c==self.selectedEnemyCoords[1]):
								if(self.remove!=True):
									name = self.enemyOptions[self.enemyOptionsIndex]
									drawImage(gui.screen,gui.enemyDict[name]['image'],(x-gui.camX,y-gui.camY))
								else:
									drawImage(gui.screen,gui.base100[3],(x-gui.camX,y-gui.camY))


						# --------IF HOVERED, CHANGE TILE TO SELECT ME 

						if(self.enemyPlacementPhase == 'setWayPoints'):
							for coords in self.patrolCoords:
								if(r == coords['table'][0] and c== coords['table'][1]):
									coordIndex = str(self.patrolCoords.index(coords))
									drawTextWithBackground(gui.screen,gui.hugeFont,coordIndex,x-gui.camX,y-gui.camY,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))


						if(self.enemyPlacementPhase == 'setWayPoints' and gui.mouseCollides(x-gui.camX,y-gui.camY,image.get_width(),image.get_height())):
							patrolCoords = str(len(self.patrolCoords))
							if(patrolCoords not in self.patrolCoords):
								drawTextWithBackground(gui.screen,gui.hugeFont,patrolCoords,x-gui.camX,y-gui.camY,textColour=(20, 50, 200),backColour= (0,0,0),borderColour=(50,50,200))
								if(gui.clicked):
									xm,ym = x + 0.5*image.get_width(),0.5*image.get_height()
									self.patrolCoords.append({'table':(r,c) , 'coords':(gui.mx +gui.camX,gui.my+gui.camY)})
							

					x += image.get_width()

				y+= image.get_height()
				x = 0



			# -------PLACE ENEMY MODE
			if(self.placingEnemy):
				self.selectEnemy(gui)
			else:
				self.nav(gui)


			self.guiMenuItems(gui,game)



	# --------SELECT TILE SECTION

	def selectTile(self,gui):

		# DRAW TILE NAME 

		setWidth=getTextWidth(gui.bigFont,'A menu item yep sure.')
		drawTextWithBackground(gui.screen,gui.bigFont,self.tileOptions[self.tileOptionsIndex],1000,150,setWidth=setWidth ,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))
		

		# increment major index (map type)
		if(gui.input.returnedKey.upper()=='D'): 
			self.tileOptionsIndex += 1
			self.tileOptionsSubIndex = 0
		if(gui.input.returnedKey.upper()=='A'): 
			self.tileOptionsIndex -= 1
			self.tileOptionsSubIndex =0 
		
		# TOP LEVEL SELECTION
		if(self.tileOptionsIndex<0):self.tileOptionsIndex = len(self.tileOptions)-1
		if(self.tileOptionsIndex>len(self.tileOptions)-1):self.tileOptionsIndex = 0

		# increment minor index (map variation)
		if(gui.input.returnedKey.upper()=='S'): self.tileOptionsSubIndex += 1
		if(gui.input.returnedKey.upper()=='W'): self.tileOptionsSubIndex -= 1
		
		if(self.tileOptionsSubIndex > len(gui.tileDict[self.tileOptions[self.tileOptionsIndex]])-1): self.tileOptionsSubIndex = 0
		if(self.tileOptionsSubIndex<0):self.tileOptionsSubIndex = len(gui.tileDict[self.tileOptions[self.tileOptionsIndex]])-1


		if(gui.rightClicked):
			self.editingTile        = False
			self.tileSelectionList   = []
			gui.clicked              = False
			self.tileSelecting       = False

		if(gui.input.returnedKey.upper()=='RETURN' or gui.clicked):
			for tile in self.tileSelectionList:
				self.gameMap['metaTiles'][tile[0]][tile[1]] = {'placed': True, 'animated':False,'type':self.tileOptions[self.tileOptionsIndex],'index':self.tileOptionsSubIndex}
				self.editingTile        = False
				self.tileSelectionList   = []
				gui.clicked              = False
				self.tileSelecting       = False





	# --------SELECT ENEMY SECTION

	def selectEnemy(self,gui):

		# -------IF DUPLICATE SET TO REMOVE 

		remove = False
		if(self.enemyPlacementPhase =='placingEnemy'):
			for enemy in self.gameMap['enemyList']:
				if(enemy['row'] == self.selectedEnemyCoords[0] and enemy['col']== self.selectedEnemyCoords[1]):
					remove = True
					self.remove = True
			
			# -------DRAW ENEMY NAME 

			setWidth=getTextWidth(gui.bigFont,'A menu item yep sure.')
			drawTextWithBackground(gui.screen,gui.bigFont,self.enemyOptions[self.enemyOptionsIndex],1000,150,setWidth=setWidth ,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))
			

			# -------increment major index (map type)

			if(gui.input.returnedKey.upper()=='D'): 
				self.enemyOptionsIndex += 1
				self.enemyOptionsSubIndex = 0
			if(gui.input.returnedKey.upper()=='A'): 
				self.enemyOptionsIndex -= 1
				self.enemyOptionsSubIndex =0 
			
			# -------TOP LEVEL SELECTION

			if(self.enemyOptionsIndex<0):self.enemyOptionsIndex = len(self.enemyOptions)-1
			if(self.enemyOptionsIndex>len(self.enemyOptions)-1):self.enemyOptionsIndex = 0
		
		if(self.enemyPlacementPhase =='setWayPoints'):

			# -------DRAW ENEMY NAME 

			setWidth=getTextWidth(gui.bigFont,'A menu item yep sure.')
			drawTextWithBackground(gui.screen,gui.bigFont,'Set Way Points',1000,150,setWidth=setWidth ,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))
			self.nav(gui)


		if(gui.rightClicked):
			self.placingEnemy           = False
			self.enemyPatrolCoordList   = []
			gui.clicked                 = False
			self.enemySelecting         = False
			self.remove 			    = False
			self.enemyPlacementPhase    = 'placingEnemy'
			self.patrolCoords 		    = []

		if(gui.input.returnedKey.upper()=='RETURN' or gui.clicked):
			
			initMe = False
			# REMOVE EXISTING IF REMOVE FLAG SET
			if(remove):
				for enemy in self.gameMap['enemyList']:
					if(enemy['row'] == self.selectedEnemyCoords[0] and enemy['col']== self.selectedEnemyCoords[1]):
						self.gameMap['enemyList'].remove(enemy)
				initMe = True
			else:
				if(self.enemyPlacementPhase =='placingEnemy'): 
					self.enemyPlacementPhase = 'setWayPoints'
				elif(self.enemyPlacementPhase =='setWayPoints'):
					if(len(self.patrolCoords)>3):
						self.enemyPlacementPhase = 'complete'
				gui.clicked                = False

			if(self.enemyPlacementPhase=='complete'):
				self.gameMap['enemyList'].append({'kind': self.enemyOptions[self.enemyOptionsIndex],'patrolCoords': self.patrolCoords,'special1':None,'row':self.selectedEnemyCoords[0],'col': self.selectedEnemyCoords[1]})
				self.patrolCoords         = []
				self.enemyPlacementPhase  ='placingEnemy'
				initMe = True
			

			if(initMe):
				self.placingEnemy          = False
				self.enemyPatrolCoordList  = []
				self.selectedEnemyCoords   = []
				gui.clicked                = False
				self.enemySelecting        = False
				self.remove 			   = False





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
					currentRow.append({'placed': False, 'animated':False,'type':'base','index':0})

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

	def guiMenuItems(self,gui,game):
		# SAVE OR GO BACK

		chosenFont = gui.largeFont
		borderColour=(60,60,200)
		
		tw,th                          = getTextWidth(chosenFont,'A menu item.'),getTextHeight(chosenFont,'A menu item yep sure.')
		save,tex,tey,saveHovered       = simpleButtonHovered(1100,0.93*gui.h,'Save',gui,chosenFont,setTw=tw,backColour=(0,0,0),borderColour=borderColour, textColour=(255,255,255))
		back,ttx,tty,backHovered       = simpleButtonHovered(tex + 0.1*tw,0.93*gui.h,'Back',gui,chosenFont,setTw=tw,backColour=(0,0,0),borderColour=borderColour, textColour=(255,255,255))
		tileMode,tex,tey,tileHovered   = simpleButtonHovered(tex + 0.1*tw,0.05*gui.h,self.tileMode,gui,chosenFont,setTw=tw,backColour=(0,0,0),borderColour=(10,170,80), textColour=(255,255,255))
		self.buttonsHovered            = saveHovered or backHovered or tileHovered



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
			self.tileModes             = ['layer1','Enemies']
			if(self.tileMode =='layer1'):
				self.state='editMap'
			if(self.tileMode =='Enemies'):
				self.state='enemyPlacement'

		# -----PRINT OUT TEXT INFORMATION SUCH AS MAP SIZE

		setWidth=getTextWidth(gui.font,'A menu item yep sure correct.')
		sentence = "Map Size: [" + str(self.gameMap['width']) + ':' + str(self.gameMap['height']) +']'
		drawTextWithBackground(gui.screen,gui.font,sentence,50,20,setWidth=setWidth ,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))
		sentence = '(' +str(gui.mx+gui.camX) + ',' + str(gui.my+gui.camY) +')'
		drawTextWithBackground(gui.screen,gui.font,sentence,50,800,setWidth=setWidth ,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))
		
		dictKeys    = list(self.gameMap.keys())
		currentKey = dictKeys[self.guiDebugDisplayIndex]
		printObj   = str(currentKey) + ': ' + str(self.gameMap[currentKey])
		drawTextWithBackground(gui.screen,gui.font,printObj,500,800,setWidth=setWidth ,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))
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
			speed = 40
		# GET DIRECTION OF ACCELLERATION
		if('W' in pressedKeys ):
			gui.camY -= speed
		if('S' in pressedKeys):
			gui.camY += speed
		if('D' in pressedKeys):
			gui.camX += speed
		if('A' in pressedKeys):
			gui.camX -= speed
