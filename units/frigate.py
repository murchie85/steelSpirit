from units.parent import *
from utils.gameUtils import *
from utils._utils import imageAnimateAdvanced,loadingBarClass
from units.turretObject import *
import pygame




class frigate(parent):
	def __init__(self,_id,gui,lv,x=None,y=None):
		super().__init__(gui)
		#self.facing+=90
		self.facing         = wrapAngle(self.facing)
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


		# ORIGIN POINTS FOR TURRETS
		self.txOrigin,self.tyOrigin = self.x + 8/8*self.w,self.y+0.15*self.h
		self.tx2Origin,self.ty2Origin = self.x + 8/8*self.w,self.y+0.88*self.h
		self.mtxOrigin,self.mtyOrigin = self.x + 10/8*self.w,self.y+0.62*self.h


		self.tx,self.ty       = self.txOrigin,self.tyOrigin
		self.tx2,self.ty2     = self.tx2Origin,self.ty2Origin
		self.mtx,self.mty     = self.mtxOrigin,self.mtyOrigin


		# SWAP WIDTH/HEIGHT
		if(self.facing==90 or self.facing==270):
			w,h = self.w,self.h
			self.w  = h
			self.h = w
		self.hitBox         = [self.x+1/8*self.w,self.y+0.25*self.h,6/8*self.w,0.53*self.h]
		

		self.turretFids       = [createFid(lv),createFid(lv),createFid(lv)]
		self.turretOne        = turret(self.turretFids[0],self.classification, gui, self.tx,self.ty ,self.turretImage,self.turretHitImg,self.turretRemainsImg,self.facing,hp=300,shootRange=0.8*gui.h,bulletType='lightRedPlasmaBall')
		self.turretTwo        = turret(self.turretFids[1],self.classification, gui, self.tx2,self.ty2,self.turretImage,self.turretHitImg,self.turretRemainsImg,self.facing,hp=200,shootRange=0.8*gui.h,bulletType='lightRedPlasmaBall')
		self.multiTurret      = turret(self.turretFids[2],self.classification, gui, self.mtx,self.mty,self.multiTimage,self.multiTHitImg,self.multiTRemainsImg,self.facing,shotType='trippleStaggered',hp=500,shootRange=0.9*gui.h,shootDelay=0.7)
		
		lv.enemyComponentList.append(self.turretOne)
		lv.enemyComponentList.append(self.turretTwo)
		lv.enemyComponentList.append(self.multiTurret)

		self.turretOne.range  = 0.8*gui.h
		self.turretTwo.range  = 0.8*gui.h

		
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


	# AI LOGIC
	def actions(self,gui,game,lv):


		if(gui.input.returnedKey.upper()=='C'): 
			self.facing+= 45
			self.facing = wrapAngle(self.facing)
			facingAngle = self.facing

		self.turretOne.x,self.turretOne.y     = self.tx, self.ty
		self.turretTwo.x,self.turretTwo.y     = self.tx2, self.ty2
		self.multiTurret.x,self.multiTurret.y = self.mtx, self.mty

		# ENSURE VECHICLE DOESN'T EXCEED BOUNDARIES
		self.stayOnField(lv)



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

		if(self.turretOne.alive==False):
			if(self.turretOne in lv.enemyComponentList):
				lv.enemyComponentList.remove(self.turretOne)
		if(self.turretTwo.alive==False):
			if(self.turretTwo in lv.enemyComponentList):
				lv.enemyComponentList.remove(self.turretTwo)
		if(self.multiTurret.alive==False):
			if(self.multiTurret in lv.enemyComponentList):
				lv.enemyComponentList.remove(self.multiTurret)






	# DRAW REMNANTS AFTER BEING DESTROYED
	def drawRemains(self,gui,lv,game):
		x,y = self.x - gui.camX,self.y  - gui.camY

		# *******BE CAREFUL ABOUNT ON SCREEN
		if(self.alive==False and onScreen(self.x,self.y,self.w,self.h,gui)):
			self.remainsAnimation.animate(gui,str('smouldering frigate remains'),[x,y],game,rotation=self.facing,repeat=True,centerOfRotation=(0,0))

			self.smokeAnimation.animate(gui,str('smouldering turret remains smoke'),[x + 0.3*self.w,y + 0.1*self.h],game,rotation=self.facing-90,repeat=True)
			self.smokeAnimation2.animate(gui,str('smouldering turret remains smoke'),[x + 0.42*self.w,y + 0.5*self.h],game,rotation=self.facing-270,repeat=True)
			self.smokeAnimation3.animate(gui,str('smouldering turret remains smoke'),[x + 0.55*self.w,y + 0.75*self.h],game,rotation=self.facing,repeat=True)

		
		# REMOVE TURRETS IF I DIE
		if(self.alive==False):
			for i in lv.enemyComponentList:
				if(i.name=='turret'):
					if(i.id in self.turretFids):
						print('removing')
						lv.enemyComponentList.remove(i)

			
			if(self.turretOne.alive):
				killme(self.turretOne,lv)
			if(self.turretTwo.alive):
				killme(self.turretTwo,lv)
			if(self.multiTurret.alive):
				killme(self.multiTurret,lv)
		





	# DRAW SELF LOGIC

	def drawSelf(self,gui,game,lv):
		x,y = self.x - gui.camX,self.y  - gui.camY
		if(self.alive==True and not self.hit and not self.coolDown):

			# NEEDS FIXING
			#onScreen(self.x,self.y,self.w,self.h,gui)
			
			#animate,self.blitPos     = self.images.animate(gui,'frigate ' + str(self.id),[x,y],game,rotation=self.facing-90)
			rotatedFrigateImage    = pygame.transform.rotate(gui.frigate[0], self.facing)
			pivot                  = pygame.math.Vector2(self.x + gui.frigate[0].get_width(), self.y + 0.5*gui.frigate[0].get_height())
			new_pivot              = pygame.math.Vector2(self.x + 0.5 * rotatedFrigateImage.get_width(), self.y + 0.5 * rotatedFrigateImage.get_height())
			# RECALCULATING TURRET 1 POSITION
			if(self.turretOne.alive):
				point             = pygame.math.Vector2(self.txOrigin,self.tyOrigin)
				rotated_point     = (point - pivot).rotate(-self.facing) + new_pivot
				self.tx,self.ty   = rotated_point.x-0.5*self.turretOne.w, rotated_point.y-0.5*self.turretOne.h

			if(self.turretTwo.alive):
				point             = pygame.math.Vector2(self.tx2Origin,self.ty2Origin)
				rotated_point     = (point - pivot).rotate(-self.facing) + new_pivot
				self.tx2,self.ty2 = rotated_point.x-0.5*self.turretTwo.w, rotated_point.y-0.5*self.turretTwo.h

			if(self.multiTurret.alive):
				point             = pygame.math.Vector2(self.mtxOrigin,self.mtyOrigin)
				rotated_point     = (point - pivot).rotate(-self.facing) + new_pivot
				self.mtx,self.mty = rotated_point.x-0.5*self.multiTurret.w, rotated_point.y-0.5*self.multiTurret.h

			
			#pygame.draw.circle(gui.screen, (200,100,0), (self.tx-gui.camX,self.ty-gui.camY), 10, 0)
			gui.screen.blit(rotatedFrigateImage ,[x,y])

			# TEST HITBOX
			#pygame.draw.rect(gui.screen,(0,0,150),(x,y,rotatedFrigateImage.get_width(),rotatedFrigateImage.get_height()))




		if(self.hit):

			x,y = self.x - gui.camX,self.y  - gui.camY
			
			if(self.alive==True and onScreen(self.x,self.y,self.w,self.h,gui)):
				
				complete,imageParms            = self.hitAnimation.animate(gui,str(self.hitsTaken) + ' hit',[x,y],game,rotation=self.facing,repeat=True,centerOfRotation=(0,0))

				if(complete):
					self.hitAnimation.reset()
					self.hit = False
					self.hitsTaken +=1
					self.coolDown = True


		if(self.coolDown and not self.hit):

			x,y = self.x - gui.camX,self.y  - gui.camY
			
			if(self.alive==True and onScreen(self.x,self.y,self.w,self.h,gui)):
				
				complete,imageParms            = self.coolDownAnimation.animate(gui,'cooldown',[x,y],game,rotation=self.facing,repeat=True,centerOfRotation=(0,0))

				if(complete):
					self.coolDownAnimation.reset()
					self.coolDown =False


	

