from utils._utils import stopTimer,loadingBarClass,wrapAngle,imageAnimateAdvanced
from utils.gameUtils import *
from units.ordinance import *

import random

import math


class parent():
	def __init__(self,gui):
		self.id              = None
		self.name            = 'undefined'
		self.kind            = 'undefined'
		self.classification  = 'enemy'
		self.hp       		 = 100
		self.x               = 750
		self.y               = 730
		self.facing          = 90
		self.alive           = True

		# SHOULD BE OVERRIDEN

		self.hitImage         = gui.scoutRedHit
		self.hitAnimation     = imageAnimateAdvanced(self.hitImage,0.2)


		# ATTRIBUTES 
		self.hp              = 100
		self.speed           = 0
		self.defaultSpeed    = 0
		self.maxSpeed        = 6
		self.maxSpeedDefault = 6
		self.slowDown        = False

		self.decelleration  = 0.2



		# BULLETS 

		self.bulletTimer        = stopTimer()           # BUFF
		self.shootDelay         = 0.1                   # BUFF
		self.bulletsFired       = 0

		# DAMAGE AND INVINCIBLE  

		self.invincible          = False               # BUFF
		self.invincibleDelay     = 0.01                # BUFF
		self.invincibleTimer     = stopTimer()
		self.invincibleCount     = 0
		self.hit 				 = False




		# ERRATIC STEERING
		self.steeringToggle   = True
		self.steeringLimit    = 60
		self.steeringMaxDelay = 3
		self.steeringDelay    = 1                       # BUFF
		self.steeringTimer    = stopTimer()
		self.steeringCounter  = 0



		# SHOOTING
		self.shootToggle        = True  				#	SET BY BUTTON 
		self.shootEnabled       = True                  # BUFF
		self.bulletTimer        = stopTimer()           # BUFF
		self.shootDelay         = 1.2                   # BUFF
		self.targetAquired      = False
		self.targetEnemy        = None

		# DESTRUCT ANIMATION 
		self.destructionComplete = False
		self.debris              = 0


		# OVERRIDE
		self.chosenExplosionImg = gui.smallCloudyExplosion
		self.explosion          = imageAnimateAdvanced(self.chosenExplosionImg,0.1)




	"""
	Moves in the direction of facing
	"""

	def moveForwards(self):
		vel_x = self.speed * math.cos(math.radians(360-self.facing))
		vel_y = self.speed * math.sin(math.radians(360-self.facing))

		self.x += vel_x 
		self.y += vel_y

		# BRING SPEED TO SLOW STOP
		if(self.slowDown):
			self.speed -= self.slowAmount * self.defaultSpeed
			if(self.speed<=0):
				self.speed =0
				self.slowDown = False
		
	
	def stayOnField(self,lv):
		# BORDER CLAMP
		if(self.x + self.w > lv.mapw): self.x -= self.maxSpeed + 3
		if(self.x < lv.mapx): self.x += self.maxSpeed+ 3
		if(self.y + self.h > lv.maph): self.y -= self.maxSpeed+ 3
		if(self.y < lv.mapy): self.y += self.maxSpeed+ 3

	def animateDestruction(self,gui,lv,game):
		x,y = self.x - gui.camX,self.y  - gui.camY

		# *******BE CAREFUL ABOUNT ON SCREEN

		if(self.destructionComplete==False and self.alive==False):
			if(hasattr(self,'centerPoint')):
				x += 0.5*self.centerPoint[0]
				y += 0.5*self.centerPoint[1]
			complete,blitPos = self.explosion.animate(gui,str(str(self.name) +' explosion'),[x,y],game)
			bid = max(([x.id for x in lv.bulletList]),default=0) + 1


			if(self.debris<=12):
				self.debris +=1
				# ADDS DEBRIS TO TO LIST
				lv.bulletList.append(bullet(gui,self.x + 0.5* self.chosenExplosionImg[0].get_width(),self.y+ 0.5* self.chosenExplosionImg[0].get_height(),bid,'debris',random.randrange(0,360),'debris',speed=10, w=3,h=3,colour=(192,192,192)))
			if(complete):
				self.destructionComplete = True

	def damageAnimation(self,gui,lv,game):
		x,y = self.x - gui.camX,self.y  - gui.camY
		
		if(self.alive==True and onScreen(self.x,self.y,self.w,self.h,gui)):
			complete,imageParms = self.hitAnimation.animate(gui,str(self.name) + ' hit',[x,y],game,rotation=self.facing-90)
			if(complete):
				self.hit = False

