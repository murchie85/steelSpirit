from units.parent import *
from utils.gameUtils import *
from utils._utils import imageAnimateAdvanced,loadingBarClass
import pygame

class samSite(parent):
	def __init__(self,_id,gui,x=None,y=None):
		super().__init__(gui)
		# MAIN OVERRIDES 
		self.id             = _id
		self.name           = 'samSite'
		self.kind           = 'structure'
		self.images         = imageAnimateAdvanced(gui.samSite,0.2)
		self.chosenExplosionImg = gui.barrelExplosion
		self.explosion          = imageAnimateAdvanced(self.chosenExplosionImg,0.04)
		self.x,self.y       = 0,0
		if(x!=None): self.x = x
		if(y!=None): self.y = y
		self.w              = int(gui.samSite[0].get_width())
		self.h              = int(gui.samSite[0].get_height())
		
		# HIT IMAGE
		self.hitImage         = gui.samSiteHit
		self.hitAnimation     = imageAnimateAdvanced(self.hitImage,0.2)
		self.hitsTaken        = 0

		# REMAINS IMAGE 
		self.remainsAnimation = imageAnimateAdvanced(gui.samSiteRemains,0.2)



		# HEALTHBAR 
		self.healthBar      = loadingBarClass(self.w,0.2*self.h,(80,220,80),(220,220,220),(0,0,200))
		self.blitPos        = None
		self.turretPos      = None

		self.state             = 'patrol'
		self.patrolLocations   = [(self.x,self.y),(self.x+700,self.y),(self.x+700,self.y+200),(self.x,self.y+200)] 
		self.currentLocIndex   = 0


		# CLASS OVERRIDES
		self.defaultHp       = 200
		self.hp              = 200
		self.defaultSpeed    = 1
		self.maxSpeed        = 1
		self.maxSpeedDefault = 1

		# ENEMY COORDS 

		self.angleDiffToEnemy = 0
		self.DistanceToEnemy  = 50000
		self.enemyTargetAngle = 0
		self.defenceSector    = self.patrolLocations[0]


	# AI LOGIC
	def actions(self,gui,game,lv):

		pass



	# DRAW REMNANTS AFTER BEING DESTROYED
	def drawRemains(self,gui,lv,game):
		x,y = self.x - gui.camX,self.y  - gui.camY

		# *******BE CAREFUL ABOUNT ON SCREEN
		if(self.alive==False and onScreen(self.x,self.y,self.w,self.h,gui) and self.destructionComplete):
			self.remainsAnimation.animate(gui,str('smouldering samSite remains'),[x,y],game,rotation=self.facing-90,repeat=True)


	def drawSelf(self,gui,game,lv):
		x,y = self.x - gui.camX,self.y  - gui.camY
		


		if(self.alive==True and onScreen(self.x,self.y,self.w,self.h,gui) and not self.hit):
			animate,self.blitPos     = self.images.animate(gui,'samSite' + str(self.id),[x,y],game,rotation=self.facing-90)


		if(self.hit):

			x,y = self.x - gui.camX,self.y  - gui.camY
			
			if(self.alive==True and onScreen(self.x,self.y,self.w,self.h,gui)):
				
				complete,imageParms            = self.hitAnimation.animate(gui,str(self.hitsTaken) + ' hit',[x,y],game,rotation=self.facing-90,repeat=True)

				if(complete ):
					self.hit = False
					self.hitsTaken +=1


	def animateDestruction(self,gui,lv,game):
		x,y = self.x - gui.camX,self.y  - gui.camY

		# *******BE CAREFUL ABOUNT ON SCREEN

		if(self.destructionComplete==False and self.alive==False):
			if(hasattr(self,'centerPoint')):
				x += 0.5*self.centerPoint[0]
				y += 0.5*self.centerPoint[1]
			
			complete,blitPos = self.explosion.animate(gui,str(str(self.name) +' explosion'),[x - 0.5*self.chosenExplosionImg[0].get_width(),y-0.5*self.chosenExplosionImg[0].get_height()],game)
			bid = max(([x.id for x in lv.bulletList]),default=0) + 1

			#---------DRAW SCORE

			if(self.killScore!=0):
				drawText(gui,gui.growingFont[self.growingFontIndex],str(self.killScore),x+ 0.4*self.w,y-0.4*self.h + -(self.growingFontIndex/20 * 0.1*gui.h), colour=(255, 255, 255),alpha=(1 - self.growingFontIndex/len(gui.growingFont))*255)
				incFont = self.fontTimer.stopWatch(0.025,'expanding font', str(self.growingFontIndex), game,silence=True)
				if(incFont):
					if(not self.growingFontIndex>=len(gui.growingFont)-1):
						self.growingFontIndex +=1


			if(self.debris<=12):
				self.debris +=1
				# ADDS DEBRIS TO TO LIST
				lv.bulletList.append(bullet(gui,self.x + 0.5* self.chosenExplosionImg[0].get_width(),self.y+ 0.5* self.chosenExplosionImg[0].get_height(),bid,'debris',random.randrange(0,360),'debris',speed=10, w=3,h=3,colour=(192,192,192)))
			
			# ADD FLYING SHRAPNELL 50% of the time
			if(random.choice([1,2])==1 and not self.shrapnellEjected):
				self.shrapnellEjected = True
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(bullet(gui,self.x + 0.5* self.chosenExplosionImg[0].get_width(),self.y+ 0.5* self.chosenExplosionImg[0].get_height(),bid,'shrapnell',random.randrange(0,360),'shrapnell',speed=5,shrapnellType='A'))
			
			if(complete):
				self.destructionComplete = True