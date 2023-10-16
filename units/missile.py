from utils._utils import stopTimer, imageAnimateAdvanced,darken
from utils.gameUtils import *
from units.ordinance import *
import pygame
import math
import random



"""
1. Go back 3 times self size 
2. Missile light flair
3. Go forward, with accelleration 
4. Emit plumes at this point


"""
class missile():
	def __init__(self,gui,x,y,bid,classification,facing,missileType,playerSpeed=3, speed=3,damage=10,jink='left',lockedOnEnemy=None, source='player'):
		self.x,self.y          = x,y
		self.ox,self.oy        = x,y
		self.id                = bid
		self.classification    = classification
		self.name 			   = 'missile'
		self.ordType           = 'missile'
		self.facing            = facing
		self.defaultSpeed      = speed
		self.speed             = playerSpeed- 3      # INITIALLY 3, WILL BE INCREASED IN ACCEL PHASE
		self.accelleration     = 0.4
		self.damage            = damage
		self.plumeTimer        = stopTimer()
		self.plumeDelay        = 0.02
		self.plumeCreated      = 0
		self.range             = 1.5*gui.w
		self.nukeRange         = 0.7*gui.h
		self.boostPhase        = 'launched'
		self.jink              = jink
		self.burnFrames        = 0 
		self.burnFramesLim     = 20
		self.lockedOnEnemy     = lockedOnEnemy
		self.cumulatedDistance = 0
		self.source 		   = source

		self.missileType     = missileType

		if(self.missileType in ['streaker']):
			self.missileImg      = gui.streakerMissile
			self.missileFrames   = imageAnimateAdvanced(self.missileImg,0.1)
		if(self.missileType in ['streakerGray']):
			self.missileImg      = gui.streakerGray
			self.missileFrames   = imageAnimateAdvanced(self.missileImg,0.1)
		if(self.missileType in ['nuke']):
			self.missileImg      = gui.nukeMissile
			self.missileFrames   = imageAnimateAdvanced(self.missileImg,0.1)


		# NUKE STUFF
		self.bombShockwaveAnimation  = imageAnimateAdvanced(gui.bombShockFrames,0.05)
		self.bombBlastAnimation      = imageAnimateAdvanced(gui.bombBlastFrames,0.05)


		self.w,self.h       = self.missileImg[0].get_width(), self.missileImg[0].get_height()

		# FOR TERMINATING SELF
		self.destructionComplete = False
		self.alive               = True
		self.debris              = 0
		self.explosion           = imageAnimateAdvanced(gui.missileExplosion,0.1)


	def move(self,gui,lv,game):
		vel_x = self.speed * math.cos(math.radians(360-self.facing))
		vel_y = self.speed * math.sin(math.radians(360-self.facing))
		self.cumulatedDistance += math.sqrt(vel_x**2 + vel_y**2)


		# --------LAUNCHED BY PLAYER 

		if(self.missileType =='streaker' and self.source=='player'):
			# MISSILES GO BACKWARDS INITIALLY
			if(self.boostPhase=='launched'):
				
				self.x += vel_x 
				self.y += vel_y

				if(self.jink=='left'):
					self.x += 3 * math.cos(math.radians(360-self.facing-90))
					self.y += 3 * math.sin(math.radians(360-self.facing-90))
				if(self.jink=='right'):
					self.x += 3 * math.cos(math.radians(360-self.facing+90))
					self.y += 3 * math.sin(math.radians(360-self.facing+90))

				distanceTravelled = self.getRelativeDistanceTravelled()
				if(abs(distanceTravelled)> 10*self.w):
					self.boostPhase='accellerating'

			if(self.boostPhase=='accellerating'):
				self.x += vel_x 
				self.y += vel_y
				self.speed += self.accelleration
				if(self.speed>=self.defaultSpeed):
					self.speed = self.defaultSpeed

				# -----PLUME DESIGN 

				plumeReady = self.plumeTimer.stopWatch(self.plumeDelay,'missilePlume', str(self.plumeCreated)  + 'plume', game,silence=True)
				if(plumeReady):
					self.plumeCreated +=1

					vel_x = -40 * math.cos(math.radians(360-self.facing)) 
					vel_y = -40 * math.sin(math.radians(360-self.facing))
					# UPDATE POSITION
					plumeX = self.x + int(vel_x )
					plumeY = self.y + int(vel_y)

					lv.plumeList.append(plume(gui,self.plumeCreated,plumeX,plumeY,self.facing))


				# -----HOMING IN ON THE ENEMY
				if(self.lockedOnEnemy!=None and self.missileType =='streaker'):
					angleDiffToEnemy,DistanceToEnemy,enemyTargetAngle = angleToTarget(self,self.x,self.y, self.lockedOnEnemy.x , self.lockedOnEnemy.y)
					faceTarget(self,angleDiffToEnemy, turnIcrement=2)	

		
		# --------NUKE		

		if(self.missileType =='nuke'):
			# MISSILES GO BACKWARDS INITIALLY
			if(self.boostPhase=='launched'):
				
				self.x += vel_x 
				self.y += vel_y

				distanceTravelled = self.getRelativeDistanceTravelled()
				if(abs(distanceTravelled)> 10*self.w):
					self.boostPhase='accellerating'

			if(self.boostPhase=='accellerating'):
				self.x += vel_x 
				self.y += vel_y
				self.speed += self.accelleration
				if(self.speed>=self.defaultSpeed):
					self.speed = self.defaultSpeed

				# -----PLUME DESIGN 

				plumeReady = self.plumeTimer.stopWatch(self.plumeDelay,'missilePlume', str(self.plumeCreated)  + 'plume', game,silence=True)
				if(plumeReady):
					self.plumeCreated +=1

					vel_x = -40 * math.cos(math.radians(360-self.facing)) 
					vel_y = -40 * math.sin(math.radians(360-self.facing))
					# UPDATE POSITION
					plumeX = self.x + int(vel_x )
					plumeY = self.y + int(vel_y)

					lv.plumeList.append(plume(gui,self.plumeCreated,plumeX,plumeY,self.facing))

			# CHECK IF DISTANCE EXCEEDS RANGE
			if(abs(self.cumulatedDistance)> self.nukeRange):
				self.killSelf(lv,killMessage=' detonating Nuke')



		# --------LAUNCHED BY ENEMY 

		if(self.missileType in ['streaker','streakerGray']  and self.source=='enemy'):
			# MISSILES GO BACKWARDS INITIALLY
			if(self.boostPhase=='launched'):
				if(self.jink=='left'):
					self.x += 2*self.w * math.cos(math.radians(360-self.facing-90))
					self.y += 2*self.w * math.sin(math.radians(360-self.facing-90))
				if(self.jink=='right'):
					self.x += 2*self.w * math.cos(math.radians(360-self.facing+90))
					self.y += 2*self.w * math.sin(math.radians(360-self.facing+90))
				if(self.jink=='farleft'):
					self.x += 4*self.w * math.cos(math.radians(360-self.facing-90))
					self.y += 4*self.w * math.sin(math.radians(360-self.facing-90))
				if(self.jink=='farright'):
					self.x += 4*self.w * math.cos(math.radians(360-self.facing+90))
					self.y += 4*self.w * math.sin(math.radians(360-self.facing+90))
				# SKIP LAUNCH PHASE
				self.boostPhase='accellerating'

			if(self.boostPhase=='accellerating'):
				self.x += vel_x 
				self.y += vel_y
				self.speed += self.accelleration
				if(self.speed>=self.defaultSpeed):
					self.speed = self.defaultSpeed

				# -----PLUME DESIGN 

				plumeReady = self.plumeTimer.stopWatch(self.plumeDelay,'missilePlume', str(self.plumeCreated)  + 'plume', game,silence=True)
				if(plumeReady):
					self.plumeCreated +=1

					vel_x = -40 * math.cos(math.radians(360-self.facing)) 
					vel_y = -40 * math.sin(math.radians(360-self.facing))
					# UPDATE POSITION
					# (self.x + velocity adjusted a bit)
					plumeX = self.x + int(self.speed * math.cos(math.radians(360-self.facing+10)) )
					plumeY = self.y + int(self.speed * math.sin(math.radians(360-self.facing+10)))

					lv.plumeList.append(plume(gui,self.plumeCreated,plumeX,plumeY,self.facing))


				# -----HOMING IN ON THE ENEMY
				if(self.lockedOnEnemy!=None and self.missileType in ['streaker','streakerGray']):
					angleDiffToEnemy,DistanceToEnemy,enemyTargetAngle = angleToTarget(self,self.x,self.y, self.lockedOnEnemy.x , self.lockedOnEnemy.y)
					faceTarget(self,angleDiffToEnemy, turnIcrement=2)



		self.rangeManager(gui,lv)

		# ALLOW MISSILE TO BE TAKEN OUT BY BULLET
		for bullet in lv.bulletList:
			if(bullet.classification!=self.classification and bullet.classification!='debris' and self.missileType!='nuke'):
				if(collidesWithHitBox(bullet,self)):
					# destroy self
					self.killSelf(lv,killMessage=str(self.missileType) + ' struck by bullet')
					# destroy attacking bullet
					if(bullet.ordType=='bullet'):
						bullet.killSelf(lv,killMessage='struck by missile',printme=True)



		
		# IGNORING ON SCREEN, TERMINATES WITH RANGE
		#if(not onScreen(self.x,self.y,self.w,self.h,gui)): self.killSelf(lv,killMessage='bullet out of screen')

	
	def getRelativeDistanceTravelled(self):
		xDelta        =  self.ox - self.x
		yDelta        =  self.oy - self.y
		distance = math.sqrt((xDelta)**2+(yDelta)**2)
		return(distance)

	def rangeManager(self,gui,lv):
		
		# CHECK IF DISTANCE EXCEEDS RANGE
		if(abs(self.cumulatedDistance)> self.range):
			self.killSelf(lv,killMessage=' Missile fuel burnout OUT OF RANGE')





	# MANAGE BULLET COLLISION WITH SELF 

	def bulletCollides(self,target,gui,lv):
		# IF BULLET CLASSIFICATION IS NOT THE SAME AS TARGETS 
		if(self.classification!=target.classification and self.classification!='debris' and self.missileType!='nuke'):
			
			target.hp -= self.damage
			target.hit = True
			self.killSelf(lv,killMessage='struck enemy')

			# ----KILL THE ENEMY 
			if(target.hp<=0):
				target.alive = False
				killme(target,lv,killMesssage=' struck by enemy fire.',printme=True)

	# ENSURE MISSILE DIES. 

	def killSelf(self,lv,killMessage=None,printme=False):
		for i in lv.bulletList:
			if(self.id==i.id):
				self.alive = False
				lv.bulletList.remove(self)
				lv.deadList.append(self)
				if(printme):
					print("Missile destroyed : " + killMessage + ' ' + str(self.classification))


	# ONLY DRAW IF IN BOUNDARY

	def drawSelf(self,gui,game,lv):
		x,y = self.x -gui.camX, self.y -gui.camY
		
		if(self.missileType in ['streaker','streakerGray','nuke']):

			if(self.boostPhase=='launched'):
				self.missileFrames.currentFrame = 0	
			if(self.boostPhase=='accellerating'):
				if(self.burnFrames<self.burnFramesLim):
					self.missileFrames.currentFrame = 3
					self.burnFrames +=1

			complete = self.missileFrames.animateLowCompute(gui,'missile burn',[x-0.5*self.missileImg[0].get_width(),y],game,rotation=self.facing-90)


	def animateDestruction(self,gui,lv,game):
		x,y = self.x - gui.camX,self.y  - gui.camY

		
		if(self.destructionComplete==False and self.alive==False and self.missileType=='nuke'):
			complete = self.nukeDetonate(gui,lv,game)
			if(complete):
				self.destructionComplete = True
				lv.deadList.remove(self)

		elif(self.destructionComplete==False and self.alive==False):
			complete,blitPos = self.explosion.animate(gui,str(str(self.id) +' missile explosion'),[x,y],game)
			bid = max(([x.id for x in lv.bulletList]),default=0) + 1


			if(self.debris<=12):
				self.debris +=1
				# ADDS DEBRIS TO TO LIST
				lv.bulletList.append(bullet(gui,self.x + 0.5* self.w,self.y+ 0.5* self.h,bid,'debris',random.randrange(0,360),'debris',speed=10, w=0.05*self.w,h=0.05*self.h,colour=(192,192,192)))
			if(complete):
				self.destructionComplete = True
				lv.deadList.remove(self)



	def nukeDetonate(self,gui,lv,game):

		bombW,bombH =gui.bombShockFrames[-1].get_width(),gui.bombShockFrames[-1].get_height()
		shockFinished,blitPos = self.bombShockwaveAnimation.animate(gui, 'playerBomb shock' + str(lv.player.nukesDropped), [(self.x - 0.5* bombW -gui.camX), (self.y - 0.5*bombH - gui.camY)] ,game,repeat=False)
		if(shockFinished):
			blastFinished,blitPos = self.bombBlastAnimation.animate(gui,'playerBomb blast' + str(lv.player.nukesDropped),[(self.x- 0.5*bombW - gui.camX),(self.y - 0.5*bombH -gui.camY)],game)
			if(blastFinished):
				lv.player.nukesDropped += 1
				# resetting shockwave
				self.bombShockwaveAnimation.reset()
				self.bombBlastAnimation.reset()
				return(True)


			# DESTROY ENEMY AFTER SHOCK WAVE
			for enemy in lv.enemyList:
				if(collidesWithObjectLess(self.x-0.5*bombW,self.y-0.5*bombH,bombW,bombH,enemy)):
					# IF BULLET CLASSIFICATION IS NOT THE SAME AS TARGETS 
					if(enemy.classification!='debris'):

						# IF THE TARGET ISN'T INVINCIBLE 
						enemy.hp -= self.damage
						enemy.hit = True

						# ----KILL THE ENEMY 
						if(enemy.hp<=0):
							enemy.alive = False
							killme(enemy,lv,killMesssage=' killed by bomb.',printme=True)





		return(False)


class plume():
	def __init__(self,gui,_id,x,y,facing,imageType=None):
		self.id              = _id
		self.x               = x
		self.y               = y
		self.plumeImg        = gui.missilePlume
		self.plumeFrames     = imageAnimateAdvanced(self.plumeImg,0.2)
		self.w,self.h        = self.plumeImg[0].get_width(),self.plumeImg[0].get_height()
		self.facing          = facing

	def drawSelf(self,gui,game,lv):
		x,y = self.x -gui.camX, self.y -gui.camY
		plumeOnScreen = onScreen(self.x,self.y,self.w,self.h,gui)

		complete = self.plumeFrames.animateLowCompute(gui,'plume Frames',[x,y],game,rotation=self.facing-90,skipBlit= not plumeOnScreen)
		if(complete):
			lv.plumeList.remove(self)






