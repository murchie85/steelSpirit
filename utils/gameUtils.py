
import pickle 
import math


def onScreen(unit,gui):
	onScreen = True

	# NEED TO CHECK CAMERA

	return(onScreen)

def clamp(value,clampValue):

	if(value>0):
		if(value>=clampValue):
			return(clampValue)
		return(value)

	if(value<0):
		if(value<= -clampValue):
			return(-clampValue)
		return(value)

	return(value)


def zero(value,decrease):

	if(value>0):
		value -= decrease
		if(value<0): 
			value = 0
		return(value)
	
	if(value<0):
		value += decrease
		if(value>0): 
			value = 0
		return(value)

	return(value)






# RETURNS ANGLE AND DISTANCE TO TARGET 
def angleToTarget(self,selfX,selfY, targetObjectX,targetObjectY):
	# GET VECTOR DIST
	xDelta        =  targetObjectX - selfX
	yDelta        =  targetObjectY - selfY
	# GET ANGLE FROM 
	targetAngleR  =  math.atan2(yDelta,xDelta) * 180/math.pi
	targetAngle   = 360-(targetAngleR) 
	
	# WRAP ANGLE
	if(targetAngle>360):
		targetAngle = targetAngle%360


	# CALCULATE ANGLE DIFF
	angleDifference = (self.facing - targetAngle + 180 + 360) % 360 - 180
	

	distance = math.sqrt((xDelta)**2+(yDelta)**2)
	return(int(angleDifference),distance,targetAngle)


# WRAPS 360 OR 0 
def wrapAngle(facing):
	
	# ----WRAP ANGLE 
	if(facing>360): facing =  facing%360
	if(facing<0): facing = facing%360

	return(facing)

# UPDATES SELF.FACING CLASS 
def faceTarget(self,angleDifference, turnIcrement=3):

	# WRAP FACING ANGLE

	#  IF ITS WITHIN 1
	if(abs(angleDifference)<=1):
		self.facing = wrapAngle(self.facing)
	elif(abs(angleDifference)<turnIcrement):
		if(angleDifference<0): 
			self.facing += abs(angleDifference)
		# IF ITS LEFT OF
		elif(angleDifference>0): 
			self.facing -= abs(angleDifference)

	# IF RIGHT OF
	elif(angleDifference<0): 
		self.facing += turnIcrement
	# IF ITS LEFT OF
	elif(angleDifference>0): 
		self.facing -= turnIcrement
	
	self.facing = wrapAngle(self.facing)

	if(abs(angleDifference)<=turnIcrement+1):
		return(True)
	else:
		return(False)



def getDistance(selfX,selfY,targetObjectX,targetObjectY,offset=False):
	xDelta        =  targetObjectX - selfX
	yDelta        =  targetObjectY - selfY
	
	if(offset):
		# OFFSET IS USUALLY AD CAM POS - HALF IMAGE W/H
		xDelta        =  targetObjectX - selfX + offset[0] 
		yDelta        =  targetObjectY - selfY + offset[1]

	distance = math.sqrt((xDelta)**2+(yDelta)**2)
	return(distance)



# --- Collides with using radius, doesn't quite have spacing right

def collidesWith(self,enemy,spacing=1):
	
	# WORK OUT THE BIGGEST RADIUS
	radius = self.w+enemy.w
	if((self.h + enemy.h) > radius): radius = self.h + enemy.h

	# if x/y average distance scaler less than half radius
	if(math.sqrt((enemy.x-self.x)**2+(enemy.y-self.y)**2)<= 0.5*(radius) + spacing ):
		return(True)

	return(False)



# LATER ADD MODIFIER SPECIFIC TO OBJECT THAT PASES HITBOX %

def collidesWithHitBox(self,enemy):

  # Check if the self's x-coordinate is within the enemy's x-coordinate range
  if self.x >= enemy.x and self.x <= enemy.x + enemy.w:
    # Check if the self's y-coordinate is within the enemy's y-coordinate range
    if self.y >= enemy.y and self.y <= enemy.y + enemy.h:
      return (True)
 
  # Check if the enemy's x-coordinate is within the self's x-coordinate range
  if enemy.x >= self.x and enemy.x <= self.x + self.w:
    # Check if the enemy's y-coordinate is within the self's y-coordinate range
    if enemy.y >= self.y and enemy.y <= self.y + self.h:
      return (True)
  return (False)




# REMOVES ENEMY FROM LIST
def killme(self,lv,killMesssage=None,printme=False):
	
	# REMOVE FROM LIST
	if(self.classification=='ally'):
		for i in lv.allyList:
			if(self.id==i.id):
				self.alive = False
				lv.allyList.remove(self)
				lv.deadList.append(self)
				if(printme):
					print(self.classification +  ' ' + str(self.id)  + " : has been KIA." + str(killMesssage))
				
				lv.log.append(self.classification +  ' ' + str(self.id)  + " : has been KIA." + str(killMesssage))
	
	if(self.classification=='enemy'):

		# REMOVE FROM LIST
		for j in lv.enemyList:
			if(self.id==j.id):
				self.alive = False
				lv.enemyList.remove(self)
				lv.deadList.append(self)
				if(printme):
					print(self.classification +  ' ' + str(self.id)  + " : has been KIA." + str(killMesssage))
				lv.log.append(self.classification +  ' ' + str(self.id)  + " : has been KIA." + str(killMesssage))




# HELICOPTER STYLE CONTROL SYSTEM

def copterControls(self,pressedKeys,lv):

	# ACCELELRATION FLAG
	vAccell,hAccell = False,False
	# GET DIRECTION OF ACCELLERATION
	if('W' in pressedKeys ):
		self.vSpeed -= 0.4
		vAccell = True
	if('S' in pressedKeys):
		self.vSpeed += 0.4
		vAccell = True
	if('D' in pressedKeys):
		self.hSpeed += 0.4
		hAccell = True
	if('A' in pressedKeys):
		self.hSpeed -= 0.4
		hAccell = True

	#---------ROTATION

	if('H' in pressedKeys ):
		self.facing += self.rotationSpeed


	if('J' in pressedKeys ):
		self.facing -= self.rotationSpeed

	# SLOW DOWN IF NOT ACCELLERATING
	if(hAccell==False): self.hSpeed = zero(self.hSpeed,self.decelleration)
	if(vAccell==False): self.vSpeed = zero(self.vSpeed,self.decelleration)


	# BORDER CLAMP

	if(self.x + self.w > lv.mapw): self.x -= self.maxHSpeed
	if(self.x < lv.mapx): self.x += self.maxHSpeed
	if(self.y + self.h > lv.maph): self.y -= self.maxVSpeed
	if(self.y < lv.mapy): self.y += self.maxVSpeed

	
	# CLAMP SPEEDS
	self.hSpeed = clamp(self.hSpeed,self.maxHSpeed)
	self.vSpeed = clamp(self.vSpeed,self.maxVSpeed)

	# UPDATE POSITION
	self.x += self.hSpeed
	self.y += self.vSpeed

