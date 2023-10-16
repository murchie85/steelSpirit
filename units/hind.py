from units.parent import *
from utils.gameUtils import *
from utils._utils import imageAnimateAdvanced,loadingBarClass
import pygame

class hind(parent):
	def __init__(self,_id,gui,x=None,y=None):
		super().__init__(gui)
		self.id             = _id
		self.name           = 'hind'
		self.kind           = 'air'
		self.images         = imageAnimateAdvanced(gui.hind,0.05)
		self.shadow         = imageAnimateAdvanced(gui.hindShadow,0.05)
		self.x,self.y       = 500,500
		if(x!=None): self.x = x
		if(y!=None): self.y = y
		self.w              = int(gui.hind[0].get_width())
		self.h              = int(gui.hind[0].get_height())
		self.healthBar      = loadingBarClass(self.w,0.2*self.h,(80,220,80),(220,220,220),(0,0,200))
		self.blitPos        = None

		self.state             = 'patrol'
		self.patrolLocations   = [(self.x,self.y),(self.x+400,self.y),(self.x+400,self.y+200),(self.x,self.y+200)] 
		self.seekStrafe        = False
		self.currentLocIndex   = 0
		self.defaultHp         = 50
		self.hp                = 50

		# HIT IMAGE
		self.hitImage         = gui.hindHit
		self.hitAnimation     = imageAnimateAdvanced(self.hitImage,0.2)

		# CLASS OVERRIDES
		self.defaultSpeed     = 2
		self.maxSpeed         = 2
		self.maxSpeedDefault  = 2

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
		self.turnPeriod         = 1.5
		self.turnDirection      = 1
		self.seekStrafe         = False

	# AI LOGIC
	def actions(self,gui,game,lv):

		if(self.seekStrafe): self.state= 'attackPursue'
		if(self.state=='patrol'):
			self.patrol(gui,lv)

		
		if(self.state=='attackPursue'):
			self.atackPursue(gui,lv,game)

		if(self.state=='alert'):
			self.alert(gui,lv)

		# ENSURE VECHICLE DOESN'T EXCEED BOUNDARIES
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
		if(DistanceToEnemy<0.65*gui.h):
			self.state = 'attackPursue'
			
			# WORK OUT WHICH SECTOR IS NEAREST

			self.defenceSector = currentDestination




	def atackPursue(self,gui,lv,game):
		
		# DISTANCE THE ENEMY IS FROM ROUTE COORD
		angleDiffToEnemy,DistanceToEnemy,enemyTargetAngle = angleToTarget(self,lv.player.x,lv.player.y,self.defenceSector[0],self.defenceSector[1])
		
		if(self.seekStrafe):
			seekDistance = 6*gui.w
			self.defaultSpeed = 3
		else:
			seekDistance = 0.7*gui.w
		
		if(DistanceToEnemy<seekDistance):

			# RECALCULATE RELATIVE POS TO ENEMY
			angleDiffToEnemy,DistanceToEnemy,enemyTargetAngle = angleToTarget(self,self.x,self.y,lv.player.x,lv.player.y)

			# -----------FACE TOWARDS DESTINATION
			
			faceTarget(self,angleDiffToEnemy, turnIcrement=5)
			
			# -----------MOVE TOWARDS DESTINATION
			self.speed = self.defaultSpeed
			
			# SLOW DOWN IF IN STRAFE MODE 

			if(DistanceToEnemy< 0.9*gui.h and self.seekStrafe):
				if(self.speed>self.defaultSpeed):
					self.speed = self.defaultSpeed
				if(self.speed>0.5*self.defaultSpeed):
					self.speed-= 0.05

			# FORWARD OR JINK
			if(DistanceToEnemy > 0.45*gui.h):
				self.moveForwards()
			elif(DistanceToEnemy < 0.35*gui.h):
				self.moveBackwards()
			else:
				changeDirection = self.turnTimer.stopWatch(self.turnPeriod,'hind turning', 'hind turning', game,silence=True)
				if(changeDirection):
					self.turnDirection = -self.turnDirection
					self.turnTimer.reset()

				vel_x = self.maxSpeed * math.cos(math.radians(360-self.facing-90))
				vel_y = self.maxSpeed * math.sin(math.radians(360-self.facing-90))
				self.x += self.turnDirection * 0.5*vel_x
				self.y += self.turnDirection * 0.5*vel_y


			# -------SHOOT
			if DistanceToEnemy<0.8*gui.h:
				self.shoot(gui,lv,game)

		else:
			self.state = 'patrol'



	def alert(self,gui,lv):
		print('alert')




	# CALLED BY allyActions/enemyActions
	def shoot(self,gui,lv,game,bulletSpeed=10, bulletColour=(255,177,42)):

		# BULLET DELAY TIMER
		shotAvailable = self.bulletTimer.stopWatch(self.shootDelay,'shoot at player', str(self.id + self.bulletsFired), game,silence=True)
		
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
			animate,self.blitPos  = self.images.animate(gui,'hind' + str(self.id),[x,y],game,rotation=self.facing-90)

