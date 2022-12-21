from utils._utils import drawImage
from utils.gameUtils import *
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

		self.bulletList = []



	def run(self,gui,game):

		if(self.state=='init'):
			self.init()
		else:


			# ------MAIN LOOP 
			self.drawMap(gui)
			
			game.player.drawSelf(gui,game)
			game.player.actions(gui,game,self)

			# PROJECTILE MANAGER
			for bullet in self.bulletList:
				bullet.drawSelf(gui,game)
				bullet.move(gui,self)



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
					drawImage(gui.screen,image,(x- gui.camX,y-gui.camY))
				

				x += image.get_width()
			y+= image.get_height()
			x = 0


	def init(self):
		print('init')

