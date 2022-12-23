from utils._utils import *
from utils.gameUtils import *
import os


class mapEditor():
	def __init__(self,gui,game):
		self.state             = 'options'
		self.questionCursor    = 0
		self.answerList        = []
		self.questionsComplete = False

		self.gameMap           = None

		# TILE SELECTION 
		self.tileSelected          = False
		self.selectedCoords        = [0,0]
		self.tileOptions           = list(gui.tileDict.keys())
		self.tileOptionsIndex      = 0
		self.tileOptionsSubIndex   = 0

		self.timer      			= stopTimer()
		self.timer      			= stopTimer()
		self.saving 				= False
		self.saves 					= 0

	def init(self,gui,game):
		self.state             = 'options'
		self.questionCursor    = 0
		self.answerList        = []
		self.questionsComplete = False

		self.gameMap           = None

		# TILE SELECTION 
		self.tileSelected          = False
		self.selectedCoords        = [0,0]
		self.tileOptions           = list(gui.tileDict.keys())
		self.tileOptionsIndex      = 0
		self.tileOptionsSubIndex  = 0

	def run(self,gui,game):


		# LOAD MAP OR CREATE NEW ONE 
		if(self.state=='options'):
			chosenFont = gui.largeFont
			borderColour=(60,60,200)
			
			tw,th   = getTextWidth(chosenFont,'A menu item yep sure.'),getTextHeight(chosenFont,'A menu item yep sure.')

			newMap,tex,tey      = simpleButton(0.5*(gui.w-tw),0.4*gui.h,'New Map',gui,chosenFont,setTw=tw,backColour=(0,0,0),borderColour=borderColour, textColour=(255,255,255))

			loadMap,tex,tey    = simpleButton(0.5*(gui.w-tw),tey + 0.8*th,'Load Map',gui,chosenFont,setTw=tw,backColour=(0,0,0),borderColour=borderColour, textColour=(255,255,255))


			if(newMap):
				self.state = 'newMap'
			if(loadMap):
				self.state = 'loadMap'
		
		






		if(self.state=='newMap'):

			# ASK QUESTIONS ABOUT NEW MAP 
			questionList = ['Name of Map file', 'Map Width', 'Map Height', 'Tile Size']

			
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


				# NUMBER OF COLUMS = map width / tileSize
				# NUMBER OF Rows   = map height / tileSize
				gameMap['cols'] = int(gameMap['width']/gameMap['tileDims'])
				gameMap['rows'] = int(gameMap['height']/gameMap['tileDims'])

				metaTiles = []
				for row in range(gameMap['rows']):
					currentRow = []
					for col in range(gameMap['cols']):
						currentRow.append({'placed': False, 'animated':False,'type':'base','index':0})

					metaTiles.append(currentRow)

				# SAVE MAP OBJECT

				gameMap['metaTiles'] = metaTiles
				self.gameMap = gameMap
				save_dict_as_pickle(self.gameMap, 'state/' + str(self.gameMap['name']) + '.pkl' )
				self.state='editMap'




		if(self.state=='loadMap'):
			loadPath       = 'state/'
			availableFiles = os.listdir(loadPath)
			availableFiles = [x for x in availableFiles if x[-4:]=='.pkl']
			chosenFont = gui.smallFont
			borderColour=(60,60,200)
			tw,th   = getTextWidth(chosenFont,'A menu item yep sure.'),getTextHeight(chosenFont,'A menu item yep sure.')

			buttonY = 300
			for f in availableFiles:
				chosenFile,tex,tey  = simpleButton(700,buttonY,f,gui,chosenFont,setTw=tw,backColour=(0,0,0),borderColour=borderColour, textColour=(255,255,255))
				hoverered, ttx,tty  = drawText(gui,gui.smallFont, 'Delete',tex+10,buttonY+10, colour=(0, 128, 0),center=False,pos=[gui.mx,gui.my])
				
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
			back,tex,tey      = simpleButton(100,0.93*gui.h,'Back',gui,chosenFont,setTw=tw,backColour=(0,0,0),borderColour=borderColour, textColour=(255,255,255))
			if(back):
				game.state = 'intro'  
				self.init(gui,game)
				print('going to intro')


		if(self.state=='editMap'):
			mapTiles = self.gameMap['metaTiles']
			

			x = 0
			y = 0
			# USES THE type and index as keys to gui.tileDict
			for r in range(len(mapTiles)):
				row = mapTiles[r]
				
				for c in range(len(row)):
					col = row[c]
					if(col['animated']==False ):
						image = gui.tileDict[col['type']][col['index']]

						# IF SELECTED, SHOW THE CURRENT BROWSED IMAGE
						if(r == self.selectedCoords[0] and c == self.selectedCoords[1] and self.tileSelected):
							drawImage(gui.screen,gui.tileDict[self.tileOptions[self.tileOptionsIndex]][self.tileOptionsSubIndex],(x-gui.camX,y-gui.camY))
					
						# IF HOVERED, CHANGE TILE TO SELECT ME 
						elif(gui.mouseCollides(x-gui.camX,y-gui.camY,image.get_width(),image.get_height()) and self.tileSelected==False):
							drawImage(gui.screen,gui.tileDict['base'][1],(x-gui.camX,y-gui.camY))
							if(gui.clicked):
								gui.clicked = False
								self.tileSelected = True
								self.selectedCoords = [r,c]

						# DRAW THE CURRENT TILE
						else:
							drawImage(gui.screen,image,(x-gui.camX,y-gui.camY))



					

					x += image.get_width()

				y+= image.get_height()
				x = 0

			

			# SELECT TILES OR NAVIGATE MODE 

			if(self.tileSelected):
				self.selectTile(gui)
			else:
				self.nav(gui)

			# SAVE OR GO BACK

			chosenFont = gui.largeFont
			borderColour=(60,60,200)
			
			tw,th   = getTextWidth(chosenFont,'A menu item.'),getTextHeight(chosenFont,'A menu item yep sure.')
			save,tex,tey      = simpleButton(1100,0.93*gui.h,'Save',gui,chosenFont,setTw=tw,backColour=(0,0,0),borderColour=borderColour, textColour=(255,255,255))
			back,tex,tey      = simpleButton(tex + 0.1*tw,0.93*gui.h,'Back',gui,chosenFont,setTw=tw,backColour=(0,0,0),borderColour=borderColour, textColour=(255,255,255))
			
			if(save):
				save_dict_as_pickle(self.gameMap, 'state/' + str(self.gameMap['name']) + '.pkl' )
				self.saving = True
			if(self.saving):
				saveMessageTimeout    = self.timer.stopWatch(2,'SaveMessage',self.saves,game)
				drawText(gui,gui.bigFont, 'Saved!',650,350,colour=(80, 255, 80))
				if(saveMessageTimeout):
					self.saving = False
					self.saves+=1

			# -----gui text

			setWidth=getTextWidth(gui.font,'A menu item yep sure correct.')
			sentence = "Map Size: [" + str(self.gameMap['width']) + ':' + str(self.gameMap['height']) +']'
			drawTextWithBackground(gui.screen,gui.font,sentence,50,20,setWidth=setWidth ,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))
			sentence = '(' +str(gui.mx+gui.camX) + ',' + str(gui.my+gui.camY) +')'
			drawTextWithBackground(gui.screen,gui.font,sentence,50,800,setWidth=setWidth ,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))
			
			#--- always goes at the end
			
			if(back):
				game.state = 'intro'  
				self.init(gui,game)
				print('going to intro')



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
		
		if(self.tileOptionsIndex<0):self.tileOptionsIndex = 0
		if(self.tileOptionsIndex>len(self.tileOptions)-1):self.tileOptionsIndex = len(self.tileOptions)-1

		# increment minor index (map variation)
		if(gui.input.returnedKey.upper()=='S'): self.tileOptionsSubIndex += 1
		if(gui.input.returnedKey.upper()=='W'): self.tileOptionsSubIndex -= 1
		
		if(self.tileOptionsSubIndex > len(gui.tileDict[self.tileOptions[self.tileOptionsIndex]])-1): self.tileOptionsSubIndex = len(gui.tileDict[self.tileOptions[self.tileOptionsIndex]])-1
		if(self.tileOptionsSubIndex<0):self.tileOptionsSubIndex = 0

		if(gui.input.returnedKey.upper()=='RETURN' or gui.clicked):
			self.gameMap['metaTiles'][self.selectedCoords[0]][self.selectedCoords[1]] = {'placed': True, 'animated':False,'type':self.tileOptions[self.tileOptionsIndex],'index':self.tileOptionsSubIndex}
			self.tileSelected        = False
			self.selectedCoords      = [0,0]
			#self.tileOptionsIndex    = 0
			#self.tileOptionsSubIndex = 0



	def nav(self,gui):
		# GET PRESSED KEYS

		#self.gameMap['metaTiles']
		pressedKeys     = [x.upper() for x in gui.input.pressedKeys]

		# ACCELELRATION FLAG
		vAccell,hAccell = False,False

		# GET DIRECTION OF ACCELLERATION
		if('W' in pressedKeys ):
			gui.camY -= 20
		if('S' in pressedKeys):
			gui.camY += 20
		if('D' in pressedKeys):
			gui.camX += 20
		if('A' in pressedKeys):
			gui.camX -= 20
