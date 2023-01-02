from utils._utils import *
from utils.gameUtils import *


def editLayer2(self,gui,game):
	

	# SHOW BOTTOM LAYER
	showUnderLayer(self,gui)

	# INIT LAYER 2 IF NOT EXIST

	if('layer2' not in self.gameMap.keys()):

		# ------- INITIALISE TILEMAP WITH DEFAULT DICT FOR EVERY COL AND ROW
		layer2 = []
		for row in range(self.gameMap['rows']):
			currentRow = []
			for col in range(self.gameMap['cols']):
				currentRow.append({'placed': False, 'animated':False,'type':'base','index':8})

			layer2.append(currentRow)

		self.gameMap['layer2'] = layer2



	# SET MAPTILES VAR

	mapTiles = self.gameMap['layer2']

	x = 0
	y = 0
	
	# USES THE type and index as keys to gui.layer2Dict

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
				image = gui.layer2Dict[col['type']][col['index']]


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
					drawImage(gui.screen, gui.layer2Dict[self.l2Options[self.l2OptionsIndex]][self.l2OptionsSubIndex],(x-gui.camX,y-gui.camY))


				# DRAW THE CURRENT TILE
				else:
					image.set_colorkey((0, 0, 0))
					#pygame.Surface.set_colorkey(image, [0,0,0])
					drawImage(gui.screen,image,(x-gui.camX,y-gui.camY))



			

			x += image.get_width()

		y+= image.get_height()
		x = 0






	# SELECT TILES OR NAVIGATE MODE 

	if(self.editingTile):
		selectL2Tile(self,gui)
	else:
		self.nav(gui)


	self.guiMenuItems(gui,game)


# --------SELECT TILE SECTION

def selectL2Tile(self,gui):

	"""
	GET ALL TILES OF CURRENT tileOptionsIndex
	DISPLAY THEM IN A GRID, IF YOU SCROLL TO BOTTOM MORE LOADS

	"""
	#gui.layer2Dict[self.l2Options[self.l2OptionsIndex]][self.l2OptionsSubIndex]
	#---------TILE LIST SELECTOR
	tx,ty = 0.75*gui.w,0.2*gui.h
	tcx = tx
	currentTiles  = gui.layer2Dict[self.l2Options[self.l2OptionsIndex]]
	colCounter,rowCounter = 0,0
	hoverSelectedTileSubIndex = None
	inrementPageB  = gui.input.returnedKey.upper() == 'F'
	inrementPage   = drawSelectableImage(gui.base100[4],gui.base100[5],(tx+190	,ty+480),gui)
	decrementPage  = drawSelectableImage(gui.base100[6],gui.base100[7],(tx,ty+480),gui)

	if(decrementPage):  self.pagedIndex -= self.previousIndex
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
		if(colCounter>=3):
			rowCounter +=1
			tx = tcx
			ty += 95
			colCounter = 0
			if(rowCounter>4):
				if(inrementPage or inrementPageB):
					self.previousIndex = self.pagedIndex
					self.pagedIndex = i
				break

	# DRAW TILE NAME 

	setWidth=getTextWidth(gui.bigFont,'A menu item yep sure.')
	drawTextWithBackground(gui.screen,gui.bigFont,self.l2Options[self.l2OptionsIndex],900,110,setWidth=setWidth ,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))
	

	# increment major index (map type)
	if(gui.input.returnedKey.upper()=='D'): 
		self.l2OptionsIndex += 1
		self.l2OptionsSubIndex = 0
		self.pagedIndex = 0
		self.previousIndex = 0
	if(gui.input.returnedKey.upper()=='A'): 
		self.l2OptionsIndex -= 1
		self.l2OptionsSubIndex =0 
		self.pagedIndex = 0
		self.previousIndex = 0
	
	# TOP LEVEL SELECTION
	if(self.l2OptionsIndex<0):self.l2OptionsIndex = len(self.l2Options)-1
	if(self.l2OptionsIndex>len(self.l2Options)-1):self.l2OptionsIndex = 0

	# increment minor index (map variation)
	if(gui.input.returnedKey.upper()=='S'): self.l2OptionsSubIndex += 1
	if(gui.input.returnedKey.upper()=='W'): self.l2OptionsSubIndex -= 1
	
	if(self.l2OptionsSubIndex > len(gui.layer2Dict[self.l2Options[self.l2OptionsIndex]])-1): self.l2OptionsSubIndex = 0
	if(self.l2OptionsSubIndex<0):self.l2OptionsSubIndex = len(gui.layer2Dict[self.l2Options[self.l2OptionsIndex]])-1


	if(gui.rightClicked):
		self.editingTile        = False
		self.tileSelectionList   = []
		gui.clicked              = False
		self.tileSelecting       = False

	if(gui.input.returnedKey.upper()=='RETURN' or gui.clicked):
		for tile in self.tileSelectionList:
			subIndex = self.l2OptionsSubIndex
			if(hoverSelectedTileSubIndex!=None):
				subIndex = hoverSelectedTileSubIndex
			self.gameMap['layer2'][tile[0]][tile[1]] = {'placed': True, 'animated':False,'type':self.l2Options[self.l2OptionsIndex],'index':subIndex}
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
				image = gui.layer2Dict[c['type']][c['index']]
				#image.set_alpha(200)
				if(onScreen(x,y,image.get_width(),image.get_height(),gui)):


					drawImage(gui.screen,image,(x- gui.camX,y-gui.camY))
					counter +=1
			

			x += image.get_width()
		y+= image.get_height()
		x = 0

