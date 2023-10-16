from utils._utils import drawImage,load_pickle
from utils.gameUtils import *
from levels.levelFunctions import *
from scenes.cutSceneGui import * 
from units.player import *

class levelFive():
	def __init__(self,gui,game):
		self.state = 'init'
		self.mapx  = 0
		self.mapy  = 0

		
		self.player    = player(gui)
		self.gameMap   = load_pickle('state/' + 'lv5.pkl')
		self.mapw      = self.gameMap['width']
		self.maph      = self.gameMap['height']



		# in game objects

		self.bulletList        = []
		self.plumeList         = []
		self.allyList          = []
		self.enemyList         = []
		self.unfieldedEnemies  = [] # this contains remaining enemies to put on the  board
		self.defaultEnemyList  = [] # This contains a backup
		self.deadList          = []
		self.fids              = [1]
		self.enemyComponentList = [] # THINGS LIKE TURRETS ETC

		self.enemyDestroyed = False


		self.log              = []
		self.remainingEnemies = None
		self.pauseGame        = False

		# -------GUI STUFF

		self.healthBar             = loadingBarClass(100,20,(80,220,80),(220,220,220),(0,0,200))
		self.objectiveArrow        = imageAnimateAdvanced(gui.objectiveArrow,0.2)
		self.displayObjectiveArrow = False 
		self.showObjectiveTimer  = stopTimer()
		self.arrowCount			 = 0
		

		# --------- OBJECTIVES
		# EACH ITEM IS AN OBJ, could be group of enemies, one enemy or location. 
		self.objectives        = {'destroyAAQ1': {'objective':'eliminate','targetObjects':[], 'status': 'notStarted', 'nextObjective':'destroyTanksQ1','pauseGame':False, 'startMessage':'Greetings rookie, take out the enemy AA and watch out for tanks, good luck!', 'completionMessage': 'Great job!','activeQuandrant': {'x':0 ,'w':0.5 *self.mapw ,'y':self.maph-2200 ,'h':2200} },
								  'destroyTanksQ1': {'objective':'eliminate','targetObjects':[], 'status': 'notStarted', 'nextObjective':'eliminateMissileBase','pauseGame':True,  'startMessage':'Next up, take out the heavy armoured tanks, use your range and missiles to make short work of them.', 'completionMessage': 'Nicely done!','activeQuandrant': {'x':0 ,'w':self.mapw ,'y':self.maph-2200 ,'h':self.maph} },
								  'eliminateMissileBase': {'objective':'eliminate','targetObjects':[], 'status': 'notStarted', 'nextObjective':'destroyBioLab', 'pauseGame':False, 'startMessage':'Ok, next up is a real challenge, take out all MLRS launchers in the missile base - dont forget to use chaff!.', 'completionMessage': "Impressive! Keep it up!",'activeQuandrant': {'x':0 ,'w':self.mapw ,'y':5090 ,'h':self.maph} },
								  'destroyBioLab': {'objective':'eliminate','targetObjects':[], 'status': 'notStarted', 'nextObjective':'complete', 'pauseGame':True, 'startMessage':'You are doing great, now comes the real reason we brought you here. There is a Bio weapons lab to the north, take it out before they can get those cannisters into trucks. Good hunting!', 'completionMessage': "Damn! If this wasn't VR training i'd have to promote you or something.",'activeQuandrant': {'x':0 ,'w':self.mapw ,'y':0 ,'h':self.maph} }
								  }
		self.currentObjective    = 'destroyAAQ1'
		self.objectiveTimer      = countUpTimer()
		self.objectiveIntroState = 'notIntroduced'

		# ------ LEVEL TIMER 

		self.levelTimer      = countUpTimer()
		self.alarmTime       = 10
		self.timeRemaining   = 10
		

		# CUTSCENE STUFF

		self.scene = 'gameUnderway'



	def run(self,gui,game):

		if(self.state=='init'):
			self.initMe(gui,game)

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
			if(self.player.alive): 
				self.player.actions(gui,game,self)
				#game.calculatePlayerSpeed(self.player)

			# ------DISPLAY OBJECTIVES 

			if('O' in gui.input.returnedKey.upper()):
				print('displaying objective')
				self.displayObjectiveArrow = True




		if(self.pauseGame):
			self.player.drawSelf(gui,game,self)

		# GUI GETS A LOT OF STATS 
		levelGui(self,gui,game)



		self.gameScenes(gui,game)       # Manage game scenes 
		self.quandrantManager(gui,game) # ensure units properly clamped 


		# OBJECTIVE MANAGER 
		if(self.scene=='gameUnderway'):  self.objectiveManager(gui,game)









	def gameScenes(self,gui,game):
		
		# ADDS THE CUTSCENE CLASS TO THIS CLASS
		if(hasattr(self, 'cutScene')==False):
			self.cutScene = cutScene(gui)




		# ------------ INTRO AND EXIT	

		# COUNT INTO SCENE 1
		if(self.scene=='start'):
			alarmTime = 1
			complete,secondsCounted = self.levelTimer.countRealSeconds(alarmTime,game)
			if(complete):
				self.levelTimer.counter = 0
				self.levelTimer.reset(3)
				self.scene ='claire'

	

		if(self.scene=='claire'):
			self.pauseGame = True

			# OPEN WINDOW
			self.cutScene.runCutScene(gui,game,scene='ally',underlay=True)


			# ANIMATE ONCE WINDOW OPEN
			if(self.cutScene.pannelOpen):
				gui.claireTalking.animateNoRotation(gui,'claireTalking',[self.cutScene.imageLeftX,self.cutScene.imageY],game)
				self.cutScene.drawMask(gui,game,overlay=False,border='ally',codec=True)
				finished = self.cutScene.dialogue.drawScrollingDialogue(gui,game,self.cutScene.textW,self.cutScene.textH,gui.smallishFont, "Welcome to training rookie, time to learn the ropes. You have a number of air, land and sea targets. Get going, good luck. Remember you will go into automatic lockon mode which changes your button inputs, press y to toggle lockon on and off.", textStartingPos=(self.cutScene.textX ,self.cutScene.textY),colour=(255,255,255),closeOutDelay=True)
				if(finished):
					self.scene    ='gameUnderway'
					self.pauseGame = False
					self.cutScene.reset()



		# MOVE INTO FINISH LEVEL CUTCENE 
		##if(self.scene =='gameUnderway' and self.remainingEnemies <=0): self.scene = 'levelComplete'

		# FINISH NOTIFICATION
		if(self.scene=='levelComplete'):
			complete,secondsCounted = self.levelTimer.countRealSeconds(3,game)
			if(not complete):
				return()
			else:
				self.scene = 'notifyComplete'
	
		if(self.scene=='notifyComplete'):
			self.cutScene.runCutScene(gui,game,scene='ally',underlay=True)
			if(self.cutScene.pannelOpen):
				gui.claireTalking.animateNoRotation(gui,'claireTalking',[self.cutScene.imageLeftX,self.cutScene.imageY],game)
				self.cutScene.drawMask(gui,game,overlay=False,border='ally',codec=True)
				finished = self.cutScene.dialogue.drawScrollingDialogue(gui,game,self.cutScene.textW,self.cutScene.textH,gui.font, "Hah not bad, this is still a Beta game in very early development, but try out level 2 for more of a challenge.", textStartingPos=(self.cutScene.textX ,self.cutScene.textY),colour=(255,255,255),closeOutDelay=True)
				if(finished):
					self.scene    ='complete'
					self.cutScene.pannelOpen = False
					self.cutScene.reset()


	def objectiveManager(self,gui,game):
	
		currentObjective = self.objectives[self.currentObjective]

		# IF ALL OBJECTIVES COMPLETE
		if(self.currentObjective==None or self.currentObjective=='complete'):
			self.scene = 'levelComplete'
			return()

		# COUNT IN TIMER FOR EACH OBJECTIVE
		if(self.objectiveIntroState=='notIntroduced' and currentObjective['status']=='notStarted'):
			complete,secondsCounted = self.objectiveTimer.countRealSeconds(1,game)
			if(not complete):
				return()
			if(complete):
				self.objectiveTimer.counter = 0
				self.objectiveIntroState='introduced'





		# ----INTRODUCE NEXT OBJECTIVE 
		
		if(currentObjective['status']=='notStarted'):
			
			if(currentObjective['pauseGame']):
				self.pauseGame = True
			
			sceneMessage = currentObjective['startMessage']
			# OPEN WINDOW
			self.cutScene.runRHSCutScene(gui,game,scene='ally',underlay=True,orientation='topRight')
			
			# ANIMATE ONCE WINDOW OPEN
			if(self.cutScene.pannelOpen):
				self.displayObjectiveArrow = True
				gui.claireTalking.animateNoRotation(gui,'claireTalking',[self.cutScene.imageLeftX,self.cutScene.imageY],game)
				self.cutScene.drawMask(gui,game,overlay=False,border='ally',codec=True)
				
				finished = self.cutScene.dialogue.drawScrollingDialogue(gui,game,self.cutScene.textW,self.cutScene.textH,gui.smallFont, sceneMessage, textStartingPos=(self.cutScene.textX ,self.cutScene.textY),colour=(51,189,251),closeOutDelay=True,maxLines=4,scrollInterval=0.02,pageWait=3)
				if(finished):
					currentObjective['status'] = 'inProgress'
					if(currentObjective['pauseGame']):
						self.pauseGame = False
					
					self.cutScene.reset()

		# -----IF ONE SUBTARGET COMPLETED/DESTROYED
		if(currentObjective['objective']=='eliminate'):
			for target in currentObjective['targetObjects']:
				# if target dead or already removed from the enemy list
				if(target.alive==False or target not in self.enemyList):
					currentObjective['targetObjects'].remove(target)


		# -----SIGNAL OBJECTIVE COMPLETE
		if(currentObjective['objective']=='eliminate'):
			if(len(currentObjective['targetObjects'])<=0):
				currentObjective['status'] = 'signalComplete'



		# ---- MOVE TO NEXT OBJECTIVE, CONGRATULATE and POPULATE NEW OBJECTIVE TARGETS

		if(currentObjective['status']=='signalComplete'):
			sceneMessage = currentObjective['completionMessage']
			# OPEN WINDOW
			self.cutScene.runRHSCutScene(gui,game,scene='ally',underlay=True,orientation='topRight')
			# ANIMATE ONCE WINDOW OPEN
			if(self.cutScene.pannelOpen):
				gui.clareSmiling.animateNoRotation(gui,'claireTalking',[self.cutScene.imageLeftX,self.cutScene.imageY],game,repeat=False)
				
				self.cutScene.drawMask(gui,game,overlay=False,border='ally',codec=True)
				finished = self.cutScene.dialogue.drawScrollingDialogue(gui,game,self.cutScene.textW,self.cutScene.textH,gui.smallFont, sceneMessage, textStartingPos=(self.cutScene.textX ,self.cutScene.textY),colour=(51,189,251),closeOutDelay=True,maxLines=4,scrollInterval=0.02)
				
				if(finished):
					#NEXT OBJECTIVE 
					currentObjective['status'] = 'complete'
					self.currentObjective = currentObjective['nextObjective']
					
					# UNPAUSE AND RESET CUTSCENE STATE
					self.cutScene.reset()

					self.objectiveIntroState='notIntroduced'

					# IF ALL OBJECTIVES COMPLETE
					if(self.currentObjective==None or self.currentObjective=='complete'):
						self.scene = 'levelComplete'
					else:
						self.fieldNewObjective(gui,game)

		


		# ------********LEVEL SPECIFIC OBJECTIVE LOADING ******

	def fieldNewObjective(self,gui,game):

		# QUANDRANT AREA AND CURRENT OBJECIVE

		currentObjective = self.objectives[self.currentObjective]
		activeQuandrant  = currentObjective['activeQuandrant']
		

		# MODIFY ENEMY LIST TO ACTIVE ENEMIES ONLY
		for enemy in self.unfieldedEnemies:
			if(inQuandrant(enemy, activeQuandrant)):
				self.enemyList.append(enemy)


		# REBUILDING LIST DUE TO COMPLEXITY WITH HOLDING DICTS

		newList = []
		for u in range(len(self.unfieldedEnemies)):
			uE = self.unfieldedEnemies[u]
			remove= False
			
			for el in self.enemyList:
				if(el.id==uE.id and el.name ==uE.name):
					remove=True
			if(remove==False):
				newList.append(uE)

		self.unfieldedEnemies = newList


		# UPDATE TARGET OBJECTIVES (WE ONLY CARE ABOUT THE ONES WE WANT TO TAKE OUT)
		for enemy in self.enemyList:

			# OBJECTIVE 2

			if(enemy.name=='tank' and self.currentObjective=='destroyTanksQ1'):
				self.objectives['destroyTanksQ1']['targetObjects'].append(enemy)

			if(enemy.name=='mlrs' and self.currentObjective=='eliminateMissileBase'):
				self.objectives['eliminateMissileBase']['targetObjects'].append(enemy)

			if(enemy.name=='bioLab' and self.currentObjective=='destroyBioLab'):
				self.objectives['destroyBioLab']['targetObjects'].append(enemy)


	def quandrantManager(self,gui,game):

		# ----CLAMP PLAYER IN CURRENT QUADRANT
		if(self.currentObjective!= None and self.currentObjective != 'complete'):
			currentObjective = self.objectives[self.currentObjective]
			activeQuandrant  = currentObjective['activeQuandrant']

			self.player.leftBoundary  = activeQuandrant['x'] 
			self.player.rightBoundary  = activeQuandrant['x'] + activeQuandrant['w']
			self.player.topBoundary    = activeQuandrant['y']
			self.player.bottomBoundary = activeQuandrant['y'] + activeQuandrant['h'] - self.player.h








	# INIT LEVEL DESIGN 

	def initMe(self,gui,game):
		init(self,gui,game)

		# QUANDRANT AREA AND CURRENT OBJECIVE

		currentObjective = self.objectives[self.currentObjective]
		activeQuandrant  = currentObjective['activeQuandrant']


		# SET PLAYER INIT POSITION 

		self.player.x = activeQuandrant['x']+ 0.1*activeQuandrant['w']
		self.player.y = activeQuandrant['y']+ 0.95*activeQuandrant['h']


		# ONLY FIELD PLAYERS ACTIVE IN THIS QUADRANT

		self.unfieldedEnemies  = self.enemyList
		self.defaultEnemyList = self.enemyList
		self.enemyList  = []


		# MODIFY ENEMY LIST TO ACTIVE ENEMIES ONLY
		for enemy in self.unfieldedEnemies:
			if(inQuandrant(enemy, activeQuandrant)):
				self.enemyList.append(enemy)


		# REBUILDING LIST DUE TO COMPLEXITY WITH HOLDING DICTS
		newList = []
		for u in range(len(self.unfieldedEnemies)):
			uE = self.unfieldedEnemies[u]
			remove= False
			
			for el in self.enemyList:
				if(el.id==uE.id and el.name ==uE.name):
					remove=True
			if(remove==False):
				newList.append(uE)

		self.unfieldedEnemies = newList


		
		# Load selected enemies in range to given objectives
		for enemy in self.enemyList:
			if(enemy.name=='aaSmall'):
				self.objectives['destroyAAQ1']['targetObjects'].append(enemy)


def inQuandrant(unit, quandrant):
	if((unit.x > quandrant['x']) and (unit.x) < (quandrant['x'] + quandrant['w']) ):
		if(unit.y > quandrant['y'] and (unit.y+unit.h) < (quandrant['y'] + quandrant['h']) ):
			return(True)

	#print('{} {} {} failed '.format(str(unit.x),str(unit.y),str(unit.name)))
	return(False)


