from units.parent import *
from utils.gameUtils import *
from utils._utils import imageAnimateAdvanced,loadingBarClass,drawImage
import pygame

class powerDrone(parent):
	def __init__(self,_id,gui,x=None,y=None):
		super().__init__(gui)
		self.id             = _id
		self.name           = 'powerDrone'
		self.kind           = 'air'
		self.collideCollected = False
		self.images         = imageAnimateAdvanced(gui.powerDrone['ready'],0.2)
		self.destructionAnimation = imageAnimateAdvanced(gui.powerDrone['destroyed'],0.05)
		self.shadow         = imageAnimateAdvanced(gui.powerDrone['shadow'],0.2)
		self.ammoImage      = gui.pdAmmo['angleRound']
		self.nextShot       = None
		self.x,self.y       = 500,500
		if(x!=None): self.x = x
		if(y!=None): self.y = y
		self.w              = int(gui.scoutRed[0].get_width())
		self.h              = int(gui.scoutRed[0].get_height())
		self.healthBar      = loadingBarClass(self.w,0.2*self.h,(80,220,80),(220,220,220),(0,0,200))
		self.blitPos        = None

		self.state             = 'patrol'
		self.patrolLocations   = [(self.x,self.y),(self.x+400,self.y),(self.x+400,self.y+200),(self.x,self.y+200)] 
		self.currentLocIndex   = 0


		self.hitImage         = gui.powerDrone['hit']
		self.hitAnimation     = imageAnimateAdvanced(self.hitImage,0.2)



		# CLASS OVERRIDES
		self.defaultSpeed    = 2

		# ENEMY COORDS 

		self.angleDiffToEnemy = 0
		self.DistanceToEnemy  = 50000
		self.enemyTargetAngle = 0
		self.defenceSector    = self.patrolLocations[0]

		self.hp              = 2000
		self.defaultHp       = 2000

		self.drawAmmo        = True
		self.ammoTimer       = stopTimer()



	# AI LOGIC
	def actions(self,gui,game,lv):
		self.facing = 90


		#------MANAGE NEXT ROUND IMAGE 

		shotType =lv.player.shotType
		if(shotType in lv.player.nextShotDict.keys()):
			self.nextShot       = lv.player.nextShotDict[lv.player.shotType]
			self.ammoImage = gui.pdAmmo[self.nextShot]
		
		elif(shotType in lv.player.maxPowerReference):
			chosenShotImageKey  = shotType
			self.ammoImage      =  gui.pdAmmo[shotType]
			self.nextShot       = shotType
		else:
			chosenShotImageKey = 'hotRound'
			self.ammoImage     = gui.pdAmmo[chosenShotImageKey]
			self.nextShot      = chosenShotImageKey






		if(self.collideCollected):
			lv.player.shotType = self.nextShot
			lv.player.flicker  = True
			killme(self,lv,killMesssage= str(self.name) + ' collected by enemy',printme=True)
		if(self.state=='patrol'):
			self.patrol(gui,lv)

		
		if(self.state=='evade'):
			self.evade(gui,lv,game)

		if(self.state=='alert'):
			self.alert(gui,lv)

		# ENSURE VECHICLE DOESN'T EXCEED BOUNDARIES
		self.stayOnField(lv)



	def patrol(self,gui,lv):
		
		# -----------GET CURRENT DESTINATION COORDS
		
		currentDestination = self.patrolLocations[self.currentLocIndex]
		angleDifference,distance,targetAngle = angleToTarget(self,self.x,self.y, currentDestination[0],currentDestination[1])

		
		# -----------MOVE TOWARDS DESTINATION
		
		self.speed = self.defaultSpeed
		tx,ty = currentDestination[0],currentDestination[1]

		if(self.x<tx):
			self.x += self.speed
		if(self.x>tx):
			self.x -= self.speed
		if(self.y<ty):
			self.y += self.speed
		if(self.y>ty):
			self.y -= self.speed

		# -----------IF DESTINATION REACHED, MOVE TO NEXT 

		if(distance< self.w): self.currentLocIndex+=1
		if(self.currentLocIndex>=len(self.patrolLocations)):
			self.currentLocIndex = 0

		# -----------GET DISTANCE TO ENEMY
		angleDiffToEnemy, DistanceToEnemy,enemyTargetAngle = angleToTarget(self,self.x,self.y, lv.player.x,lv.player.y)
		if(DistanceToEnemy<0.65*gui.h):
			self.state = 'patrol'
			
			# WORK OUT WHICH SECTOR IS NEAREST

			self.defenceSector = currentDestination




	def evade(self,gui,lv,game):
		pass


	def alert(self,gui,lv):
		print('alert')




	def drawSelf(self,gui,game,lv):
		x,y = self.x - gui.camX,self.y  - gui.camY

		shadow_x = x + 15
		shadow_y = y + 15
		self.shadow.animate(gui,'scout shadow',[shadow_x,shadow_y],game,rotation=self.facing-90)

		if(self.hit):
			self.damageAnimation(gui,lv,game)
		elif(self.alive==True and onScreen(self.x,self.y,self.w,self.h,gui) ):
			animate,self.blitPos  = self.images.animate(gui,'scout' + str(self.id),[x,y],game,rotation=self.facing-90)

			ammoTimer = self.ammoTimer.stopWatch(0.8,'ammo flicker', str(self.drawAmmo), game,silence=True)
			
			if(ammoTimer):
				self.drawAmmo = not self.drawAmmo
			
			if(self.drawAmmo):
				drawImage(gui.screen,self.ammoImage,(x,y))


	def animateDestruction(self,gui,lv,game):
		x,y = self.x - gui.camX,self.y  - gui.camY

		# *******BE CAREFUL ABOUNT ON SCREEN

		if(self.destructionComplete==False and self.alive==False):
			if(hasattr(self,'centerPoint')):
				x += 0.5*self.centerPoint[0]
				y += 0.5*self.centerPoint[1]
			complete,blitPos = self.destructionAnimation.animate(gui,str(str(self.name) +' destructionAnimation'),[x,y],game)

			
			if(complete):
				self.destructionComplete = True

