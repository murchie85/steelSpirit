from units.parent import *
from utils.gameUtils import *
from utils._utils import imageAnimateAdvanced,loadingBarClass
from units.turretObject import *
import pygame




class frigate(parent):
	def __init__(self,_id,gui,lv,x=None,y=None):
		super().__init__(gui)
		# MAIN OVERRIDES 
		self.id             = _id
		self.name           = 'frigate'
		self.kind           = 'bigBoat'
		self.images         = imageAnimateAdvanced(gui.frigate,0.2)
		
		self.turretImage        = imageAnimateAdvanced(gui.frigateTurret,0.2)
		self.turretHitImg       = imageAnimateAdvanced(gui.frigateTurretHit,0.2)
		self.turretRemainsImg   = imageAnimateAdvanced(gui.frigateTurretRemains,0.2)
		

		self.multiTimage         = imageAnimateAdvanced(gui.frigateMulti,0.2)
		self.multiTHitImg        = imageAnimateAdvanced(gui.frigatMultiHit,0.2)
		self.multiTRemainsImg    = imageAnimateAdvanced(gui.frigateMultiRemains,0.2)
		self.smokeAnimation       = imageAnimateAdvanced(gui.medSmoke,0.2)
		self.smokeAnimation2      = imageAnimateAdvanced(gui.medSmoke,0.2)
		self.smokeAnimation3      = imageAnimateAdvanced(gui.medSmoke,0.2)



		self.shadow         = imageAnimateAdvanced(gui.greenTankShadow,0.2)
		if(x!=None): self.x = x
		if(y!=None): self.y = y
		self.w              = int(gui.frigate[0].get_width())
		self.h              = int(gui.frigate[0].get_height())
		self.hitBox         = [self.x+1/8*self.w,self.y+0.25*self.h,6/8*self.w,0.53*self.h]
		
		print(self.facing)
		self.turretOne       = turret(createFid(lv),self.classification, gui, self.x,self.y+0.05*self.h,self.turretImage,self.turretHitImg,self.turretRemainsImg,self.facing,hp=300,shootRange=0.8*gui.h,bulletType='lightRedPlasmaBall')
		self.turretTwo       = turret(createFid(lv),self.classification, gui, self.x,self.y +0.74*self.h,self.turretImage,self.turretHitImg,self.turretRemainsImg,self.facing,hp=200,shootRange=0.8*gui.h,bulletType='lightRedPlasmaBall')
		self.multiTurret     = turret(createFid(lv),self.classification, gui, self.x + 1/8*self.w,self.y + 0.48*self.h,self.multiTimage,self.multiTHitImg,self.multiTRemainsImg,self.facing,shotType='trippleStaggered',hp=500,shootRange=0.9*gui.h,shootDelay=0.7)
		


		self.turretOne.range  = 0.8*gui.h
		self.turretTwo.range  = 0.8*gui.h

		self.multiFacing       = self.facing


		self.multiTx        = self.x + 1/8*self.w
		self.multiTy        = self.y + 0.48*self.h
		
		# HIT IMAGE
		self.hitImage         = gui.frigateHit
		self.hitAnimation     = imageAnimateAdvanced(self.hitImage,0.2)
		self.hitsTaken        = 0

		self.coolDown          = False
		self.coolDownAnimation = imageAnimateAdvanced(self.hitImage[::-1],0.1)

		# REMAINS IMAGE 
		self.remainsAnimation = imageAnimateAdvanced(gui.frigateRemains,0.2)

		# HEALTHBAR 
		self.healthBar      = loadingBarClass(self.w,0.2*self.h,(80,220,80),(220,220,220),(0,0,200))
		self.blitPos        = None
		
		self.turretPos      = None
		self.turret2Pos     = None
		self.multiPos       = None

		self.state             = 'patrol'
		self.patrolLocations   = [(self.x,self.y),(self.x+700,self.y),(self.x+700,self.y+200),(self.x,self.y+200)] 
		self.currentLocIndex   = 0


		# CLASS OVERRIDES
		self.hp              = 1000
		self.defaultSpeed    = 1
		self.maxSpeed        = 1
		self.maxSpeedDefault = 1

		# ENEMY COORDS 

		self.angleDiffToEnemy = 0
		self.DistanceToEnemy  = 50000
		self.enemyTargetAngle = 0
		self.defenceSector    = self.patrolLocations[0]

		# SHOOT 
		self.shootDelay           = 0.3                   # BUFF
		self.bulletsFired         = 0

		self.multiTimer1           = stopTimer()           # BUFF
		self.multiTimer2           = stopTimer()           # BUFF
		self.multiTimer3           = stopTimer()           # BUFF
		self.multiDelay           = 0.1
		self.multiFired           = 0

		self.facingSet            = False


	# AI LOGIC
	def actions(self,gui,game,lv):

		if(self.facing==0 and not self.facingSet):
			self.facingSet = True
			self.turretOne       = turret(createFid(lv),self.classification, gui, self.x - 10/8*self.w,self.y+0.4*self.h,self.turretImage,self.turretHitImg,self.turretRemainsImg,self.facing,hp=300,shootRange=0.8*gui.h,bulletType='lightRedPlasmaBall',centerOfRotation=(0.4,0.5))
			self.turretTwo       = turret(createFid(lv),self.classification, gui, self.x + 9/8*self.w,self.y +0.36*self.h,self.turretImage,self.turretHitImg,self.turretRemainsImg,self.facing,hp=200,shootRange=0.8*gui.h,bulletType='lightRedPlasmaBall',centerOfRotation=(0.4,0.5))
			self.multiTurret     = turret(createFid(lv),self.classification, gui, self.x - 3/8*self.w,self.y + 0.4*self.h,self.multiTimage,self.multiTHitImg,self.multiTRemainsImg,self.facing,shotType='trippleStaggered',hp=500,shootRange=0.9*gui.h,shootDelay=0.7)
			


		# ENSURE VECHICLE DOESN'T EXCEED BOUNDARIES
		self.stayOnField(lv)

		# keep turret udpated with current pos
		#self.turretOneCoords = self.x,self.y+0.05*self.h


		self.turretOne.actions(gui,game,lv,self.facing)
		self.turretTwo.actions(gui,game,lv,self.facing)
		self.multiTurret.actions(gui,game,lv,self.facing)

		if(self.turretOne.alive==False and self.turretTwo.alive==True):

			self.hitBox         = [self.x+1/8*self.w,self.y,6/8*self.w,0.78*self.h]
		if(self.turretOne.alive==True and self.turretTwo.alive==False):
			#self.hitBox         = [self.x+1/8*self.w,self.y+0.25*self.h,6/8*self.w,0.53*self.h]
			self.hitBox         = [self.x+1/8*self.w,self.y+0.25*self.h,6/8*self.w,self.h-0.25*self.h]
		if(self.turretOne.alive==False and self.turretTwo.alive==False):
			self.hitBox = [self.x+1/8*self.w,self.y,6/8*self.w,self.h]

		#self.turretOne.x, self.turretOne.y = self.x,self.y+0.05*self.h
		#self.multiTurret.x, self.multiTurret.y = self.x + 1/8*self.w, self.y + 0.48*self.h
		





	# DRAW REMNANTS AFTER BEING DESTROYED
	def drawRemains(self,gui,lv,game):
		x,y = self.x - gui.camX,self.y  - gui.camY

		# *******BE CAREFUL ABOUNT ON SCREEN
		if(self.alive==False and onScreen(self.x,self.y,self.w,self.h,gui)):
			self.remainsAnimation.animate(gui,str('smouldering frigate remains'),[x,y],game,rotation=self.facing-90,repeat=True)

			self.smokeAnimation.animate(gui,str('smouldering turret remains smoke'),[x + 0.3*self.w,y + 0.1*self.h],game,rotation=self.facing-90,repeat=True)
			self.smokeAnimation2.animate(gui,str('smouldering turret remains smoke'),[x + 0.42*self.w,y + 0.5*self.h],game,rotation=self.facing-270,repeat=True)
			self.smokeAnimation3.animate(gui,str('smouldering turret remains smoke'),[x + 0.55*self.w,y + 0.75*self.h],game,rotation=self.facing,repeat=True)

	# DRAW SELF LOGIC

	def drawSelf(self,gui,game,lv):
		x,y = self.x - gui.camX,self.y  - gui.camY
		if(self.alive==True and onScreen(self.x,self.y,self.w,self.h,gui) and not self.hit):
			animate,self.blitPos     = self.images.animate(gui,'frigate ' + str(self.id),[x,y],game,rotation=self.facing-90)
			
			# TEST HITBOX
			#pygame.draw.rect(gui.screen,(0,0,150),(self.hitBox[0]-gui.camX,self.hitBox[1]-gui.camY,self.hitBox[2],self.hitBox[3]))

		if(self.hit):

			x,y = self.x - gui.camX,self.y  - gui.camY
			
			if(self.alive==True and onScreen(self.x,self.y,self.w,self.h,gui)):
				
				complete,imageParms            = self.hitAnimation.animate(gui,str(self.hitsTaken) + ' hit',[x,y],game,rotation=self.facing-90,repeat=True)

				if(complete):
					self.hitAnimation.reset()
					self.hit = False
					self.hitsTaken +=1
					self.coolDown = True


		if(self.coolDown and not self.hit):

			x,y = self.x - gui.camX,self.y  - gui.camY
			
			if(self.alive==True and onScreen(self.x,self.y,self.w,self.h,gui)):
				
				complete,imageParms            = self.coolDownAnimation.animate(gui,'cooldown',[x,y],game,rotation=self.facing-90,repeat=True)

				if(complete):
					self.coolDownAnimation.reset()
					self.coolDown =False


	

