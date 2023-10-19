from utils._utils import *
from utils.gameUtils import *


def spawnZones(self,gui,game):
	

	# ------ draw back canvas

	showUnderLayer(self,gui)
	# ------ GET MAPTILE LIST
	if('spawnZones' not in self.gameMap.keys()):
		self.gameMap['spawnZones'] = []

	# ------USES THE type and index as keys to gui.tileDict
	collidesWithExisting = False
	startingColour       = (20,30,70)
	collideIndex = 0
	for sz in range(len(self.gameMap['spawnZones'])):
		spawnZone = self.gameMap['spawnZones'][sz]
		# DELETE EXISTING IF CLICKED
		if(gui.mouseCollides(spawnZone[0]-gui.camX,spawnZone[1]-gui.camY,spawnZone[2],spawnZone[3])):
			collidesWithExisting = True
			collideIndex = sz

		# MERGE JOINT BOXES
		for sz2 in range(len(self.gameMap['spawnZones'])):
			spawnZoneTwo = self.gameMap['spawnZones'][sz2]
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
				self.gameMap['spawnZones'].remove(spawnZone)
				self.gameMap['spawnZones'].remove(spawnZoneTwo)
				self.gameMap['spawnZones'].append(newBox)
				return()


		# DRAW SPAWN ZONE
		pygame.draw.rect(gui.screen,startingColour,(spawnZone[0]-gui.camX,spawnZone[1]-gui.camY,spawnZone[2],spawnZone[3]))
		startingColour  = lighten(startingColour)
		drawTextWithBackground(gui.screen,gui.font,str(sz),spawnZone[0]-gui.camX + 0.4*spawnZone[2],spawnZone[1]-gui.camY + 0.3*spawnZone[3],textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))



	# ------MAKE A SPAWN ZONE BY DRAGGING MOUSE


	if(collidesWithExisting and gui.clicked):
		print('deleting ' + str(collideIndex))
		del self.gameMap['spawnZones'][collideIndex]
		gui.pressed=False
		gui.clicked = False
		return()
	elif(self.buttonsHovered!=True):
		boxSelector(self,gui,game)







	# ------ SELECT TILES OR NAVIGATE MODE 

	self.nav(gui)

	# ------ MENU DISPLAY
	self.guiMenuItems(gui,game,showSelectMode=False)



def boxSelector(self,gui,game):

	# SELECTING UNITS 
	selectedArea = self.dragSelect.dragSelect(gui,gui.camX,gui.camY)
	if(selectedArea!=None):
		if(selectedArea[2] > 1 and selectedArea[3] > 1):
			self.gameMap['spawnZones'].append(selectedArea)



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

