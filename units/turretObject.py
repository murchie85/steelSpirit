from utils.gameUtils import *
from utils._utils import stopTimer,loadingBarClass,wrapAngle,imageAnimateAdvanced
import random
import math
from units.ordinance import *
import pygame


class turret():
	def __init__(self,_id,classification,gui,x,y,turretImg,turretHitImg, turretRemainsImg,facing,shotType='single',hp=200,shootRange=None,bulletType='turretShell',shootDelay=0.3,centerOfRotation=(0.5,0.5)):
		# MAIN OVERRIDES 
		self.id             = _id
		self.classification = classification
		self.name           = 'turret'
		self.kind           = 'vehicle'
		self.turretImage    = turretImg
		self.x,self.y       = x,y
		self.w              = int(turretImg.imageFrames[0].get_width())
		self.h              = int(turretImg.imageFrames[0].get_height())
		self.centerPoint    = [0.8*self.w,0.5*self.h]
		self.turretFacing   = facing
		self.blitPos        = None  # not in use

		self.shotType       = shotType

		self.range          = shootRange
		if(shootRange==None): self.range          = 0.5*gui.h
		
		# HIT IMAGE
		self.hit              = False
		self.turretHitImg     = turretHitImg
		self.hitsTaken        = 0
		self.bulletType       = bulletType

		# REMAINS IMAGE 
		self.remainsAnimation = turretRemainsImg
		self.smokeAnimation   = imageAnimateAdvanced(gui.medSmoke,0.2)

		# HEALTHBAR 
		self.healthBar      = loadingBarClass(self.w,0.2*self.h,(80,220,80),(220,220,220),(0,0,200))
		self.turretPos      = None
		self.alive             = True

		self.centerOfRotation  = centerOfRotation

		# CLASS OVERRIDES
		self.hp              = hp
		self.defaultSpeed    = 1
		self.maxSpeed        = 1
		self.maxSpeedDefault = 1

		# ENEMY COORDS 

		self.angleDiffToEnemy = 0
		self.DistanceToEnemy  = 50000
		self.enemyTargetAngle = 0

		# SHOOT 
		self.bulletTimer        = stopTimer()           # BUFF
		self.shootDelay         = shootDelay                  # BUFF
		self.bulletsFired       = 0

		self.multiTimer1        = stopTimer()           # BUFF
		self.multiTimer2        = stopTimer()           # BUFF
		self.multiTimer3        = stopTimer()           # BUFF

		# DESTRUCT ANIMATION 
		self.destructionComplete = False
		self.debris              = 0
		self.shrapnellEjected = False
		# OVERRIDE
		self.chosenExplosionImg = gui.smallCloudyExplosion
		self.explosion          = imageAnimateAdvanced(self.chosenExplosionImg,0.1)


	# AI LOGIC
	def actions(self,gui,game,lv,parentFacing):
		

		if(self.alive and onScreen(self.x,self.y,self.w,self.h,gui)):
			self.turretActions(gui,lv,game,self.bulletType)
			self.drawSelf(gui,game,lv)
			
			for bullet in lv.bulletList:
				if(bullet.classification!=self.classification):
					if(collidesWithHitBox(bullet,self)):
						self.hp -= bullet.damage
						self.hit = True
						bullet.killSelf(lv,killMessage='struck enemy')


		if(self.hp<0): self.alive = False

		if(self.alive==False):
			# ENSURE REMOVED FROM COMPONENT LIST
			if(self in lv.enemyComponentList):
				lv.enemyComponentList.remove(self)
			
			self.animateDestruction(gui,lv,game)
		if(self.destructionComplete):
			self.drawRemains(gui,lv,game)



	def turretActions(self,gui,lv,game,bulletType='turretShell'):
		# RECALCULATE RELATIVE POS TO ENEMY
		angleDiffToEnemy,DistanceToEnemy,enemyTargetAngle = turretAngleToTarget(self,self.x,self.y,lv.player.x,lv.player.y)

		# -------SHOOT
		if DistanceToEnemy<self.range and self.turretPos!=None: 
			# -----------FACE TOWARDS DESTINATION
			turretFaceTarget(self,angleDiffToEnemy, turnIcrement=5)
			
			if(self.shotType=='single'):
				self.shoot(gui,lv,game,self.turretPos['midTop'][0],self.turretPos['midTop'][1],self.turretFacing,self.bulletTimer,bulletType=bulletType)
			elif(self.shotType=='tripple'):
				self.shoot(gui,lv,game,self.turretPos['center'][0],self.turretPos['center'][1],self.turretFacing,self.multiTimer1,speed=10,bulletType=bulletType)
				self.shoot(gui,lv,game,self.turretPos['centerL'][0],self.turretPos['centerL'][1],self.turretFacing,self.multiTimer2,speed=10,bulletType=bulletType)
				self.shoot(gui,lv,game,self.turretPos['centerR'][0],self.turretPos['centerR'][1],self.turretFacing,self.multiTimer3,speed=10,bulletType=bulletType)
			elif(self.shotType=='trippleStaggered'):
				facing_direction_radians = wrapAngle(math.radians(self.turretFacing-90))
				xl = (self.x + 0.5*self.w )- (math.cos(facing_direction_radians)*50) 
				yl = (self.y + 0.5*self.h) + (math.sin(facing_direction_radians)*50) 
				#xl = (xl+ 0.5*self.w )- (math.cos(facing_direction_radians)*50) - gui.camX
				#yl = (yl + 0.5*self.h) + (math.sin(facing_direction_radians)*50) - gui.camY
				facing_direction_radians = math.radians(self.turretFacing)
				xc = (self.x + 0.5*self.w )- (math.cos(facing_direction_radians)) 
				yc = (self.y + 0.5*self.h) + (math.sin(facing_direction_radians)) 
				
				facing_direction_radians = wrapAngle(math.radians(self.turretFacing+90))
				xr = (self.x + 0.5*self.w )- (math.cos(facing_direction_radians)*50) 
				yr = (self.y + 0.5*self.h) + (math.sin(facing_direction_radians)*50) 
				

				trippleAvailable = self.multiTimer1.stopWatch(self.shootDelay,'shoot at player', str(self.id + self.bulletsFired), game,silence=True)
				if(trippleAvailable):
					self.bulletsFired +=1
					# ADDS BULLET TO BULLET LIST
					bid = max(([x.id for x in lv.bulletList]),default=0)
					bid1 = max(([x.id for x in lv.bulletList]),default=0)+1
					bid2 = max(([x.id for x in lv.bulletList]),default=0)+2
					lv.bulletList.append(bullet(gui,xl ,yl ,bid,self.classification, self.turretFacing,bulletType, speed=10,damage=2,colour=[250,218,94],w=8,h=8 ))
					lv.bulletList.append(bullet(gui,xc ,yc ,bid1,self.classification, self.turretFacing,bulletType, speed=10,damage=2,colour=[250,218,94],w=8,h=8 ))
					lv.bulletList.append(bullet(gui,xr ,yr ,bid2,self.classification, self.turretFacing,bulletType, speed=10,damage=2,colour=[250,218,94],w=8,h=8 ))
				


	# CALLED BY allyActions/enemyActions
	def shoot(self,gui,lv,game,bulletX,bulletY,facing,timer,    bulletSpeed=10, bulletColour=(255,177,42),speed=7,bulletType='turretShell'):

		# BULLET DELAY TIMER
		shotAvailable = timer.stopWatch(self.shootDelay,'shoot at player', str(self.id + self.bulletsFired), game,silence=True)
		
		# IF SHOOT CRITEREA MET,
		if((shotAvailable and self.turretPos!=None)):

				self.bulletsFired +=1
				# ADDS BULLET TO BULLET LIST
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(bullet(gui,bulletX + gui.camX,bulletY + gui.camY,bid,self.classification, facing,bulletType, speed=speed,damage=2,colour=[250,218,94],w=8,h=8 ))
			




	# DRAW SELF LOGIC

	def drawSelf(self,gui,game,lv):
		x,y = self.x - gui.camX,self.y  - gui.camY
		
		#shadow_x = x + 10
		#shadow_y = y + 10
		#self.shadow.animate(gui,'aa shadow',[shadow_x,shadow_y],game,rotation=self.facing-90)

		if(self.alive==True and onScreen(self.x,self.y,self.w,self.h,gui) and not self.hit):
			turretAnimage,self.turretPos  = self.turretImage.animate(gui,'turret' + str(self.id),[x,y],game,rotation=self.turretFacing-90,centerOfRotation=self.centerOfRotation)

		if(self.hit):
			x,y = self.x - gui.camX,self.y  - gui.camY
			
			if(self.alive==True and onScreen(self.x,self.y,self.w,self.h,gui)):
				turretComplete,self.turretPos  = self.turretHitImg.animate(gui,str(self.hitsTaken) + ' hit',[x,y],game,rotation=self.turretFacing-90,repeat=True,centerOfRotation=self.centerOfRotation)

				if(turretComplete):
					self.turretHitImg.reelComplete = False
					self.hit      = False
					self.hitsTaken +=1

		#pygame.draw.rect(gui.screen,(0,0,150),(self.x-gui.camX + 0.5*self.w,self.y-gui.camY + 0.5*self.h,10,10))


	# DRAW REMNANTS AFTER BEING DESTROYED
	def drawRemains(self,gui,lv,game):
		x,y = self.x - gui.camX,self.y  - gui.camY

		# *******BE CAREFUL ABOUNT ON SCREEN
		if(self.alive==False and onScreen(self.x,self.y,self.w,self.h,gui)):
			self.remainsAnimation.animate(gui,str('smouldering f turret remains'),[x,y],game,rotation=self.turretFacing-90,repeat=True)
			self.smokeAnimation.animate(gui,str('smouldering turret remains smoke'),[x + 0.3*self.w,y + 0.3*self.h],game,rotation=self.turretFacing-90,repeat=True)

	

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
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(bullet(gui,self.x + 0.5* self.chosenExplosionImg[0].get_width(),self.y+ 0.5* self.chosenExplosionImg[0].get_height(),bid,'debris',random.randrange(0,360),'debris',speed=10, w=3,h=3,colour=(192,192,192)))
			
			# ADD FLYING SHRAPNELL 50% of the time
			if(random.choice([1,2])==1 and not self.shrapnellEjected):
				self.shrapnellEjected = True
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(bullet(gui,self.x + 0.5* self.chosenExplosionImg[0].get_width(),self.y+ 0.5* self.chosenExplosionImg[0].get_height(),bid,'shrapnell',random.randrange(0,360),'shrapnell',speed=7,shrapnellType='A'))
			
			if(complete):
				self.destructionComplete = True
