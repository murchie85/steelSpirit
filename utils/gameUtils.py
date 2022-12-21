
import pickle 


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


# SAVE FILE 

def save_dict_as_pickle(dictionary, file_path):
  try:
    with open(file_path, 'wb') as file:
      pickle.dump(dictionary, file)
  except Exception as e:
    print(f'Error saving dictionary to {file_path}: {e}')
    exit()

# LOAD
def load_pickle(file_path):
  try:
    with open(file_path, 'rb') as file:
      return pickle.load(file)
  except Exception as e:
    print(f'Error loading pickle from {file_path}: {e}')
    exit()




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

