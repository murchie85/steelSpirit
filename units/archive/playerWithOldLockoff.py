from utils._utils import *
from utils.gameUtils import *
from utils._utils import stopTimer
from units.ordinance import *
from units.missile import *
from units.flare import *
import time
import numpy
import random


"""
- actions
- detectEnemies
- lockon
- shoot
- set invincible
- classicControls
- camera
- drawSelf
- drawCone
- animateDestruction
- damageAnimation
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
		self.vel_x           = 0
		self.vel_y           = 0
		
		# ------KEYS 
		self.SHOOTKEY                  = 'H'
		self.BOOST_BUTTON              = 'U' 
		self.JINK_BUTTON               = 'K'
		self.ENABLE_LOCKON_BUTTON      = 'Y'
		self.SPECIAL                   = 'J'
		self.FLARE_BUTTON              = 'F'
		
		self.TILTLEFT           = '--' # INITIALLY DISABLED IF LOCKON ON
		self.TILTRIGHT          = '--'


		self.accellerating   = False

		# JINKING
		self.jinking           = False
		self.jinkDuration      = 6
		self.jinkCooldownTime  = 3
		self.jinkTimer         = stopTimer()           # BUFF
		self.jinkCoolDown      = stopTimer()
		self.jinkAvailable     = True
		self.jinkCount         = 0
		self.initJinkFacing    = None # allows strafe in clear line
		self.jinkFacingTotal   = 0    # USED TO LIMIT SPRAY ANGLE


		# ---LOCKON 

		self.cone_points     = None 	
		self.lockonActive    = True
		self.lockedOn        = False
		self.lockOnAvailable = False
		self.lockedEnemy     = None
		self.lockonIndex     = 0
		self.cone_length     = 480
		self.cone_angle      = 80
		self.firing          = False
		self.initLockonFacing = False
		self.switchedLockon  = False

		self.shake_timer     = 0
		self.camShakeStarted = False


		self.lockOffMode     = 'strafing'
		# SHOULD BE OVERRIDEN

		self.hitImage         = gui.playerHit
		self.hitAnimation     = imageAnimateAdvanced(self.hitImage,0.2)



		# ATTRIBUTES 
		self.defaultHp         = 100
		self.hp                = self.defaultHp
		self.speed             = 0
		self.maxSpeed          = 8
		self.lockTurnSpeed     = 4
		self.maxSpeedDefault   = 8
		self.boostSpeed        = 16
		

		# BOOSTING 

		self.boosting          = False
		self.boostDuration     = 5
		self.boostCooldownTime = 3
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
		self.shotType			= 'hotRound'
		self.availableWeapons   = ['hotRound','hotDouble','hotTripple','pellet','doublePellet' ,'slitherShot','doubleSlither','triBlast']
		self.bulletAttrs        = {'hotRound':{'speed':10,'damage':10}, 'hotDouble':{'speed':10,'damage':8}, 'hotTripple':{'speed':10,'damage':7},  'pellet':{'speed':15,'damage':7}, 'doublePellet':{'speed':15,'damage':7},  'slitherShot':{'speed':3,'damage':20}, 'doubleSlither':{'speed':3,'damage':20} , 'triBlast':{'speed':12,'damage':30} }
		
		self.bulletTimer        = stopTimer()           # BUFF
		self.shootDelay         = 0.1                   # BUFF
		self.bulletsFired       = 0

		# MISSILES 
		self.missileType	     = 'streaker'
		self.availableMissiles   = ['streaker']
		self.missileAttrs        = { 'streaker':{'speed':6,'damage':150}}
		self.missileTimer        = stopTimer()           # BUFF
		self.missileDelay        = 1                   # BUFF
		self.missilesFired       = 0
		self.missileFiring       = False


		self.flaresAvailable     = True
		self.launchFlares        = False
		self.flareID			 = 0
		self.flareDelay          = 0.5
		self.flareBatchDelay     = 3
		self.flareBatchComplete  = False 
		self.flareBachNo         = 0

		# DESTROY 
		self.destructionComplete = False
		self.chosenExplosionImg  = gui.smallYellowExplosion
		self.explosion           = imageAnimateAdvanced(self.chosenExplosionImg,0.1)
		self.debris 			 = 0

	
	# MANAGE ACCELLERATION 
	
	def actions(self,gui,game,lv):
		
		# --------BUTTON CONTROLLS
		# LOCKON OFF 
		if(self.lockonActive==False):
			if(self.lockOffMode=='strafing'):
				self.TILTLEFT           = 'J'
				self.TILTRIGHT          = 'K'
				self.SPECIAL            = 'L'
		# LOCKED ON 
		if(self.lockonActive==True):
			self.SHOOTKEY           = 'H'
			self.BOOST_BUTTON       = 'U' 
			self.JINK_BUTTON        = 'K' 
			self.SPECIAL            = 'J'

		# --------GET PRESSED KEYS

		pressedKeys     = [x.upper() for x in gui.input.pressedKeys]


		# --------MOVEMENT LOGIC

		self.classicControls(gui,pressedKeys,lv,game)

		# --------BUILD DETECTION CONE

		self.cone_points = detectionCone(self.x,self.y,gui,-self.facing,cone_length=self.cone_length,cone_angle=self.cone_angle)

		# -------LOCK ON

		enemies = self.detectEnemies(gui,lv,self.cone_points)
		self.lockOn(gui,enemies,game,pressedKeys)


		# ---------MANAGE CAMERA 

		self.camera(gui,lv)



		# ------MANAGE INVINCIBILITY DURATION

		self.setInvincible(game)

		# ------KILL ME
		
		if(self.hp<1):
			killme(self,lv,killMesssage=' collided with enemy.',printme=True)

		# ---------SHOOT

		self.firing = False
		if(self.SHOOTKEY in pressedKeys):
			self.shoot(game,lv,gui)
		if(self.SPECIAL in pressedKeys):
			self.launchMissiles(game,lv,gui,enemies)

	def detectEnemies(self,gui,lv,cone_points):

		# Create a Rect object for the cone of vision
		cone_rect = pygame.Rect(min([p[0] for p in cone_points]), min([p[1] for p in cone_points]), max([p[0] for p in cone_points]) - min([p[0] for p in cone_points]), max([p[1] for p in cone_points]) - min([p[1] for p in cone_points]))

		detectEnemies = []
		for enemy in lv.enemyList:
			if(onScreen(enemy.x,enemy.y,enemy.w,enemy.h,gui)):
				if cone_rect.collidepoint((enemy.x, enemy.y)):
					distance = getDistance(self.x,self.y,enemy.x,enemy.y)
					detectEnemies.append((enemy,int(distance)))

		# RETURN ENEMY LIST IN ORDER OF NEAREST
		sorted_list  = sorted(detectEnemies, key=lambda x: x[1])
		enemies      = [tuple[0] for tuple in sorted_list]

		return(enemies)

	def lockOn(self,gui,enemies,game,pressedKeys):

		
		# INCREMENT LOCKON STATE 
		
		if(gui.input.returnedKey.upper()==self.ENABLE_LOCKON_BUTTON):
			self.lockonActive = not self.lockonActive
			if(self.lockonActive==False):
				self.lockedOn = False
		

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
					
					# IS NOT ALREADY CHOSEN
					if(self.lockedEnemy==None):

						# ------RENDER LOCKON AROUND POTENTIAL ENEMY

						complete,blitPos = self.lockOnImage.animate(gui,str(enemies[0].id) + str(self.lockedOn),[lx,ly],game,repeat=False)

						# ------ IF YOU CHOSE TO LOCKON TO THIS ENEMY
						# ALWAYS LOCKON
						self.lockedOn     = True
						self.lockedEnemy  = enemies[self.lockonIndex]

						"""
						if(gui.input.returnedKey.upper()=='L'):
							self.lockedOn     = True
							self.lockedEnemy  = enemies[self.lockonIndex]
						"""
					
					# USER SWITCHES LOCKON TO NEXT ENEMY
					elif(self.lockedEnemy):
						if(gui.input.returnedKey.upper()== self.JINK_BUTTON):
							self.switchedLockon = True
							if(self.lockonIndex+1 <len(enemies)):
								self.lockonIndex += 1
								self.lockedEnemy  = enemies[self.lockonIndex]
							else:
								self.lockonIndex = 0
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
				complete= self.lockOnImage.animateNoRotation(gui,str(self.lockedEnemy.id) + str(self.lockedOn),[lx-gui.camX,ly-gui.camY],game,repeat=False)
				
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








	# CALLED BY allyActions/enemyActions
	def shoot(self,game,lv,gui, bulletColour=(255,177,42)):

		self.firing = True

		# BULLET DELAY TIMER
		shotAvailable = self.bulletTimer.stopWatch(self.shootDelay,'player shoot', str(self.id + self.bulletsFired), game,silence=True)
		
		# IF SHOOT CRITEREA MET,
		if((shotAvailable and self.blitPos!=None)):

			if(self.shotType=='doublePellet'):
				self.bulletsFired +=1
				# ADDS BULLET TO BULLET LIST
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(bullet(gui,self.blitPos['leftTop'][0]+ gui.camX,self.blitPos['leftTop'][1]+ gui.camY,bid,self.classification, self.facing,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))
				
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



			else:
				self.bulletsFired +=1
				# ADDS BULLET TO BULLET LIST
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(bullet(gui,self.blitPos['midTop'][0] + gui.camX,self.blitPos['midTop'][1]+ gui.camY,bid,self.classification, self.facing,self.shotType, speed=self.maxSpeed + self.bulletAttrs[self.shotType]['speed'],damage=self.bulletAttrs[self.shotType]['damage'],colour=bulletColour))

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


	def setInvincible(self,game):
		
		if(self.invincible):
			invincibleTimer = self.invincibleTimer.stopWatch(self.invincibleDelay,str(self.id + self.hp),self,game,silence=True)
			if(invincibleTimer):
				self.invincible = False


	def classicControls(self,gui,pressedKeys,lv,game):

		self.accellerating = False # ACCELELRATION FLAG
		self.vel_x = 0
		self.vel_y = 0
		self.maxSpeed = self.maxSpeedDefault

		if(self.lockonActive):
			self.lockonControl(gui,pressedKeys,lv,game)
		if(self.lockonActive==False):
			self.freeRoamControl(gui,pressedKeys,lv,game)


		self.standardControls(gui,pressedKeys,lv,game)
		self.flares(gui,pressedKeys,lv,game)


	def lockonControl(self,gui,pressedKeys,lv,game):

		self.hp = 10000000
		# ------MOVEMENT
		self.accellerating= False # ACCELELRATION FLAG

		# -------LOCKED ON MOVEMENT
		if(self.lockedOn):

			# UPDATE INIT FACING FOR NEW LOCKON EVENT
			if(self.initLockonFacing==None or self.switchedLockon):
				self.initLockonFacing = self.facing

			self.maxSpeed = 5
			
			# THE RELATIVE COMPONENTS NEEDED TO GO FORWARD, NOT ACTUAL X,Y VELS
			vel_x = self.maxSpeed * math.cos(math.radians(360-self.facing-90))
			vel_y = self.maxSpeed * math.sin(math.radians(360-self.facing-90))

			vx = self.maxSpeed * math.cos(math.radians(360-self.facing))
			vy = self.maxSpeed * math.sin(math.radians(360-self.facing))
			
			# RIGHT    - TURN IF JINK BUTTON HELD
			if('D' in pressedKeys and self.JINK_BUTTON in pressedKeys):
				self.facing -= 3
			# OTHER WISE MOVE IN JINK FASHION
			if('D' in pressedKeys):
				self.x  += 0.8*self.maxSpeed

			# LEFT     - TURN IF JINK BUTTON HELD
			if('A' in pressedKeys and self.JINK_BUTTON in pressedKeys):
				self.facing += 3
			# OTHER WISE MOVE IN JINK FASHION
			if('A' in pressedKeys):
				self.x  -= 0.8*self.maxSpeed
			
			# UP
			if('W' in pressedKeys ):
				#self.x += vx
				self.y     -= 0.6*self.maxSpeed # MOVES UP/DOWN REL
				self.vel_y -= 0.8*self.maxSpeed # ALSO MOVES RADIALLY

			# DOWN
			if('S' in pressedKeys):	
				#self.x -= vel_x
				self.y     += 0.6*self.maxSpeed
				self.vel_y += 0.8*self.maxSpeed
		
		# ---------JINK FOR LOCKON MODE NOT LOCKED ON

		if((self.JINK_BUTTON in pressedKeys or self.firing) and not self.lockedOn):
			self.maxSpeed = 5
			vel_x = self.maxSpeed * math.cos(math.radians(360-self.facing-90))
			vel_y = self.maxSpeed * math.sin(math.radians(360-self.facing-90))
			
			if('D' in pressedKeys):
				if('J' in pressedKeys and self.firing):
					self.facing +=0.6
				
				self.x -= vel_x
				self.y -= vel_y

			if('A' in pressedKeys):
				if('J' in pressedKeys and self.firing):
					self.facing -=0.6
				self.x += vel_x
				self.y += vel_y
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
			
			# This ensures the left/right strafing line doesn't keep changing witj angle
			if(self.initJinkFacing==None):
				self.initJinkFacing = self.facing

			invert = 1
			if(self.initJinkFacing>220 and self.initJinkFacing<330):
				invert = -1
			

			self.maxSpeed       = 5
			self.maxStrafeSpeed = 7
			sprayRange          = 80


			# FOR MOVING HORIZONTALLY
			vel_x = self.maxStrafeSpeed * math.cos(math.radians(360-self.initJinkFacing-90))
			vel_y = self.maxStrafeSpeed * math.sin(math.radians(360-self.initJinkFacing-90))
			
			# RIGHT
			if('D' in pressedKeys):
				self.x -= vel_x * invert
				self.y -= vel_y * invert

				
				if(self.lockOffMode=='spinning'):
					if(self.SHOOTKEY in pressedKeys and self.JINK_BUTTON in pressedKeys):
						self.facing -= 2
			# LEFT
			if('A' in pressedKeys):
				self.x += vel_x * invert
				self.y += vel_y * invert
				
				if(self.lockOffMode=='spinning'):
					if(self.SHOOTKEY in pressedKeys and self.JINK_BUTTON in pressedKeys):
						self.facing += 2

			

			if(self.lockOffMode=='strafing'):
				TILTRIGHT = self.TILTRIGHT
				TILTLEFT = self.TILTLEFT
				if(invert==-1):
					TILTRIGHT = self.TILTLEFT
					TILTLEFT = self.TILTRIGHT

				if(self.SHOOTKEY in pressedKeys and TILTRIGHT in pressedKeys):
					if(self.jinkFacingTotal - 2  > -sprayRange):
						self.jinkFacingTotal -= 2 
						self.facing -= 2 
				
				if(self.SHOOTKEY in pressedKeys and TILTLEFT in pressedKeys):
					if(self.jinkFacingTotal+2  < sprayRange):
						self.jinkFacingTotal += 2 
						self.facing += 2 
					
			
			# UP
			if('W' in pressedKeys ):
				self.speed += 0.7 
				self.accellerating = True

			# DOWN
			if('S' in pressedKeys):
				self.speed -= 0.7 
				self.accellerating = True
		else:
			# RESETS JINK STATE
			self.initJinkFacing = None
			self.jinkFacingTotal = 0


	



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
			if('D' in pressedKeys):
				self.facing -= 3
			if('A' in pressedKeys):
				self.facing += 3



		# ------INCREMENT SHOT TYPE 

		if(gui.input.returnedKey.upper()=='E'):
			nextIndex    = (self.availableWeapons.index(self.shotType) + 1) % len(self.availableWeapons)
			self.shotType = self.availableWeapons[nextIndex]

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

		# UPDATE POSITION
		self.x += int(self.vel_x )
		self.y += int(self.vel_y)

		# SLOWDOWN WHEN NOT ACCELLERATING
		if(self.accellerating==False):
			self.speed = zero(self.speed,self.decelleration)

		# BORDER CLAMP
		if(self.x + self.w > lv.mapw): self.x -= self.maxSpeed
		if(self.x < lv.mapx): self.x += self.maxSpeed
		if(self.y + self.h > lv.maph): self.y -= self.maxSpeed
		if(self.y < lv.mapy): self.y += self.maxSpeed



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
			lv.bulletList.append(flare(gui,self.blitPos['midTop'][0] + gui.camX,self.blitPos['midTop'][1]+ gui.camY,bid,self.classification, wrapAngle(self.facing+random.randrange(35,65)),playerSpeed=self.speed, speed=self.speed,jink='left'))
			
			bid = max(([x.id for x in lv.bulletList]),default=0) + 1
			lv.bulletList.append(flare(gui,self.blitPos['midTop'][0] + gui.camX,self.blitPos['midTop'][1]+ gui.camY,bid,self.classification, wrapAngle(self.facing-random.randrange(35,65)),playerSpeed=self.speed, speed=self.speed,jink='right'))
			
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
			
			self.shadow.animate(gui,'player shadow',[self.shadowPos[0],self.shadowPos[1]],game,rotation=self.facing-90,noseAdjust=True)
			
			if(self.boosting):
				animate,imageParms = self.boostImage.animate(gui,'playerBoosting',[x,y],game,rotation=self.facing-90)
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
				lv.bulletList.append(bullet(gui,self.x + 0.5* self.chosenExplosionImg[0].get_width(),self.y+ 0.5* self.chosenExplosionImg[0].get_height(),bid,'debris',random.randrange(0,360),'debris',speed=10, w=0.05*self.w,h=0.05*self.h,colour=(192,192,192)))
			if(complete):
				self.destructionComplete = True

	def damageAnimation(self,gui,lv,game):
		x,y = self.x - gui.camX,self.y  - gui.camY
		
		if(self.alive==True and onScreen(self.x,self.y,self.w,self.h,gui)):
			complete,imageParms = self.hitAnimation.animate(gui,str(self.name) + ' hit',[x,y],game,rotation=self.facing-90)
			if(complete):
				self.hit = False

