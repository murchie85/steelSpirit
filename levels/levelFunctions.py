from utils._utils import drawImage,load_pickle,getTextWidth,getTextHeight,drawTextWithBackground
from utils.gameUtils import *
from units.scout import *
from units.hind import *
from units.tank import *
from units.snowTank import *
from units.greenTank import *
from units.attackBoat import *
from units.aaSmall import *
from units.mlrs import *
from buildings.bioLab import *
from buildings.barrelRed import *
import math as math



def drawMap(self,gui):


	mapTiles = self.gameMap['metaTiles']
	# USES THE type and index as keys to gui.tileDict
	sampleImage = gui.tileDict[mapTiles[0][0]['type']][mapTiles[0][0]['index']]
	
	# *** SETTING THE INDEX'S GREATLY SPEEDS UP AND REDUCES LAG
	yIndexOne = math.floor((gui.camY)/sampleImage.get_height())
	yIndexTwo = math.ceil((gui.camY+gui.camH)/sampleImage.get_height())
	xIndexOne = math.floor((gui.camX)/sampleImage.get_width())
	xIndexTwo = math.ceil((gui.camX+gui.camW)/sampleImage.get_width())
	for r in range(yIndexOne,yIndexTwo):
		row = mapTiles[r]
		y = r *sampleImage.get_height()
		for c in range(xIndexOne,xIndexTwo):
			col = row[c]
			x = c *sampleImage.get_width()
			

			if(col['animated']==False ):
				image = gui.tileDict[col['type']][col['index']]
				#image.set_alpha(200)
				if(onScreen(x,y,image.get_width(),image.get_height(),gui)):
					drawImage(gui.screen,image,(x- gui.camX,y-gui.camY))
			


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
					if(c['type'] in gui.layer2Dict.keys()):
						image = gui.layer2Dict[c['type']][c['index']]
					else:
						image = gui.layer2Dict['base'][8]
					
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

	
	# ---- sidebar 

	#pygame.draw.rect(gui.screen,(0,0,150),(0.82*gui.w,0,0.18*gui.w,gui.h))
	#pygame.draw.rect(gui.screen,(200,200,200),(0.82*gui.w,0,0.18*gui.w,gui.h),5)

	# ANIMATE OBJECTIVE BY LOOKING AT TARGETS IN THE OBJECTIVES
	# ONLY SHOW FOR 4 SECONDS THEN SWITCH FLAG OFF		
	if(self.displayObjectiveArrow):
		displayObjectiveComplete = self.showObjectiveTimer.stopWatch(4,'showing objectives' + str(self.currentObjective) + str(self.arrowCount), 'objective ' + str(self.objectives[self.currentObjective]), game,silence=True)
		if(not displayObjectiveComplete):
			if(hasattr(self, 'objectives')):
				if(self.currentObjective!=None and self.currentObjective!='complete'):
					if('targetObjects' in self.objectives[self.currentObjective].keys()):
						targetObjectives = self.objectives[self.currentObjective]['targetObjects']
						if(len(targetObjectives)>0):
							target = targetObjectives[0]
							angleDiffToEnemy,DistanceToEnemy,enemyTargetAngle = angleToTarget(self.player,self.player.x,self.player.y, target.x + (0.5*target.w) , target.y + (0.5*target.h))

							vel_x = 300 * math.cos(math.radians(360-enemyTargetAngle)) 
							vel_y = 300 * math.sin(math.radians(360-enemyTargetAngle))
							#ox,oy = 0.5*gui.w + vel_x, 0.5*gui.h+vel_y
							ox,oy = self.player.x + vel_x - gui.camX, self.player.y +vel_y - gui.camY
							self.objectiveArrow.animate(gui,str(self.currentObjective),[ox,oy],game,rotation=enemyTargetAngle-90) 
		else:
			self.displayObjectiveArrow = False
			self.arrowCount +=1

				

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



# ---- Applies to enemies 
def manageCollisions(self,enemy,gui,game):
	

	# GET PLAYER OUT OF SELF SPACE
	if(collidesWith(self.player,enemy) and self.player.invincible==False and enemy.kind not in ['structure','vechicle','boat']):
		self.player.hp         -= int(0.1*self.player.defaultHp)
		self.player.hit        = True
		self.player.invincible = True

		if self.player.x < enemy.x:
		    # Player is to the left of enemy, move player to the right
		    self.player.x = enemy.x - 0.2*self.player.w
		elif self.player.x > enemy.x:
		    # Player is to the right of enemy, move player to the left
		    self.player.x = enemy.x + 0.2*enemy.w
		elif self.player.y < enemy.y:
		    # Player is above enemy, move player down
		    self.player.y = enemy.y - 0.2*self.player.h
		elif self.player.y > enemy.y:
		    # Player is below enemy, move player up
		    self.player.y = enemy.y + 0.2*enemy.h
	

	if(onScreen(enemy.x,enemy.y,enemy.w,enemy.h,gui)):
		
		for otherEnemy in self.enemyList:
			if(collidesWith(otherEnemy,enemy)):
				if((enemy.kind =='air' and otherEnemy.kind =='air') or 
					# if bump into me
				   (enemy.kind in ['structure','vechicle']  and otherEnemy.kind in['vechicle','boat']) or 
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


	
	# KIND JUST MEANS NAME FROM DICT, NOT ENEMY KIND
	if(enemy['kind']=='scout'):
		enemyObject = scout(createFid(self),gui,x=x,y=y)
	if(enemy['kind']=='hind'):
		enemyObject = hind(createFid(self),gui,x=x,y=y)
	elif(enemy['kind']=='tank'):
		enemyObject = tank(createFid(self),gui,x=x,y=y)
	elif(enemy['kind']=='snowTank'):
		enemyObject = snowTank(createFid(self),gui,x=x,y=y)
	elif(enemy['kind']=='attackBoat'):
		enemyObject = attackBoat(createFid(self),gui,x=x,y=y)
	elif(enemy['kind']=='greenTank'):
		enemyObject = greenTank(createFid(self),gui,x=x,y=y)
	elif(enemy['kind']=='aaSmall'):
		enemyObject = aaSmall(createFid(self),gui,x=x,y=y)
	elif(enemy['kind']=='mlrs'):
		enemyObject = mlrs(createFid(self),gui,x=x,y=y)
	elif(enemy['kind']=='bioLab'):
		enemyObject = bioLab(createFid(self),gui,x=x,y=y)
	elif(enemy['kind']=='barrelRed'):
		enemyObject = barrelRed(createFid(self),gui,x=x,y=y)
	
	if('patrolCoords' in enemy.keys()):
		enemyObject.patrolLocations = [x['coords'] for x in enemy['patrolCoords']]
	if('seekAndStrafe' in enemy.keys()):
		enemyObject.seekStrafe = enemy['seekAndStrafe']

	self.enemyList.append(enemyObject)
