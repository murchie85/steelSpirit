from utils._utils import *
from utils.gameUtils import *


def editMap(self,gui,game):
	# GET MAPTILE LIST
	mapTiles = self.gameMap['metaTiles']
	
	# USES THE type and index as keys to gui.tileDict

	# MANAGES STATE
	
	if(gui.clicked and self.tileHovered and self.buttonsHovered!=True):
		if(self.selectMode=='tile'):
			if(self.tileSelecting==False and self.editingTile==False):
				self.tileSelecting = True
				gui.clicked        = False
			elif(self.tileSelecting==True and self.editingTile==False):
				self.editingTile = True
				self.tileSelecting = False
				gui.clicked = False
		


	self.tileHovered = False
	# draw back canvas
	showUnderLayer(self,gui)

	if(self.selectMode=='tile'):
		tileSelector(self,gui,game,mapTiles)
	if(self.selectMode=='box'):
		boxSelector(self,gui,game,mapTiles)




	# SELECT TILES OR NAVIGATE MODE 

	if(self.editingTile):
		selectTile(self,gui)
	else:
		self.nav(gui)


	self.guiMenuItems(gui,game)



# --------TILE SELECTOR MODE 

def tileSelector(self,gui,game,mapTiles):
	x = 0
	y = 0
	for r in range(len(mapTiles)):
		row = mapTiles[r]
		
		for c in range(len(row)):
			col = row[c]

			if(col['animated']==False ):
				image = gui.tileDict[col['type']][col['index']]


				# -----------IF HOVER MULTI-SELECT 

				if(gui.mouseCollides(x-gui.camX,y-gui.camY,image.get_width(),image.get_height())):
					self.tileHovered = True
					if(self.tileSelecting):
						# ADD TO EDIT LIST
						selectedCoords = [r,c]
						if(selectedCoords not in self.tileSelectionList): 
							self.tileSelectionList.append(selectedCoords)

				#  -----------IF SELECTED, SHOW BASE SELECTING TILE

				if([r,c] in self.tileSelectionList and self.tileSelecting):
					drawImage(gui.screen,gui.base100[2],(x-gui.camX,y-gui.camY))
			
				#  -----------IF EDITING, SHOW THE CURRENT BROWSED IMAGE

				elif([r,c] in self.tileSelectionList and self.editingTile):
					drawImage(gui.screen, gui.tileDict[self.tileOptions[self.tileOptionsIndex]][self.tileOptionsSubIndex],(x-gui.camX,y-gui.camY))


			x += image.get_width()

		y+= image.get_height()
		x = 0

def boxSelector(self,gui,game,mapTiles):

	# SELECTING UNITS 
	selectedArea = self.dragSelect.dragSelect(gui,gui.camX,gui.camY)
	
	# if CURSOR AREA SELECTION
	if(selectedArea!=None):

		mapTiles = self.gameMap['metaTiles']
		x,y = 0,0
		# USES THE type and index as keys to gui.layer2Dict
		counter = 0

		for r in range(len(mapTiles)):
			row = mapTiles[r]
			for c in range(len(row)):
				col = row[c]
				if(col['animated']==False ):
					image = gui.tileDict[col['type']][col['index']]
					if(collidesObjectless(x,y,image.get_width(),image.get_height(),selectedArea[0],selectedArea[1],selectedArea[2],selectedArea[3])):
						selectedCoords = [r,c]
						if(selectedCoords not in self.tileSelectionList): 
							self.tileSelectionList.append(selectedCoords)

				x += image.get_width()
			y+= image.get_height()
			x = 0

		self.editingTile   = True
		self.tileSelecting = False
		self.selectMode    ='tile'  




# --------SELECT TILE SECTION

