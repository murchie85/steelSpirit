from utils._utils import *
from utils.gameUtils import *



"""
**** ENEMIES ARE DEFINED IN ENEMYDICT IN SETUP

"""
def placeUnits(self,gui,game):
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


	showUnderLayer(self,gui)
	# -------PLACE ENEMY MODE
	if(self.placingEnemy):
		selectEnemy(self,gui)
	else:
		self.nav(gui)


	self.guiMenuItems(gui,game)




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


def showUnderLayer(self,gui):


	# SHOW ANYTHING THAT MIGHT BE ON THIS LAYER
	for item in self.gameMap['tilelessL1']:
		image = gui.tilelessL1Dict[item['dictKey']][item['index']]
		if(onScreen(item['x'],item['y'],image.get_width(),image.get_height(),gui)):
			drawImage(gui.screen,image,(item['x']- gui.camX,item['y']-gui.camY))
