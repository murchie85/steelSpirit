from utils._utils import *
from utils.gameUtils import *
from utils._utils import stopTimer
from ordinance import *
import time
import random

# CAMERA IS ALL MANAGED BY PLAYER 
class player():
	def __init__(self,gui):
		self.id             = 0
		self.classification = 'ally'
		self.alive          = True

		# IMAGE AND DIRECTION 
		self.x              = 750
		self.y              = 730
		self.facing         = 90
		self.images         = imageAnimateAdvanced(gui.player,0.2)
		self.boostImage     = imageAnimateAdvanced(gui.playerBoost,0.2)
		self.shadow         = imageAnimateAdvanced(gui.playerShadow,0.2)
		self.w              = int(gui.player[0].get_width())
		self.h              = int(gui.player[0].get_height())
		self.blitPos       = [self.x,self.y]
		self.shadowPos     = [self.x,self.y]
		self.rotatedW	   = self.w
		self.rotatedH	   = self.h
		
		# ATTRIBUTES 
		self.hp              = 100
		self.speed           = 0
		self.maxSpeed        = 6
		self.maxSpeedDefault = 6
		self.boostSpeed      = 12
		self.boosting        = False
		self.boostTimer      = stopTimer()           # BUFF
		self.boostCoolDown   = stopTimer()
		self.boostAvailable  = True
		self.boostCount      = 0

		self.decelleration  = 0.2
		self.rotationSpeed  = 5



		# BULLETS 

		self.bulletTimer        = stopTimer()           # BUFF
		self.shootDelay         = 0.1                   # BUFF
		self.bulletsFired       = 0


		# DESTROY 
		self.destructionComplete = False


	
	# MANAGE ACCELLERATION 
	def actions(self,gui,game,lv):
		
		# GET PRESSED KEYS

		pressedKeys     = [x.upper() for x in gui.input.pressedKeys]

		self.classicControls(pressedKeys,lv,game)


		#---------CAMERA MOVEMENT

		margins     = [0.9*gui.w,0.1*gui.w,0.85*gui.h,0.15*gui.h]
		softMargins = [0.7*gui.w,0.3*gui.w, 0.65*gui.h, 0.35*gui.h]


		# MOVE THE CAMERA SO IT STAYS AHEAD OF  MARGINS
		if(self.x  > gui.camX + softMargins[0]): 
			gui.camX += self.maxSpeed

		if(self.x  < gui.camX + softMargins[1]): 
			gui.camX -= self.maxSpeed

		if(self.y  > gui.camY + softMargins[2]): 
			gui.camY += self.maxSpeed

		if(self.y  < gui.camY + softMargins[3]): 
			gui.camY -= self.maxSpeed

		"""	
		if(self.x  > gui.camX + margins[0]): 
			gui.camX += self.maxSpeed

		if(self.x  < gui.camX + margins[1]): 
			gui.camX -= self.maxSpeed	
	
		if(self.y  > gui.camY + margins[2]): 
			gui.camY += self.maxSpeed

		if(self.y  < gui.camY + margins[3]): 
			gui.camY -= self.maxSpeed

		"""


		# ---------SHOOT

		if('H' in pressedKeys):
			self.shoot(game,lv,gui)




	# CALLED BY allyActions/enemyActions
	def shoot(self,game,lv,gui,bulletSpeed=10, bulletColour=(255,177,42)):

		# BULLET DELAY TIMER
		shotAvailable = self.bulletTimer.stopWatch(self.shootDelay,'player shoot', str(self.id + self.bulletsFired), game,silence=True)
		
		# IF SHOOT CRITEREA MET,
		if((shotAvailable)):
			self.bulletsFired +=1
			# ADDS BULLET TO BULLET LIST
			bid = max(([x.id for x in lv.bulletList]),default=0) + 1
			lv.bulletList.append(bullet(gui,self.blitPos[0],self.blitPos[1],bid,self.classification, self.facing,'slitherShot', speed=self.maxSpeed + bulletSpeed,colour=bulletColour))
		


	def drawSelf(self,gui,game):
		x,y = self.x - gui.camX,self.y  - gui.camY
		
		if(self.alive==True and onScreen(self,gui)):
			
			self.shadow.animate(gui,'player shadow',[self.shadowPos[0],self.shadowPos[1]],game,rotation=self.facing-90,noseAdjust=True)
			
			if(self.boosting):
				animate,imageParms = self.boostImage.animate(gui,'playerBoosting',[x,y],game,rotation=self.facing-90)
			else:
				animate,imageParms = self.images.animate(gui,'player',[x,y],game,rotation=self.facing-90)
			
			self.blitPos = imageParms['midTop']
			self.shadowPos = imageParms['behind']
			

		else:
			if(self.destructionComplete==False):
				"""
				complete,blitPos,w,h = self.explosion.animate(battleManager.gui,'drone kaboom',[x,y],battleManager.game)
				bid = max(([x.id for x in battleManager.bulletList]),default=0) + 1


				if(self.debris<=5):
					self.debris +=1
					# ADDS DEBRIS TO TO LIST
					battleManager.bulletList.append(bullet(self.x + 0.5* battleManager.gui.droneExplosion[0].get_width(),self.y+ 0.5* battleManager.gui.droneExplosion[0].get_height(),bid,'debris', random.randrange(0,360),w=0.2*self.w,h=0.2*self.h,colour=(192,192,192),speed=2 ))
					
				if(complete):
					self.destructionComplete = True

				"""

	def classicControls(self,pressedKeys,lv,game):

		# ACCELELRATION FLAG
		accell= False
		# GET DIRECTION OF ACCELLERATION
		if('W' in pressedKeys ):
			self.speed += 0.4
			accell = True
		if('S' in pressedKeys):
			self.speed -= 0.4
			accell = True
		if('D' in pressedKeys):
			self.facing -= 4
		if('A' in pressedKeys):
			self.facing += 4

		# SPEED BOOST
		if('J' in pressedKeys):
			
			boostComplete = self.boostTimer.stopWatch(2,'boost', str(self.boostCount),game,silence=True)
			
			if(not boostComplete):
				self.boosting = True
				self.maxSpeed = self.boostSpeed
			if(boostComplete==True):
				self.boostAvailable = False
			
		if(('J' not in pressedKeys) or self.boostAvailable == False):
			self.boosting       = False
			self.maxSpeed       = self.maxSpeedDefault
			if(self.boostAvailable == False):
				self.boostAvailable = self.boostCoolDown.stopWatch(2,'boost cooldown Counter', str(self.boostCount),game,silence=True)
				if(self.boostAvailable):
					self.boostCount +=1

			

		#self.boostTimer      = stopTimer()           # BUFF
		#self.boostCoolDown   = stopTimer()
		#self.boostAvailable  = True
	
		# WRAP ANGLE
		self.facing = wrapAngle(self.facing)

		# CLAMP SPEED
		self.speed = clamp(self.speed,self.maxSpeed)

		# APPLY SPEED COMPONENT
		vel_x = self.speed * math.cos(math.radians(360-self.facing))
		vel_y = self.speed * math.sin(math.radians(360-self.facing))

		# UPDATE POSITION
		self.x += int(vel_x )
		self.y += int(vel_y)

		# SLOWDOWN WHEN NOT ACCELLERATING
		if(accell==False):
			self.speed = zero(self.speed,self.decelleration)


		# BORDER CLAMP
		if(self.x + self.w > lv.mapw): self.x -= self.maxSpeed
		if(self.x < lv.mapx): self.x += self.maxSpeed
		if(self.y + self.h > lv.maph): self.y -= self.maxSpeed
		if(self.y < lv.mapy): self.y += self.maxSpeed

		#---------JINK
		"""
		if('H' in pressedKeys ):
			self.facing += self.rotationSpeed


		if('J' in pressedKeys ):
			self.facing -= self.rotationSpeed
		"""
