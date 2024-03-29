from utils._utils import *
from utils.gameUtils import *



"""
# layer 2
self.t1Options             = list(gui.tilelessL1Dict.keys())
self.t1OptionsIndex      = 0
self.t1OptionsSubIndex   = 0

		# tileLess
self.t1Options           = list(gui.tilelessL1Dict.keys())
self.t1OptionsIndex      = 0
self.t1OptionsSubIndex   = 0
"""


# TODO 

# replace values above 
# Ask to add tileless if not available
# REPLACE LOGIC TO 

#tilelessL1Dict

def tilelessL1(self,gui,game):
	



	# INIT LAYER 2 IF NOT EXIST

	if('tilelessL1' not in self.gameMap.keys()):
		self.gameMap['tilelessL1'] = []

	else:

		# SHOW BOTTOM LAYER
		showUnderLayer(self,gui)
		




		if(self.buttonsHovered!=True):


			# --- TILE ALREADY EXISTS

			if(self.tl1SelectionState == None):

				if(not self.editingTile):
					
					# REMOVE EXISTING TILE 
					for t in range(0,len(self.gameMap['tilelessL1'])):
						tile = self.gameMap['tilelessL1'][t]
						image = gui.tilelessL1Dict[tile['dictKey']][tile['index']]
						if(gui.mouseCollides(tile['x']-gui.camX,tile['y']-gui.camY,image.get_width(),image.get_height())):
							drawImage(gui.screen,gui.base100[3],(gui.mx,gui.my))
							if(gui.clicked):
								del self.gameMap['tilelessL1'][t]
								gui.clicked=False
								return()


				# ---- GO TO SELECT ITEM 

				if(gui.clicked and not self.editingTile):
					self.editingTile = True
					gui.clicked = False

			

			# DRAW THE ITEM AT THE CURSOR 

			if(self.tl1SelectionState == 'placingItem' and not self.editingTile):
				image = gui.tilelessL1Dict[self.t1Options[self.t1OptionsIndex]][self.t1OptionsSubIndex]
				drawImage(gui.screen,image,((gui.mx+gui.camX)-gui.camX, (gui.my+gui.camY)-gui.camY))


			# --- COMPLETE ITEM PLACEMENT

			if(gui.clicked and not self.editingTile and self.tl1SelectionState == 'placingItem'):
				self.tl1SelectedCoords = gui.mx + gui.camX, gui.my + gui.camY
				gui.clicked = False
				
				if('animated' in self.t1Options[self.t1OptionsIndex]):
					self.gameMap['tilelessL1'].append({'dictKey':self.t1Options[self.t1OptionsIndex],'index':self.t1OptionsSubIndex,'animated':True,'x':self.tl1SelectedCoords[0], 'y':self.tl1SelectedCoords[1]} )
				else:
					self.gameMap['tilelessL1'].append({'dictKey':self.t1Options[self.t1OptionsIndex],'index':self.t1OptionsSubIndex,'animated':False,'x':self.tl1SelectedCoords[0], 'y':self.tl1SelectedCoords[1]} )
				
				self.editingTile         = False
				gui.clicked              = False
				self.tl1SelectedCoords   = []
				self.tl1SelectionState   = None
				self.t1OptionsIndex      = 0
				self.t1OptionsSubIndex   = 0

			# RESET SELECTION WITH RIGHT CLICK

			if(gui.rightClicked and self.tl1SelectionState == 'placingItem'):
				self.editingTile        = False
				gui.clicked              = False
				self.tl1SelectedCoords   = []
				self.tl1SelectionState   = None
				self.t1OptionsIndex      = 0
				self.t1OptionsSubIndex   = 0



	# SELECT TILES OR NAVIGATE MODE 

	if(self.editingTile and not self.buttonsHovered):
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


	


	#---------TILE LIST SELECTOR

	tx,ty = 0.25*gui.w,0.6*gui.h
	tcx = tx
	currentTiles  = gui.tilelessL1Dict[self.t1Options[self.t1OptionsIndex]]
	colCounter,rowCounter = 0,0
	hoverSelectedTileSubIndex = None
	inrementPageB  = gui.input.returnedKey.upper() == 'F'
	inrementPage   = drawSelectableImage(gui.base100[4],gui.base100[5],(tx-190	,ty),gui)
	decrementPage  = drawSelectableImage(gui.base100[6],gui.base100[7],(tx-190,ty+100),gui)

	if(decrementPage):  self.pagedIndex = self.previousIndex
	if(self.pagedIndex<0): self.pagedIndex = 0
	
	# SHOW TILE PREVIEW 
	if(self.pagedIndex>len(currentTiles)-1): self.pagedIndex = len(currentTiles)-1
	for i in range(self.pagedIndex,len(currentTiles)):
		x = currentTiles[i]
		
		# draw the image 
		if(x.get_width() > 300):
			drawImage(gui.screen,x,(tx,ty),(0.5*x.get_width(),0.5*x.get_height(),100,100))
		else:
			drawImage(gui.screen,x,(tx,ty))
		

		if(gui.mouseCollides(tx,ty,100,100)):
			pygame.draw.rect(gui.screen,(200,200,200),(tx,ty,100,100),5)
			hoverSelectedTileSubIndex = i
		else:
			pygame.draw.rect(gui.screen,(5,9,20),(tx,ty,100,100),5)
		tx+= 95
		colCounter+=1
		if(colCounter>=10):
			rowCounter +=1
			tx = tcx
			ty += 95
			colCounter = 0
			if(rowCounter>3):
				if(inrementPage or inrementPageB):
					self.previousIndex = self.pagedIndex
					self.pagedIndex = i
				break

	# DRAW TILE NAME 

	setWidth=getTextWidth(gui.bigFont,'A menu item yep sure.')
	drawTextWithBackground(gui.screen,gui.bigFont,self.t1Options[self.t1OptionsIndex],900,110,setWidth=setWidth ,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))
	

	# increment major index (map type)
	if(gui.input.returnedKey.upper()=='D'): 
		self.t1OptionsIndex += 1
		self.t1OptionsSubIndex = 0
		self.pagedIndex = 0
		self.previousIndex = 0
	if(gui.input.returnedKey.upper()=='A'): 
		self.t1OptionsIndex -= 1
		self.t1OptionsSubIndex =0 
		self.pagedIndex = 0
		self.previousIndex = 0
	
	# TOP LEVEL SELECTION
	if(self.t1OptionsIndex<0):self.t1OptionsIndex = len(self.t1Options)-1
	if(self.t1OptionsIndex>len(self.t1Options)-1):self.t1OptionsIndex = 0

	# increment minor index (map variation)
	if(gui.input.returnedKey.upper()=='S'): self.t1OptionsSubIndex += 1
	if(gui.input.returnedKey.upper()=='W'): self.t1OptionsSubIndex -= 1
	
	if(self.t1OptionsSubIndex > len(gui.tilelessL1Dict[self.t1Options[self.t1OptionsIndex]])-1): self.t1OptionsSubIndex = 0
	if(self.t1OptionsSubIndex<0):self.t1OptionsSubIndex = len(gui.tilelessL1Dict[self.t1Options[self.t1OptionsIndex]])-1


	if(gui.rightClicked):
		self.editingTile        = False
		gui.clicked              = False
		self.tl1SelectedCoords   = []


	# IF USER SELECTS A TILE FIRST 
	if(gui.input.returnedKey.upper()=='RETURN' or gui.clicked and self.tl1SelectionState==None):
		self.tl1SelectionState = 'placingItem'
		# set the sub index
		if(hoverSelectedTileSubIndex!=None):
			self.t1OptionsSubIndex = hoverSelectedTileSubIndex
		self.editingTile        = False
		gui.clicked              = False







