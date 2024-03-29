from utils._utils import *
from utils._utils import stopTimer
from scenes.profile import *
from scenes.settings import *
import random


class introScreen():
	def __init__(self,gui):
		self.state      = 'start'
		self.textState  = None
		self.fadeState  = None
		self.timer      = stopTimer()
		self.timer2     = stopTimer()
		self.timer3     = stopTimer()
		self.timer4     = stopTimer()
		self.introY     = None
		self.menuImage  = random.choice([gui.bunnyGirlYCover,gui.madgeInv,gui.bunnyTank,gui.apacheJack,gui.sarah])
		#self.menuImage  = gui.bunnyGirlYCover

		self.dynamicBorder = dynamicBorder(borderColour=(60,60,200),noShadeShifts=10)
		

		# alpha overlay
		self.alphaI         = 100      # used on fade out (goes up to 255)
		self.fadeSurface    = pygame.Surface((gui.w,gui.h))


		# TITLE BUTTONS SELECTED
		self.buttonIndex      = 0


		# PROFILE 

		self.profile    = profilePage(gui)
		self.settings   = settingsPage(gui)



	def mainMenu_and_startup(self,gui,game):


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
			fadeReady    = self.timer4.stopWatch(1,'fade in',self.textState,game)
			startup      = self.timer.stopWatch(2,'intro',self.textState,game)

			
			dcy = 0.15*gui.h
			fsH   = 0.8*gui.h
			h2022 = 0.85*gui.h
			
			# LOGO IMAGE 
			drawImage(gui.screen,gui.cover1,(0.5*(gui.w-gui.cover1.get_width()),0.44*(gui.h-gui.cover1.get_height())))
			# 2022
			drawText(gui,smallTitleFont, '2022',0.9*gui.w,h2022, 0.2*gui.w,colour=(100, 100, 200))
			
			if(fadeReady):
				self.fadeSurface.set_alpha(self.alphaI)
				self.fadeSurface.fill((0,0,0))
				gui.screen.blit(self.fadeSurface,(0,0))
			if(startup):		
				drawImage(gui.screen,gui.coverLogo,(0.5*(gui.w-gui.coverLogo.get_width()),50))
				#drawText(gui,titleFontB, 'Steel Spirit',gui.x,dcy, gui.w,colour=(129, 212, 250),center=gui.w,pos=None)
				subtitle = self.timer2.stopWatch(1,'intro',self.textState,game)
				if(subtitle):
					drawText(gui,titleFont, 'First Strike',gui.x,fsH, gui.w,colour=gui.white,center=gui.w,pos=None)
					title = self.timer3.stopWatch(1,'intro',self.textState,game)
					if(title):
						drawBlinkingText(gui.screen,gui.bigNokiaFont, 'Press Start',0.44*gui.w,0.65*gui.h, colour=(255, 255, 30))

			gui.input.processInput()
			if(gui.input.returnedKey=='ENTER'):
				self.state = 'menu'
				gui.input.returnedKey=''

		if(self.state=='menu'):


			pygame.draw.rect(gui.screen,(5,9,20),(0.05*gui.w, 0.05*gui.h,0.9*gui.w ,0.9*gui.h))
			# ANIMATE PLANET 

			drawImage(gui.screen,self.menuImage,[0,0])
			


			# DRAWS BORDER 

			self.dynamicBorder.animateBorder('menu border',game,gui)
			chosenFont = gui.largeFont
			borderColour=(60,60,200)
			
			tw,th   = getTextWidth(chosenFont,'A menu item yep sure.'),getTextHeight(chosenFont,'A menu item yep sure.')

			
			# MANAGE DPAD CONTROL OF BUTTONS 
			buttonColourList = [(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)]
			if(gui.input.returnedKey.upper()=='S'): self.buttonIndex  +=1
			if(gui.input.returnedKey.upper()=='W'): self.buttonIndex  -=1
			if(self.buttonIndex<0): self.buttonIndex = len(buttonColourList) -1
			if(self.buttonIndex>len(buttonColourList)-1): self.buttonIndex = 0
			backColour                   = buttonColourList
			backColour[self.buttonIndex] = darken(borderColour,60)




			startGame,tex,tey       = simpleButton(0.8*(gui.w-tw),0.3*gui.h,'Start Game',gui,chosenFont,setTw=tw,backColour=backColour[0],borderColour=borderColour, textColour=(255,255,255),hoveredColour=(0,0,0))

			profile,tex,tey         = simpleButton(0.8*(gui.w-tw),tey + 0.8*th,'Profile',gui,chosenFont,setTw=tw,backColour=backColour[1],borderColour=borderColour, textColour=(255,255,255),hoveredColour=(0,0,0))

			loadGame,tex,tey        = simpleButton(0.8*(gui.w-tw),tey + 0.8*th,'Load Game',gui,chosenFont,setTw=tw,backColour=backColour[2],borderColour=borderColour, textColour=(255,255,255),hoveredColour=(0,0,0))

			newMapEditor,tex,tey    = simpleButton(0.8*(gui.w-tw),tey + 0.8*th,'New Map Editor',gui,chosenFont,setTw=tw,backColour=backColour[3],borderColour=borderColour, textColour=(255,255,255),hoveredColour=(0,0,0))

			mapEditor,tex,tey       = simpleButton(0.8*(gui.w-tw),tey + 0.8*th,'Map Editor',gui,chosenFont,setTw=tw,backColour=backColour[4],borderColour=borderColour, textColour=(255,255,255),hoveredColour=(0,0,0))

			settings,tex,tey        = simpleButton(0.8*(gui.w-tw),tey + 0.8*th,'Settings',gui,chosenFont,setTw=tw,backColour=backColour[5],borderColour=borderColour, textColour=(255,255,255),hoveredColour=(0,0,0))

			
			# IF ENTER PRESSED - SELECT THE CHOSEN BUTTON
			if(gui.input.returnedKey=='return'):
				startGame    = 0==self.buttonIndex
				profile      = 1==self.buttonIndex
				newMapEditor = 3==self.buttonIndex
				mapEditor    = 4==self.buttonIndex
				settings    = 5==self.buttonIndex
				gui.input.returnedKey       = ''



			if(startGame  ):
				game.state = 'start'
				self.state = 'finish'

			if(profile  ):
				self.state = 'profile'

			if(newMapEditor):
				game.state = 'newMapEditor'
				self.state = 'title'

			if(mapEditor):
				game.state = 'editor'
				self.state = 'title'
			
			if(settings  ):
				self.state = 'settings'

		if(self.state=='profile'):
			self.profile.renderProfile(gui,game)
		
		if(self.state=='settings'):
			self.settings.renderSettings(gui,game)


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

