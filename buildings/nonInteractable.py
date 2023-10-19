from utils._utils import stopTimer,loadingBarClass,wrapAngle,imageAnimateAdvanced
from utils.gameUtils import *
from units.ordinance import *

import random

import math


class nonInteractable():
	def __init__(self,x,y,images,imageObject, gui):
		self.id              = None
		self.name            = 'undefined'
		self.kind            = 'undefined'
		self.classification  = 'enemy'
		self.x               = x
		self.y               = y
		self.facing          = 90
		self.images          = imageObject
		self.w               = images[0].get_width()
		self.h               = images[0].get_height()

	def drawSelf(self,gui,game,lv=None):
		x,y = self.x - gui.camX,self.y  - gui.camY
		
		if(onScreen(self.x,self.y,self.w,self.h,gui)):
			self.images.animate(gui,self.kind + str(self.id),[x,y],game,rotation=self.facing-90)
