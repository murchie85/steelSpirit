from units.parent import *
from utils.gameUtils import *
from utils._utils import imageAnimateAdvanced,loadingBarClass
import pygame



"""

DEATH ANIMATION SHOULD BE HIT -> DAMAGED FOR A FEW SECONDS BEFORE EXPLODING



STATES = PATROL, PURSUIT, ENGAGING, DISENGAGING, 
IF IN ALERT RANGE BUT NOT DETECTION RANGE = SPEED UP TOWARDS PLAYER

if in patrol state
	if within detection = go pursuit
	speed equals boost speed

if in pursuite state

	if in attackRange = slow down to stop: 
		keep pointing
		fire once stopped
		state = DISENGAGING
	
	if not in detection
		state = patrol


if in disengaging 

"""



class comanche(parent):
	def __init__(self,_id,gui,x=None,y=None):
		super().__init__(gui)
		self.id             = _id
		self.name           = 'comanche'
		self.kind           = 'air'
		self.images         = imageAnimateAdvanced(gui.comanche,0.05)
		self.shadow         = imageAnimateAdvanced(gui.comancheShadow,0.05)
		self.x,self.y       = 500,500
		if(x!=None): self.x = x
		if(y!=None): self.y = y
		self.w              = int(gui.hind[0].get_width())
		self.h              = int(gui.hind[0].get_height())
		self.healthBar      = loadingBarClass(self.w,0.2*self.h,(80,220,80),(220,220,220),(0,0,200))
		self.blitPos        = None

		self.state             = 'patrol'
		self.patrolLocations   = [(self.x,self.y),(self.x+400,self.y),(self.x+400,self.y+200),(self.x,self.y+200)] 
		self.currentLocIndex   = 0
		self.defaultHp         = 40
		self.hp                = 40

		# HIT IMAGE
		self.hitImage         = gui.comancheHit
		self.hitAnimation     = imageAnimateAdvanced(self.hitImage,0.1)
		self.damageReel       = imageAnimateAdvanced(gui.comancheDamaged,0.2)

		# CLASS OVERRIDES
		self.defaultSpeed     = 2
		self.maxSpeed         = 2
		self.speed            = self.defaultSpeed
		self.maxSpeedDefault  = 2
		self.boostSpeed       = 4*self.maxSpeed

		# ENEMY COORDS 

		self.angleDiffToEnemy = 0
		self.DistanceToEnemy  = 50000
		self.enemyTargetAngle = 0
		self.defenceSector    = self.patrolLocations[0]

		# SHOOTT 
		self.bulletTimer        = stopTimer()           # BUFF
		self.shootDelay         = 2                     # BUFF
		self.bulletsFired       = 0

		self.turnTimer          = stopTimer()
		self.destroyTimer        = stopTimer()
		self.turnPeriod         = 1.5
		self.turnDirection      = 1
		self.seekStrafe         = True
		self.detectionRange     = 1.2 *gui.w
		self.decelRange         = 0.8 * gui.h
		self.attackRange        = 0.45 * gui.h
		self.firstShot 			= True
		

		# ZIP BEHAVIOUR 

		self.zipAttack          = False
		# destroy animation
		self.deathDirection     = random.choice([1,-1])
		self.destructionDecision = False
		self.beginDestroy        = False
		self.spinOutOfControl    = False

	# AI LOGIC
	def actions(self,gui,game,lv):

		self.stayOnField(lv)
		if(self.state=='patrol'):
			self.patrol(gui,lv)

		
		if(self.state=='attackPursue'):
			self.atackPursue(gui,lv,game)

		if(self.state=='alert'):
			self.alert(gui,lv)

		# ENSURE vehicle DOESN'T EXCEED BOUNDARIES
		self.stayOnField(lv)



	def patrol(self,gui,lv):
		
		# -----------GET CURRENT DESTINATION COORDS
		
		currentDestination = self.patrolLocations[self.currentLocIndex]
		angleDifference,distance,targetAngle = angleToTarget(self,self.x,self.y, currentDestination[0],currentDestination[1])


		# -----------FACE TOWARDS DESTINATION
		
		faceTarget(self,angleDifference, turnIcrement=5)
		
		# -----------MOVE TOWARDS DESTINATION
		
		self.speed = self.defaultSpeed
		self.moveForwards()

		# -----------IF DESTINATION REACHED, MOVE TO NEXT 

		if(distance< self.w): self.currentLocIndex+=1
		if(self.currentLocIndex>=len(self.patrolLocations)):
			self.currentLocIndex = 0

		# -----------GET DISTANCE TO ENEMY
		
		angleDiffToEnemy, DistanceToEnemy,enemyTargetAngle = angleToTarget(self,self.x,self.y, lv.player.x,lv.player.y)
		
		if(DistanceToEnemy<self.detectionRange):
			self.state = 'attackPursue'
			# WORK OUT WHICH SECTOR IS NEAREST
			self.defenceSector = currentDestination
			self.speed  = self.boostSpeed




	def atackPursue(self,gui,lv,game):
		
		# RECALCULATE RELATIVE POS TO ENEMY
		angleDiffToEnemy,DistanceToEnemy,enemyTargetAngle = angleToTarget(self,self.x,self.y,lv.player.x,lv.player.y)

		
		
		if(DistanceToEnemy<self.detectionRange):


			# -----------FACE TOWARDS DESTINATION
			
			faceTarget(self,angleDiffToEnemy, turnIcrement=5)
			
			
			if(DistanceToEnemy>0.9*self.attackRange):
				self.moveForwards()

			if(DistanceToEnemy < self.decelRange and self.alive):
				if(self.speed>1):
					self.speed -= 0.05*self.defaultSpeed




			if(self.firstShot==False):
				changeDirection = self.turnTimer.stopWatch(self.turnPeriod,'comanche turning', 'comanche turning', game,silence=True)
				if(changeDirection):
					self.turnDirection = -self.turnDirection
					self.turnTimer.reset()

				vel_x = self.maxSpeed * math.cos(math.radians(360-self.facing-90))
				vel_y = self.maxSpeed * math.sin(math.radians(360-self.facing-90))
				self.x += self.turnDirection * 0.5*vel_x
				self.y += self.turnDirection * 0.5*vel_y


			# -------SHOOT
			if DistanceToEnemy<self.attackRange:
				self.shoot(gui,lv,game)

		
		# GIVE A BUFFER SO NOT FUZZING ABOUT

		if(DistanceToEnemy>1.1*self.detectionRange):
			self.state = 'patrol'

	def zipAttack(self,gui,lv,game):

		"""
		SPEED UP TO ENEMY
		COAST WHEN IN RANGE, BUT OFF AT AN ANGLE 

		"""
		
		# RECALCULATE RELATIVE POS TO ENEMY
		angleDiffToEnemy,DistanceToEnemy,enemyTargetAngle = angleToTarget(self,self.x,self.y,lv.player.x,lv.player.y)

		
		
		if(DistanceToEnemy<self.detectionRange):


			# -----------FACE TOWARDS DESTINATION
			
			faceTarget(self,angleDiffToEnemy, turnIcrement=5)
			
			
			if(DistanceToEnemy>0.9*self.attackRange):
				self.moveForwards()

			if(DistanceToEnemy < self.decelRange and self.alive):
				if(self.speed>1):
					self.speed -= 0.05*self.defaultSpeed




			if(self.firstShot==False):
				changeDirection = self.turnTimer.stopWatch(self.turnPeriod,'comanche turning', 'comanche turning', game,silence=True)
				if(changeDirection):
					self.turnDirection = -self.turnDirection
					self.turnTimer.reset()

				vel_x = self.maxSpeed * math.cos(math.radians(360-self.facing-90))
				vel_y = self.maxSpeed * math.sin(math.radians(360-self.facing-90))
				self.x += self.turnDirection * 0.5*vel_x
				self.y += self.turnDirection * 0.5*vel_y


			# -------SHOOT
			if DistanceToEnemy<self.attackRange:
				self.shoot(gui,lv,game)

		
		# GIVE A BUFFER SO NOT FUZZING ABOUT

		if(DistanceToEnemy>1.1*self.detectionRange):
			self.state = 'patrol'



	def alert(self,gui,lv):
		print('alert')




	# CALLED BY allyActions/enemyActions
	def shoot(self,gui,lv,game,bulletSpeed=10, bulletColour=(255,177,42)):

		# BULLET DELAY TIMER
		shotAvailable = self.bulletTimer.stopWatch(self.shootDelay,'shoot at player', str(self.id + self.bulletsFired), game,silence=True)


		
		if(self.firstShot):	
			shotAvailable = True
			self.firstShot = False

		# IF SHOOT CRITEREA MET,
		if((shotAvailable and self.blitPos!=None)):

				self.bulletsFired +=1
				# ADDS BULLET TO BULLET LIST
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(bullet(gui,self.blitPos['midTop'][0] + gui.camX,self.blitPos['midTop'][1]+ gui.camY,bid,self.classification, self.facing,'redPlasmaBall', speed=8,damage=3,colour=[230,80,80],w=8,h=8))







	def drawSelf(self,gui,game,lv):
		x,y = self.x - gui.camX,self.y  - gui.camY

		shadow_x = x + 15
		shadow_y = y + 15
		self.shadow.animate(gui,'hind shadow',[shadow_x,shadow_y],game,rotation=self.facing-90)


		if(self.hit):
			self.damageAnimation(gui,lv,game)
		elif(self.alive==True and onScreen(self.x,self.y,self.w,self.h,gui) ):
			if(self.hp>20):
				animate,self.blitPos  = self.images.animate(gui,'comanche' + str(self.id),[x,y],game,rotation=self.facing-90)
			else:
				animate,self.blitPos  = self.damageReel.animate(gui,'comanche damaged' + str(self.id),[x,y],game,rotation=self.facing-90)


	def animateDestruction(self,gui,lv,game):
		x,y = self.x - gui.camX,self.y  - gui.camY

		# *******BE CAREFUL ABOUNT ON SCREEN


		# decide how destruction animation will go
		if(self.destructionComplete==False and self.alive==False):

			# if going fast then spin out of control, otherwise just 1 in every 4
			if(self.destructionDecision==False):
				if(self.speed >=2):
					self.spinOutOfControl = True
				else:
					self.spinOutOfControl = random.choice([True, False, False, False])

				# go to destruction animation
				if(not self.spinOutOfControl):
					self.beginDestroy = True

				self.destructionDecision = True

			

			# SPIN OUT OF CONTROL

			if(self.spinOutOfControl):
				showdestruction = self.destroyTimer.stopWatch(0.5,'show damaged reel', str(self.id), game,silence=True)
				if(not showdestruction):
					animate,self.blitPos  = self.damageReel.animate(gui,'comanche damaged' + str(self.id),[x,y],game,rotation=self.facing-90)
					self.facing +=5* self.deathDirection
					self.speed = 2
					self.moveForwards()
				else:
					self.beginDestroy = True


			# RENDER ACTUAL DESTROY ANIMATION
			if(self.beginDestroy==True):
			

				if(hasattr(self,'centerPoint')):
					x += 0.5*self.centerPoint[0]
					y += 0.5*self.centerPoint[1]
				complete,blitPos = self.explosion.animate(gui,str(str(self.name) +' explosion'),[x,y],game)
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1


				#---------DRAW SCORE

				if(self.killScore!=0):
					drawText(gui,gui.growingFontLarge[self.growingFontIndex],str(self.killScore),x+ 0.4*self.w,y-0.4*self.h + -(self.growingFontIndex/20 * 0.1*gui.h), colour=(255, 255, 255),alpha=(1 - self.growingFontIndex/len(gui.growingFontLarge))*255)
					incFont = self.fontTimer.stopWatch(0.025,'expanding font', str(self.growingFontIndex), game,silence=True)
					if(incFont):
						if(not self.growingFontIndex>=len(gui.growingFontLarge)-1):
							self.growingFontIndex +=1

				if(self.showBonusNumber):
					drawText(gui,gui.growingFont[self.growingFontIndex],str(self.showBonusNumber),x+ 0.4*self.w,y-0.4*self.h + -(self.growingFontIndex/20 * 0.1*gui.h), colour=(0, 200, 0),alpha=(1 - self.growingFontIndex/len(gui.growingFont))*255)
					incFont = self.fontTimer.stopWatch(0.025,'expanding font', str(self.growingFontIndex), game,silence=True)
					if(incFont):
						if(not self.growingFontIndex>=len(gui.growingFont)-1):
							self.growingFontIndex +=1


				if(self.debris<=12):
					self.debris +=1
					# ADDS DEBRIS TO TO LIST
					lv.bulletList.append(bullet(gui,self.x + 0.5* self.chosenExplosionImg[0].get_width(),self.y+ 0.5* self.chosenExplosionImg[0].get_height(),bid,'debris',random.randrange(0,360),'debris',speed=10, w=3,h=3,colour=(192,192,192)))
				
				# ADD FLYING SHRAPNELL 50% of the time
				if(random.choice([1,2])==1 and not self.shrapnellEjected):
					self.shrapnellEjected = True
					bid = max(([x.id for x in lv.bulletList]),default=0) + 1
					lv.bulletList.append(bullet(gui,self.x + 0.5* self.chosenExplosionImg[0].get_width(),self.y+ 0.5* self.chosenExplosionImg[0].get_height(),bid,'shrapnell',random.randrange(0,360),'shrapnell',speed=7,shrapnellType='A'))
				
				if(complete):
					self.destructionComplete = True

