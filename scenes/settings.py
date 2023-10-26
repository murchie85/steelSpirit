from utils._utils import stopTimer,dynamicBorder,drawTextWithBackground,getTextWidth,getTextHeight,drawImage
import pygame

class settingsPage():
	def __init__(self,gui):
		self.timer = stopTimer()
		self.borderColour  = 60, 165, 200
		self.dynamicBorder = dynamicBorder(borderColour=self.borderColour,noShadeShifts=10)
		self.alphaI         = 100      # used on fade out (goes up to 255)
		self.fadeSurface    = pygame.Surface((gui.w,gui.h))


	def renderSettings(self,gui,game):


		# --------draw background image

		drawImage(gui.screen, gui.settingsBackground,(0,0))

		# --------draw alpha opacity mask over it 
		self.fadeSurface.set_alpha(self.alphaI)
		self.fadeSurface.fill((0,0,0))
		gui.screen.blit(self.fadeSurface,(0,0))

		# --------draw dynamic colour border 
		self.dynamicBorder.animateBorder('menu border',game,gui)
		chosenFont = gui.largeFont
		borderColour=self.borderColour

		#  ------- draw setting text
		drawTextWithBackground(gui.screen,gui.hugeFont,'Settings Mode',0.48*(gui.w- getTextWidth(gui.hugeFont,'Profile Stats') ),0.05*gui.h - 0.5* getTextHeight(gui.hugeFont,'Profile Summary'),setWidth=1.2*getTextWidth(gui.hugeFont,'Battle Stats'),setHeight=None, textColour=(200, 200, 200),backColour= (0,0,0),borderColour=None)