from units.parent import *
from utils.gameUtils import *
from utils._utils import imageAnimateAdvanced,loadingBarClass
from units.missile import *
import pygame

class mlrs(parent):
	def __init__(self,_id,gui,x=None,y=None):
		super().__init__(gui)
		# MAIN OVERRIDES 
		self.id             = _id
		self.name           = 'mlrs'
		self.kind           = 'structure'
		self.images         = imageAnimateAdvanced(gui.mlrs,0.2)
		self.turretImage    = imageAnimateAdvanced(gui.mlrsTurret,0.2)
		self.shadow         = imageAnimateAdvanced(gui.mlrsShadow,0.2)
		self.x,self.y       = 500,500
		if(x!=None): self.x = x
		if(y!=None): self.y = y
		self.w              = int(gui.mlrs[0].get_width())
		self.h              = int(gui.mlrs[0].get_height())
		self.turretFacing   = self.facing
		#self.centerPoint    = [76,75]
		
		# HIT IMAGE
		self.hitImage         = gui.tankHit
		self.hitAnimation     = imageAnimateAdvanced(gui.mlrsHit,0.2)
		self.turretHitImg     = imageAnimateAdvanced(gui.mlrsTurretHit ,0.2)
		self.hitsTaken        = 0

		# REMAINS IMAGE 
		self.remainsAnimation = imageAnimateAdvanced(gui.mlrsRemains,0.2)



		# HEALTHBAR 
		self.healthBar      = loadingBarClass(self.w,0.2*self.h,(80,220,80),(220,220,220),(0,0,200))
		self.blitPos        = None
		self.turretPos      = None

		self.state             = 'patrol'
		self.patrolLocations   = [(self.x,self.y),(self.x+700,self.y),(self.x+700,self.y+200),(self.x,self.y+200)] 
		self.currentLocIndex   = 0


		# CLASS OVERRIDES
		self.hp              = 300
		self.defaultSpeed    = 1
		self.maxSpeed        = 1
		self.maxSpeedDefault = 1

		# ENEMY COORDS 

		self.angleDiffToEnemy = 0
		self.DistanceToEnemy  = 50000
		self.enemyTargetAngle = 0
		self.defenceSector    = self.patrolLocations[0]

		# SHOOT 
		self.bulletTimer        = stopTimer()           # BUFF
		self.shootDelay         = 0.1                   # BUFF
		self.bulletsFired       = 0
		self.burstTimer         = stopTimer()
		self.burstCoolDown      = False
		self.burstLimit         = 4
		self.burstCount         = 0
		self.burstDelay         = 2

		self.missileType	     = 'streakerGray'
		self.availableMissiles   = ['streakerGray']
		self.missileAttrs        = { 'streaker':{'speed':3,'damage':20},'streakerGray':{'speed':3,'damage':20} }
		self.missileFiring      = False
		self.missilesFired      = 0
		self.missileTimer       = stopTimer()
		self.missileDelay       = 2

	# AI LOGIC
	def actions(self,gui,game,lv):

		# ENSURE VECHICLE DOESN'T EXCEED BOUNDARIES
		self.stayOnField(lv)


		# -----------GET DISTANCE TO ENEMY
		angleDiffToEnemy,DistanceToEnemy,enemyTargetAngle = turretAngleToTarget(self,self.x,self.y,lv.player.x,lv.player.y)
		turretFaceTarget(self,angleDiffToEnemy, turnIcrement=2)
		
		if(DistanceToEnemy<0.7*gui.h):
			self.launchMissiles(game,lv,gui)





	# CALLED BY allyActions/enemyActions
	def shoot(self,gui,lv,game,bulletSpeed=10, bulletColour=(255,177,42)):

		# BULLET DELAY TIMER
		shotAvailable = self.bulletTimer.stopWatch(self.shootDelay,'shoot at player', str(self.id + self.bulletsFired), game,silence=True)
		
		# BURST WAIT TIMER 
		if(self.burstCoolDown):
			burstReset = self.burstTimer.stopWatch(self.burstDelay,'burstCoolDown', str(self.id + self.bulletsFired), game,silence=True)
			
			if(burstReset):
				self.burstCoolDown=False
				self.burstCount = 0
		
		# IF SHOOT CRITEREA MET,
		if((shotAvailable and self.blitPos!=None and self.burstCoolDown==False)):

				self.bulletsFired +=1
				self.burstCount   += 1
				# ADDS BULLET TO BULLET LIST
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(bullet(gui,self.turretPos['midTop'][0] + gui.camX,self.turretPos['midTop'][1]+ gui.camY,bid,self.classification, self.turretFacing,'mlrs', speed=7,damage=2,colour=[200,80,20],w=10,h=10 ))

				if(self.burstCount > self.burstLimit):
					self.burstCoolDown = True

	def launchMissiles(self,game,lv,gui):




		if((self.missileFiring==False and self.turretPos!=None)):	
			if(self.missileType in ['streaker','streakerGray']):
				self.missilesFired +=4
				
				#ADDS MISSILES TO BULLET LIST
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(missile(gui,self.turretPos['midTop'][0] + gui.camX,self.turretPos['midTop'][1]+ gui.camY,bid,self.classification, self.turretFacing,self.missileType, speed=self.missileAttrs[self.missileType]['speed'],damage=self.missileAttrs[self.missileType]['damage'],jink='left',lockedOnEnemy=lv.player,source='enemy'))
				
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(missile(gui,self.turretPos['midTop'][0] + gui.camX,self.turretPos['midTop'][1]+ gui.camY,bid,self.classification, self.turretFacing,self.missileType, speed=self.missileAttrs[self.missileType]['speed'],damage=self.missileAttrs[self.missileType]['damage'],jink='right',lockedOnEnemy=lv.player,source='enemy'))
				

				#ADDS MISSILES TO BULLET LIST
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(missile(gui,self.turretPos['center'][0] + gui.camX,self.turretPos['center'][1]+ gui.camY,bid,self.classification, self.turretFacing,self.missileType, speed=self.missileAttrs[self.missileType]['speed'],damage=self.missileAttrs[self.missileType]['damage'],jink='farleft',lockedOnEnemy=lv.player,source='enemy'))
				
				bid = max(([x.id for x in lv.bulletList]),default=0) + 1
				lv.bulletList.append(missile(gui,self.turretPos['center'][0] + gui.camX,self.turretPos['center'][1]+ gui.camY,bid,self.classification, self.turretFacing,self.missileType, speed=self.missileAttrs[self.missileType]['speed'],damage=self.missileAttrs[self.missileType]['damage'],jink='farright',lockedOnEnemy=lv.player,source='enemy'))
				



				self.missileFiring = True

		#  RESET WHEN TIME REACHED
		if(self.missileFiring == True):
			# BULLET DELAY TIMER
			missilesReady = self.missileTimer.stopWatch(self.missileDelay,'mlrs shoot missile', str(self.id + self.missilesFired), game,silence=True)
			# READY TO FIRE AGAIN
			if((missilesReady )):
				self.missileFiring = False








	# DRAW REMNANTS AFTER BEING DESTROYED
	def drawRemains(self,gui,lv,game):
		x,y = self.x - gui.camX,self.y  - gui.camY

		# *******BE CAREFUL ABOUNT ON SCREEN
		if(self.alive==False and onScreen(self.x,self.y,self.w,self.h,gui) and self.destructionComplete):
			self.remainsAnimation.animate(gui,str('smouldering MLRS remains'),[x,y],game,rotation=self.facing-90,repeat=True)


	def drawSelf(self,gui,game,lv):
		x,y = self.x - gui.camX,self.y  - gui.camY
		
		shadow_x = x + 20
		shadow_y = y + 20
		self.shadow.animate(gui,'aa shadow',[shadow_x,shadow_y],game,rotation=self.facing-90)

		if(self.alive==True and onScreen(self.x,self.y,self.w,self.h,gui) and not self.hit):
			
			animate,self.blitPos     = self.images.animate(gui,'tank' + str(self.id),[x,y],game,rotation=self.facing-90)
			turretAnimage,self.turretPos  = self.turretImage.animate(gui,'turret' + str(self.id),[x,y],game,rotation=self.turretFacing-90)

			#pygame.draw.circle(gui.screen, (244,0,0), (self.patrolLocations[self.currentLocIndex][0]- gui.camX ,self.patrolLocations[self.currentLocIndex][1]- gui.camY) , 15, 0)

		if(self.hit):

			x,y = self.x - gui.camX,self.y  - gui.camY
			
			if(self.alive==True and onScreen(self.x,self.y,self.w,self.h,gui)):
				
				complete,imageParms            = self.hitAnimation.animate(gui,str(self.hitsTaken) + ' hit',[x,y],game,rotation=self.facing-90,repeat=True)
				turretComplete,self.turretPos  = self.turretHitImg.animate(gui,str(self.hitsTaken) + ' hit',[x,y],game,rotation=self.turretFacing-90,repeat=True)

				if(complete and turretComplete):
					self.turretHitImg.reelComplete = False
					self.hit = False
					self.hitsTaken +=1


