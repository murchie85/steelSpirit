import pygame
import math
from pygame.locals import *
from utils._utils import stopTimer
import time




"""
GUI 

- Border
- mouseCollides
- fadeIn
- fadeOut
- boxOut
- classDebug


"""

class gui():
    def __init__(self,screen,width,height,guiTheme,IMAGEASSETPATH):
        self.clicked         = False
        self.rightClicked    = False
        self.pressed         = False
        self.KEYDOWN         = False
        self.scrollUp        = False
        self.scrollDown      = False
        self.scrollEnabled   = True
        self.input           = None # Assigned during main

        self.screen          = screen
        self.x               = 0
        self.y               = 0
        self.w               = width
        self.h               = height
        self.mx              = 0 
        self.my              = 0 

        self.basePath        = IMAGEASSETPATH



        self.camX            = 0
        self.camY            = 0
        self.camW            = 1500
        self.camH            = 850
        self.camdx, self.camdy      = 0,0

        # ------------------------------ 
        #     CLASSES
        # ------------------------------

        self.smsDialogue            = None # UPDATED IN SETUP
        self.smsScrollDialogue      = None # UPDATED IN SETUP



        # ------------------------------ 
        #     COLOURS
        # ------------------------------
        self.white              = (255,255,255)
        self.green              = (0,255,0)
        self.black              = (0,0,0)
        self.blue               = (176,224,230)

        self.guiTheme           = guiTheme # SET AS 'main' for now
        c = returnColourScheme(guiTheme)
        self.colourA                              = c['a']
        self.colourB                              = c['b']
        self.colourC                              = c['c']
        self.colourD                              = c['d']
        self.bgColour                             = (175,175,175)
        self.innerBGColour                        = (119,121,118)
        self.bannerColour                         = (14,0,135)
        self.bannerTextColour                     = self.white





        # ------------------------------ 
        #     SPECIAL EFFECTS
        # ------------------------------

        # ----------FADE

        self.fadeInState    = None
        self.fadeOutState   = None
        self.resetFadeIn    = True
        self.resetFadeOut   = True
        self.fadeAlphaIndex = 100    # used on fade in, goes down to 0
        self.alphaI         = 0      # used on fade out (goes up to 255)
        self.fadeSurface    = pygame.Surface((self.w,self.h))

        self.contortMapDelay     = 0.4                # BUFF
        self.contortMapTimer     = stopTimer()
        self.contortMapCount     = 0



        self.boxOutState  = None
        self.boxInit      = False
        self.boxFill      = 0
        self.boxComplete  = False


        self.menuBG            = None
        self.hideExitButton    = False

    def resetMouseInputs(self):
        self.clicked                   = False 
        self.rightClicked              = False
        self.scrollUp                  = False  
        self.scrollDown                = False  



    ############################################
    #          INITIALISATION COMPLETE 
    ############################################






    def border(self,colour=(128,0,0)):
        self.bx,self.by = 0.1*self.width,0.1*self.height
        self.bw,self.bh = 0.8*self.width,0.8*self.height
        rect = pygame.draw.rect(self.screen, colour, [self.bx, self.by,self.bw , self.bh],4)


    def mouseCollides(self,x,y,w,h,mousePos=None):
        
        if(mousePos==None): mousePos = [self.mx,self.my]
        
        if mousePos[0] > x and mousePos[0] < x + w:
            if mousePos[1] > y and mousePos[1] < y + h:
                return(True)
        return(False)



    def moveCamera(self,game):

        # skip if scroll disabled 
        if(self.scrollEnabled==False):
            return
        
        drift = 0.3

        scroll     = 15
        softscroll = 8


        horizontal,vertical = 0,0

        if(self.mx< 0.1*self.w):
            horizontal -= scroll
        elif(self.mx< 0.2*self.w):
            horizontal -= softscroll

        if(self.mx> 0.9*self.w):
            horizontal += scroll
        elif(self.mx> 0.8*self.w):
            horizontal += softscroll


        if(self.my< 0.1*self.h):
            vertical -= scroll
        elif(self.my< 0.2*self.h):
            vertical -= softscroll

        if(self.my> 0.9*self.h):
            vertical += scroll
        elif(self.my> 0.8*self.h):
            vertical += softscroll



        self.camX += horizontal
        self.camY += vertical




    # ------------------------------ 
    #     SPECIAL EFFECTS
    # ------------------------------

    def fadeIn(self,gameState,inc=5,skip=False):
        #--------Init
        complete = False

        # INITIALISE FADE IF STATES DON'T MATCH
        if(self.fadeInState!=gameState):self.resetFadeIn=True
        
        if(self.resetFadeIn):
            self.fadeAlphaIndex = 255
            self.fadeInState    = gameState
            self.resetFadeIn    =False

        #------increment Alpha down

        self.fadeSurface.set_alpha(self.fadeAlphaIndex)
        self.fadeSurface.fill((0,0,0))
        self.screen.blit(self.fadeSurface,(0,0))
        self.fadeAlphaIndex -=inc
        if(self.fadeAlphaIndex<1):self.fadeAlphaIndex = 0
        if(self.fadeAlphaIndex<1): complete = True
        if(skip): self.fadeAlphaIndex = 0

        return(complete)

    def fadeOut(self,gameState,inc=5,alpha=254):
        """ increments an index related to alpha"""

        #--------Init
        complete = False
        if(self.fadeOutState!=gameState):self.resetFadeOut=True
        if(self.resetFadeOut):
            self.alphaI = 0
            self.fadeOutState = gameState
            self.resetFadeOut=False

        #------increment Alpha up

        self.fadeSurface.set_alpha(self.alphaI)
        self.fadeSurface.fill((0,0,0))
        self.screen.blit(self.fadeSurface,(0,0))
        self.alphaI +=inc
        if(self.alphaI>alpha):self.alphaI = alpha
        if(self.alphaI>=alpha): complete = True

        return(complete)

    def boxOut(self,gameState,inc=10):
        """ increments an index related to alpha"""
        

        #--------capture state change and init
        if(self.boxOutState!=gameState):self.boxInit=False
        

        #--------Init
        if(self.boxInit==False):
            self.boxOutState = gameState
            self.boxComplete = False
            self.boxInit     = True
            self.boxFill     = 0

        #------increment boxes inwards
        if(self.boxComplete==False):
            rect = pygame.draw.rect(self.screen, (0,0,0), [0,0, 1500,850],self.boxFill)
            self.boxFill += inc
            if(self.boxFill>self.h):
                self.boxComplete = True
                self.boxInit     = False
        
        return(self.boxComplete)







    def classDebug(self):
        debug = vars(self)
        returnArray = [str(str(x) + ': ' + str(debug[x])) for x in debug]
        return(returnArray)




def returnColourScheme(value):
    colorScheme = {
    'main':{
                'a':(43, 62, 179),
                'b':(63, 82, 199),
                'c':(103, 122, 239),
                'd': (43, 62, 179) ,
                'd': (100, 62, 179),
                'f': (150, 112, 239),
            }

    }
    return(colorScheme[value])




