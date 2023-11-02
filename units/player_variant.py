from utils._utils import *
from utils.gameUtils import *
from utils._utils import stopTimer
from units.ordinance import *
from units.missile import *
from units.chaff import *
import time
import numpy
import random


"""
*********CYCLES LOCKON LEFT/RIGHT******
"""


# CAMERA IS ALL MANAGED BY PLAYER 
class player():
	def __init__(self,gui):
		self.id             = 0
		self.name 			= 'player'
		self.classification = 'ally'
		self.alive          = True

		# IMAGE AND DIRECTION 
		self.x              = 750
		self.y              = 730
		self.facing         = 90
		self.images         = imageAnimateAdvanced(gui.player,0.2)
		self.boostImage     = imageAnimateAdvanced(gui.playerBoost,0.2)
		self.thrustRImg     = imageAnimateAdvanced(gui.playerThustR,0.2)
		self.thrustLImg     = imageAnimateAdvanced(gui.playerThustL,0.2)
		self.reversingImg   = imageAnimateAdvanced(gui.playerReverse,0.2)
		self.shadow         = imageAnimateAdvanced(gui.playerShadow,0.2)
		self.shootingImg    = imageAnimateAdvanced(gui.playerShooting,0.2)
		self.lockOnImage    = imageAnimateAdvanced(gui.lockOn,0.05)
		self.flareTimer     = stopTimer()


		self.w              = int(gui.player[0].get_width())
		self.h              = int(gui.player[0].get_height())
		self.blitPos         = None
		self.shadowPos       = [self.x,self.y]
		self.rotatedW	     = self.w
		self.rotatedH	     = self.h
		self.vel_x             = 0
		self.vel_y             = 0
		self.cumulatedDistance = 0
		self.facingIncrementFreeRoam = 1.2



		self.rightBoundary   = None
		self.leftBoundary    = None
		self.topBoundary     = None
		self.bottomBoundary  = None

		
		# ------KEYS 
		self.SHOOTKEY                  = 'H'
		self.BOOST_BUTTON              = 'U' 
		self.JINK_BUTTON               = 'K'
		self.ENABLE_LOCKON_BUTTON      = 'Y'
		self.SPECIAL                   = 'J'
		self.FLARE_BUTTON              = 'F'
		self.BOMBKEY  				   = 'B'
		


		self.accellerating   = False
		self.reversing       = False

		# JINKING
		self.jinking           = False
		self.jinkDuration      = 6
		self.jinkCooldownTime  = 3
		self.jinkTimer         = stopTimer()           # BUFF
		self.jinkCoolDown      = stopTimer()
		self.jinkAvailable     = True
		self.jinkCount         = 0


		# ---LOCKON 

		self.cone_points     = None 	
		self.lockonActive    = True
		self.lockedOn        = False
		self.lockOnAvailable = False
		self.lockonTimer     = stopTimer()
		self.cycleRight      = False
		self.cycleLeft       = False
		self.lockedEnemy     = None
		self.lockonIndex     = 0
		self.cone_length     = 530
		self.cone_angle      = 100
		self.firing          = False
		self.initLockonFacing = False
		self.switchedLockon  = False

		self.shake_timer     = 0
		self.camShakeStarted = False

		self.thrustingR      = False
		self.thrustingL      = False

		# SHOULD BE OVERRIDEN

		self.hitImage         = gui.playerHit
		self.hitAnimation     = imageAnimateAdvanced(self.hitImage,0.2)



		# ATTRIBUTES 
		self.defaultHp         = 20
		self.hp                = self.defaultHp
		self.speed             = 0
		self.maxSpeedDefault   = 8
		self.maxSpeed          = self.maxSpeedDefault
		self.lockTurnSpeed     = 4
		self.boostSpeed        = 16
		

		# BOOSTING 

		self.boosting          = False
		self.boostDuration     = 15
		self.boostCooldownTime = 1
		self.boostTimer        = stopTimer()           # BUFF
		self.boostCoolDown     = stopTimer()
		self.boostAvailable    = True
		self.boostCount        = 0





		self.decelleration     = 0.2
		self.rotationSpeed     = 5


		# DAMAGE AND INVINCIBLE  
		self.hit 			     = False
		self.invincible          = False               # BUFF
		self.invincibleDelay     = 0.05                # BUFF
		self.invincibleTimer     = stopTimer()
		self.invincibleCount     = 0

		# BULLETS 
		self.shotType			= 'angleRound'
		#						   'pellet','doublePellet' ,'tripplePellet',
		self.availableWeapons   = ['angleRound','angleRoundFaster','angleRoundFullSpeed','angleRound3', 'hotRound','hotDouble','hotTripple','beam','slitherShot','doubleSlither','triBlast']
		self.bulletAttrs        = {'hotRound':{'speed':20,'damage':10}, 'hotDouble':{'speed':20,'damage':10}, 'hotTripple':{'speed':20,'damage':10},  'angleRound':{'speed':20,'damage':10},'angleRoundFaster':{'speed':20,'damage':10},'angleRoundFullSpeed':{'speed':20,'damage':10}, 'angleround2':{'speed':20,'damage':10}, 'angleRound3':{'speed':20,'damage':10},'pellet':{'speed':15,'damage':7}, 'doublePellet':{'speed':15,'damage':7}, 'tripplePellet':{'speed':15,'damage':7},  'slitherShot':{'speed':3,'damage':20}, 'doubleSlither':{'speed':3,'damage':20} , 'triBlast':{'speed':12,'damage':30}, 'beam':{'speed':12,'damage':30}}
		self.beamImage          = imageAnimateAdvanced(gui.beamPart,0.2)
		self.beamHead           = imageAnimateAdvanced(gui.beamHead,0.2)
		self.loadOutImageDict   = {"angleRound":gui.weaponsLoadout["missiles_angleRound"],"angleRoundFaster":gui.weaponsLoadout["missiles_angleRoundFaster"],"angleRoundFullSpeed":gui.weaponsLoadout["missiles_angleRoundFullSpeed"],"angleRound3":gui.weaponsLoadout["missiles_angleRound3"], "hotRound":gui.weaponsLoadout["missiles_1hot"],"hotDouble":gui.weaponsLoadout["missiles_2hot"],"hotTripple":gui.weaponsLoadout["missiles_3hot"]}
		self.loadOutCurrentImage = self.loadOutImageDict[self.shotType]
		
		self.nextShotDict        = {"angleRound":"angleRoundFaster","angleRoundFaster":"angleRoundFullSpeed","angleRoundFullSpeed":"angleRound3","hotRound":"hotDouble","hotDouble":"hotTripple"}
		self.swapShotDict        = {"angleRound":"hotRound","angleRoundFaster":"hotRound","angleRoundFullSpeed":"hotDouble","angleRound3":"hotTripple",
									"hotRound":"angleRound","hotDouble":"angleRoundFaster","hotTripple":"angleRound3"}
		self.maxPowerReference   = ['angleRound3','hotTripple']

		self.bulletTimer        = stopTimer()           # BUFF
		self.angleTimer         = stopTimer()           # BUFF
		self.blastCount         = 3
		self.angleDelay         = 0.4
		self.shootDelay         = 0.1                   # BUFF
		self.bulletsFired       = 0

		# MISSILES 
		self.missileType	     = 'streaker'
		self.availableMissiles   = ['streaker']
		self.missileAttrs        = { 'streaker':{'speed':6,'damage':150},'nuke':{'speed':12,'damage':1000}, }
		self.missileTimer        = stopTimer()           # BUFF
		self.missileDelay        = 1                   # BUFF
		self.missilesFired       = 0
		self.missileFiring       = False
		self.nukesAvailable      = 3


		self.flaresAvailable     = True
		self.launchFlares        = False
		self.flareID			 = 0
		self.flareDelay          = 0.5
		self.flareBatchDelay     = 3
		self.flareBatchComplete  = False 
		self.flareBachNo         = 0


		# BOMB 

		self.nukesDropped        = 0
		self.nukeAway            = False

		# DESTROY 
		self.destructionComplete = False
		self.chosenExplosionImg  = gui.smallYellowExplosion
		self.explosion           = imageAnimateAdvanced(self.chosenExplosionImg,0.1)
		self.debris 			 = 0
		self.score               = 0

	
	# MANAGE ACCELLERATION 
	
	def actions(self,gui,game,lv):


		# --------GET PRESSED KEYS

		pressedKeys     = [x.upper() for x in gui.input.pressedKeys]

		# --------BUTTON CONTROLLS
		# LOCKON OFF 
		if(self.lockonActive==False):
			self.SPECIAL            = 'L'
		# LOCKED ON 
		if(self.lockonActive==True):
			self.SHOOTKEY           = 'H'
			self.BOOST_BUTTON       = 'U' 
			self.JINK_BUTTON        = 'K' 
			self.SPECIAL            = 'L'


		if(self.LOCKON_MODE == 'NEEDS_LOCKON_PRESSED'):
			
			self.cycleLockon = False
			if('H' in pressedKeys):
				self.lockonActive = True
			else:
				self.lockonActive = False
				self.lockedOn     = False
				self.cycling      = True
			if(gui.input.returnedKey.upper()=='H' and self.lockonActive):
				self.cycleLockon = True

		if(self.cycling):
			# if self.lockonActive changes, the timer resets and counts again.
			lockonExpired = self.lockonTimer.stopWatch(1,'lockon countdown', str(self.lockonActive),game,silence=True)
			if(gui.input.returnedKey.upper()=='H'):
				self.cycleLockon = True
				self.lockonActive = True
			
			if(lockonExpired):
				self.cycling      = False

		elif(self.LOCKON_MODE =='HOLD_TOGGLE_LOCKON'):
			
			self.cycleLockon = False
			if('H' in pressedKeys and self.lockpressed==False):
				self.lockonActive = not self.lockonActive
				self.lockpressed = True
			if(gui.input.returnedKey.upper()=='H' and self.lockonActive):
				self.cycleLockon = True
			if(self.lockonActive==False):
				self.lockedOn     = False
			if('H' not in pressedKeys):
				self.lockpressed = False

		# ---- SIMPLER LOCKON SYSTEM WHERE YOU TAP SHOOT TO CYCLE

		# if('J' in pressedKeys):
		# 	self.lockonActive = True
		# else:
		# 	self.lockonActive = False
		# 	self.lockedOn = False

		# if(self.lockonActive):
		# 	if(gui.input.returnedKey.upper()=='H'):
		# 		self.cycleLockon=True


		# HOLD BOTH SHOOT AND LOCKON TO SWITCH
		self.cycleRight,self.cycleLeft = False,False
		if('H' in pressedKeys and 'J' in pressedKeys):
			if(gui.input.returnedKey.upper()=='D'):
				self.cycleRight=True
			if(gui.input.returnedKey.upper()=='A'):
				self.cycleLeft=True


			#pressedKeys.remove('H')

		
		elif(gui.input.returnedKey.upper()=='J'):
			self.lockonActive = not self.lockonActive

		if(self.lockonActive==False):
			self.lockedOn = False

		

		# ensure animation not stuck
		self.thrustingL,self.thrustingR = False,False
		self.reversing       = False




		# --------MOVEMENT LOGIC

		self.classicControls(gui,pressedKeys,lv,game)

		# --------BUILD DETECTION CONE

		self.cone_points = detectionCone(self.x,self.y,gui,-self.facing,cone_length=self.cone_length,cone_angle=self.cone_angle)
		#self.draw_cone(self.x,self.y,gui,self.cone_points,lv)

		# -------LOCK ON

		enemies = self.detectEnemies(gui,lv,self.cone_points)
		self.lockOn(gui,enemies,game,pressedKeys)


		# ---------MANAGE CAMERA 

		self.camera(gui,lv)



		# ------MANAGE INVINCIBILITY DURATION

		self.setInvincible(game)

		# ------KILL ME
		
		if(self.hp<1):
			killme(self,lv,killMesssage=' died because hp under 1.',printme=True)

		# ---------SHOOT

		self.firing = False
		if(self.SHOOTKEY in pressedKeys):
			self.shoot(game,lv,gui)
		if(self.SPECIAL in pressedKeys):
			self.launchMissiles(game,lv,gui,enemies)

		if(self.BOMBKEY in gui.input.returnedKey.upper()):
			self.launchNuke(game,lv,gui)

	def detectEnemies(self,gui,lv,cone_points):

		# Create a Rect object for the cone of vision
		cone_rect = pygame.Rect(min([p[0] for p in cone_points]), min([p[1] for p in cone_points]), max([p[0] for p in cone_points]) - min([p[0] for p in cone_points]), max([p[1] for p in cone_points]) - min([p[1] for p in cone_points]))

		detectEnemies = []
		targetList = lv.enemyList + lv.enemyComponentList
		for enemy in targetList:
			if(enemy.name in ['powerDrone']):
				continue
			if(onScreen(enemy.x,enemy.y,enemy.w,enemy.h,gui)):
				if cone_rect.collidepoint((enemy.x, enemy.y)):
					distance = getDistance(self.x,self.y,enemy.x,enemy.y)
					if(distance>200):
						detectEnemies.append((enemy,int(distance)))

		# RETURN ENEMY LIST IN ORDER OF NEAREST
		sorted_list  = sorted(detectEnemies, key=lambda x: x[1])
		enemies      = [tuple[0] for tuple in sorted_list]

		return(enemies)

	def lockOn(self,gui,enemies,game,pressedKeys):

		
		

		# IF LOCKON FUNCTION AVAILABLE
		if(self.lockonActive):

			self.switchedLockon = False
			# IF LEN ENEMIES GREATER THAN 0

			if(len(enemies)>0 and not self.boosting):

				# ------GET THE FIRST ENEMY COORDS
				try:
					ex,ey                = enemies[self.lockonIndex].x , enemies[self.lockonIndex].y
				except:
					print("****ERROR----FAIL, SOMEHOW ENEMIES DROPPING TO 0 line 196")
					print('Enemeies ' + str(len(enemies)))
					self.lockonIndex = 0
					return()
				
				exAdjusted,eyAdjusted = ex-gui.camX, ey-gui.camY
				ew,eh = enemies[self.lockonIndex].w , enemies[self.lockonIndex].h
				
				# ------GET ADJUSTED LOCKON ANIMATION X Y COORDS
				
				lx,ly = exAdjusted+0.5*(ew-gui.lockOn[0].get_width()),eyAdjusted+0.5*(eh-gui.lockOn[0].get_height())
				
				
				# ------IF THE ENEMY IS ON SCREEN TO REGISTER
				
				if(onScreen(ex,ey,gui.lockOn[0].get_width(),gui.lockOn[0].get_height(),gui)):
					
					# LOCK AN ENEMY IF NOT ALREADY DONE SO
					if(self.lockedEnemy==None):
						# ------RENDER LOCKON AROUND POTENTIAL ENEMY

						self.lockOnImage.animate(gui,str(enemies[0].id) + str(self.lockedOn),[lx,ly],game,repeat=True)
						self.lockedOn     = True
						self.lockedEnemy  = enemies[self.lockonIndex]

					
					# USER SWITCHES LOCKON TO NEXT ENEMY
					elif(self.lockedEnemy):
						if(self.cycleRight):
							self.switchedLockon = True
							if(self.lockonIndex+1 <len(enemies)):
								self.lockonIndex += 1
								self.lockedEnemy  = enemies[self.lockonIndex]
							else:
								self.lockonIndex = 0
								self.lockedEnemy  = enemies[self.lockonIndex]
						if(self.cycleLeft):
							self.switchedLockon = True
							if(self.lockonIndex-1 > 0):
								self.lockonIndex -= 1
								self.lockedEnemy  = enemies[self.lockonIndex]
							else:
								self.lockonIndex = len(enemies) -1
								self.lockedEnemy  = enemies[self.lockonIndex]




				else:
					
					# ------RESET IF THERE ARE NO ENEMIES ON SCREEN
					
					self.lockedOn = False
					self.lockonIndex = 0

			# IF LOCKED ON TO CHOSEN ENEMY
			if(self.lockedOn and self.lockedEnemy!=None and not self.boosting):
				
				# RENDER GREEN LOCKON AROUND TARGET
				if(self.lockedEnemy.blitPos!=None):
					lx,ly = self.lockedEnemy.x + 0.5* ( self.lockedEnemy.blitPos['rotatedDims'][0] - gui.lockOn[0].get_width()) ,self.lockedEnemy.y + 0.5*(self.lockedEnemy.blitPos['rotatedDims'][1] - gui.lockOn[0].get_height())
				else:
					lx,ly = self.lockedEnemy.x + 0.5* (gui.lockOn[0].get_width() -self.lockedEnemy.w ) ,self.lockedEnemy.y - 0.5*(gui.lockOn[0].get_height()-self.lockedEnemy.h )

				# if center point of drawing is not the actual center
				if(hasattr(self.lockedEnemy,'centerPoint')):
					lx,ly = self.lockedEnemy.x + 0.5* (gui.lockOn[0].get_width() -self.lockedEnemy.w ) , self.lockedEnemy.y  + 0.5* (gui.lockOn[0].get_height() -self.lockedEnemy.h ) 
				

				#drawImage(gui.screen,gui.lockOn[0],(lx-gui.camX,ly-gui.camY))
				complete= self.lockOnImage.animateNoRotation(gui,str(self.lockedEnemy.id) + str(self.lockedOn),[lx-gui.camX,ly-gui.camY],game,repeat=True)
				
				# FACE ENEMY 
				angleDiffToEnemy,DistanceToEnemy,enemyTargetAngle = angleToTarget(self,self.x,self.y, self.lockedEnemy.x , self.lockedEnemy.y)
				faceTarget(self,angleDiffToEnemy, turnIcrement=2)	

			# ENEMY IS DEAD, GET ANOTHER
			if(self.lockedEnemy!=None):
				if(self.lockedEnemy.alive==False):
					self.lockedOn    = False
					self.lockedEnemy = None


			# ----SWITCH OFF CONDITIONS 
			if(self.lockedOn==False or self.boosting or(onScreen(self.lockedEnemy.x,self.lockedEnemy.y,self.lockedEnemy.w,self.lockedEnemy.h,gui)==False)):
				self.lockedEnemy = None
				self.lockonIndex = 0

		# RESET LOCKON IF NO ENEMIES OR IN BOOST MODE
		if(len(enemies)<1 or  self.boosting):
			#self.lockOnImage.currentFrame = 0
			self.lockedOn                 = False



	def classicControls(self,gui,pressedKeys,lv,game):

		self.accellerating = False # ACCELELRATION FLAG
		self.vel_x = 0
		self.vel_y = 0
		self.maxSpeed = self.maxSpeedDefault

		if(self.lockonActive):
			self.lockonControl(gui,pressedKeys,lv,game)
		elif(self.lockonActive==False):
			self.freeRoamControl(gui,pressedKeys,lv,game)

		self.standardControls(gui,pressedKeys,lv,game)
		self.flares(gui,pressedKeys,lv,game)


	def lockonControl(self,gui,pressedKeys,lv,game):

		# ------MOVEMENT
		self.accellerating= False # ACCELELRATION FLAG

		# -------LOCKED ON MOVEMENT
		if(self.lockedOn):

			# UPDATE INIT FACING FOR NEW LOCKON EVENT
			if(self.initLockonFacing==None or self.switchedLockon):
				self.initLockonFacing = self.facing

			self.maxSpeed = 7
			
			# THE RELATIVE COMPONENTS NEEDED TO GO FORWARD, NOT ACTUAL X,Y VELS
			vel_x = self.maxSpeed * math.cos(math.radians(360-self.facing-90))
			vel_y = self.maxSpeed * math.sin(math.radians(360-self.facing-90))

			vx = self.maxSpeed * math.cos(math.radians(360-self.facing))
			vy = self.maxSpeed * math.sin(math.radians(360-self.facing))

			
			self.thrustingR,self.thrustingL = False, False
			# MOVE X COMP
			if('D' in pressedKeys):
				self.x  +=    0.8*self.maxSpeed
				self.thrustingR = True
			# TURN
			if('D' in pressedKeys and self.JINK_BUTTON in pressedKeys):
				self.facing -= 4

			# MOVE X COMP
			if('A' in pressedKeys):
				self.x  -= 0.8*self.maxSpeed
				self.thrustingL = True
			# LEFT     - TURN IF JINK BUTTON HELD
			if('A' in pressedKeys and self.JINK_BUTTON in pressedKeys):
				self.facing += 4
			
			# UP
			if('W' in pressedKeys ):
				#self.x += vx
				#self.vel_y -= 0.8*self.maxSpeed # ALSO MOVES RADIALLY
				self.y     -= 0.6*self.maxSpeed # MOVES UP/DOWN REL

			# DOWN
			if('S' in pressedKeys):	
				#self.x -= vel_x
				#self.vel_y += 0.8*self.maxSpeed
				self.y     += 0.6*self.maxSpeed
				self.reversing     = True
		

		# ---------JINK FOR LOCKON MODE NOT LOCKED ON

		if((self.JINK_BUTTON in pressedKeys or self.firing) and not self.lockedOn):
			self.maxSpeed = 5
			vel_x = self.maxSpeed * math.cos(math.radians(360-self.facing-90))
			vel_y = self.maxSpeed * math.sin(math.radians(360-self.facing-90))
			
			if('D' in pressedKeys):
				if('J' in pressedKeys and self.firing):
					self.facing -=1.4
				
				self.x -= vel_x
				self.y -= vel_y
				self.thrustingR = True


			if('A' in pressedKeys):
				if('J' in pressedKeys and self.firing):
					self.facing +=1.4
				self.x += vel_x
				self.y += vel_y
				self.thrustingL = True
			
			if('W' in pressedKeys ):
				self.speed += 0.7
				accell = True
			if('S' in pressedKeys):
				self.speed -= 0.7
				accell = True







	def freeRoamControl(self,gui,pressedKeys,lv,game):

		
		# NO LOCKON 
		
		# -------JINK IF EITHER JINK PRESSED OR SHOOT PRESSED

		# maybe simplify to ENABLE_LOCKON_BUTTON = FALSE...NOT SURE
		if( (self.JINK_BUTTON in pressedKeys and not self.lockedOn ) or (self.SHOOTKEY in pressedKeys and not self.lockedOn)):
			
			

			self.maxSpeed       = 5
			self.maxStrafeSpeed = 7


			# FOR MOVING HORIZONTALLY
			vel_x = self.maxStrafeSpeed * math.cos(math.radians(360-self.facing-90))
			vel_y = self.maxStrafeSpeed * math.sin(math.radians(360-self.facing-90))

			
			# RIGHT
			if('D' in pressedKeys):
				if('J' in pressedKeys and self.firing):
					self.facing +=self.facingIncrementFreeRoam
					self.thrustingR = True
				else:
					self.x -= vel_x 
					self.y -= vel_y 
					

			# LEFT
			if('A' in pressedKeys):
				if('J' in pressedKeys and self.firing):
					self.facing -=self.facingIncrementFreeRoam
					self.thrustingL = True
				else:
					self.x += vel_x 
					self.y += vel_y 
					
				

			
			# UP
			if('W' in pressedKeys ):
				self.speed += 0.7 
				self.accellerating = True

			# DOWN
			if('S' in pressedKeys):
				self.speed -= 0.7 
				self.reversing     = True
				self.accellerating = True


	



	def standardControls(self,gui,pressedKeys,lv,game):	

		# -------STANDARD MOVEMENT
		if((self.JINK_BUTTON not in pressedKeys) and not self.lockedOn and not self.firing):
			# GET DIRECTION OF ACCELLERATION
			if('W' in pressedKeys ):
				self.speed += 0.4
				self.accellerating = True
			if('S' in pressedKeys):
				self.speed -= 0.4
				self.accellerating = True
				self.reversing     = True
			if('D' in pressedKeys):
				self.facing -= 3
			if('A' in pressedKeys):
				self.facing += 3



		# ------INCREMENT SHOT TYPE 

		if(gui.input.returnedKey.upper()=='E'):
			nextIndex    = (self.availableWeapons.index(self.shotType) + 1) % len(self.availableWeapons)
			self.shotType = self.availableWeapons[nextIndex]
			if(self.shotType in self.loadOutImageDict.keys()):
				self.loadOutCurrentImage = self.loadOutImageDict[self.shotType]

		# -------SPEED BOOST PHASE 1
		
		if(self.BOOST_BUTTON in pressedKeys and not self.JINK_BUTTON in pressedKeys):
			
			boostComplete = self.boostTimer.stopWatch(self.boostDuration,'boost', str(self.boostCount),game,silence=True)
			
			if(not boostComplete):
				self.boosting = True
				self.maxSpeed = self.boostSpeed
			if(boostComplete==True):
				self.boostAvailable = False
		
		# -------SPEED BOOST PHASE COOLDOWN

		if((self.BOOST_BUTTON not in pressedKeys) or self.boostAvailable == False):
			self.boosting       = False
			self.maxSpeed       = self.maxSpeedDefault
			if(self.boostAvailable == False):
				self.boostAvailable = self.boostCoolDown.stopWatch(self.boostCooldownTime,'boost cooldown Counter', str(self.boostCount),game,silence=True)
				if(self.boostAvailable):
					self.boostCount +=1


	
		# WRAP ANGLE
		self.facing = wrapAngle(self.facing)

		# CLAMP SPEED
		self.speed = clamp(self.speed,self.maxSpeed)

		# APPLY SPEED COMPONENT
		self.vel_x = self.speed * math.cos(math.radians(360-self.facing)) 
		self.vel_y = self.speed * math.sin(math.radians(360-self.facing))
		self.cumulatedDistance += math.sqrt(self.vel_x**2 + self.vel_y**2)
		
		# UPDATE POSITION
		self.x += int(self.vel_x )
		self.y += int(self.vel_y)

		# SLOWDOWN WHEN NOT ACCELLERATING
		if(self.accellerating==False):
			self.speed = zero(self.speed,self.decelleration)




		# BORDER CLAMP

		# update once 
		if(self.rightBoundary==None):
			self.rightBoundary   = lv.mapw
			self.leftBoundary    = lv.mapx
			self.topBoundary     = lv.maph
			self.bottomBoundary  = lv.mapy


		if(self.x + self.w > self.rightBoundary): self.x -= self.maxSpeed
		if(self.x < self.leftBoundary): self.x += self.maxSpeed
		if(self.y + self.h > self.topBoundary): self.y -= self.maxSpeed
		if(self.y < self.bottomBoundary): self.y += self.maxSpeed






	# CALLED BY allyActions/enemyActions
	def shoot(self,game,lv,gui, bulletColour=(255,177,42)):

		self.firing = True


		# BULLET DELAY TIMER
		shotAvailable = self.bulletTimer.stopWatch(self.shootDelay,'player shoot', str(self.id + self.bulletsFired), game,silence=True)
		
		# IF SHOOT CRITEREA MET,
		if((shotAvailable and self.blitPos!=None)):




			if(self.shotType=='angleRound'):
				self.angleDelay = 0.4

				if(self.blastCount>0):
					self.bulletsFired +=2
					self.blastCount  -= 1

					# ADDS BULLET TO BULLET LIST
					bid = max(([x.id for x in lv.bulletList]),default=0) + 1
					lv.bulletList.append(bullet(gui,self.blitPos['middleL'][0]+ gui.camX,self.blitPos['middleL'][1]+ gui.camY,bid,self.classification, self.facing,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))
					bid = max(([x.id for x in lv.bulletList]),default=0) + 1
					lv.bulletList.append(bullet(gui,self.blitPos['middleR'][0]+ gui.camX,self.blitPos['middleR'][1]+ gui.camY,bid,self.classification, self.facing,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))



				else:
					angleReload = self.angleTimer.stopWatch(self.angleDelay,'player angleRound', str(self.id + self.bulletsFired + self.blastCount), game,silence=True)
					if(angleReload):
						self.blastCount = 3


			elif(self.shotType=='angleRoundFaster'):
				self.angleDelay = 0.15


				if(self.blastCount>0):
					self.bulletsFired +=2
					self.blastCount  -= 1
					# ADDS BULLET TO BULLET LIST
					bid = max(([x.id for x in lv.bulletList]),default=0) + 1
					lv.bulletList.append(bullet(gui,self.blitPos['middleL'][0]+ gui.camX,self.blitPos['middleL'][1]+ gui.camY,bid,self.classification, self.facing,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))
					bid = max(([x.id for x in lv.bulletList]),default=0) + 1
					lv.bulletList.append(bullet(gui,self.blitPos['middleR'][0]+ gui.camX,self.blitPos['middleR'][1]+ gui.camY,bid,self.classification, self.facing,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))

				else:
					angleReload = self.angleTimer.stopWatch(self.angleDelay,'player angleRoundFaster', str(self.id + self.bulletsFired + self.blastCount), game,silence=True)
					if(angleReload):
						self.blastCount = 3


			elif(self.shotType=='angleRoundFullSpeed'):

				self.angleDelay = 0.05



				if(self.blastCount>0):
					self.bulletsFired +=2
					self.blastCount  -= 1
					# ADDS BULLET TO BULLET LIST
					bid = max(([x.id for x in lv.bulletList]),default=0) + 1
					lv.bulletList.append(bullet(gui,self.blitPos['middleL'][0]+ gui.camX,self.blitPos['middleL'][1]+ gui.camY,bid,self.classification, self.facing,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))
					bid = max(([x.id for x in lv.bulletList]),default=0) + 1
					lv.bulletList.append(bullet(gui,self.blitPos['middleR'][0]+ gui.camX,self.blitPos['middleR'][1]+ gui.camY,bid,self.classification, self.facing,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))


				else:
					angleReload = self.angleTimer.stopWatch(self.angleDelay,'player angleRoundFullSpeed', str(self.id + self.bulletsFired + self.blastCount), game,silence=True)
					if(angleReload):
						self.blastCount = 3

			elif(self.shotType=='angleRound3'):
				self.angleDelay = 0.3



				if(self.blastCount>0):
					self.bulletsFired +=6
					self.blastCount  -= 1
					# ADDS BULLET TO BULLET LIST
					bid = max(([x.id for x in lv.bulletList]),default=0) + 1
					lv.bulletList.append(bullet(gui,self.blitPos['middleL'][0]+ gui.camX,self.blitPos['middleL'][1]+ gui.camY,bid,self.classification, self.facing,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))
					bid = max(([x.id for x in lv.bulletList]),default=0) + 1
					lv.bulletList.append(bullet(gui,self.blitPos['middleR'][0]+ gui.camX,self.blitPos['middleR'][1]+ gui.camY,bid,self.classification, self.facing,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))

					bid = max(([x.id for x in lv.bulletList]),default=0) + 1
					lv.bulletList.append(bullet(gui,self.blitPos['centerL'][0]+ gui.camX,self.blitPos['centerL'][1]+ gui.camY,bid,self.classification, self.facing-15,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))
					bid = max(([x.id for x in lv.bulletList]),default=0) + 1
					lv.bulletList.append(bullet(gui,self.blitPos['centerR'][0]+ gui.camX,self.blitPos['centerR'][1]+ gui.camY,bid,self.classification, self.facing-15,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))

					bid = max(([x.id for x in lv.bulletList]),default=0) + 1
					lv.bulletList.append(bullet(gui,self.blitPos['centerL'][0]+ gui.camX,self.blitPos['centerL'][1]+ gui.camY,bid,self.classification, self.facing+15,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))
					bid = max(([x.id for x in lv.bulletList]),default=0) + 1
					lv.bulletList.append(bullet(gui,self.blitPos['centerR'][0]+ gui.camX,self.blitPos['centerR'][1]+ gui.camY,bid,self.classification, self.facing+15,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))


				else:
					angleReload = self.angleTimer.stopWatch(self.angleDelay,'player angleRound3', str(self.id + self.bulletsFired + self.blastCount), game,silence=True)
					if(angleReload):
						self.blastCount = 3




			elif(self.shotType=='pellet'):

				# ADDS BULLET TO BULLET LIST
				self.bulletsFired +=1
				# ADDS BULLET TO BULLET LIST
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(bullet(gui,self.blitPos['midTop'][0] + gui.camX,self.blitPos['midTop'][1]+gui.camY,bid,self.classification, self.facing,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))


			elif(self.shotType=='doublePellet'):
				self.bulletsFired +=1
				# ADDS BULLET TO BULLET LIST
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(bullet(gui,self.blitPos['leftTop'][0]+ gui.camX,self.blitPos['leftTop'][1]+ gui.camY,bid,self.classification, self.facing,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))
				
				# ADDS BULLET TO BULLET LIST
				self.bulletsFired +=1
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(bullet(gui,self.blitPos['rightTop'][0]+ gui.camX,self.blitPos['rightTop'][1]+ gui.camY,bid,self.classification, self.facing,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))

			elif(self.shotType=='tripplePellet'):
				self.bulletsFired +=1
				# ADDS BULLET TO BULLET LIST
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(bullet(gui,self.blitPos['leftTop'][0]+ gui.camX,self.blitPos['leftTop'][1]+ gui.camY,bid,self.classification, self.facing,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))

				# ADDS BULLET TO BULLET LIST
				self.bulletsFired +=1
				# ADDS BULLET TO BULLET LIST
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(bullet(gui,self.blitPos['midTop'][0] + gui.camX,self.blitPos['midTop'][1]+gui.camY,bid,self.classification, self.facing,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))


				# ADDS BULLET TO BULLET LIST
				self.bulletsFired +=1
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(bullet(gui,self.blitPos['rightTop'][0]+ gui.camX,self.blitPos['rightTop'][1]+ gui.camY,bid,self.classification, self.facing,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))

			
			elif(self.shotType=='doubleSlither'):
				self.bulletsFired +=2
				# ADDS BULLET TO BULLET LIST
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(bullet(gui,self.blitPos['leftTop'][0]+ gui.camX,self.blitPos['leftTop'][1]+ gui.camY,bid,self.classification, self.facing,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))
				lv.bulletList.append(bullet(gui,self.blitPos['rightTop'][0]+ gui.camX,self.blitPos['rightTop'][1]+ gui.camY,bid+1,self.classification, self.facing,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))

			elif(self.shotType=='triBlast'):
				self.bulletsFired +=1
				# ADDS BULLET TO BULLET LIST
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(bullet(gui,self.blitPos['midTop'][0]+ gui.camX,self.blitPos['midTop'][1]+ gui.camY,bid,self.classification, self.facing,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))
			elif(self.shotType=='hotRound'):
				self.bulletsFired +=1
				# ADDS BULLET TO BULLET LIST
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(bullet(gui,self.blitPos['midTop'][0]+ gui.camX,self.blitPos['midTop'][1]+ gui.camY,bid,self.classification, self.facing,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))
			elif(self.shotType=='hotDouble'):
				self.bulletsFired +=2
				# ADDS BULLET TO BULLET LIST
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(bullet(gui,self.blitPos['centerL'][0]+ gui.camX,self.blitPos['centerL'][1]+ gui.camY,bid,self.classification, self.facing,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))
				lv.bulletList.append(bullet(gui,self.blitPos['centerR'][0]+ gui.camX,self.blitPos['centerR'][1]+ gui.camY,bid+1,self.classification, self.facing,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))
			elif(self.shotType=='hotTripple'):
				self.bulletsFired +=1
				# ADDS BULLET TO BULLET LIST
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(bullet(gui,self.blitPos['midTop'][0]+ gui.camX,self.blitPos['midTop'][1]+ gui.camY,bid,self.classification, self.facing,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))
				lv.bulletList.append(bullet(gui,self.blitPos['centerL'][0]+ gui.camX,self.blitPos['centerL'][1]+ gui.camY,bid+1,self.classification, self.facing,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))
				lv.bulletList.append(bullet(gui,self.blitPos['centerR'][0]+ gui.camX,self.blitPos['centerR'][1]+ gui.camY,bid+2,self.classification, self.facing,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))
			elif(self.shotType=='beam'):
				ox,oy = self.x - gui.camX,self.y  - gui.camY
				
				# CENTER POINT
				cx, cy =self.x-gui.camX - 0.5*gui.beamHead[0].get_width(),self.y-gui.camY- 0.5*gui.beamHead[0].get_height()
				cx,cy  = cx + 50,cy+50
				fx,fy  = cx + 50*math.cos(math.radians(360-self.facing)),cy + 50*math.sin(math.radians(360-self.facing))
				
				cx, cy = self.x-gui.camX - 0.5*gui.beamPart[0].get_width(),self.y-gui.camY- 0.5*gui.beamPart[0].get_height()
				cx,cy  = cx + 50,cy+50
				x,y  = cx + 50*math.cos(math.radians(360-self.facing)),cy + 50*math.sin(math.radians(360-self.facing))

				blitBeam  = True
				for i in range(70):
					if(blitBeam):
						self.beamImage.animate(gui,'beamshot',[x,y],game,rotation=self.facing-90)
						vel_x = 14 * math.cos(math.radians(360-self.facing))
						vel_y = 14 * math.sin(math.radians(360-self.facing))

						x += vel_x 
						y += vel_y
						enemyBullets = [x for x in lv.bulletList if (x.classification=='enemy' and x.name=='missile')]
						enemyList = lv.enemyList + lv.enemyComponentList + enemyBullets
						for e in enemyList:
							if(collidesObjectless(x+gui.camX,y+gui.camY,15,15,e.x,e.y,e.w,e.h)):
								self.beamHead.animate(gui,'beamHead',[x-10*math.cos(math.radians(360-self.facing+90)),y-10*math.cos(math.radians(360-self.facing+90))],game,rotation=self.facing-90)
								
								if(e.name=='missile'):
									e.killSelf(lv,killMessage='missile destroyed by beam')
								else:
									blitBeam=False
									e.hp -= 3
									e.hit = True
									if(e.hp<1):
										e.alive = False
										killme(e,lv)
								break


				self.beamHead.animate(gui,'beamHead',[fx,fy],game,rotation=self.facing-90)

			else:
				self.bulletsFired +=1
				# ADDS BULLET TO BULLET LIST
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(bullet(gui,self.blitPos['midTop'][0] + gui.camX,self.blitPos['midTop'][1]+gui.camY,bid,self.classification, self.facing,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))

	def launchMissiles(self,game,lv,gui,enemies):


		if((self.missileFiring==False and self.blitPos!=None)):	
			if(self.missileType=='streaker'):
				self.missilesFired +=2

				targetList = []
				if(self.lockedEnemy): targetList.append(self.lockedEnemy)
				targetList += [i for i in enemies if i!=self.lockedEnemy]
				if(len(targetList)<1): targetList = [None,None]
				if(len(targetList)<2): targetList = [self.lockedEnemy,None]
				
				#ADDS MISSILES TO BULLET LIST
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(missile(gui,self.blitPos['midTop'][0] + gui.camX,self.blitPos['midTop'][1]+ gui.camY,bid,self.classification, self.facing,self.missileType,playerSpeed=self.speed, speed=abs(self.maxSpeed) + self.missileAttrs[self.missileType]['speed'],damage=self.missileAttrs[self.missileType]['damage'],jink='left',lockedOnEnemy=targetList[0]))
				
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(missile(gui,self.blitPos['midTop'][0] + gui.camX,self.blitPos['midTop'][1]+ gui.camY,bid,self.classification, self.facing,self.missileType,playerSpeed=self.speed, speed=abs(self.maxSpeed) + self.missileAttrs[self.missileType]['speed'],damage=self.missileAttrs[self.missileType]['damage'],jink='right',lockedOnEnemy=targetList[1]))
				

				self.missileFiring = True

		#  RESET WHEN TIME REACHED
		if(self.missileFiring == True):
			# BULLET DELAY TIMER
			missilesReady = self.missileTimer.stopWatch(self.missileDelay,'player shoot missile', str(self.id + self.missilesFired), game,silence=True)
			# READY TO FIRE AGAIN
			if((missilesReady )):
				self.missileFiring = False


	def launchNuke(self,game,lv,gui):
		

		if(self.nukeAway==False and self.nukesAvailable >0):
			#ADDS MISSILES TO BULLET LIST
			bid = max(([x.id for x in lv.bulletList]),default=0) + 1
			lv.bulletList.append(missile(gui,self.blitPos['midTop'][0] + gui.camX,self.blitPos['midTop'][1]+ gui.camY,bid,self.classification, self.facing,'nuke',playerSpeed=self.speed, speed=abs(self.maxSpeed) + self.missileAttrs['nuke']['speed'], damage=self.missileAttrs['nuke']['damage']))
			self.nukesAvailable -=1
			#self.nukeAway=True



	def setInvincible(self,game):
		
		if(self.invincible):
			invincibleTimer = self.invincibleTimer.stopWatch(self.invincibleDelay,str(self.id + self.hp),self,game,silence=True)
			if(invincibleTimer):
				self.invincible = False




	def flares(self,gui,pressedKeys,lv,game):

		"""
		launch like a missle, but the missle animation is the yellow bit
		Give it the x,y,plus 1/2 current velocity

		"""

		# SET LAUNCH FLARES FLAG IF BUTTON PRESSED
		if(self.blitPos!=None and self.launchFlares==False):	
			if(gui.input.returnedKey.upper() == self.FLARE_BUTTON):
				self.launchFlares = True

		# IF AVAILABLE, FIRE TWO FLARES
		if(self.launchFlares and self.flaresAvailable):

			self.missilesFired +=2
			
			#ADDS MISSILES TO BULLET LIST
			bid = max(([x.id for x in lv.bulletList]),default=0) + 1
			lv.bulletList.append(chaff(gui,self.blitPos['midTop'][0] + gui.camX,self.blitPos['midTop'][1]+ gui.camY,bid,self.classification, wrapAngle(self.facing+random.randrange(35,65)),playerSpeed=self.speed, speed=self.speed,jink='left'))
			
			bid = max(([x.id for x in lv.bulletList]),default=0) + 1
			lv.bulletList.append(chaff(gui,self.blitPos['midTop'][0] + gui.camX,self.blitPos['midTop'][1]+ gui.camY,bid,self.classification, wrapAngle(self.facing-random.randrange(35,65)),playerSpeed=self.speed, speed=self.speed,jink='right'))
			
			self.flaresAvailable = False

		
		#  SET AVAILABLE AFTER COOLDOWN TIMER, LOCK OUT ONCE 5 BATCHES
		if(self.blitPos!=None  and self.flaresAvailable == False and self.flareBatchComplete==False):
			# FLARE DELAY TIMER
			flaresComplete = self.flareTimer.stopWatch(self.flareDelay,'player launched flares', 'flaresEjected ' + str(self.flareID), game,silence=True)
			# READY TO FIRE AGAIN
			if((flaresComplete )):
				self.flareBachNo += 1
				self.flaresAvailable = True
				self.flareID +=1

		# LOCK OUT BATCHES
		if(self.flareBachNo>5):
			self.flareBatchComplete = True

		# TIME OUT UNTIL NEXT BATCH AVAILABLE
		if(self.flareBatchComplete==True):
			batchComplete = self.flareTimer.stopWatch(self.flareBatchDelay,'player flare batch complete', 'flaresEjected ' + str(self.flareID), game,silence=True)
			if(batchComplete):
				self.flaresAvailable   = True
				self.flareBatchComplete = False
				self.launchFlares       = False
				self.flareBachNo        = 0






	def camera(self,gui,lv):

		margins = [0.5*gui.w,0.45*gui.h]
		interpolation_factor = 0.7


		# -------------CAMERA SHAKE

		shake_duration = 250  # Duration of the camera shake in milliseconds 

		# Interpolate between current and target camera positions
		target_camX = self.x - margins[0]
		target_camY = self.y - margins[1]
		
		# CAMERA SHAKE INIT
		if lv.enemyDestroyed and self.camShakeStarted==False:
		  # Add a random offset to the target camera position to create a shake effect
		  self.camShakeStarted = True
		  self.shake_timer = pygame.time.get_ticks()  # Reset the shake timer

		 # START SHAKE TIMER 
		elif(self.camShakeStarted):
		  # Gradually decrease the interpolation factor back to its original value
		  elapsed_time = pygame.time.get_ticks() - self.shake_timer
		  target_camX += random.uniform(-25, 25)
		  target_camY += random.uniform(-25, 25)

		  # SMOOTH OUT AS TIME DECREASES
		  if elapsed_time < shake_duration:
		    interpolation_factor = 0.7 + 0.3 * (elapsed_time / shake_duration)
		  else:
		    interpolation_factor = 0.7  # Return interpolation factor to its original value
		    lv.enemyDestroyed = False  # Set the enemyDestroyed variable to False
		    self.shake_timer = pygame.time.get_ticks()
		    self.camShakeStarted = False

		
		gui.camX = (1 - interpolation_factor) * gui.camX + interpolation_factor * target_camX
		gui.camY = (1 - interpolation_factor) * gui.camY + interpolation_factor * target_camY
		


		#-----FORCE  INTO OBJECTIVE QUADRANT

		if(hasattr(lv,'objectives')):
			if(lv.currentObjective not in [None,'complete']):
				currentObjective = lv.objectives[lv.currentObjective]
				# DONT CONSTRAIN PLAYER IF NOT NEEDED
				if(currentObjective['constrain']==False):
					return
				
				activeQuandrant  = currentObjective['activeQuandrant']
				if(gui.camX > activeQuandrant['x'] + activeQuandrant['w'] - gui.camW):
					gui.camX = activeQuandrant['x'] + activeQuandrant['w'] - gui.camW
				if(gui.camX < activeQuandrant['x']): 
					gui.camX = activeQuandrant['x']
				if(gui.camY > activeQuandrant['y'] + activeQuandrant['h'] - gui.camH):
					gui.camY = activeQuandrant['y'] + activeQuandrant['h'] - gui.camH
				if(gui.camY < activeQuandrant['y']): 
					gui.camY = activeQuandrant['y']


		




		"""
		margins = [0.5*gui.w,0.44*gui.h]

		interpolation_factor = 0.5

		xFudge,yFudge = 3,3
		#xFudge,yFudge = 0.01*gui.w,0.02*gui.h
		#if(self.firing): xFudge,yFudge = 0.005*gui.w,0.01*gui.h

		# Calculate the look-ahead distance based on the player's velocity
		look_ahead_distancex = xFudge * self.vel_x
		look_ahead_distancey = yFudge * self.vel_y

		# Calculate the target camera positions, taking into account the look-ahead distance
		target_camX = self.x + look_ahead_distancex - margins[0]
		target_camY = self.y + look_ahead_distancey - margins[1]

		# Interpolate between current and target camera positions, using a higher interpolation factor for both the x and y directions
		gui.camX = (1 - interpolation_factor) * gui.camX + interpolation_factor * target_camX
		gui.camY = (1 - interpolation_factor) * gui.camY + interpolation_factor * target_camY

		"""

	def drawSelf(self,gui,game,lv):
		x,y = self.x - gui.camX,self.y  - gui.camY



		if(self.hit):
			self.damageAnimation(gui,lv,game)
		elif(self.alive==True and onScreen(self.x,self.y,self.w,self.h,gui)):
			# UPDATE POSITION
			shadow_x = x + 60
			shadow_y = y + 80

			self.shadow.animate(gui,'player shadow',[shadow_x,shadow_y],game,rotation=self.facing-90)
			#drawImage(gui.screen,gui.playerShadow[0],(self.shadowPos[0],self.shadowPos[1]))
			
			if(self.boosting):
				animate,imageParms = self.boostImage.animate(gui,'playerBoosting',[x,y],game,rotation=self.facing-90)
			if(self.reversing):
				animate,imageParms = self.reversingImg.animate(gui,'playerReversing',[x,y],game,rotation=self.facing-90)
			elif(self.thrustingR):
				animate,imageParms = self.thrustRImg.animate(gui,'playerThrusting',[x,y],game,rotation=self.facing-90,repeat= True, repeatIndex=len(gui.playerThustR)-3)
			elif(self.thrustingL):
				animate,imageParms = self.thrustLImg.animate(gui,'playerThrusting',[x,y],game,rotation=self.facing-90,repeat= True, repeatIndex=len(gui.playerThustL)-3)
			else:
				animate,imageParms = self.images.animate(gui,'player',[x,y],game,rotation=self.facing-90)
			
			self.blitPos   = imageParms
			self.shadowPos = imageParms['behind']
		if(self.firing and self.alive):
			animate,imageParms = self.shootingImg.animate(gui,'player shooting',[x,y],game,rotation=self.facing-90)

		# DRAW DETECTION CONE
		#if(self.cone_points!=None): self.draw_cone(x,y,gui, self.cone_points,lv)

	
	def draw_cone(self,x,y,gui,cone_points,lv):

		cone_points = detectionCone(self.x-gui.camX,self.y-gui.camY,gui,-self.facing,cone_length=self.cone_length,cone_angle=self.cone_angle)
		# Draw the cone of vision using the polygon() function
		pygame.draw.polygon(gui.screen, (255, 255, 255), cone_points,3)



	def animateDestruction(self,gui,lv,game):
		x,y = self.x - gui.camX,self.y  - gui.camY

		if(self.destructionComplete==False and self.alive==False):
			complete,blitPos = self.explosion.animate(gui,str(str(self.name) +' explosion'),[x,y],game)
			bid = max(([x.id for x in lv.bulletList]),default=0) + 1


			if(self.debris<=12):
				self.debris +=1
				# ADDS DEBRIS TO TO LIST
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(bullet(gui,self.x + 0.5* self.chosenExplosionImg[0].get_width(),self.y+ 0.5* self.chosenExplosionImg[0].get_height(),bid,'debris',random.randrange(0,360),'debris',speed=10, w=0.05*self.w,h=0.05*self.h,colour=(192,192,192)))
			if(complete):
				self.destructionComplete = True

	def damageAnimation(self,gui,lv,game):
		x,y = self.x - gui.camX,self.y  - gui.camY
		
		if(self.alive==True and onScreen(self.x,self.y,self.w,self.h,gui)):
			complete,imageParms = self.hitAnimation.animate(gui,str(self.name) + ' hit',[x,y],game,rotation=self.facing-90)
			if(complete):
				self.hit = False

