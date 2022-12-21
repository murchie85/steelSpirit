from utils._utils import *
from utils._utils import stopTimer
from scenes.profile import *
import random


class introScreen():
	def __init__(self,gui):
		self.state      = 'start'
		self.textState  = None
		self.fadeState  = None
		self.timer      = stopTimer()
		self.timer2     = stopTimer()
		self.timer3     = stopTimer()
		self.introY     = None

		self.dynamicBorder = dynamicBorder(borderColour=(60,60,200),noShadeShifts=10)
		self.reels         = []
		for x in range(7):
			self.reels.append({'cometReel':imageAnimateAdvanced(gui.blueFire,0.3),'x':random.randrange(0,1500),'y':random.randrange(-500,0),'skip':False} )
		
		self.bfReel        = imageAnimateAdvanced(gui.blueFire,0.3)


		# PROFILE 

		self.profile   = profilePage(gui)



	def showstartup(self,gui,game):


		if(self.state=='start'):


			# FADE IN 
			complete = self.fadeInOut(gui,game,'intro logo',['McMurchie Games', 'Presents'],gui.white,fadeInTime=1,fadeoutTime=2)
			if(complete):
				self.state='intro'

			gui.input.processInput()
			if(gui.input.returnedKey=='ENTER'):
				self.state='intro'
				gui.input.returnedKey=''

		if(self.state=='intro'):
			message = "In 2099 the year of our lord, despite all the progress in repairing our world, humanity was brought to the precipise of anhialation. \nVindictive lifeforms residing from the stars and the depths of our oceans, launched an all out assault on the earth. \nFor two long years we fought, we were ravaged and systematically exterminated, everyday brought us closer to the brink. After several nuclear holocausts, in our despair and desperation humanity unleashed the most powerful weapon in its arsenal: Ultima-net. A new race of hyper advanced AIs were born. Soon they formed an alliance with humans known as the forum, signing the scorched-earth directive with immediate effect. Factories around the world were repurposed to devote all resources on drone production. Combining their forces, the forum aliance coordinated a last ditch Counter-Strike: which saw the deployment of a hundred million drones, after a brief but decisive battle, the invaders to their knees, humanity was free once again. \n \n Soon after, humans and their digital equals built a new world, forming an uneasy peace with the aliens. Soon factions emerged, the tainted earth and ravaged economy brought about the rise of the hacker nation, who hijacked drone armies and tore down world governments, re-introducing uncertainty into the world. \nToday, nothing is a sure thing, the only constant is drones,  "
			message = "In 2099 the year of our lord, humanity was brought to the precipise of anhialation. \nCombined assults from the oceans and the stars, saw jealous visitors seek to erradicate and sterilize the earth. In a last ditch gesture, humans unleashed the Ultima-net. \n \n Within days a new race of hyper intelligent AIs were born, they quickly formed an alliance with the humans and started building millions of drones. In a decisive Counter Strike the visitors were brought to their knees, forcing them to negotiate reigning in a new era of peace and stability. \n \n The unexpected success of the drones affectived society deeply, humans, aliens and AIs alike saught them out, for business, for status and for power. Earth and the outer planets were plunged into a series of cold wars and gold rushes once again bringing about uncertainty and instability. Soon religions and myths emerged, prophecising the coming of an individual who could reign in the era of drones, bringing peace and prosperity to the world. Others talked about a great leader who could unite the drone factions, for years the planets speculated on this person, who they would be, who would be ..... \n \n \n THE DRONE COMMANDER."
			message = "In 2099 the year of our lord, humanity was brought to the precipise of anhialation. \nCombined assults from the oceans and the stars, saw jealous visitors seek to erradicate and sterilize the earth. \n In a last ditch gesture, humans unleashed the Ultima-net. \n \n A new race of hyper intelligent machines were born, they immediately began building millions of drones. In a decisive Counter Strike the visitors were brought to their knees. \n \n The unexpected success of the drones affected society deeply, humans, aliens and AIs alike saught them out, for business, for status and for power. This obsession soon plunged the Earth into chaos. Today it is said that a person will emerge, who will unite the drone factions and reign in the era of drones, bringing peace and prosperity to the world. This person is known as.... \n \n \n THE DRONE COMMANDER."
			message = message.upper()
			font = gui.fontTerminatorL
			if(self.introY==None): self.introY =1.05*gui.h
			textList = textWordWrap(message,font,(0,0,200),0.8*gui.w,margin=0.75,marginMax=0.85)
			x,y = 0.15*gui.w,self.introY
			for textsurface in textList:
				gui.screen.blit(textsurface,(x,y))
				y+= 1.5*getTextHeight(font,'SSS')

			self.introY -= 0.3

			gui.input.processInput()
			if(gui.input.returnedKey=='ENTER'):
				self.state='title'
				gui.input.returnedKey=''



		if(self.state=='title'):
			titleFont      = gui.titleFont
			titleFontB     = gui.titleFontB
			smallTitleFont = gui.smallNokiaFont
			pygame.draw.rect(gui.screen, (gui.colourA), [0.05*gui.w, 0.05*gui.h,0.9*gui.w ,0.9*gui.h],4)
			startup = self.timer.stopWatch(1,'intro',self.textState,game)
			dcy = 0.15*gui.h
			fsH   = 0.8*gui.h
			h2022 = 0.85*gui.h
			
			# LOGO IMAGE 
			drawImage(gui.screen,gui.titleLogo,(0.5*(gui.w-gui.titleLogo.get_width()),0.44*(gui.h-gui.titleLogo.get_height())))
			
			# 2022
			drawText(gui,smallTitleFont, '2022',0.9*gui.w,h2022, 0.2*gui.w,colour=(100, 100, 200))
			if(startup):
				drawText(gui,titleFontB, 'DRONE COMMANDER',gui.x,dcy, gui.w,colour=(129, 212, 250),center=gui.w,pos=None)
				subtitle = self.timer2.stopWatch(1,'intro',self.textState,game)
				if(subtitle):
					drawText(gui,titleFont, 'FIRST STRIKE',gui.x,fsH, gui.w,colour=gui.white,center=gui.w,pos=None)
					title = self.timer3.stopWatch(1,'intro',self.textState,game)
					if(title):
						drawBlinkingText(gui.screen,gui.nokiaFont, 'Press Start',0.44*gui.w,0.65*gui.h, colour=(100, 100, 200))

			gui.input.processInput()
			if(gui.input.returnedKey=='ENTER'):
				self.state = 'menu'
				gui.input.returnedKey=''

		if(self.state=='menu'):


			pygame.draw.rect(gui.screen,(5,9,20),(0.05*gui.w, 0.05*gui.h,0.9*gui.w ,0.9*gui.h))
			# ANIMATE PLANET 

			drawImage(gui.screen,gui.planet,[0.05*gui.w, 0.3*gui.h],trim=(0*gui.w,0.05*gui.h,gui.w,0.65*gui.h))
			


			# ANIMATE COMMETS 

			for i in range(len(self.reels)):
				j = self.reels[i]
				j['x'] -= 5
				j['y'] += 5



				# RESET COORDINATES
				if(j['y']> gui.h and j['x'] < 0 ): j['x'],j['y']= random.randrange(0,gui.w+300),random.randrange(-500,0)

				# CHANGE SLIDES BASED ON POSITION
				if(j['x'] < 799 and j['cometReel'].imageFrames  != gui.bluefireEntry and j['y'] > 450):
					j['cometReel'].imageFrames  = gui.bluefireEntry
					j['cometReel'].currentFrame = 0
					j['cometReel'].changeCount  = 0
				if(j['x'] < 500 and j['cometReel'].imageFrames== gui.bluefireEntry and j['cometReel'].currentFrame > len(j['cometReel'].imageFrames)-2 ):
					j['skip']=True

				elif(j['x'] > 799 and j['cometReel'].imageFrames  != gui.blueFire):
					j['cometReel'].imageFrames  = gui.blueFire
					j['cometReel'].currentFrame = 0
					j['cometReel'].changeCount  = 0
					j['skip']=False

				
				# RENDER IMAGE IF IN BOX
				imgWidth,imageHeight = j['cometReel'].imageFrames[0].get_width(),j['cometReel'].imageFrames[0].get_height()
				if(j['x']-imgWidth<0.05*gui.w or j['x'] > 0.9*gui.w or j['y'] < 0.05*gui.h or j['y']+imageHeight > 0.9*gui.h or j['skip']):
					pass
				else:
					j['cometReel'].animate(gui,'blueFire',(j['x'],j['y']),game,rotation=0)


			# DRAWS BORDER 

			self.dynamicBorder.animateBorder('menu border',game,gui)
			chosenFont = gui.largeFont
			borderColour=(60,60,200)
			
			tw,th   = getTextWidth(chosenFont,'A menu item yep sure.'),getTextHeight(chosenFont,'A menu item yep sure.')

			profile,tex,tey     = simpleButton(0.5*(gui.w-tw),0.4*gui.h,'Profile',gui,chosenFont,setTw=tw,backColour=(0,0,0),borderColour=borderColour, textColour=(255,255,255))

			startGame,tex,tey    = simpleButton(0.5*(gui.w-tw),tey + 0.8*th,'Start Game',gui,chosenFont,setTw=tw,backColour=(0,0,0),borderColour=borderColour, textColour=(255,255,255))

			loadGame,tex,tey    = simpleButton(0.5*(gui.w-tw),tey + 0.8*th,'Load Game',gui,chosenFont,setTw=tw,backColour=(0,0,0),borderColour=borderColour, textColour=(255,255,255))

			mapEditor,tex,tey   = simpleButton(0.5*(gui.w-tw),tey + 0.8*th,'Map Editor',gui,chosenFont,setTw=tw,backColour=(0,0,0),borderColour=borderColour, textColour=(255,255,255))

			settings,tex,tey    = simpleButton(0.5*(gui.w-tw),tey + 0.8*th,'Settings',gui,chosenFont,setTw=tw,backColour=(0,0,0),borderColour=borderColour, textColour=(255,255,255))



			if(startGame):
				game.state = 'start'
				self.state = 'finish'

			if(profile):
				self.state = 'profile'

			if(mapEditor):
				game.state = 'editor'
				self.state = 'title'

		if(self.state=='profile'):
			self.profile.renderProfile(gui,game)


	def fadeInOut(self,gui,game,uniqueMessage,messageList,textColour,fadeInTime=1,fadeoutTime=2):
		
		if(self.fadeState==None):
			startup = self.timer.stopWatch(1,uniqueMessage+'startup',game.state + uniqueMessage,game)
			if(startup):
				drawText(gui,gui.bigFont, messageList[0],gui.x,0.4*gui.h, gui.w,colour=textColour,center=gui.w,pos=None)
				if(len(messageList)==2):
					drawText(gui,gui.bigFont, messageList[1],gui.x,0.46*gui.h, gui.w,colour=textColour,center=gui.w,pos=None)
				fadeComplete = gui.fadeIn(game.state,inc=fadeInTime)
				if(fadeComplete): 
					self.fadeState='fadeout'
					gui.resetFadeIn = True
		# FADE OUT
		if(self.fadeState=='fadeout'):
			drawText(gui,gui.bigFont, messageList[0],gui.x,0.4*gui.h, gui.w,colour=textColour,center=gui.w,pos=None)
			if(len(messageList)==2):
				drawText(gui,gui.bigFont, messageList[1],gui.x,0.46*gui.h, gui.w,colour=textColour,center=gui.w,pos=None)
			fadeComplete = gui.fadeOut(game.state,inc=fadeoutTime)
			if(fadeComplete): 
				return(True)

		return(False)

