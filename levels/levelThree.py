from utils._utils import drawImage,load_pickle
from utils.gameUtils import *
from levels.levelFunctions import *
from scenes.cutSceneGui import *
from units.player import *

class levelThree():
	def __init__(self,gui,game):
		self.state = 'init'
		self.mapx  = 0
		self.mapy  = 0

		
		self.player    = player(gui)
		self.gameMap   = load_pickle('state/' + 'lv3.pkl')
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



		# --------- OBJECTIVES
		# EACH ITEM IS AN OBJ, could be group of enemies, one enemy or location. 
		self.objectives        = {'destroyAAQ1': {'objective':'eliminate','targetObjects':[], 'status': 'notStarted', 'nextObjective':'destroyTanksQ1','pauseGame':False, 'startMessage':'First up, take out the enemy AA, good luck!', 'completionMessage': 'Great job!','activeQuandrant': {'x':0 ,'w':self.mapw ,'y':0 ,'h':self.maph} },
								  'destroyTanksQ1': {'objective':'eliminate','targetObjects':[], 'status': 'notStarted', 'nextObjective':'eliminateMissileBase','pauseGame':True,  'startMessage':'Next up, take out the heavy armoured tanks, use your range and missiles to make short work of them.', 'completionMessage': 'Nicely done!','activeQuandrant': {'x':0 ,'w':self.mapw ,'y':self.maph-2200 ,'h':self.maph} },
								  'eliminateMissileBase': {'objective':'eliminate','targetObjects':[], 'status': 'notStarted', 'nextObjective':'destroyBioLab', 'pauseGame':False, 'startMessage':'Ok, next up is a real challenge, take out all MLRS launchers in the missile base - dont forget to use chaff!.', 'completionMessage': "Impressive! Keep it up!",'activeQuandrant': {'x':0 ,'w':self.mapw ,'y':5090 ,'h':self.maph} },
								  'destroyBioLab': {'objective':'eliminate','targetObjects':[], 'status': 'notStarted', 'nextObjective':'complete', 'pauseGame':True, 'startMessage':'You are doing great, now comes the real reason we brought you here. There is a Bio weapons lab to the north, take it out before they can get those cannisters into trucks. Good hunting!', 'completionMessage': "Damn! If this wasn't VR training i'd have to promote you or something.",'activeQuandrant': {'x':0 ,'w':self.mapw ,'y':0 ,'h':self.maph} }
								  }
		self.currentObjective    = 'destroyAAQ1'
		self.objectiveTimer      = countUpTimer()
		self.objectiveIntroState = 'notIntroduced'

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
		
		# SCENES

		self.scene = 'start'





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



		#self.lv3CutScenes(gui,game)


		levelGui(self,gui,game)


	def lv3CutScenes(self,gui,game):
		
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

			# OPEN WINDOW
			self.cutScene.runCutScene(gui,game,scene='ally',underlay=True)


			# ANIMATE ONCE WINDOW OPEN
			if(self.cutScene.pannelOpen):
				gui.claireTalking.animateNoRotation(gui,'claireTalking',[self.cutScene.imageLeftX,self.cutScene.imageY],game)
				self.cutScene.drawMask(gui,game,overlay=False,border='ally',codec=True)
				finished = self.cutScene.dialogue.drawScrollingDialogue(gui,game,self.cutScene.textW,self.cutScene.textH,gui.font, "Welcome to training rookie, time to learn the ropes.", textStartingPos=(self.cutScene.textX ,self.cutScene.textY),colour=(255,255,255),closeOutDelay=True)
				if(finished):
					self.scene    ='drake'
					self.cutScene.pannelOpen = False
		if(self.scene=='drake'):
			self.cutScene.runCutScene(gui,game,scene='ally',underlay=True)


			# ANIMATE ONCE WINDOW OPEN
			if(self.cutScene.pannelOpen):
				gui.claireTalking.animateNoRotation(gui,'claireTalking',[self.cutScene.imageLeftX,self.cutScene.imageY],game)
				self.cutScene.drawMask(gui,game,overlay=False,border='ally',codec=True)
				finished = self.cutScene.dialogue.drawScrollingDialogue(gui,game,self.cutScene.textW,self.cutScene.textH,gui.font, "follow up.", textStartingPos=(self.cutScene.textX ,self.cutScene.textY),colour=(255,255,255),closeOutDelay=True)



		# CUTSCENE NOTES 

		# 1. set scene flag
		# 2. if panel open, talk, draw mask, animate dialogue
		# 3. go to next scene after dialogue

		# look at camtolocationn
		# self.cutScene.dialogue.closeOutDelay
		# self.cutScene.drawMask(bm.gui,bm,border='ally',codec=False,overlay=False)

