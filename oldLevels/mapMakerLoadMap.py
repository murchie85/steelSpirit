from utils._utils import *
from utils.gameUtils import *

def loadMap(self,gui,game):
	borderColour = (153, 204, 255)
	backColour   = (51, 102, 255)
	textColour   = (255,255,255)

	gui.screen.fill((51, 51, 153))
	drawImage(gui.screen,gui.madge,[0,0])
	
	self.levelScreenMask.set_alpha(self.alphaI)
	self.levelScreenMask.fill((0,0,0))
	gui.screen.blit(self.levelScreenMask,(0,0))

	# ------GET LOADED MAPS 
	loadPath       = 'state/old/'
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

