from units.parent import *
from utils.gameUtils import *
from utils._utils import imageAnimateAdvanced,loadingBarClass
import pygame

class greenTank(parent):
	def __init__(self,_id,gui,x=None,y=None):
		super().__init__(gui)
		# MAIN OVERRIDES 
		self.id             = _id
		self.name           = 'greenTank'
		self.kind           = 'vechicle'
		self.images         = imageAnimateAdvanced(gui.greenTank,0.2)
		self.turretImage    = imageAnimateAdvanced(gui.greenTurret,0.2)
		self.x,self.y       = 500,500
		if(x!=None): self.x = x
		if(y!=None): self.y = y
		self.w              = int(gui.tank[0].get_width())
		self.h              = int(gui.tank[0].get_height())
		self.turretFacing   = self.facing
		
		# HIT IMAGE
		self.hitImage         = gui.greenTankHit
		self.hitAnimation     = imageAnimateAdvanced(self.hitImage,0.2)
		self.turretHitImg     = imageAnimateAdvanced(gui.greenTurretHit,0.2)
		self.hitsTaken        = 0

		# REMAINS IMAGE 
		self.remainsAnimation = imageAnimateAdvanced(gui.greenTankRemains,0.2)

		# HEALTHBAR 
		self.healthBar      = loadingBarClass(self.w,0.2*self.h,(80,220,80),(220,220,220),(0,0,200))
		self.blitPos        = None
		self.turretPos      = None

		self.state             = 'patrol'
		self.patrolLocations   = [(self.x,self.y),(self.x+700,self.y),(self.x+700,self.y+200),(self.x,self.y+200)] 
		self.currentLocIndex   = 0


		# CLASS OVERRIDES
		self.hp              = 200
		self.defaultSpeed    = 1
		self.maxSpeed        = 1
		self.maxSpeedDefault = 1

		# ENEMY COORDS 

		self.angleDiffToEnemy = 0
		self.DistanceToEnemy  = 50000
		self.enemyTargetAngle = 0
		self.defenceSector    = self.patrolLocations[0]

		# SHOOT 
		self.bulletTimer        = stopTimer()           # BUFF
		self.shootDelay         = 0.3                   # BUFF
		self.bulletsFired       = 0

	# AI LOGIC
	def actions(self,gui,game,lv):

		# ENSURE VECHICLE DOESN'T EXCEED BOUNDARIES
		self.stayOnField(lv)


		if(self.state=='patrol'):
			self.patrol(gui,lv)


		if(self.state=='attackPursue'):
			self.atackPursue(gui,lv,game)




	def patrol(self,gui,lv):
		
		# -----------GET CURRENT DESTINATION COORDS
		
		currentDestination = self.patrolLocations[self.currentLocIndex]
		angleDifference,distance,targetAngle = angleToTarget(self,self.x,self.y, currentDestination[0],currentDestination[1])



		# -----------FACE TOWARDS DESTINATION
		
		faceTarget(self,angleDifference, turnIcrement=2)
		
		# -----------MOVE TOWARDS DESTINATION
		
		self.speed = self.defaultSpeed
		self.moveForwards()

		# -----------IF DESTINATION REACHED, MOVE TO NEXT 

		if(distance< 0.3*self.w): self.currentLocIndex+=1
		if(self.currentLocIndex>=len(self.patrolLocations)):
			self.currentLocIndex = 0

		# -----------GET DISTANCE TO ENEMY
		angleDiffToEnemy, DistanceToEnemy,enemyTargetAngle = angleToTarget(self,self.x,self.y, lv.player.x,lv.player.y)
		
		self.turretFacing = self.facing
		if(DistanceToEnemy<0.5*gui.h):
			self.state = 'attackPursue'
			
			# WORK OUT WHICH SECTOR IS NEAREST

			self.defenceSector = currentDestination






	def atackPursue(self,gui,lv,game):
		# RECALCULATE RELATIVE POS TO ENEMY
		angleDiffToEnemy,DistanceToEnemy,enemyTargetAngle = turretAngleToTarget(self,self.x,self.y,lv.player.x,lv.player.y)

		# -----------FACE TOWARDS DESTINATION
		
		turretFaceTarget(self,angleDiffToEnemy, turnIcrement=5)


		# -------SHOOT
		if DistanceToEnemy<0.5*gui.h:
			self.shoot(gui,lv,game)
		else:
			self.state = 'patrol'

		#if(DistanceToEnemy>0.7*gui.h): self.state = 'patrol'



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
				lv.bulletList.append(bullet(gui,self.turretPos['midTop'][0] + gui.camX,self.turretPos['midTop'][1]+ gui.camY,bid,self.classification, self.turretFacing,'smallTankShell', speed=7,damage=2,colour=[250,218,94],w=6,h=6 ))
			



	# DRAW REMNANTS AFTER BEING DESTROYED
	def drawRemains(self,gui,lv,game):
		x,y = self.x - gui.camX,self.y  - gui.camY

		# *******BE CAREFUL ABOUNT ON SCREEN
		if(self.alive==False and onScreen(self.x,self.y,self.w,self.h,gui)):
			self.remainsAnimation.animate(gui,str('smouldering tank remains'),[x,y],game,rotation=self.facing-90,repeat=True)

	# DRAW SELF LOGIC

	def drawSelf(self,gui,game,lv):
		x,y = self.x - gui.camX,self.y  - gui.camY
		


		if(self.alive==True and onScreen(self.x,self.y,self.w,self.h,gui) and not self.hit):
			animate,self.blitPos     = self.images.animate(gui,'tank' + str(self.id),[x,y],game,rotation=self.facing-90)
			turretAnimage,self.turretPos  = self.turretImage.animate(gui,'turret' + str(self.id),[x,y],game,rotation=self.turretFacing-90)

			#pygame.draw.circle(gui.screen, (244,0,0), (self.patrolLocations[self.currentLocIndex][0]- gui.camX ,self.patrolLocations[self.currentLocIndex][1]- gui.camY) , 15, 0)

		if(self.hit):

			x,y = self.x - gui.camX,self.y  - gui.camY
			
			if(self.alive==True and onScreen(self.x,self.y,self.w,self.h,gui)):
				
				complete,imageParms            = self.hitAnimation.animate(gui,str(self.hitsTaken) + ' hit',[x,y],game,rotation=self.facing-90,repeat=True)
				turretComplete,self.turretPos  = self.turretHitImg.animate(gui,str(self.hitsTaken) + ' hit',[x,y],game,rotation=self.turretFacing-90,repeat=True)

				if(complete and turretComplete):
					self.turretHitImg.reelComplete = False
					self.hit = False
					self.hitsTaken +=1

	