def showUnderLayer(self,gui):
	mapTiles = self.gameMap['metaTiles']

	# -----SHOW LAYER ONE TILES 

	# USES THE type and index as keys to gui.tileDict
	sampleImage = gui.tileDict[mapTiles[0][0]['type']][mapTiles[0][0]['index']]
	# *** SETTING THE INDEX'S GREATLY SPEEDS UP AND REDUCES LAG
	yIndexOne = math.floor((gui.camY)/sampleImage.get_height())
	yIndexTwo = math.ceil((gui.camY+gui.camH)/sampleImage.get_height())
	#
	xIndexOne = math.floor((gui.camX)/sampleImage.get_width())
	xIndexTwo = math.ceil((gui.camX+gui.camW)/sampleImage.get_width())
	if(xIndexOne<0):
		return()
	#print(' number of rows {}'.format(str(len(mapTiles))))
	for r in range(yIndexOne,yIndexTwo):
		if(r < len(mapTiles)):
			row = mapTiles[r]
			y = r *sampleImage.get_height()
			for c in range(xIndexOne,xIndexTwo):
				if(c <len(row)):
					col = row[c]
					x = c *sampleImage.get_width()
					
					if(col['animated']==False ):
						image = gui.tileDict[col['type']][col['index']]
						#image.set_alpha(200)
						if(onScreen(x,y,image.get_width(),image.get_height(),gui)):
							drawImage(gui.screen,image,(x- gui.camX,y-gui.camY))


	# -----SHOW ANYTHING THAT MIGHT BE ON THIS LAYER

	
	for item in self.gameMap['tilelessL1']:
		image = gui.tilelessL1Dict[item['dictKey']][item['index']]
		if(onScreen(item['x'],item['y'],image.get_width(),image.get_height(),gui)):
			drawImage(gui.screen,image,(item['x']- gui.camX,item['y']-gui.camY))

