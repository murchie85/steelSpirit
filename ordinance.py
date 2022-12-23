from utils._utils import stopTimer, imageAnimateAdvanced,darken
from utils.gameUtils import killme
import pygame
import math

class bullet():
	def __init__(self,gui,x,y,bid,classification,facing,bulletType,speed=5,w=5,h=5,colour=(255,177,42),damage=10,_range=1200):
		self.x,self.y       = x,y
		self.ox,self.oy     = x,y
		self.id             = bid
		self.classification = classification
		self.facing         = facing
		self.speed          = speed
		self.colour         = colour
		self.damage         = damage
		self.w,self.h       = w,h
		self.debrisTimer    = stopTimer()
		self.debrisDelay    = 0.3
		self.range          = _range

		self.bulletType     = bulletType

		if(self.bulletType in ['slitherShot','doubleSlither']):
			self.bulletImage   = imageAnimateAdvanced(gui.slitherShot,0.1)


	def move(self,gui,lv,game):
		vel_x = self.speed * math.cos(math.radians(360-self.facing))
		vel_y = self.speed * math.sin(math.radians(360-self.facing))

		self.x += vel_x 
		self.y += vel_y


		self.checkBoundary(gui,lv)

		if(self.classification=='debris'):
			removeMe = self.debrisTimer.stopWatch(self.debrisDelay,'debris', str(self.id) + str(self.classification) + 'debris', game,silence=True)
			self.colour = darken(self.colour,darkenAmount=1)
			if(removeMe):
				self.killBullet(lv,killBulletsssage='debris Fadeout')
		

	def checkBoundary(self,gui,lv):

		if((self.x < self.ox-self.range ) or 
		   (self.x > self.ox + self.range)  or 
		   (self.y < self.oy-self.range) or 
		   (self.y > self.oy + self.range)
		   ):
			self.killBullet(lv,killBulletsssage=' BULLET OUT OF BOUNDS')
			#print('killed :' + str(self.id))

	# ONLY DRAW IF IN BOUNDARY

	def drawSelf(self,gui,game):
		x,y = self.x -gui.camX, self.y -gui.camY
		
		if(self.bulletType=='doublePellet'):
			pygame.draw.circle(gui.screen, self.colour, (x,y), self.w, 0)
		elif(self.bulletType in ['slitherShot','doubleSlither']):
			self.bulletImage.animate(gui,'slitherShotBullet',[x-0.5*gui.slitherShot[0].get_width(),y],game,rotation=self.facing-90)
		else:
			pygame.draw.circle(gui.screen, self.colour, (x,y), self.w, 0)




	# MANAGE BULLET COLLISION WITH SELF 

	def bulletCollides(self,target,gui,lv):
		# IF BULLET CLASSIFICATION IS NOT THE SAME AS TARGETS 
		if(self.classification!=target.classification and self.classification!='debris'):
			
			# IF THE TARGET ISN'T INVINCIBLE 
			if(not target.invincible):
				target.hp -= self.damage
				target.hit = True
				self.killBullet(lv,killBulletsssage='struck enemy')

			# ----KILL THE ENEMY 
			if(target.hp<=0):
				target.alive = False
				killme(target,lv,killMesssage=' struck by enemy fire.',printme=True)

	# ENSURE BULLET DIES. 

	def killBullet(self,lv,killBulletsssage=None,printme=False):
		for i in lv.bulletList:
			if(self.id==i.id):
				lv.bulletList.remove(self)
				if(printme):
					print("Bullett destroyed : " + killBulletsssage + ' ' + str(self.classification))