def selectTile(self,gui):

	"""
	GET ALL TILES OF CURRENT tileOptionsIndex
	DISPLAY THEM IN A GRID, IF YOU SCROLL TO BOTTOM MORE LOADS

	"""
	#gui.tileDict[self.tileOptions[self.tileOptionsIndex]][self.tileOptionsSubIndex]
	#---------TILE LIST SELECTOR
	tx,ty = 0.2*gui.w,0.58*gui.h
	tcx = tx
	currentTiles  = gui.tileDict[self.tileOptions[self.tileOptionsIndex]]
	colCounter,rowCounter = 0,0
	hoverSelectedTileSubIndex = None
	inrementPageB  = gui.input.returnedKey.upper() == 'F'
	
	
	inrementPage   = drawSelectableImage(gui.base100[4],gui.base100[5],(tx-190	,ty),gui)
	decrementPage  = drawSelectableImage(gui.base100[6],gui.base100[7],(tx-190,ty+100),gui)
	fillAll        = drawSelectableImage(gui.base100[9],gui.base100[10],(tx-190,ty+200),gui)





	if(decrementPage):  self.pagedIndex = self.previousIndex
	if(self.pagedIndex<0): self.pagedIndex = 0
	
	if(self.pagedIndex>len(currentTiles)-1): self.pagedIndex = len(currentTiles)-1
	for i in range(self.pagedIndex,len(currentTiles)):
		x = currentTiles[i]
		drawImage(gui.screen,x,(tx,ty))
		if(gui.mouseCollides(tx,ty,100,100)):
			pygame.draw.rect(gui.screen,(200,200,200),(tx,ty,100,100),5)
			hoverSelectedTileSubIndex = i
		else:
			pygame.draw.rect(gui.screen,(5,9,20),(tx,ty,100,100),5)
		tx+= 95
		colCounter+=1
		if(colCounter>=12):
			rowCounter +=1
			tx = tcx
			ty += 95
			colCounter = 0
			if(rowCounter>2):
				if(inrementPage or inrementPageB):
					self.previousIndex = self.pagedIndex
					self.pagedIndex = i
				break

	# DRAW TILE NAME 

	setWidth=getTextWidth(gui.bigFont,'A menu item yep sure.')
	drawTextWithBackground(gui.screen,gui.bigFont,self.tileOptions[self.tileOptionsIndex],900,110,setWidth=setWidth ,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))
	

	# increment major index (map type)
	if(gui.input.returnedKey.upper()=='D'): 
		self.tileOptionsIndex += 1
		self.tileOptionsSubIndex = 0
		self.pagedIndex = 0
		self.previousIndex = 0
	if(gui.input.returnedKey.upper()=='A'): 
		self.tileOptionsIndex -= 1
		self.tileOptionsSubIndex =0 
		self.pagedIndex = 0
		self.previousIndex = 0
	
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
			subIndex = self.tileOptionsSubIndex
			if(hoverSelectedTileSubIndex!=None):
				subIndex = hoverSelectedTileSubIndex
			self.gameMap['metaTiles'][tile[0]][tile[1]] = {'placed': True, 'animated':False,'type':self.tileOptions[self.tileOptionsIndex],'index':subIndex}
			self.editingTile        = False
			self.tileSelectionList   = []
			gui.clicked              = False
			self.tileSelecting       = False

	if(fillAll):
		for r in range(0,len(self.gameMap['metaTiles'])):
			row = self.gameMap['metaTiles'][r]
			for c in range(0,len(row)):
				col = row[c]
				selectedType = self.gameMap['metaTiles'][self.tileSelectionList[0][0]][self.tileSelectionList[0][1]] 
				if(col['type']==selectedType['type'] and col['index']==selectedType['index']):
					self.gameMap['metaTiles'][r][c]['type']  = self.tileOptions[self.tileOptionsIndex]
					self.gameMap['metaTiles'][r][c]['index'] = self.tileOptionsSubIndex

		self.editingTile        = False
		self.tileSelectionList   = []
		gui.clicked              = False
		self.tileSelecting       = False







def showUnderLayer(self,gui):
	mapTiles = self.gameMap['metaTiles']

	#gui.screen.fill((255,0,0 ))
	x = 0
	y = 0
	# USES THE type and index as keys to gui.layer2Dict
	counter = 0
	for row in mapTiles:
		for c in row:
			if(c['animated']==False ):
				image = gui.tileDict[c['type']][c['index']]
				#image.set_alpha(200)
				if(onScreen(x,y,image.get_width(),image.get_height(),gui)):


					drawImage(gui.screen,image,(x- gui.camX,y-gui.camY))
					counter +=1
			

			x += image.get_width()
		y+= image.get_height()
		x = 0

