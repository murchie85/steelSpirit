from utils._utils import drawImage,load_pickle
from utils.gameUtils import *
from units.scout import *
from units.tank import *

from units.player import *

class levelTwo():
	def __init__(self,gui,game):
		self.state = 'init'
		self.mapx  = 0
		self.mapy  = 0

		
		self.player    = player(gui)
		self.gameMap   = load_pickle('state/' + 'lv2.pkl')
		self.mapw      = self.gameMap['width']
		self.maph      = self.gameMap['height']



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
				
				# check if bullet hits any enemies
				for ally in self.allyList:

					if(collidesWithHitBox(bullet,ally)):
						bullet.bulletCollides(ally,gui,self)

				# move bullet
				bullet.drawSelf(gui,game)
				bullet.move(gui,self,game)


			# ----PLAYER 

			self.player.drawSelf(gui,game,self)
			if(self.player.alive): self.player.actions(gui,game,self)

			# ENEMY ACTIONS

			for enemy in self.enemyList:
				enemy.drawSelf(gui,game,self)
				enemy.actions(gui,game,self)

				if(collidesWith(self.player,enemy) and self.player.invincible==False):
					self.player.hp         -= int(0.1*self.player.defaultHp)
					self.player.hit        = True
					self.player.invincible = True

					if self.player.x < enemy.x:
					    # Player is to the left of enemy, move player to the right
					    player.x = enemy.x - self.player.w
					elif self.player.x > enemy.x:
					    # Player is to the right of enemy, move player to the left
					    self.player.x = enemy.x + enemy.w
					elif self.player.y < enemy.y:
					    # Player is above enemy, move player down
					    self.player.y = enemy.y - self.player.h
					elif self.player.y > enemy.y:
					    # Player is below enemy, move player up
					    self.player.y = enemy.y + enemy.h


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



		mapTiles = self.gameMap['metaTiles']
		enemies  = self.gameMap['enemyList']
		#--------------ADD ENEMIES
		x,y = 0,0
		# USES THE type and index as keys to gui.tileDict
		for r in range(len(mapTiles)):
			row = mapTiles[r]
			for c in range(len(row)):
				col = row[c]
				# needed to increment x,y values respectively
				image = gui.tileDict[col['type']][col['index']]
				
				# ADD ENEMY IF AT THIS R,C LEVEL
				for enemy in self.gameMap['enemyList']:
					if(r == enemy['row'] and c== enemy['col']):
						self.addEnemy(x,y,enemy,gui)

				x += image.get_width()
			y+= image.get_height()
			x = 0



		self.allyList.append(self.player)
		self.player.x = 0.5*self.mapw
		self.player.y = 0.5*self.maph
		self.state= ' start'
	
	def addEnemy(self,x,y,enemy,gui):
		if(enemy['kind']=='scout'):
			_scout = scout(createFid(self),gui,x=x,y=y)
			_scout.patrolLocations = [x['coords'] for x in enemy['patrolCoords']]
			self.enemyList.append(_scout)
		if(enemy['kind']=='tank'):
			_tank = tank(createFid(self),gui,x=x,y=y)
			_tank.patrolLocations = [x['coords'] for x in enemy['patrolCoords']]
			self.enemyList.append(_tank)

