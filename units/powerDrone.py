from units.parent import *
from utils.gameUtils import *
from utils._utils import imageAnimateAdvanced,loadingBarClass,drawImage
import pygame

class powerDrone(parent):
	def __init__(self,_id,gui,x=None,y=None):
		super().__init__(gui)
		self.id             = _id
		self.name           = 'powerDrone'
		self.powerType      = 'ammo'
		self.kind           = 'air'
		self.collideCollected = False
		self.images         = imageAnimateAdvanced(gui.powerDrone['ready'],0.2)
		self.healthImg      = gui.Utils['health']
		self.countDownImgs  = imageAnimateAdvanced([gui.powerDrone['3'],gui.powerDrone['2'],gui.powerDrone['1'],gui.powerDrone['0'],],1)
		self.destructionAnimation = imageAnimateAdvanced(gui.powerDrone['destroyed'],0.05)
		self.shadow         = imageAnimateAdvanced(gui.powerDrone['shadow'],0.2)
		self.bonusDisplayImage      = gui.pdAmmo['angleRound']
		self.nextShot       = 'hotRound'
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

		self.growingFontIndex = 0
		self.fontTimer        = stopTimer()

		# CLASS OVERRIDES
		self.defaultSpeed    = 1

		# ENEMY COORDS 

		self.angleDiffToEnemy = 0
		self.DistanceToEnemy  = 50000
		self.enemyTargetAngle = 0
		self.defenceSector    = self.patrolLocations[0]

		self.hp              = 2000
		self.defaultHp       = 2000

		self.drawAmmo            = True
		self.ammoTimer           = stopTimer()
		self.weaponTimer         = stopTimer()
		self.startTerminateTimer = stopTimer()
		self.facing              = 0
		self.destructCountDown   = False
		self.terminateSelf       = False
		self.changeCount         = 0
		self.swappedWeapon       = False
		self.typeInitialised     = False



	# AI LOGIC
	def actions(self,gui,game,lv):
		self.facing = 90



		# -----COLLECT ME 

		if(self.collideCollected):
			if(self.powerType== 'HealthUp'):
				self.bonusNumber  = int(0.33*lv.player.defaultHp)
				lv.player.hp      += self.bonusNumber

				if(lv.player.hp>lv.player.defaultHp):
					lv.player.hp = lv.player.defaultHp
			else:
				lv.player.shotType = self.nextShot
			
			lv.player.flicker  = True
			killme(self,lv,killMesssage= str(self.name) + ' collected by enemy',printme=True)
		
		if(self.state=='patrol'):
			self.patrol(gui,lv)

		
		if(self.state=='evade'):
			self.evade(gui,lv,game)

		if(self.state=='alert'):
			self.alert(gui,lv)




		if(self.destructCountDown==True):
			beginTermination = self.startTerminateTimer.stopWatch(8,'wait to countdown termination', 'wait to terminate', game,silence=True)
			if(beginTermination):
				self.terminateSelf = True

		self.updateSelf(gui,lv,game)

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
		if(DistanceToEnemy<0.35*gui.h):
			self.state = 'evade'
			self.destructCountDown = True
			
			# WORK OUT WHICH SECTOR IS NEAREST

			self.defenceSector = currentDestination




	def evade(self,gui,lv,game):
		
		# -----------GET DISTANCE TO ENEMY
		angleDiffToEnemy, DistanceToEnemy,enemyTargetAngle = angleToTarget(self,self.x,self.y, lv.player.x,lv.player.y)
		if(DistanceToEnemy>0.5*gui.h):
			self.state = 'patrol'

		self.speed = self.defaultSpeed
		tx,ty = lv.player.x, lv.player.y

		if(self.x<tx):
			self.x -= self.speed
		if(self.x>tx):
			self.x += self.speed
		if(self.y<ty):
			self.y -= self.speed
		if(self.y>ty):
			self.y += self.speed

	def updateSelf(self,gui,lv,game):

		if(self.powerType== 'ammo'):

			shotType =lv.player.shotType

			if(self.swappedWeapon==False):
				if(shotType in lv.player.nextShotDict.keys()):
					self.nextShot       = lv.player.nextShotDict[lv.player.shotType]
					self.bonusDisplayImage     = gui.pdAmmo[self.nextShot]
				
				elif(shotType in lv.player.maxPowerReference):
					chosenShotImageKey  = shotType
					self.bonusDisplayImage      =  gui.pdAmmo[shotType]
					self.nextShot       = shotType
				else:
					chosenShotImageKey = 'hotRound'
					self.bonusDisplayImage     = gui.pdAmmo[chosenShotImageKey]
					self.nextShot      = chosenShotImageKey


			changeWeapon = self.weaponTimer.stopWatch(3,'changeWeapon', str(self.changeCount), game,silence=True)
			if(changeWeapon):
				if(lv.player.shotType in lv.player.swapShotDict.keys()):
					
					self.nextShot       = lv.player.swapShotDict[lv.player.shotType]
					self.bonusDisplayImage      = gui.pdAmmo[self.nextShot]
					self.changeCount   +=1
					print("Changing Weapon to " + str(self.nextShot))

					
					if(self.swappedWeapon==True):
						self.swappedWeapon = False
						return()


					self.swappedWeapon = True
		if(self.powerType== 'HealthUp'):
			if(self.typeInitialised==False):
				self.bonusDisplayImage   = self.healthImg
				self.showBonusNumber = True
				self.typeInitialised     = True










	def alert(self,gui,lv):
		print('alert')




	def drawSelf(self,gui,game,lv):
		x,y = self.x - gui.camX,self.y  - gui.camY

		shadow_x = x + 15
		shadow_y = y + 15
		self.shadow.animate(gui,'powerdrone shadow',[shadow_x,shadow_y],game,rotation=self.facing-90)

		if(self.hit):
			self.damageAnimation(gui,lv,game)
		elif(self.alive==True and onScreen(self.x,self.y,self.w,self.h,gui) ):
			animate,self.blitPos  = self.images.animate(gui,'powerdrone' + str(self.id),[x,y],game,rotation=self.facing-90)

			ammoTimer = self.ammoTimer.stopWatch(0.8,'ammo flicker', str(self.drawAmmo), game,silence=True)
			
			if(ammoTimer):
				self.drawAmmo = not self.drawAmmo
			
			# DRAW OVERLAPPING IMAGE
			if(self.terminateSelf == False):
				if(self.drawAmmo):
					drawImage(gui.screen,self.bonusDisplayImage,(x,y))
			
			else:
				animateComplete,self.blitPos  = self.countDownImgs.animate(gui,'terminating' + str(self.id),[x,y],game,rotation=self.facing-90,repeat=False)
				if(animateComplete):
					killme(self,lv)


	def animateDestruction(self,gui,lv,game):
		x,y = self.x - gui.camX,self.y  - gui.camY

		# *******BE CAREFUL ABOUNT ON SCREEN

		if(self.destructionComplete==False and self.alive==False):
			if(hasattr(self,'centerPoint')):
				x += 0.5*self.centerPoint[0]
				y += 0.5*self.centerPoint[1]
			complete,blitPos = self.destructionAnimation.animate(gui,str(str(self.name) +' destructionAnimation'),[x,y],game)

			if(self.showBonusNumber):
				drawText(gui,gui.growingFontLarge[self.growingFontIndex],'+' +str(self.bonusNumber) + ' HP' ,x+ 0.4*self.w,y-0.4*self.h + -(self.growingFontIndex/20 * 0.1*gui.h), colour=(0, 200, 0),alpha=(1 - self.growingFontIndex/len(gui.growingFontLarge))*255)
				incFont = self.fontTimer.stopWatch(0.025,'expanding font', str(self.growingFontIndex), game,silence=True)
				if(incFont):
					if(not self.growingFontIndex>=len(gui.growingFontLarge)-1):
						self.growingFontIndex +=1
			
			if(complete):
				self.destructionComplete = True

