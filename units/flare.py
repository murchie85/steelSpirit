from utils._utils import stopTimer, imageAnimateAdvanced,darken
from utils.gameUtils import *
from units.ordinance import *
import pygame
import math
import random



class flare():
	def __init__(self,gui,x,y,bid,classification,facing,playerSpeed=3, speed=3,damage=10,jink='left', source='player'):
		self.x,self.y          = x,y
		self.ox,self.oy        = x,y
		self.id                = bid
		self.classification    = classification
		self.name 			   = 'flare'
		self.ordType           = 'chaff'
		self.facing            = facing
		self.defaultSpeed      = speed
		self.speed             = -5      # INITIALLY 3, WILL BE INCREASED IN ACCEL PHASE
		self.accelleration     = 0.4
		self.plumeTimer        = stopTimer()
		self.plumeDelay        = 0.03
		self.plumeCreated      = 0
		self.range             = 0.7*gui.h
		self.chaffPhase        = 'launched'
		self.jink              = jink
		self.burnFrames        = 0 
		self.burnFramesLim     = 20
		self.lockedOnEnemy     = None
		self.cumulatedDistance = 0
		self.source 		   = source
		self.chaffAnimation	   = imageAnimateAdvanced(gui.chaffHead,0.2)
		self.destructTimer     = stopTimer()
		self.destructTime      = 3
		self.facingChange      = random.choice([-1,1])

		self.w,self.h       = gui.chaffHead[0].get_width(), gui.chaffHead[0].get_height()

		# FOR TERMINATING SELF
		self.alive               = True
		self.debris              = 0


	def move(self,gui,lv,game):
		vel_x = self.speed * math.cos(math.radians(360-self.facing))
		vel_y = self.speed * math.sin(math.radians(360-self.facing))
		self.x += vel_x 
		self.y += vel_y
		self.cumulatedDistance += math.sqrt(vel_x**2 + vel_y**2)

		self.facing += self.facingChange * 0.5


		# --------LAUNCHED BY PLAYER 
		flaresComplete = self.destructTimer.stopWatch(self.destructTime,'flare lifecycle', 'flaresEjected ', game,silence=True)
		if(flaresComplete):
			self.killSelf(lv,killMissilesssage=' self destructed')


		# -----PLUME DESIGN 

		plumeReady = self.plumeTimer.stopWatch(self.plumeDelay,'chaffPlume', str(self.plumeCreated)  + 'plume', game,silence=True)
		if(plumeReady):
			self.plumeCreated +=1
			lv.plumeList.append(plume(gui,self.plumeCreated,self.x + random.randrange(-int(0.3*self.w), int(0.3*self.w)),self.y,self.facing))

		# -----FOOL ENEMIES

		for ordinance in lv.bulletList:

			if(ordinance.classification!=self.classification):
				if(ordinance.ordType=='missile'):
					if(getDistance(self.x,self.y,ordinance.x,ordinance.y) < 200):
						ordinance.facing -=3


		self.rangeManager(gui,lv)


	
	def getRelativeDistanceTravelled(self):
		xDelta        =  self.ox - self.x
		yDelta        =  self.oy - self.y
		distance = math.sqrt((xDelta)**2+(yDelta)**2)
		return(distance)

	def rangeManager(self,gui,lv):
		
		# CHECK IF DISTANCE EXCEEDS RANGE
		if(abs(self.cumulatedDistance)> self.range):
			self.killSelf(lv,killMissilesssage=' chaff fuel burnout OUT OF RANGE')





	# MANAGE BULLET COLLISION WITH SELF 

	def bulletCollides(self,target,gui,lv):
		# IF BULLET CLASSIFICATION IS NOT THE SAME AS TARGETS 
		if(self.classification!=target.classification):
			if(target.name=='missile'):
				target.killMissile(lv,killMissilesssage='missile disabled by chaff')

	# ENSURE MISSILE DIES. 

	def killSelf(self,lv,killMissilesssage=None,printme=False):
		for i in lv.bulletList:
			if(self.id==i.id):
				self.alive = False
				lv.bulletList.remove(self)

	# ONLY DRAW IF IN BOUNDARY

	def drawSelf(self,gui,game,lv):
		x,y = self.x -gui.camX, self.y -gui.camY

		self.chaffAnimation.animate(gui,'chaff',[x-0.5*gui.chaffHead[0].get_width(),y],game,rotation=self.facing)




class plume():
	def __init__(self,gui,_id,x,y,facing,imageType=None):
		self.id              = _id
		self.x               = x
		self.y               = y
		self.plumeImg        = gui.missilePlume
		self.plumeFrames     = imageAnimateAdvanced(self.plumeImg,0.2)
		self.facing          = facing

	def drawSelf(self,gui,game,lv):
		x,y = self.x -gui.camX, self.y -gui.camY
		
		complete, frames = self.plumeFrames.animate(gui,'plume Frames',[x,y],game,rotation=self.facing-90)
		if(complete):
			lv.plumeList.remove(self)



