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
	def __init__(self,gui,x=None,y=None):
		super().__init__(gui)
		self.name           = 'scout'
		self.images         = imageAnimateAdvanced(gui.scoutRed,0.2)
		if(x!=None): self.x = x
		if(y!=None): self.y = y
		self.w              = int(gui.scoutRed[0].get_width())
		self.h              = int(gui.scoutRed[0].get_height())
		self.healthBar      = loadingBarClass(self.w,0.2*self.h,(80,220,80),(220,220,220),(0,0,200))


		self.state             = 'patrol'
		self.patrolLocations   = [(730,110),(1440,110),(1440,540),(730,540)] 
		self.currentLocIndex   = 0


		# CLASS OVERRIDES
		self.defaultSpeed    = 4
		



	# AI LOGIC
	def actions(self,gui,game,lv):

		if(self.state=='patrol'):
			self.patrol()

		
		if(self.state=='attackPursue'):
			self.atackPursue()

		if(self.state=='alert'):
			self.alert()



	def patrol(self):
		
		currentCoords = self.patrolLocations[self.currentLocIndex]
		angleDifference,distance,targetAngle = angleToTarget(self,self.x,self.y, currentCoords[0],currentCoords[1])

		faceTarget(self,angleDifference, turnIcrement=8)
		self.speed = 3
		self.moveForwards()

		if(distance< self.w): self.currentLocIndex+=1
		if(self.currentLocIndex>=len(self.patrolLocations)):
			self.currentLocIndex = 0

		
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




	def atackPursue(self):
		print('Atack and pusue ')


	def alert(self):
		print('alert')






	def drawSelf(self,gui,game,lv):
		x,y = self.x - gui.camX,self.y  - gui.camY
		
		if(self.alive==True and onScreen(self,gui)):
			animate,imageParms = self.images.animate(gui,'scout',[x,y],game,rotation=self.facing-90)

