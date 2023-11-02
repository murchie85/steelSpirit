
from units.parent import *
from utils.gameUtils import *
from utils._utils import imageAnimateAdvanced,loadingBarClass
import pygame

class greenBarracks(parent):
	def __init__(self,_id,gui,x=None,y=None):
		super().__init__(gui)
		# MAIN OVERRIDES 
		self.id             = _id
		self.name           = 'greenBarracks'
		self.kind           = 'structure'
		self.images         = imageAnimateAdvanced(gui.greenBarracks,0.2)
		self.x,self.y       = 500,500
		if(x!=None): self.x = x
		if(y!=None): self.y = y
		self.w              = int(gui.greenBarracks[0].get_width())
		self.h              = int(gui.greenBarracks[0].get_height())
		
		self.chosenExplosionImg = gui.bigCloudyExplosion
		self.explosion          = imageAnimateAdvanced(self.chosenExplosionImg,0.1)
		
		# HIT IMAGE
		self.hitImage         = gui.greenBarracksHit
		self.hitAnimation     = imageAnimateAdvanced(self.hitImage,0.2)
		self.hitsTaken        = 0

		# DAMAGE IMAGES
		self.damagedBarracksImgs    = imageAnimateAdvanced(gui.greenBarracksDamaged,0.2)
		self.damagedBarracksImgsHit = imageAnimateAdvanced(gui.greenBarracksDamaged,0.2)

		# REMAINS IMAGE 
		self.remainsAnimation = imageAnimateAdvanced(gui.greenBarracksDestroyed,0.2)



		# HEALTHBAR 
		self.healthBar      = loadingBarClass(self.w,0.2*self.h,(80,220,80),(220,220,220),(0,0,200))
		self.blitPos        = None
		self.turretPos      = None

		self.state             = 'patrol'
		self.patrolLocations   = [(self.x,self.y),(self.x+700,self.y),(self.x+700,self.y+200),(self.x,self.y+200)] 
		self.currentLocIndex   = 0


		# CLASS OVERRIDES
		self.defaultHp       = 500
		self.hp              = 500
		self.defaultSpeed    = 1
		self.maxSpeed        = 1
		self.maxSpeedDefault = 1

		# ENEMY COORDS 

		self.angleDiffToEnemy = 0
		self.DistanceToEnemy  = 50000
		self.enemyTargetAngle = 0
		self.defenceSector    = self.patrolLocations[0]
		self.damaged          = False

	# AI LOGIC
	def actions(self,gui,game,lv):

		pass



	# DRAW REMNANTS AFTER BEING DESTROYED
	def drawRemains(self,gui,lv,game):
		x,y = self.x - gui.camX,self.y  - gui.camY

		# *******BE CAREFUL ABOUNT ON SCREEN
		if(self.alive==False and onScreen(self.x,self.y,self.w,self.h,gui)):
			self.remainsAnimation.animate(gui,str('smouldering biolab remains'),[x,y],game,rotation=self.facing-90,repeat=True)


	def drawSelf(self,gui,game,lv):
		x,y = self.x - gui.camX,self.y  - gui.camY
		

		if(self.hp<100):
			self.damaged = True

		if(self.alive==True and onScreen(self.x,self.y,self.w,self.h,gui) and not self.hit):

			if(not self.damaged):
				animate,self.blitPos     = self.images.animate(gui,'barracks ' + str(self.id),[x,y],game,rotation=self.facing-90)
			else:
				animate,self.blitPos     = self.damagedBarracksImgs.animate(gui,'barracks  damaged' + str(self.id),[x,y],game,rotation=self.facing-90)



		
		if(self.hit):

			x,y = self.x - gui.camX,self.y  - gui.camY
			
			if(self.alive==True and onScreen(self.x,self.y,self.w,self.h,gui)):
				

				if(not self.damaged):
				
					complete,imageParms            = self.hitAnimation.animate(gui,str(self.hitsTaken) + ' hit',[x,y],game,rotation=self.facing-90,repeat=True)

					if(complete ):
						self.hit = False
						self.hitsTaken +=1

				else:
					
					complete,imageParms            = self.damagedBarracksImgsHit.animate(gui,str(self.hitsTaken) + ' hit',[x,y],game,rotation=self.facing-90,repeat=True)

					if(complete ):
						self.hit = False
						self.hitsTaken +=1



