from units.parent import *
from utils.gameUtils import *
from utils._utils import imageAnimateAdvanced,loadingBarClass
import pygame

"""
Googles Code Red, 
Blockchains AI art ownership solution 
and GPT3 plagiarism.


ENEMY TO HAVE 3 STATES: 

1 --> 2 --> 3 <-> 2,::1


STATE 1 - PATROL 

			SENSING 

			LOGIC: FOLLOW PATROL ROUTE
					IF ENEMY DETECTED, GO TO STATE 2

					IF I AM OUTSIDE MY PATROL ROUTE, RETURN TO PATROL ROUTE 

STATE 2 - ATTACK & PURSUE

		- IF IN RANGE:

			- PURSUE (if in range)
				- Do not exceed given boundary patrol route * 2
			- SHOOT THE ENEMY
			- Assumption player is faster (or detection boundary is not infinte)

		
		- IF NOT IN RANGE 
			- GO TO STATE 3

			

STATE 3 - ALERT 

			- do a localised small patrol loop 
				- If enemy seen, return to state 2 
			
			- Count down from 60
			- if counter = 0
			- go to state 1


"""


class scout(parent):
	def __init__(self,_id,gui,x=None,y=None):
		super().__init__(gui)
		self.id             = _id
		self.name           = 'scout'
		self.images         = imageAnimateAdvanced(gui.scoutRed,0.2)
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


		# CLASS OVERRIDES
		self.defaultSpeed    = 2

		# ENEMY COORDS 

		self.angleDiffToEnemy = 0
		self.DistanceToEnemy  = 50000
		self.enemyTargetAngle = 0
		self.defenceSector    = self.patrolLocations[0]

		# SHOOTT 
		self.bulletTimer        = stopTimer()           # BUFF
		self.shootDelay         = 0.5                   # BUFF
		self.bulletsFired       = 0

	# AI LOGIC
	def actions(self,gui,game,lv):


		if(self.state=='patrol'):
			self.patrol(gui,lv)

		
		if(self.state=='attackPursue'):
			self.atackPursue(gui,lv,game)

		if(self.state=='alert'):
			self.alert(gui,lv)



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
		if(DistanceToEnemy<0.4*gui.h):
			self.state = 'attackPursue'
			
			# WORK OUT WHICH SECTOR IS NEAREST

			self.defenceSector = currentDestination


		"""
		[0,0], [400,0], [400,400], [0,400]

		
		what destination am i going to at this moment
		
		moveToDestinationFunction()
			
			what is the target coordinates
			what is the target coordinates relative to my position
			from my position, where am i facing
			from my facing and position, how much do i need to turn, to face the destination

			ajdust facing position, so always facing target


			move forward


		"""




	def atackPursue(self,gui,lv,game):
		
		# DISTANCE THE ENEMY IS FROM ROUTE COORD
		angleDiffToEnemy,DistanceToEnemy,enemyTargetAngle = angleToTarget(self,lv.player.x,lv.player.y,self.defenceSector[0],self.defenceSector[1])
		
		if(DistanceToEnemy<0.8*gui.h):

			# RECALCULATE RELATIVE POS TO ENEMY
			angleDiffToEnemy,DistanceToEnemy,enemyTargetAngle = angleToTarget(self,self.x,self.y,lv.player.x,lv.player.y)

			# -----------FACE TOWARDS DESTINATION
			
			faceTarget(self,angleDiffToEnemy, turnIcrement=5)
			
			# -----------MOVE TOWARDS DESTINATION
			
			self.speed = self.defaultSpeed
			self.moveForwards()


			# -------SHOOT
			if DistanceToEnemy<0.4*gui.h:
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
				lv.bulletList.append(bullet(gui,self.blitPos['midTop'][0] + gui.camX,self.blitPos['midTop'][1]+ gui.camY,bid,self.classification, self.facing,'slitherShot', speed=self.maxSpeed + 1,damage=2,colour=[150,150,20]))
			


	def drawSelf(self,gui,game,lv):
		x,y = self.x - gui.camX,self.y  - gui.camY
		
		if(self.hit):
			self.damageAnimation(gui,lv,game)
		elif(self.alive==True and onScreen(self.x,self.y,self.w,self.h,gui) ):
			animate,self.blitPos  = self.images.animate(gui,'scout' + str(self.id),[x,y],game,rotation=self.facing-90)

