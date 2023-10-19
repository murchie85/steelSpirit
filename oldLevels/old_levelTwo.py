from utils._utils import drawImage,load_pickle
from utils.gameUtils import *
from oldLevels.levelFunctions import *
from scenes.cutSceneGui import * 
from units.player import *

class old_levelTwo():
	def __init__(self,gui,game,filePath):
		self.state = 'init'
		self.mapx  = 0
		self.mapy  = 0

		
		self.player    = player(gui)
		self.gameMap   = load_pickle(filePath)
		self.gameMap['tilelessL1'] = []
		self.gameMap['listTiles'] = []
		self.gameMap['converted'] = []
		self.gameMap['spawnZones'] = []
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


		self.log              = []
		self.remainingEnemies = None
		self.pauseGame        = False



		# --------- OBJECTIVES
		# EACH ITEM IS AN OBJ, could be group of enemies, one enemy or location. 
		self.objectives        = {'destroyAAQ1': {'objective':'eliminate','targetObjects':[], 'status': 'notStarted', 'nextObjective':'destroyTanksQ1','pauseGame':False, 'startMessage':'First up, take out the enemy AA, good luck!', 'completionMessage': 'Great job!','activeQuandrant': {'x':0 ,'w':0.5 *self.mapw ,'y':self.maph-2200 ,'h':2200} },
								  'destroyTanksQ1': {'objective':'eliminate','targetObjects':[], 'status': 'notStarted', 'nextObjective':'eliminateMissileBase','pauseGame':True,  'startMessage':'Next up, take out the heavy armoured tanks, use your range and missiles to make short work of them.', 'completionMessage': 'Nicely done!','activeQuandrant': {'x':0 ,'w':self.mapw ,'y':self.maph-2200 ,'h':self.maph} },
								  'eliminateMissileBase': {'objective':'eliminate','targetObjects':[], 'status': 'notStarted', 'nextObjective':'destroyBioLab', 'pauseGame':False, 'startMessage':'Ok, next up is a real challenge, take out all MLRS launchers in the missile base - dont forget to use chaff!.', 'completionMessage': "Impressive! Keep it up!",'activeQuandrant': {'x':0 ,'w':self.mapw ,'y':5090 ,'h':self.maph} },
								  'destroyBioLab': {'objective':'eliminate','targetObjects':[], 'status': 'notStarted', 'nextObjective':'complete', 'pauseGame':True, 'startMessage':'You are doing great, now comes the real reason we brought you here. There is a Bio weapons lab to the north, take it out before they can get those cannisters into trucks. Good hunting!', 'completionMessage': "Damn! If this wasn't VR training i'd have to promote you or something.",'activeQuandrant': {'x':0 ,'w':self.mapw ,'y':0 ,'h':self.maph} }
								  }
		self.currentObjective    = 'destroyAAQ1'
		self.objectiveTimer      = countUpTimer()
		self.objectiveIntroState = 'notIntroduced'

		self.objectives        = {'destroyAA': {'objective':'eliminate','targetObjects':[], 'status': 'notStarted', 'nextObjective':'destroyTanks', 'startMessage':'Welcome to training bootcamp rookie, first up, take out the enemy AA, good luck!', 'completionMessage': 'Great job!','activeQuandrant': {'x':0 ,'w':self.mapw ,'y':0 ,'h':self.maph}  },
								  'destroyTanks': {'objective':'eliminate','targetObjects':[], 'status': 'notStarted', 'nextObjective':None, 'startMessage':'Next job, mop up them tanks.', 'completionMessage': 'Nicely done!' ,'activeQuandrant': {'x':0 ,'w':self.mapw ,'y':0 ,'h':self.maph} }
								  }
		self.currentObjective  = 'destroyAA'


		# -------GUI STUFF

		self.healthBar             = loadingBarClass(100,20,(80,220,80),(220,220,220),(0,0,200))
		self.objectiveArrow        = imageAnimateAdvanced(gui.objectiveArrow,0.2)
		self.displayObjectiveArrow = False 
		self.showObjectiveTimer  = stopTimer()
		
		# ------ LEVEL TIMER 

		self.levelTimer      = countUpTimer()
		self.alarmTime       = 10
		self.timeRemaining   = 10
		

		# CUTSCENE STUFF

		self.scene = 'start'



	def run(self,gui,game):

		if(self.state=='init'):
			init(self,gui,game)
			self.player.x,self.player.y = 300,900
			return()

		# ------MAIN LOOP 

		drawMap(self,gui)
		
		if(not self.pauseGame):

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


			# ----PLAYER 

			self.player.drawSelf(gui,game,self)
			if(self.player.alive): self.player.actions(gui,game,self)

		if(self.pauseGame):
			self.player.drawSelf(gui,game,self)

		# GUI GETS A LOT OF STATS 
		levelGui(self,gui,game)



		self.lv2CutScenes(gui,game)





	def lv2CutScenes(self,gui,game):
		
		# ADDS THE CUTSCENE CLASS TO THIS CLASS
		if(hasattr(self, 'cutScene')==False):
			self.cutScene = cutScene(gui)

		# COUNT INTO SCENE 1
		if(self.scene=='start'):
			alarmTime = 1
			complete,secondsCounted = self.levelTimer.countRealSeconds(alarmTime,game)
			if(complete):
				self.scene ='claire'



		

		if(self.scene=='claire'):
			self.pauseGame = True

			# OPEN WINDOW
			self.cutScene.runCutScene(gui,game,scene='ally',underlay=True)


			# ANIMATE ONCE WINDOW OPEN
			if(self.cutScene.pannelOpen):
				gui.claireTalking.animateNoRotation(gui,'claireTalking',[self.cutScene.imageLeftX,self.cutScene.imageY],game)
				self.cutScene.drawMask(gui,game,overlay=False,border='ally',codec=True)
				finished = self.cutScene.dialogue.drawScrollingDialogue(gui,game,self.cutScene.textW,self.cutScene.textH,gui.smallishFont, "Welcome back rookie, this is a harder scenario this time. Don't forget to use chaff when you get locked on to, good luck.", textStartingPos=(self.cutScene.textX ,self.cutScene.textY),colour=(255,255,255),closeOutDelay=True)
				if(finished):
					self.scene    ='gameUnderway'
					self.pauseGame = False
					self.cutScene.reset()



		# MOVE INTO FINISH LEVEL CUTCENE 
		if(self.scene =='gameUnderway' and self.remainingEnemies <=0):
			self.scene = 'finishNotify'

		# FINISH NOTIFICATION
		if(self.scene=='finishNotify'):
			self.cutScene.runCutScene(gui,game,scene='ally',underlay=True)
			if(self.cutScene.pannelOpen):
				gui.claireTalking.animateNoRotation(gui,'claireTalking',[self.cutScene.imageLeftX,self.cutScene.imageY],game)
				self.cutScene.drawMask(gui,game,overlay=False,border='ally',codec=True)
				finished = self.cutScene.dialogue.drawScrollingDialogue(gui,game,self.cutScene.textW,self.cutScene.textH,gui.font, "Hah not bad, this is still a Beta game in very early development, but try out the map maker functionality to build your own world - ciao!", textStartingPos=(self.cutScene.textX ,self.cutScene.textY),colour=(255,255,255),closeOutDelay=True)
				if(finished):
					self.scene    ='complete'
					self.cutScene.reset()


