from utils._utils import drawImage,load_pickle,getTextWidth,getTextHeight,drawTextWithBackground
from utils.gameUtils import *
from units.scout import *
from units.tank import *
from units.greenTank import *
from units.attackBoat import *
from units.aaSmall import *
from units.mlrs import *
from buildings.bioLab import *
from buildings.barrelRed import *




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


	# LAYER 2 
	if('layer2' in self.gameMap.keys()):
		layer2 = self.gameMap['layer2']

		#gui.screen.fill((255,0,0 ))
		x = 0
		y = 0
		# USES THE type and index as keys to gui.tileDict
		for row in layer2:
			for c in row:
				if(c['animated']==False ):
					image = gui.layer2Dict[c['type']][c['index']]
					if(c['type']!='base'):
						if(onScreen(x,y,image.get_width(),image.get_height(),gui)):
							drawImage(gui.screen,image,(x- gui.camX,y-gui.camY))
					

				x += image.get_width()
			y+= image.get_height()
			x = 0

	# SHOW ANYTHING THAT MIGHT BE ON THIS LAYER
	if('tilelessL1' in self.gameMap.keys()):
		for item in self.gameMap['tilelessL1']:
			image = gui.tilelessL1Dict[item['dictKey']][item['index']]
			if(onScreen(item['x'],item['y'],image.get_width(),image.get_height(),gui)):
				drawImage(gui.screen,image,(item['x']- gui.camX,item['y']-gui.camY))


def levelGui(self,gui,game):
	setWidth=getTextWidth(gui.hugeFont,'ENEMIES.')
	
	# SELF REFERS TO LEVEL OBJECT
	self.remainingEnemies = len([x for x in self.enemyList if(x.alive)])
	drawTextWithBackground(gui.screen,gui.hugeFont,str(self.remainingEnemies),50,20, setWidth=setWidth,textColour=(255, 255, 255),backColour= (0,0,0),borderColour=(50,50,200))
	if(hasattr(self,'healthBar')):
		self.healthBar.load(100,0.9*gui.h,gui,self.player.hp/self.player.defaultHp,borderThickness=2)

	# ANIMATE OBJECTIVE BY LOOKING AT TARGETS IN THE OBJECTIVES DICT
	if(hasattr(self, 'objectives')):
		if('targetObjects' in self.objectives[self.currentObjective].keys()):
			if(self.objectives[self.currentObjective]!=None):
				targetObjectives = self.objectives[self.currentObjective]['targetObjects']
				if(len(targetObjectives)>0):
					target = targetObjectives[0]
					angleDiffToEnemy,DistanceToEnemy,enemyTargetAngle = angleToTarget(self.player,self.player.x,self.player.y, target.x , target.y)
					self.objectiveArrow.animate(gui,str(self.currentObjective),[self.player.x - gui.camX +50, self.player.y-gui.camY -300],game,rotation=enemyTargetAngle-90) 
		
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
					addEnemy(self,x,y,enemy,gui)

			x += image.get_width()
		y+= image.get_height()
		x = 0



	self.allyList.append(self.player)
	self.player.x = 0.5*self.mapw
	self.player.y = 0.5*self.maph
	self.state= ' start'



def manageCollisions(self,enemy,gui,game):
	
	# GET PLAYER OUT OF SELF SPACE
	if(collidesWith(self.player,enemy) and self.player.invincible==False and enemy.kind not in ['structure','vechicle']):
		self.player.hp         -= int(0.1*self.player.defaultHp)
		self.player.hit        = True
		self.player.invincible = True

		if self.player.x < enemy.x:
		    # Player is to the left of enemy, move player to the right
		    self.player.x = enemy.x - self.player.w
		elif self.player.x > enemy.x:
		    # Player is to the right of enemy, move player to the left
		    self.player.x = enemy.x + enemy.w
		elif self.player.y < enemy.y:
		    # Player is above enemy, move player down
		    self.player.y = enemy.y - self.player.h
		elif self.player.y > enemy.y:
		    # Player is below enemy, move player up
		    self.player.y = enemy.y + enemy.h
	if(onScreen(enemy.x,enemy.y,enemy.w,enemy.h,gui)):
		for otherEnemy in self.enemyList:
			if(collidesWith(otherEnemy,enemy)):
				if((enemy.kind =='air' and otherEnemy.kind =='air') or 
				   (enemy.kind in ['structure','vechicle']  and otherEnemy.kind in['structure','vechicle','boat']) or 
				   (enemy.kind =='boat' and otherEnemy.kind =='boat')):
					# MOVE OUT WAY
					if otherEnemy.x < enemy.x:
					    # Player is to the left of enemy, move player to the right
					    otherEnemy.x = enemy.x - otherEnemy.w
					elif otherEnemy.x > enemy.x:
					    # Player is to the right of enemy, move player to the left
					    otherEnemy.x = enemy.x + enemy.w
					elif otherEnemy.y < enemy.y:
					    # Player is above enemy, move player down
					    otherEnemy.y = enemy.y - otherEnemy.h
					elif otherEnemy.y > enemy.y:
					    # Player is below enemy, move player up
					    otherEnemy.y = enemy.y + enemy.h


def addEnemy(self,x,y,enemy,gui):
	if(enemy['kind']=='scout'):
		_scout = scout(createFid(self),gui,x=x,y=y)
		_scout.patrolLocations = [x['coords'] for x in enemy['patrolCoords']]
		self.enemyList.append(_scout)
	if(enemy['kind']=='tank'):
		_tank = tank(createFid(self),gui,x=x,y=y)
		_tank.patrolLocations = [x['coords'] for x in enemy['patrolCoords']]
		self.enemyList.append(_tank)
	if(enemy['kind']=='attackBoat'):
		_attackBoat = attackBoat(createFid(self),gui,x=x,y=y)
		_attackBoat.patrolLocations = [x['coords'] for x in enemy['patrolCoords']]
		self.enemyList.append(_attackBoat)
	if(enemy['kind']=='greenTank'):
		_greenTank = greenTank(createFid(self),gui,x=x,y=y)
		_greenTank.patrolLocations = [x['coords'] for x in enemy['patrolCoords']]
		self.enemyList.append(_greenTank)			
	if(enemy['kind']=='aaSmall'):
		_aaSmall = aaSmall(createFid(self),gui,x=x,y=y)
		self.enemyList.append(_aaSmall)
	if(enemy['kind']=='mlrs'):
		_mlrs = mlrs(createFid(self),gui,x=x,y=y)
		self.enemyList.append(_mlrs)
	if(enemy['kind']=='bioLab'):
		_bioLab = bioLab(createFid(self),gui,x=x,y=y)
		self.enemyList.append(_bioLab)
	if(enemy['kind']=='barrelRed'):
		_barrelRed = barrelRed(createFid(self),gui,x=x,y=y)
		self.enemyList.append(_barrelRed)
