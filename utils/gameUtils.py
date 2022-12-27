
import pickle 
import math

"""

- onScreen
- clamp
- zero
- angleToTarget
- wrapAngle
- faceTarget
- getDistance
- collidesWith
- collidesWithHitBox
- killme
- createFid
- Detection Cone 


"""



"""
DEFINE VIEPORT HERE (JUST DO OVERLAY, NOT RESTRICT)
"""
def onScreen(xOrign,yOrign,w,h,gui):
	onScreen = False
	if((xOrign+w > gui.camX) and (xOrign<gui.camX+gui.camW)):
		if((yOrign+h > gui.camY) and (yOrign<gui.camY+gui.camH)):
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
	targetAngle = wrapAngle(targetAngle)


	# CALCULATE ANGLE DIFF
	angleDifference = (self.facing - targetAngle + 180 + 360) % 360 - 180

	#angleDifference = wrapAngle(angleDifference)
	

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



# RETURNS ANGLE AND DISTANCE TO TARGET 
def turretAngleToTarget(self,selfX,selfY, targetObjectX,targetObjectY):
	# GET VECTOR DIST
	xDelta        =  targetObjectX - selfX
	yDelta        =  targetObjectY - selfY
	# GET ANGLE FROM 
	targetAngleR  =  math.atan2(yDelta,xDelta) * 180/math.pi
	targetAngle   = 360-(targetAngleR) 
	
	# WRAP ANGLE
	targetAngle = wrapAngle(targetAngle)


	# CALCULATE ANGLE DIFF
	angleDifference = (self.turretFacing - targetAngle + 180 + 360) % 360 - 180

	#angleDifference = wrapAngle(angleDifference)
	

	distance = math.sqrt((xDelta)**2+(yDelta)**2)
	return(int(angleDifference),distance,targetAngle)


# UPDATES SELF.turretFacing CLASS 
def turretFaceTarget(self,angleDifference, turnIcrement=3):

	# WRAP turretFacing ANGLE

	#  IF ITS WITHIN 1
	if(abs(angleDifference)<=1):
		self.turretFacing = wrapAngle(self.turretFacing)
	elif(abs(angleDifference)<turnIcrement):
		if(angleDifference<0): 
			self.turretFacing += abs(angleDifference)
		# IF ITS LEFT OF
		elif(angleDifference>0): 
			self.turretFacing -= abs(angleDifference)

	# IF RIGHT OF
	elif(angleDifference<0): 
		self.turretFacing += turnIcrement
	# IF ITS LEFT OF
	elif(angleDifference>0): 
		self.turretFacing -= turnIcrement
	
	self.turretFacing = wrapAngle(self.turretFacing)

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



def createFid(self):
	rfid = max(self.fids,default=0) + 1
	self.fids.append(rfid)
	return(rfid)





def detectionCone(x,y,gui,facing,cone_length=200,cone_angle=100):
		
		# Define the cone of vision properties
		cone_length = cone_length
		cone_angle = cone_angle

		# Calculate the radius of the cone at the base
		cone_radius = math.sqrt(cone_length**2 / 4 + cone_length**2 * math.tan(math.radians(cone_angle/2))**2)

		# Calculate the x and y coordinates of the end of the cone
		end_x = x + cone_length * math.cos(math.radians(facing))
		end_y = y + cone_length * math.sin(math.radians(facing))

		# Create a list of points to define the shape of the cone
		cone_points  = [(x, y)]
		cone_points += [(x + cone_radius * math.cos(math.radians(angle)), y + cone_radius * math.sin(math.radians(angle))) for angle in range(round(facing - cone_angle/2), round(facing + cone_angle/2 + 1))]
		return(cone_points)
		