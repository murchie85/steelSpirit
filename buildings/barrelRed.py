from units.parent import *
from utils.gameUtils import *
from utils._utils import imageAnimateAdvanced,loadingBarClass
import pygame

class barrelRed(parent):
	def __init__(self,_id,gui,x=None,y=None):
		super().__init__(gui)
		# MAIN OVERRIDES 
		self.id             = _id
		self.name           = 'barrelRed'
		self.kind           = 'structure'
		self.images         = imageAnimateAdvanced(gui.barrelGroupRed,0.2)

		self.chosenExplosionImg = gui.redExplosion
		self.explosion          = imageAnimateAdvanced(self.chosenExplosionImg,0.1)
		self.x,self.y       = 500,500
		if(x!=None): self.x = x
		if(y!=None): self.y = y
		self.w              = int(gui.barrelGroupRed[0].get_width())
		self.h              = int(gui.barrelGroupRed[0].get_height())
		
		# HIT IMAGE
		self.hitImage         = gui.bioLabHit
		self.hitAnimation     = imageAnimateAdvanced(gui.barrelGroupRedHit,0.2)
		self.hitsTaken        = 0

		# REMAINS IMAGE 
		self.remainsAnimation = imageAnimateAdvanced(gui.barrelGroupRedRemains,0.2)



		# HEALTHBAR 
		self.healthBar      = loadingBarClass(self.w,0.2*self.h,(80,220,80),(220,220,220),(0,0,200))
		self.blitPos        = None
		self.turretPos      = None

		self.state             = 'patrol'
		self.patrolLocations   = [(self.x,self.y),(self.x+700,self.y),(self.x+700,self.y+200),(self.x,self.y+200)] 
		self.currentLocIndex   = 0


		# CLASS OVERRIDES
		self.hp              = 70
		self.defaultSpeed    = 1
		self.maxSpeed        = 1
		self.maxSpeedDefault = 1

		# ENEMY COORDS 

		self.angleDiffToEnemy = 0
		self.DistanceToEnemy  = 50000
		self.enemyTargetAngle = 0
		self.defenceSector    = self.patrolLocations[0]

		# CHECK NEARBY BARRELS
		self.deathBarrelCheck    = False
		self.chainEffectDistance = 300


	# AI LOGIC
	def actions(self,gui,game,lv):

		if(self.hp<1):
			killme(self,lv,killMesssage=' HP below 1.',printme=True)



	# DRAW REMNANTS AFTER BEING DESTROYED
	def drawRemains(self,gui,lv,game):
		x,y = self.x - gui.camX,self.y  - gui.camY

		# *******BE CAREFUL ABOUNT ON SCREEN
		if(self.alive==False and onScreen(self.x,self.y,self.w,self.h,gui) and self.destructionComplete):
			self.remainsAnimation.animate(gui,str('smouldering barrelGroupRed remains'),[x,y],game,rotation=self.facing-90,repeat=True)


		# ### CHECK NEARBY

		for enemy in lv.enemyList:
			if(self.deathBarrelCheck==False):
				distanceToEnemy = getDistance(self.x,self.y,enemy.x,enemy.y)
				if(distanceToEnemy<self.chainEffectDistance):
					enemy.hp -= 120

		self.deathBarrelCheck = True


	def drawSelf(self,gui,game,lv):
		x,y = self.x - gui.camX,self.y  - gui.camY
		


		if(self.alive==True and onScreen(self.x,self.y,self.w,self.h,gui) and not self.hit):
			animate,self.blitPos     = self.images.animate(gui,'barrelGroupRed' + str(self.id),[x,y],game,rotation=self.facing-90)


		if(self.hit):

			x,y = self.x - gui.camX,self.y  - gui.camY
			
			if(self.alive==True and onScreen(self.x,self.y,self.w,self.h,gui)):
				
				complete,imageParms            = self.hitAnimation.animate(gui,str(self.hitsTaken) + ' hit',[x,y],game,rotation=self.facing-90,repeat=True)

				if(complete ):
					self.hit = False
					self.hitsTaken +=1


