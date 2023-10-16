import pygame
import os
from utils._utils import textWrap

global shift


#################################    USER INPUT      ################################# 






class userInputObject():
    def __init__(self,returnedKey,enteredString, gui,directionBtn=None,  inputLimit = 20,shift=False):
        self.returnedKey   = returnedKey
        self.enteredString = enteredString
        self.pressedKeys   = []
        self.gui           = gui
        self.directionBtn  = directionBtn
        self.inputLimit    = inputLimit
        self.defaultLimit  = inputLimit
        self.stopProcesing = False
        self.initString    = None
        self.fillC         = (0, 51, 0)
        self.borderC       = (24, 156, 48)
        self.currentText   = None
        self.w             = 0

        self.KEYDOWN       = False

        self.shift         = shift
        self.keyMap = {'a': pygame.K_a, 'b': pygame.K_b ,'c': pygame.K_c ,'d': pygame.K_d ,'e': pygame.K_e ,'f': pygame.K_f ,'g': pygame.K_g ,'h': pygame.K_h ,'i': pygame.K_i ,'j': pygame.K_j ,'k': pygame.K_k ,'l': pygame.K_l  ,'m': pygame.K_m ,'n': pygame.K_n ,'o': pygame.K_o ,'p': pygame.K_p ,'q': pygame.K_q ,'r': pygame.K_r ,'s': pygame.K_s ,'t': pygame.K_t ,'u': pygame.K_u ,'v': pygame.K_v ,'w': pygame.K_w ,'x': pygame.K_x ,'y': pygame.K_y ,'z': pygame.K_z, 'return':pygame.K_RETURN,'left meta': pygame.K_LMETA,';':pygame.K_SEMICOLON }



    def help():
        print('This object holds a current returned key and builds up an entered string. It also can draw text with blink at end value and draw a box.')

    def initEnteredString(self,defaultString):
        if(self.initString!=defaultString):
            self.initString    = defaultString
            self.enteredString = defaultString

    def reset(self,defaultString=''):
        print('initialising')
        self.initString    = defaultString
        self.enteredString = defaultString
        self.inputLimit    = self.defaultLimit
        self.stopProcesing = False

    def processInput(self,inputLimit=False):

        # override input limit
        if(inputLimit!=False): self.inputLimit = inputLimit

        # Clear out lingering direction Button
        self.directionBtn = None
        if((self.returnedKey.upper()=="UP") or (self.returnedKey.upper()=="DOWN")): self.directionBtn = self.returnedKey.upper()
        
        if(len(self.enteredString) >= self.inputLimit):
            print('**input limit reached***')
            
        # If input given
        if((self.returnedKey!="") and (len(self.enteredString) < self.inputLimit) and self.stopProcesing!=True):
            
            # if space
            if(self.returnedKey.upper()=='SPACE'): self.returnedKey = " "
            
            # If single value, append to string
            if(len(self.returnedKey) == 1):
                
                # UPPER CASE
                capslock = pygame.key.get_mods() & pygame.KMOD_CAPS
                if(capslock):
                    self.returnedKey = self.returnedKey.upper()

                self.enteredString = self.enteredString +  self.returnedKey
        
        # if backspace delete value
        if(self.returnedKey.upper()=='BACKSPACE'): self.enteredString = self.enteredString[:-1]
        if(self.returnedKey.upper()=='RETURN'): 
            self.returnedKey = 'ENTER'
            return(self.enteredString)
        # clear out
        self.returnedKey   = ""

        return(self.enteredString)

    def getButtonInputs(self,event):
        
        
        #print(pygame.key.get_pressed())
        #print(pygame.key.get_pressed()[pygame.K_w] )
        #if pygame.key.get_pressed()[K_w]:


        if event.type == pygame.KEYDOWN:
            self.returnedKey = str(pygame.key.name(event.key))
            self.pressedKeys.append(str(pygame.key.name(event.key)))
            self.KEYDOWN     = True
        if(event.type==pygame.KEYUP):
            self.KEYDOWN= False
            # remove depressed keys
            self.popKeys()

        

        if (event.type == pygame.KEYDOWN):
            if(event.mod == pygame.KMOD_LSHIFT):

                if(str(self.returnedKey) == "'"): self.returnedKey = '"'
                
                if(str(self.returnedKey) == "1"): self.returnedKey = "!"
                if(str(self.returnedKey) == "2"): self.returnedKey = "@"
                if(str(self.returnedKey) == "3"): self.returnedKey = "£"
                if(str(self.returnedKey) == "4"): self.returnedKey = "$"
                if(str(self.returnedKey) == "5"): self.returnedKey = "%"
                if(str(self.returnedKey) == "6"): self.returnedKey = "^"
                if(str(self.returnedKey) == "7"): self.returnedKey = "&"
                if(str(self.returnedKey) == "8"): self.returnedKey = "*"
                if(str(self.returnedKey) == "9"): self.returnedKey = "("
                if(str(self.returnedKey) == "0"): self.returnedKey = ")"
                if(str(self.returnedKey) == "-"): self.returnedKey = "_"
                if(str(self.returnedKey) == "="): self.returnedKey = "+"
                if(str(self.returnedKey) == ";"): self.returnedKey = ":"
                if(str(self.returnedKey) == "["): self.returnedKey = "{"
                if(str(self.returnedKey) == "]"): self.returnedKey = "}"
                if(str(self.returnedKey) == ","): self.returnedKey = "<"
                if(str(self.returnedKey) == "."): self.returnedKey = ">"
                if(str(self.returnedKey) == "/"): self.returnedKey = "?"
                if(str(self.returnedKey) == '\\'): self.returnedKey = "|"

                if(str(self.returnedKey).isalpha()): self.returnedKey = self.returnedKey.upper()


        return(self)

    def popKeys(self):
        for key in self.pressedKeys:
            # IF KEY IN KEY MAP
            if(key.lower() in self.keyMap.keys()):
                # REMOVE IT IF DEPRESSED
                if( pygame.key.get_pressed()[self.keyMap[key.lower()]] ==False):
                    self.pressedKeys.remove(key)
        


    def drawTextInputSingleLine(self,text,x,y,gui,colour=(0, 128, 0), blink = {'blinkDuration':5,'blinkValue':5,'displayInterval':5,'displayValue':5},chosenFont=None,limit=None,box=True,boxBorder=None,boxFill=None,boxLen=None):

        # for any new call reset the limit 
        if(text!=self.currentText):
            self.currentText = text
            self.inputLimit  = self.defaultLimit

        # update limit if specified
        if(limit!=None): self.inputLimit = limit
        
        # change text colour to white if box is being drawn 
        if(box): colour =(255,255,255) # set to white if boxing
        
        gui = self.gui
        if(chosenFont==None): chosenFont=gui.font


        # --------------BLINK TEXT ON/OFF
        blink['blinkValue'] -= 1
        if(blink['blinkValue'] < 0):
            blink['displayValue'] -= 1
            text = text + '_'
            if(blink['displayValue']<0):
                blink['blinkValue']   = blink['blinkDuration']
                blink['displayValue']   = blink['displayInterval']
        
        # --------------DRAW TEXT SURFACE
        text = text.rstrip()
        textsurface = chosenFont.render(text, True, colour)



        # -----------DRAW BOX and Text
        if(box):
            dummy = ''.join(['++' for x in range(self.inputLimit + 5)])
            dts = chosenFont.render(dummy, True, colour)
            
            # COLOUR OVERRIDE
            fillC,borderC = self.fillC,self.borderC
            if(boxBorder!=None and boxFill!=None):
                fillC,borderC = boxFill,boxBorder

            # ------DRAW TEXTBOX
            if(boxLen==None):
                boxLen = dts.get_rect().w


            self.w = dts.get_rect().w
            if(boxFill!=None):
                pygame.draw.rect(gui.screen, fillC, (x, y, boxLen, 2*(dts.get_rect().h)))
            pygame.draw.rect(gui.screen, borderC, (x, y, boxLen, 2*(dts.get_rect().h)),5,border_radius=1, border_top_left_radius=-1, border_top_right_radius=-1, border_bottom_left_radius=-1, border_bottom_right_radius=-1)

            gui.screen.blit(textsurface,(x + 0.05*boxLen,y + 0.5*(dts.get_rect().h)))

        else:
            gui.screen.blit(textsurface,(x,y))


    def drawTextInputPara(self,gui,text,x,y,width,yCap,colour=(0, 128, 0), blink = {'blinkDuration':5,'blinkValue':5,'displayInterval':5,'displayValue':5},chosenFont=None,limit=None,box=False, center=False):
        # --------------INITIALISATION

        # for any new call reset the limit 
        if(text!=self.currentText):
            self.currentText = text
            self.inputLimit  = self.defaultLimit

        # update limit if specified
        if(limit!=None): self.inputLimit = limit
        
        # change text colour to white if box is being drawn 
        if(box): colour =(255,255,255) # set to white if boxing
        
        gui = self.gui
        if(chosenFont==None): chosenFont=gui.font

        
        # --------------BLINK TEXT ON/OFF
        if(not center):
            blink['blinkValue'] -= 1
            if(blink['blinkValue'] < 0):
                blink['displayValue'] -= 1
                text = text + '_'
                if(blink['displayValue']<0):
                    blink['blinkValue']   = blink['blinkDuration']
                    blink['displayValue']   = blink['displayInterval']




        # --------------GET TEXT SURFACE ARRAY  

        text = text.rstrip()
        textsurfaces = textWrap(text,chosenFont,colour,width)

        if(box):
            pygame.draw.rect(gui.screen, self.fillC,   (x-20, y-20, width, yCap-y + 20) )
            pygame.draw.rect(gui.screen, self.borderC, (x-20, y-20, width, yCap-y + 20),5,border_radius=1, border_top_left_radius=-1, border_top_right_radius=-1, border_bottom_left_radius=-1, border_bottom_right_radius=-1)


        # --------------DRAW TEXT SURFACE
        yc = y
        for ts in textsurfaces:
            if(center):
                gui.screen.blit(ts,(x + 0.5*(width - ts.get_width()),yc))
            else:
                gui.screen.blit(ts,(x,yc))

            yc = yc + 1.2*ts.get_rect().h
            if(yc>=yCap): 
                self.stopProcesing = True
                self.enteredString = text[:len(text)-2]
                print('Maximum Y reached for drawTextInputPara')
                break

        return(yc)


