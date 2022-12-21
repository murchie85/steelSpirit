from utils._utils import stopTimer,dynamicBorder,drawTextWithBackground,getTextWidth,getTextHeight

class profilePage():
	def __init__(self,gui):
		self.timer = stopTimer()
		self.borderColour  = 60, 165, 200
		self.dynamicBorder = dynamicBorder(borderColour=self.borderColour,noShadeShifts=10)

	def renderProfile(self,gui,game):
		self.dynamicBorder.animateBorder('menu border',game,gui)
		chosenFont = gui.largeFont
		borderColour=self.borderColour

		drawTextWithBackground(gui.screen,gui.hugeFont,'Profile Stats',0.48*(gui.w- getTextWidth(gui.hugeFont,'Profile Stats') ),0.05*gui.h - 0.5* getTextHeight(gui.hugeFont,'Profile Summary'),setWidth=1.2*getTextWidth(gui.hugeFont,'Battle Stats'),setHeight=None, textColour=(200, 200, 200),backColour= (0,0,0),borderColour=None)