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
		messagex, messagey  = 500,300
		drawTextWithBackground(gui.screen,gui.font,'Create TileLess Layer 1?',messagex,messagey,textColour=(80, 120, 255),backColour= (0,0,0),borderColour=(50,50,200))
		tw,th                        = getTextWidth(gui.bigFont,'A menu item.'),getTextHeight(gui.bigFont,'A menu item yep sure.')
		yes,tex,tey,saveHovered      = simpleButtonHovered(messagex,messagey + 3*th,'yes',gui,gui.font,setTw=tw,backColour=(0,0,0),borderColour=(50,50,200), textColour=(255,255,255))
		no,ttx,tty,backHovered       = simpleButtonHovered(tex + 0.1*tw,messagey +3*th,'No',gui,gui.font,setTw=tw,backColour=(0,0,0),borderColour=(50,50,200), textColour=(255,255,255))


		# ------- INITIALISE TILEMAP WITH DEFAULT DICT FOR EVERY COL AND ROW
		if(yes):
			tilelessL1 = []
			#tilelessL1 examples ... [ {'dictKey': keyTotilelessL1Dict, 'x':0,'y':0, 'animated':False}]
			self.gameMap['tilelessL1'] = tilelessL1
		if(no):
			self.tileMode ='Enemies'
			self.state    ='enemyPlacement'

	else:

		# SHOW BOTTOM LAYER
		showUnderLayer(self,gui)

		if(self.buttonsHovered!=True):
			# ---- GO TO SELECT ITEM 
			if(gui.clicked and not self.editingTile and self.tl1SelectionState == None):
				self.editingTile = True
				gui.clicked = False
			
			# DRAW THE ITEM AT THE CURSOR 
			if(not self.editingTile and self.tl1SelectionState == 'placingItem'):
				image = gui.tilelessL1Dict[self.t1Options[self.t1OptionsIndex]][self.t1OptionsSubIndex]
				drawImage(gui.screen,image,((gui.mx+gui.camX)-gui.camX, (gui.my+gui.camY)-gui.camY))

			# --- COMPLETE ITEM PLACEMENT
			if(gui.clicked and not self.editingTile and self.tl1SelectionState == 'placingItem'):
				self.tl1SelectedCoords = gui.mx + gui.camX, gui.my + gui.camY
				gui.clicked = False
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

	tx,ty = 0.75*gui.w,0.2*gui.h
	tcx = tx
	currentTiles  = gui.tilelessL1Dict[self.t1Options[self.t1OptionsIndex]]
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

	# SHOW FIRST LAYER 
	x = 0
	y = 0
	# USES THE type and index as keys to gui.tilelessL1Dict
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

	# SHOW ANYTHING THAT MIGHT BE ON THIS LAYER
	for item in self.gameMap['tilelessL1']:
		image = gui.tilelessL1Dict[item['dictKey']][item['index']]
		if(onScreen(item['x'],item['y'],image.get_width(),image.get_height(),gui)):
			drawImage(gui.screen,image,(item['x']- gui.camX,item['y']-gui.camY))

