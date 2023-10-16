from utils._utils import *
from utils.gameUtils import *



"""
**** ENEMIES ARE DEFINED IN ENEMYDICT IN SETUP

"""
def placeUnits(self,gui,game):
	if('enemyList' not in self.gameMap):
		print("****Initializing Enemy list on gameMap as does not exist")
		self.gameMap['enemyList'] = []

	#print(len(self.gameMap['enemyList']))

	# GET MAPTILE LIST
	mapTiles = self.gameMap['metaTiles']
	x,y = 0,0


	mapTiles    = self.gameMap['metaTiles'] # 2,3 = type index
	sampleImage = gui.tileDict[mapTiles[0][0]['type']][mapTiles[0][0]['index']]
	yIndexOne = math.floor((gui.camY)/sampleImage.get_height())
	yIndexTwo = math.ceil((gui.camY+gui.camH)/sampleImage.get_height())
	xIndexOne = math.floor((gui.camX)/sampleImage.get_width())
	xIndexTwo = math.ceil((gui.camX+gui.camW)/sampleImage.get_width())
	removeCoords = None
	objectiveNumberCoords = None

	# ITERATE THROUGH ENEMIES ON SCREEN 

	self.tileHovered = False
	for r in range(yIndexOne,yIndexTwo):
		row = mapTiles[r]
		y = r *sampleImage.get_height()

		for c in range(len(row)):
			col = row[c]
			x = c *sampleImage.get_width()

			if(col['animated']==False ):
				image = gui.tileDict[col['type']][col['index']]

				# ----IF HOVERED, CHANGE TILE TO SELECT ME 

				if(self.placingEnemy == False and gui.mouseCollides(x-gui.camX,y-gui.camY,image.get_width(),image.get_height())):
					drawImage(gui.screen,gui.base100[2],(x-gui.camX,y-gui.camY))
					
					# ------PLACING ENEMY

					if(gui.clicked and self.buttonsHovered!=True):
						self.placingEnemy         = True
						self.selectedEnemyCoords  = [r,c]
						gui.clicked = False
				
				# --------DRAW THE CURRENT TILE

				else:
					drawImage(gui.screen,image,(x-gui.camX,y-gui.camY))

				
				# --------DISPLAY CURRENT SELECTED ENEMY
				if(self.placingEnemy):
					if(r==self.selectedEnemyCoords[0] and c==self.selectedEnemyCoords[1]):
						
						# ADD ENEMY
						if(self.remove==False and self.enemyObjectiveMode=='Place Enemy'):
							name = self.enemyOptions[self.enemyOptionsIndex]
							image = pygame.transform.rotate(gui.enemyDict[name]['image'],self.enemyRotation)

							drawImage(gui.screen,image,(x-gui.camX,y-gui.camY))
						
						elif(self.remove==False and self.enemyObjectiveMode=='Set Objective Number'):
							objectiveNumberCoords = x-gui.camX,y-gui.camY
						# SHOW DELETE LOGO (DELETE HANDLED IN SELECT ENEMY FUNC)
						elif(self.remove==True and self.enemyObjectiveMode=='Place Enemy'):
							drawImage(gui.screen,gui.base100[3],(x-gui.camX,y-gui.camY))
							removeCoords = x-gui.camX,y-gui.camY


				# --------IF HOVERED, CHANGE TILE TO SELECT ME 

				if(self.enemyPlacementPhase == 'setWayPoints'):
					for coords in self.patrolCoords:
						if(r == coords['table'][0] and c== coords['table'][1]):
							coordIndex = str(self.patrolCoords.index(coords))
							drawTextWithBackground(gui.screen,gui.hugeFont,coordIndex,x-gui.camX,y-gui.camY,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))

				# SET WAYPOINTS
				if(self.enemyPlacementPhase == 'setWayPoints'):
					if(gui.mouseCollides(x-gui.camX,y-gui.camY,image.get_width(),image.get_height())):
						patrolCoords = str(len(self.patrolCoords))
						if(patrolCoords not in self.patrolCoords):
							drawTextWithBackground(gui.screen,gui.hugeFont,patrolCoords,x-gui.camX,y-gui.camY,textColour=(20, 50, 200),backColour= (0,0,0),borderColour=(50,50,200))
							if(gui.clicked):
								xm,ym = x + 0.5*image.get_width(),0.5*image.get_height()
								self.patrolCoords.append({'table':(r,c) , 'coords':(gui.mx +gui.camX,gui.my+gui.camY)})
						


	
	# -------PLACE ENEMY MODE
	if(self.placingEnemy):
		selectEnemy(self,gui)
	else:
		self.nav(gui)

	showUnderLayer(self,gui,removeCoords,objectiveNumberCoords)


	self.guiMenuItems(gui,game,enemySelectMode=True)




