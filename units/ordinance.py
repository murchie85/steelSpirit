from utils._utils import stopTimer, imageAnimateAdvanced,darken
from utils.gameUtils import killme,onScreen
import pygame
import math

class bullet():
	def __init__(self,gui,x,y,bid,classification,facing,bulletType,speed=5,w=5,h=5,colour=(255,177,42),damage=10,shrapnellType=None):
		self.x,self.y             = x,y
		self.ox,self.oy           = x,y
		self.id                   = bid
		self.ordType              = 'bullet'
		self.name                 = 'bullet'
		self.classification       = classification
		self.facing               = facing
		self.speed                = speed
		self.colour               = colour
		self.damage               = damage
		self.w,self.h             = w,h
		self.cumulatedDistance    = 0
		self.debrisTimer          = stopTimer()
		self.debrisDelay          = 0.3
		self.shrapnellAnimation   = imageAnimateAdvanced(gui.shrapnellA,0.2)
		self.shrapnellPlume       = imageAnimateAdvanced(gui.shrapnellPlume,0.1)
		self.shrapnellType        = shrapnellType


		self.range          = 1.5*gui.w

		self.bulletType     = bulletType

		self.slitherTypes       = ['slitherShot','doubleSlither']
		self.triTypes           = ['triBlast']
		self.yellowPlasma       = ['smallAA','yellowPlasma']
		self.redPlasmaBall      = ['redPlasmaBall']
		self.lightRedPlasmaBall = ['lightRedPlasmaBall']
		self.hotRoundTypes      = ['hotRound','hotDouble','hotTripple']
		
		if(self.bulletType in self.slitherTypes):
			self.bulletImage   = imageAnimateAdvanced(gui.slitherShot,0.1)
		if(self.bulletType in self.triTypes):
			self.bulletImage   = imageAnimateAdvanced(gui.triBlast,0.1)
		if(self.bulletType in self.yellowPlasma):
			self.bulletImage   = imageAnimateAdvanced(gui.yellowPlasma,0.1)
		if(self.bulletType in self.redPlasmaBall):
			self.bulletImage   = imageAnimateAdvanced(gui.redPlasma,0.1)
		if(self.bulletType in self.lightRedPlasmaBall):
			self.bulletImage   = imageAnimateAdvanced(gui.lightRedPlasma,0.1)
		if(self.bulletType in self.hotRoundTypes):
			self.bulletImage   = imageAnimateAdvanced(gui.hotRound,0.1)


	def move(self,gui,lv,game):
		vel_x = self.speed * math.cos(math.radians(360-self.facing))
		vel_y = self.speed * math.sin(math.radians(360-self.facing))
		self.cumulatedDistance += math.sqrt(vel_x**2 + vel_y**2)

		self.x += vel_x 
		self.y += vel_y

		# KILL IF OUT OF BOUNDS
		self.checkBoundary(gui,lv)

		# KILL IF OFF SCREEN
		if(not onScreen(self.x,self.y,self.w,self.h,gui)):
			self.killSelf(lv,killMessage='bullet out of screen')

		if(self.classification=='debris'):
			removeMe = self.debrisTimer.stopWatch(self.debrisDelay,'debris', str(self.id) + str(self.classification) + 'debris', game,silence=True)
			self.colour = darken(self.colour,darkenAmount=1)
			if(removeMe):
				self.killSelf(lv,killMessage='debris Fadeout')

		# APPEND A PLUME EVERY 30 pixels
		if(self.shrapnellType=='A'):
			if(self.cumulatedDistance > 20):
				self.cumulatedDistance  = 0
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(bullet(gui,self.x ,self.y,bid,'shrapnell',self.facing,'shrapnell',speed=0,shrapnellType='A_plume'))
			


	def checkBoundary(self,gui,lv):

		if((self.x < self.ox-self.range ) or 
		   (self.x > self.ox + self.range)  or 
		   (self.y < self.oy-self.range) or 
		   (self.y > self.oy + self.range)
		   ):
			self.killSelf(lv,killMessage=' BULLET OUT OF BOUNDS')
			#print('killed :' + str(self.id))

	# ONLY DRAW IF IN BOUNDARY

	def drawSelf(self,gui,game,lv):
		x,y = self.x -gui.camX, self.y -gui.camY
		
		if(self.bulletType=='doublePellet'):
			pygame.draw.circle(gui.screen, self.colour, (x,y), self.w, 0)
		# ------SLITHER
		elif(self.bulletType in self.slitherTypes):
			self.bulletImage.animate(gui,'slitherShotBullet',[x-0.5*gui.slitherShot[0].get_width(),y],game,rotation=self.facing-90)
		# ------TRI BLAST 
		elif(self.bulletType in self.triTypes):
			self.bulletImage.animate(gui,'triBlast',[x-0.5*gui.triBlast[0].get_width(),y-0.5*gui.triBlast[0].get_height()],game,rotation=self.facing-90)
		# ------YELLOW PLASMA 
		elif(self.bulletType in self.yellowPlasma):
			self.bulletImage.animate(gui,'yellowPlasma fire',[x-0.5*gui.yellowPlasma[0].get_width(),y-0.5*gui.yellowPlasma[0].get_height()],game,rotation=self.facing-90)
		# ------RED PLASMA 
		elif(self.bulletType in self.redPlasmaBall):
			self.bulletImage.animate(gui,'redplasma fire',[x-0.5*gui.yellowPlasma[0].get_width(),y-0.5*gui.yellowPlasma[0].get_height()],game,rotation=self.facing-90)
		# ------LIGHT RED PLASMA 
		elif(self.bulletType in self.lightRedPlasmaBall):
			self.bulletImage.animate(gui,'light redplasma fire',[x-0.5*gui.yellowPlasma[0].get_width(),y-0.5*gui.yellowPlasma[0].get_height()],game,rotation=self.facing-90)
		# ------HOT ROUNDS
		elif(self.bulletType in self.hotRoundTypes):
			self.bulletImage.animate(gui,'hotRound fire',[x-0.5*gui.hotRound[0].get_width(),y-0.5*gui.hotRound[0].get_height()],game,rotation=self.facing-90)
		elif(self.shrapnellType==None):
			pygame.draw.circle(gui.screen, self.colour, (x,y), self.w, 0)


		# ANIMATE SHRAPNELL AND KILL WHEN IMAGE COMPLETE
		if(self.shrapnellType=='A'):
			sc, sb = self.shrapnellAnimation.animate(gui,'shrapnell',[x,y],game,rotation=self.facing-90)
			if(sc):
				self.killSelf(lv,killMessage='shrapnell complete')
		if(self.shrapnellType=='A_plume'):
			spc, spb = self.shrapnellPlume.animate(gui,'shrapnellPlume',[x,y],game,rotation=self.facing-90)
			if(spc):
				self.killSelf(lv,killMessage='shrapnell complete')



	# MANAGE BULLET COLLISION WITH SELF 

	def bulletCollides(self,target,gui,lv):
		# IF BULLET CLASSIFICATION IS NOT THE SAME AS TARGETS 
		if(self.classification!=target.classification and self.classification not in ['debris','shrapnell']):
			
			# IF THE TARGET ISN'T INVINCIBLE 
			if(not target.invincible):
				target.hp -= self.damage
				target.hit = True
				self.killSelf(lv,killMessage='struck enemy')

			# ----KILL THE ENEMY 
			if(target.hp<=0):
				target.alive = False
				killme(target,lv,killMesssage= str(target.name) + ' struck by enemy fire.',printme=True)

	# ENSURE BULLET DIES. 

	def killSelf(self,lv,killMessage=None,printme=False):
		for i in lv.bulletList:
			if(self.id==i.id):
				lv.bulletList.remove(self)
				if(printme):
					print("Bullett destroyed : " + killMessage + ' ' + str(self.classification))








