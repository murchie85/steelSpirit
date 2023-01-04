from utils._utils import drawImage,load_pickle
from utils.gameUtils import *
from levels.levelFunctions import *

from units.player import *

class levelFour():
	def __init__(self,gui,game):
		self.state = 'init'
		self.mapx  = 0
		self.mapy  = 0

		
		self.player    = player(gui)
		self.gameMap   = load_pickle('state/' + 'lv4.pkl')
		self.mapw      = self.gameMap['width']
		self.maph      = self.gameMap['height']



		# in game objects

		self.bulletList  = []
		self.plumeList   = []
		self.allyList    = []
		self.enemyList   = []
		self.deadList    = []
		self.fids        = [1]

		self.enemyDestroyed = False




		# -------GUI STUFF

		self.healthBar         = loadingBarClass(100,20,(80,220,80),(220,220,220),(0,0,200))
		self.objectiveArrow    = imageAnimateAdvanced(gui.objectiveArrow,0.2)


		self.log         = []



	def run(self,gui,game):

		if(self.state=='init'):
			init(self,gui,game)
		else:


			# ------MAIN LOOP 

			drawMap(self,gui)
			

			# ------BULLET MANAGER

			for bullet in self.bulletList:

				# check if bullet hits any enemies
				for enemy in self.enemyList:

					if(collidesWithHitBox(bullet,enemy)):
						bullet.bulletCollides(enemy,gui,self)
				
				# check if bullet hits any enemies
				for ally in self.allyList:

					if(collidesWithHitBox(bullet,ally)):
						bullet.bulletCollides(ally,gui,self)

				# move bullet
				bullet.drawSelf(gui,game,self)
				bullet.move(gui,self,game)

			# ------MISSILE PLUME
			for plume in self.plumeList:
				plume.drawSelf(gui,game,self)






			# ----PLAYER 

			self.player.drawSelf(gui,game,self)
			if(self.player.alive): self.player.actions(gui,game,self)

			# ENEMY ACTIONS

			for enemy in self.enemyList:
				enemy.drawSelf(gui,game,self)
				enemy.actions(gui,game,self)
				manageCollisions(self,enemy,gui,game)

			#-----Death animations
			for dead in self.deadList:
				if(dead.alive==False):

					# DRAW STREWN CARCAS
					if(hasattr(dead,'drawRemains')):
						dead.drawRemains(gui,self,game)

					# SHAKE CAMERA ONCE
					if(dead.name=='tank'):
						if(not hasattr(dead,'deathShake')):
							dead.deathShake = False
						elif(dead.deathShake == False):
							# Initiates shake and Will be reset by player
							self.enemyDestroyed = True
							dead.deathShake = True

					# DRAW DEATH EXPLOSION
					dead.animateDestruction(gui,self,game)




		levelGui(self,gui,game)