# --------SELECT ENEMY SECTION

def selectEnemy(self,gui):

	# -------IF DUPLICATE SET TO REMOVE 

	remove          = False
	assignObjective = False
	if(self.enemyPlacementPhase =='placingEnemy'):
		for enemy in self.gameMap['enemyList']:
			if(enemy['row'] == self.selectedEnemyCoords[0] and enemy['col']== self.selectedEnemyCoords[1]):
				if(self.enemyObjectiveMode=='Set Objective Number'):
					assignObjective = True
				else:
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

		if(gui.input.returnedKey.upper()=='W'):
			self.enemyRotation += 90
		if(gui.input.returnedKey.upper()=='S'):
			self.enemyRotation -= 90
		self.enemyRotation = wrapAngle(self.enemyRotation)
		
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
		elif(assignObjective):
			for e in range(len(self.gameMap['enemyList'])):
				enemy = self.gameMap['enemyList'][e]
				if(enemy['row'] == self.selectedEnemyCoords[0] and enemy['col']== self.selectedEnemyCoords[1]):
					if(self.gameMap['enemyList'][e]['objectiveNumber'] == self.currentEnemyObjective):
						self.gameMap['enemyList'][e]['objectiveNumber'] = None
					else:
						self.gameMap['enemyList'][e]['objectiveNumber'] = self.currentEnemyObjective
			
			initMe = True
		
		# MANAGE LOGIC
		else:
			if(self.enemyPlacementPhase =='placingEnemy'): 
				self.enemyPlacementPhase = 'setWayPoints'
			elif(self.enemyPlacementPhase =='setWayPoints'):
				if(len(self.patrolCoords)>3):
					self.enemyPlacementPhase = 'complete'
			gui.clicked                = False

		# ----ADD THE ENEMY
		
		if(self.enemyPlacementPhase=='complete'):
			self.gameMap['enemyList'].append({'kind': self.enemyOptions[self.enemyOptionsIndex],'patrolCoords': self.patrolCoords,'special1':None,'row':self.selectedEnemyCoords[0],'col': self.selectedEnemyCoords[1],'objectiveNumber':None,'rotation':self.enemyRotation})
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


def showUnderLayer(self,gui,removeCoords,objectiveNumberCoords):

	# SHOW ANYTHING THAT MIGHT BE ON THIS LAYER

	for item in self.gameMap['tilelessL1']:
		image = gui.tilelessL1Dict[item['dictKey']][item['index']]
		if(onScreen(item['x'],item['y'],image.get_width(),image.get_height(),gui)):
			drawImage(gui.screen,image,(item['x']- gui.camX,item['y']-gui.camY))
	
	mapTiles    = self.gameMap['metaTiles'] # 2,3 = type index
	sampleImage = gui.tileDict[mapTiles[0][0]['type']][mapTiles[0][0]['index']]
	

	# ------DRAW ALL ENEMIES
	for item in self.gameMap['enemyList']:
		if('rotation' in item.keys()):
			image = pygame.transform.rotate(gui.enemyDict[item['kind']]['image'], item['rotation'])
		else:
			image = gui.enemyDict[item['kind']]['image']
		drawImage(gui.screen,image,( (item['col']*sampleImage.get_width())- gui.camX,(item['row']*sampleImage.get_height())-gui.camY))
		
		# -----DRAW ENEMY OBJECTIVE NUMBER
		if('objectiveNumber' in item.keys()):
			drawTextWithBackground(gui.screen,gui.font,str(item['objectiveNumber']),item['col']*sampleImage.get_width()-gui.camX,item['row']*sampleImage.get_height()-gui.camY+20,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))


	
	# SHOW DELETE BOX 
	if(removeCoords!=None):
		drawImage(gui.screen,gui.base100[3],removeCoords)
	if(objectiveNumberCoords!=None):
		drawImage(gui.screen,gui.base100[11],objectiveNumberCoords)

