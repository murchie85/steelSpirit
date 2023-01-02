from utils._utils import *
from utils.gameUtils import *

def mapMakerOptions(self,gui):
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

		