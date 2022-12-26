from utils._utils import drawImage,load_pickle
from utils.gameUtils import *
from units.scout import *

class levelOne():
	def __init__(self,gui):
		self.state = 'init'
		self.grass = [gui.grassTiles[0] for x in range(800)]
		self.mapx  = 0
		self.mapy  = 0


		self.gameMap = load_pickle('state/' + 'lv1.pkl')
		self.mapw  = self.gameMap['width']
		self.maph  = self.gameMap['height']



		# in game objects

		self.bulletList  = []
		self.allyList    = []
		self.enemyList   = []
		self.deadList    = []
		self.fids        = [1]


		self.log         = []



	def run(self,gui,game):

		if(self.state=='init'):
			self.init(gui,game)
		else:


			# ------MAIN LOOP 

			self.drawMap(gui)
			

			# ------BULLET MANAGER

			for bullet in self.bulletList:

				# check if bullet hits any enemies
				for enemy in self.enemyList:

					if(collidesWithHitBox(bullet,enemy)):
						bullet.bulletCollides(enemy,gui,self)


				# move bullet
				bullet.drawSelf(gui,game)
				bullet.move(gui,self,game)


			# ----PLAYER 

			game.player.drawSelf(gui,game,self)
			if(game.player.alive): game.player.actions(gui,game,self)

			# ENEMY ACTIONS

			for enemy in self.enemyList:
				enemy.drawSelf(gui,game,self)
				enemy.actions(gui,game,self)

				if(collidesWith(game.player,enemy) and game.player.invincible==False):
					game.player.hp         -= int(0.1*game.player.defaultHp)
					game.player.hit        = True
					game.player.invincible = True

					dx = 0.5*gui.w - game.player.x
					dy = 0.5*gui.h - game.player.y
					game.player.x += dx
					game.player.y += dy



			#-----Death animations
			for dead in self.deadList:
				if(dead.alive==False):
					dead.animateDestruction(gui,self,game)


	def drawMap(self,gui):



		mapTiles = self.gameMap['metaTiles']

		#gui.screen.fill((255,0,0 ))
		x = 0
		y = 0
		# USES THE type and index as keys to gui.tileDict
		for row in mapTiles:
			for c in row:
				if(c['animated']==False ):
					image = gui.tileDict[c['type']][c['index']]
					#image.set_alpha(200)
					if(onScreen(x,y,image.get_width(),image.get_height(),gui)):
						drawImage(gui.screen,image,(x- gui.camX,y-gui.camY))
				

				x += image.get_width()
			y+= image.get_height()
			x = 0


	def init(self,gui,game):

		#---place enemies on battlefield
		_scout = scout(createFid(self),gui,x=500,y=100)
		_scout.patrolLocations   = [(730,110),(1440,110),(1440,540),(730,540)] 
		self.enemyList.append(_scout)

		# ----scout 2
		_scout = scout(createFid(self),gui,x=580,y=100)
		self.enemyList.append(_scout)


		_scout = scout(createFid(self),gui,x=630,y=400)
		self.enemyList.append(_scout)


		_scout = scout(createFid(self),gui,x=700,y=400)
		self.enemyList.append(_scout)

		_scout = scout(createFid(self),gui,x=770,y=400)
		self.enemyList.append(_scout)


		self.allyList.append(game.player)
		self.state= ' start'

