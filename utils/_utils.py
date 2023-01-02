from pygame.locals import *
import pygame
import time
import pygame
import pickle 
import math
import os




"""
DRAW 


# -------TEXT 

- drawText
- getWidthandHeight
- getTextWidth
- getTextHeight
- textWrap
- truncateText
- drawTextWithBackground
- drawBlinkingText
- simpleSelectableTextBox


# ---------BOX 

- drawSimpleShadedBox

# ---------TEXT BOX AND TABLE 

- drawTextBoxNoLabel
- drawTextandBox
- drawTextandBoxGrid
- drawFullTableMech
- fittedSentenceBox

# -------BUTTON 

- simpleButton


# -------COLOURS 

- approachColour
- returnColourScheme
- darken
- lighten

# ------IMAGE

- drawImage
- drawSelectableImage
- loadImageFiles

# ------MATH 

- wrapAngle()

# ------STATE 

- save_dict_as_pickle
- load_picle


CLASSES

- class button()
- class monitorExpandAnimationClass()
- fullyWappedSelectableTextRowsPaginated
- scrollingDialogue
- imageAnimate
- imageAnimateAdvanced
- animateMouseCursor
- button
- stopTimer
- Countdown timer
- dynamicBorder
- buttonWrap
- stretchBox 

SFX  

- loadingBarClass


"""






####################################################################################################
####################################################################################################



#                                TEXT


####################################################################################################
####################################################################################################



def drawText(gui,myfont, text,x,y,maxw=None, colour=(0, 128, 0),center=False,pos=None):
    """ Center means giving the far x point """
    hovered = None 
    textsurface = myfont.render(text, True, colour)

    

    # Center info from infoBox
    if(center!=False): 
        if(maxw==None):
            maxw = gui.w
        x = x + (0.5*(int(maxw) - textsurface.get_rect().width))


    tw = textsurface.get_rect().width
    th = textsurface.get_rect().height


    # If curser over text lightup
    if(pos!=None):
        textRect = Rect(x,y, x+textsurface.get_rect().width,y+textsurface.get_rect().height)
        if pos[0] > textRect.x and pos[0] < textRect.width:
            if pos[1] > textRect.y and pos[1] < textRect.height:
                textsurface = myfont.render(text, True, (128,0,0))
                hovered = text

    gui.screen.blit(textsurface,(x,y))
    return(hovered,tw,th)



def getWidthandHeight(text='sampleText',textColour='tobedefined',font='tobedefined'):
    textsurface    = font.render(text, True, textColour)
    tw = textsurface.get_rect().width
    th = textsurface.get_rect().height
    return(tw,th)

def getTextWidth(font,text):
    textsurface    = font.render(text, True, (200,200,200))
    tw = textsurface.get_rect().width
    return(tw)
def getTextHeight(font,text):
    textsurface    = font.render(text, True, (200,200,200))
    th = textsurface.get_rect().height
    return(th)




"""
Returns a list of text surfaces that fit width
"""
def textWrap(message,font,colour,width,margin=0.75,marginMax=0.85):
    printLine = ""
    fullMsg = []
    for x in range(len(message)):
        
        letter = message[x]

        # ------Newline scrub existing letter
        if(str(message[x]) =='\n'):
            fullMsg.append(font.render(printLine, True, colour))
            letter    = ""
            printLine = ""
        
        # ------- process a new letter     
        printLine+=letter

        # -----create text surface
        ts = font.render(printLine, True, colour)

        if(ts.get_rect().width>margin*width):
            # if a word space found
            if(letter==' '):
                fullMsg.append(ts)
                printLine= ""
            elif(ts.get_rect().width>marginMax*width):
                fullMsg.append(ts)
                printLine= ""


    if(len(printLine) >0): fullMsg.append(ts)

    return(fullMsg)


"""
Returns a list of text surfaces that fit width
"""
def textWordWrap(message,font,colour,width,margin=0.75,marginMax=0.85):
    printLine = ""
    fullMsg = []
    message = message.split(' ')
    for x in range(len(message)):
        
        word = message[x] 

        # ------Newline scrub existing word
        sameline=True
        if('\n' in str(message[x])):
            fullMsg.append(font.render(printLine, True, colour))
            word    = ""
            printLine = ""
            sameline = False
        
        # ------- process a new word
        printLine+=word
        if(sameline): printLine+= ' '

        # -----create text surface
        ts = font.render(printLine, True, colour)

        if(ts.get_rect().width>margin*width):
            # take a new line if space (because we are between margin and max)
            if((ts.get_rect().width>marginMax*width) or (word==' ')):
                fullMsg.append(ts)
                printLine= ""
    if(len(printLine) >0): fullMsg.append(ts)

    return(fullMsg)





def truncateText(SCREEN,myfont, text,x,y, colour=(0, 128, 0),center='no',pos=None,limitWidth=None):
    """ Center means giving the far x point """
    hovered = None 
    textsurface = myfont.render(text, True, colour)
    tw = textsurface.get_rect().width
    th = textsurface.get_rect().height
    
    # ========LIMIT TEXT LENGTH TO FIT
    if(limitWidth):
        if(textsurface.get_rect().width > limitWidth):
            maxLen = round(limitWidth/textsurface.get_rect().width * len(text))
            printText = text[0:maxLen-6] + '...'  
            textsurface = myfont.render(printText, True, colour)
            tw = textsurface.get_rect().width
            th = textsurface.get_rect().height



    # Center info from infoBox
    if(center!='no'): x = x + (0.5*(int(center) - textsurface.get_rect().width))

    # If curser over text lightup
    if(pos!=None):
        textRect = Rect(x,y, x+textsurface.get_rect().width,y+textsurface.get_rect().height)
        if pos[0] > textRect.x and pos[0] < textRect.width:
            if pos[1] > textRect.y and pos[1] < textRect.height:
                textsurface = myfont.render(text, True, (128,0,0))
                hovered = text

    SCREEN.blit(textsurface,(x,y))
    return(hovered,tw,th)




# TEXT WITH A COLOURED BACKGROUND

def drawTextWithBackground(SCREEN,myfont,text,x,y,setWidth=None,setHeight=None, textColour=(0, 128, 0),backColour= None,borderColour=None):
    
    # TEXT DETAILS
    textsurface = myfont.render(text, True, textColour)
    tw = textsurface.get_rect().width
    th = textsurface.get_rect().height
    
    if(setWidth==None):
        bw = tw
    else:
        bw = setWidth
    if(setHeight==None):
        bh= th
    else:
        bh = setHeight
    # DRAW RECT
    if(backColour):
        pygame.draw.rect(SCREEN,(backColour),[x,y,bw,bh])
    
    if(borderColour):
        pygame.draw.rect(SCREEN,(borderColour),[x,y,bw,bh],3)

    # DRAW TEXT
    SCREEN.blit(textsurface,(x+0.5*(bw-tw),y+0.5*(bh-th)))
    return(tw,th)






def drawBlinkingText(SCREEN,myfont, text,x,y, colour=(0, 128, 0),blinkFraction=0.5,fast=False):
    """ Center means giving the far x point """
    textsurface = myfont.render(text, True, colour)
    tw = textsurface.get_rect().width
    th = textsurface.get_rect().height

    if(not fast):
        if time.time() % 1 > blinkFraction:
            SCREEN.blit(textsurface,(x,y))
    else:
        if time.time() % 0.5 > 0.25:
            SCREEN.blit(textsurface,(x,y))

    return(tw,th)





def simpleSelectableTextBox(core,screen,text,x,y,w,h,bc,fc,fcSelected,font,tc,borderW=4):
    
    fillColour = fc
    if(core.collides(x,y,w,h)):
        fillColour = fcSelected
        if(core.clicked):
            core.clicked = False
            gui.pressed = False
            return(True)


    pygame.draw.rect(screen,fillColour,(x,y,w,h))
    pygame.draw.rect(screen,bc,(x,y,w,h),borderW)
    ts = font.render(text,True,tc)
    xs = x  + 0.5*(w-ts.get_rect().w)
    if(xs<=x):
        xs=x + borderW
    ys = y + 0.5*(h-ts.get_rect().h) 
    screen.blit(ts,(xs,ys),(0,0,w,h))

    return(False)











####################################################################################################
####################################################################################################



#                                BOXES


####################################################################################################
####################################################################################################




def drawSimpleShadedBox(SCREEN, x,y,w,h ,boxColour=(15,56,15),boxLineColours=((41,64,49),(41,64,49),(139,172,15),(139,172,15)),     minLineWidth=3):
    """ 
    BOX WITH NO TEXT
    """

    bw = w
    bh = h
    bx = x 
    by = y


    lineColourL=boxLineColours[0]
    lineColourU=boxLineColours[1]
    lineColourR=boxLineColours[2]
    lineColourD=boxLineColours[3]
    # draw box and shading
    pygame.draw.rect(SCREEN, (boxColour), [bx, by,bw ,bh])


    if(lineColourL!=(0,0,0)):
        pygame.draw.line(SCREEN,lineColourL, (bx,by),(bx,by+bh),minLineWidth) # dark colour
    if(lineColourU!=(0,0,0)):
        pygame.draw.line(SCREEN,lineColourU, (bx,by),(bx+bw,by),minLineWidth) # dark colour
    if(lineColourR!=(0,0,0)):
        pygame.draw.line(SCREEN,(lineColourR), (bx+bw,by),(bx+bw,by+bh),minLineWidth) # right ver
    if(lineColourD!=(0,0,0)):
        pygame.draw.line(SCREEN,(lineColourD), (bx,by+bh),(bx+bw,by+bh),minLineWidth) # bottom hor
    

    txe2 = bx + bw
    the2 = by + bh
    return(txe2,the2)


def drawSimpleShadedBoxSelectable(gui, x,y,w,h ,boxColour=(15,56,15),boxLineColours=((41,64,49),(41,64,49),(139,172,15),(139,172,15)),     minLineWidth=3,selectme=True):
    """ 
    BOX WITH NO TEXT
    """

    bw = w
    bh = h
    bx = x 
    by = y


    lineColourL=boxLineColours[0]
    lineColourU=boxLineColours[1]
    lineColourR=boxLineColours[2]
    lineColourD=boxLineColours[3]
    # draw box and shading
    pygame.draw.rect(gui.screen, (boxColour), [bx, by,bw ,bh])


    if(lineColourL!=(0,0,0)):
        pygame.draw.line(gui.screen,lineColourL, (bx,by),(bx,by+bh),minLineWidth) # dark colour
    if(lineColourU!=(0,0,0)):
        pygame.draw.line(gui.screen,lineColourU, (bx,by),(bx+bw,by),minLineWidth) # dark colour
    if(lineColourR!=(0,0,0)):
        pygame.draw.line(gui.screen,(lineColourR), (bx+bw,by),(bx+bw,by+bh),minLineWidth) # right ver
    if(lineColourD!=(0,0,0)):
        pygame.draw.line(gui.screen,(lineColourD), (bx,by+bh),(bx+bw,by+bh),minLineWidth) # bottom hor


    selected = False
    # If curser over label lightup
    if(selectme==True):
        if(gui.mouseCollides(x,y,w,h)):
            pygame.draw.line(gui.screen,(darken(lineColourR,darkenAmount=60)), (bx+bw,by),(bx+bw,by+bh),minLineWidth) # right ver
            pygame.draw.line(gui.screen,(darken(lineColourD,darkenAmount=90)), (bx,by+bh),(bx+bw,by+bh),minLineWidth) # bottom hor
            pygame.draw.rect(gui.screen, (darken(boxColour)), [bx, by,bw ,bh])

            if(gui.clicked):
                gui.pressed = False
                gui.clicked = False
                selected    = True


    txe2 = bx + bw
    the2 = by + bh
    return(selected,txe2,the2)




def classicBox(gui, x,y,w,h,text,font,bannerColour,bannerTxtColour,crossColour = (0,0,0),boxColour=(15,56,15),boxLineColours=((41,64,49),(41,64,49),(139,172,15),(139,172,15)),bannerOutline=False, minLineWidth=3):
    """ 
    BOX WITH NO TEXT
    """

    bw = w
    bh = h
    bx = x 
    by = y



    lineColourL=boxLineColours[0]
    lineColourU=boxLineColours[1]
    lineColourR=boxLineColours[2]
    lineColourD=boxLineColours[3]
    
    # DRAW MAIN BOX

    pygame.draw.rect(gui.screen, (boxColour), [bx, by,bw ,bh])

    # DRAW LINES
    if(lineColourL!=(0,0,0)):
        pygame.draw.line(gui.screen,lineColourL, (bx,by),(bx,by+bh),minLineWidth) # dark colour
    if(lineColourU!=(0,0,0)):
        pygame.draw.line(gui.screen,lineColourU, (bx,by),(bx+bw,by),minLineWidth) # dark colour
    if(lineColourR!=(0,0,0)):
        pygame.draw.line(gui.screen,(lineColourR), (bx+bw,by),(bx+bw,by+bh),minLineWidth) # right ver
    if(lineColourD!=(0,0,0)):
        pygame.draw.line(gui.screen,(lineColourD), (bx,by+bh),(bx+bw,by+bh),minLineWidth) # bottom hor
    
    # DRAW BANNER  

    x,y,w,h = x+0.02*w,y+0.02*h,0.96*w,0.07*h
    pygame.draw.rect(gui.screen, (bannerColour), [x,y,w,h])
    if(bannerOutline!=False):
        pygame.draw.rect(gui.screen, (bannerOutline), [x,y,w,h],4)

    yt = y + 0.5*(h- getTextHeight(font,text))
    drawText(gui,font, text,x+0.02*w,yt,w, colour=bannerTxtColour)

    # EXIT
    x,y,w,h = x + 0.95*w, y + 0.2*h, 0.025*gui.w, 0.6*h 
    selected,txe2,the2 = drawSimpleShadedBoxSelectable(gui,x,y,w,h,boxColour=boxColour,boxLineColours=(lineColourL,lineColourU,lineColourR,lineColourD),     minLineWidth=3)
    if(gui.mouseCollides(x,y,w,h)):
        crossColour = lighten(crossColour,lightenAmount=70)
    pygame.draw.line(gui.screen,crossColour, (x+0.25*w,y+ 0.2*h),(x+0.75*w,y+0.8*h),minLineWidth)
    pygame.draw.line(gui.screen,crossColour, (x+0.25*w,y+0.8*h),(x+0.75*w,y+0.2*h),minLineWidth) 



    txe2 = bx + bw
    the2 = by + bh
    return(txe2,the2)


####################################################################################################
####################################################################################################



#                                TEXT BOX AND TABLE 


####################################################################################################
####################################################################################################




def drawTextandBox(SCREEN,myfont, x,y,label, value, textColour=(215, 233, 149),boxColour=(15,56,15),lineColour=(139,172,15),pos=None,minBoxWidth=3):
    """ 
        Text + box i.e. myvalue [009] 
        
        for more functionality make new function
    """
    hovered = None 
    labelsurface        = myfont.render(label, True, textColour)
    tw = labelsurface.get_rect().width
    th = labelsurface.get_rect().height


    # TextBox Values
    smallestSurface = myfont.render('S', True, textColour)
    x2           = x + tw + smallestSurface.get_rect().height
    y2           = y
    if(len(value)<minBoxWidth): value = str(''.join(['0' for x in range(minBoxWidth-len(value))]) )  +str(value)
    valuesurface = myfont.render(value, True, textColour)
    tw2          = valuesurface.get_rect().width
    th2          = valuesurface.get_rect().height

    bw = tw2 + 1.5*smallestSurface.get_rect().width
    bh = th2 + smallestSurface.get_rect().height
    bx = x2 - 0.75*smallestSurface.get_rect().width
    by = y2 - 0.5*smallestSurface.get_rect().height


    # If curser over label lightup
    if(pos!=None):
        labelRect = Rect(x,y, x+labelsurface.get_rect().width,y+labelsurface.get_rect().height)
        if pos[0] > labelRect.x and pos[0] < labelRect.width:
            if pos[1] > labelRect.y and pos[1] < labelRect.height:
                labelsurface = myfont.render(label, True, (128,0,0))
                hovered = label

    SCREEN.blit(labelsurface,(x,y))

    # draw box and shading
    pygame.draw.rect(SCREEN, (boxColour), [bx, by,bw ,bh])
    pygame.draw.line(SCREEN,(lineColour), (bx,by+bh),(bx+bw,by+bh),3)
    pygame.draw.line(SCREEN,(lineColour), (bx+bw,by),(bx+bw,by+bh),3)
    
    SCREEN.blit(valuesurface,(x2,y2))

    txe2 = bx + bw
    the2 = by + bh
    return(txe2,the2)





def drawTextBoxNoLabel(SCREEN,myfont, x,y, value, boxHeight = 2,textColour=(215, 233, 149),boxColour=(15,56,15),boxLineColours=((41,64,49),(41,64,49),(139,172,15),(139,172,15)) ,minBoxWidth=3,paddingMultiplier=2):
    """ 
        box i.e. [009] 
        
        for more functionality make new function
    """
    hovered = None 
    textsurface        = myfont.render(value, True, textColour)
    w = textsurface.get_rect().width
    h = textsurface.get_rect().height

    # GET SPACING FOR ONE LETTER
    letterTs   = myfont.render('S', True, textColour)
    wLetter    = letterTs.get_rect().width * paddingMultiplier
    hLetter    = letterTs.get_rect().height



    bw = 1.2*w + 2*wLetter
    bh = boxHeight*h 
    bx = x 
    by = y



    lineColourL=boxLineColours[0]
    lineColourU=boxLineColours[1]
    lineColourR=boxLineColours[2]
    lineColourD=boxLineColours[3]


    # draw box and shading
    pygame.draw.rect(SCREEN, (boxColour), [bx, by,bw ,bh])

    if(lineColourL!=(0,0,0)):
        pygame.draw.line(SCREEN,lineColourL, (bx,by),(bx,by+bh),minBoxWidth)         # LEFT
    if(lineColourU!=(0,0,0)):
        pygame.draw.line(SCREEN,lineColourU, (bx,by),(bx+bw,by),minBoxWidth)         # TOP
    if(lineColourR!=(0,0,0)):
        pygame.draw.line(SCREEN,lineColourR, (bx+bw,by),(bx+bw,by+bh),minBoxWidth) # RIGHT
    if(lineColourD!=(0,0,0)):
        pygame.draw.line(SCREEN,lineColourD, (bx,by+bh),(bx+bw,by+bh),minBoxWidth) # BOTTOM
    
    SCREEN.blit(textsurface,(bx + (bw-w)/2  ,by + (bh-h)/2))

    txe2 = bx + bw
    the2 = by + bh
    return(txe2,the2,bw)



#----------------------------------
#
# DRAWS TEXT LABEL WITH BOX TO RIGHT
#
# EXAMPLE: myvalue [009] 
#
#----------------------------------

def drawTextandBoxGrid(SCREEN,myfont, x,y,pairArray, textColour=(215, 233, 149),boxColour=(15,56,15),lineColour=(139,172,15),pos=None,minBoxWidth=3):
    """ 
        Text + box i.e. myvalue [009] 
        
        for more functionality make new function
    """

    # IF GRID EMPTY RETURN
    if(len(pairArray)==0):
        return(x,y)


    widthArray = []
    rhsArray   = []
    for i in pairArray: widthArray.append(myfont.render(i[0], True, textColour).get_rect().width)
    tw = max(widthArray)

    for j in pairArray:
        label, value = j[0],j[1]
        hovered = None 
        labelsurface        = myfont.render(label, True, textColour)
        th = labelsurface.get_rect().height


        # TextBox Values
        smallestSurface = myfont.render('S', True, textColour)
        x2           = x + tw + 2*smallestSurface.get_rect().height
        y2           = y
        if(len(value)<minBoxWidth): value = str(''.join(['0' for x in range(minBoxWidth-len(value))]) )  +str(value)
        valuesurface = myfont.render(value, True, textColour)
        tw2          = valuesurface.get_rect().width
        th2          = valuesurface.get_rect().height

        bw = tw2 + 1.5*smallestSurface.get_rect().width
        bh = th2 + smallestSurface.get_rect().height
        bx = x2 - 0.75*smallestSurface.get_rect().width
        by = y2 - 0.5*smallestSurface.get_rect().height


        bw2 = tw + 1.5*smallestSurface.get_rect().width
        bh2 = th + smallestSurface.get_rect().height
        bx2 = x - 0.75*smallestSurface.get_rect().width
        by2 = y - 0.5*smallestSurface.get_rect().height



        # If curser over label lightup
        if(pos!=None):
            labelRect = Rect(x,y, x+labelsurface.get_rect().width,y+labelsurface.get_rect().height)
            if pos[0] > labelRect.x and pos[0] < labelRect.width:
                if pos[1] > labelRect.y and pos[1] < labelRect.height:
                    labelsurface = myfont.render(label, True, (128,0,0))
                    hovered = label




        # draw box and shading
        pygame.draw.rect(SCREEN, (boxColour), [bx2, by2,bw2 ,bh2])
        pygame.draw.line(SCREEN,(lineColour), (bx2,by2+bh2),(bx2+bw2,by2+bh2),4)
        pygame.draw.line(SCREEN,(lineColour), (bx2+bw2,by2),(bx2+bw2,by2+bh2),4)

        SCREEN.blit(labelsurface,(x,y))

        # draw box and shading
        pygame.draw.rect(SCREEN, (boxColour), [bx, by,bw ,bh])
        pygame.draw.line(SCREEN,(lineColour), (bx,by+bh),(bx+bw,by+bh),4)
        pygame.draw.line(SCREEN,(lineColour), (bx+bw,by),(bx+bw,by+bh),4)
        
        SCREEN.blit(valuesurface,(x2,y2))

        y = y +bh + (0.3*bh)

        #append the right side, so it can be 
        # worked out what is longest
        rhsArray.append((bx + bw))


    # return xend,yend
    txe2 = max(rhsArray)
    the2 = y +(0.4*bh)

    return(txe2,the2)


########################################################
#
#           FULL RANK TABLE
#           WITH COLUMNS AND ROWS
#           TODO: ADD PAGINATION
#
########################################################

def drawFullTableMech(gui,xStart=200,rowYStart=200,horizontalGap=20,verticalGap=20, windowHeight=200,windowWidth=200,itemNames=[], tableDictArray=[], paddingList=[], currentlySelected = None, font='choseFont',headerFont='chosenFont',headTextColour=(255, 255, 255),textColour=(215, 233, 149),boxColour=(15,56,15),boxLineColours=((41,64,49),(41,64,49),(0,0,0),(0,0,0)),demoMe=False):
    """
    ITEM NAMES IS KEY TO DICT,
    xStart = itemX
    horizontalGap = adjsutments
    """
    selected               = None
    rowXValues             = [] # gets filled in by loop
    xCurrent, yHeader      = xStart, rowYStart

    # PRINT COL HEADERS
    for c in range(len(itemNames)):
        col = itemNames[c][0].upper() + itemNames[c][1:]
        xc = xCurrent 
        xCurrent,yRow,xW   = drawTextBoxNoLabel(gui.screen,headerFont,xCurrent + horizontalGap,yHeader,col, textColour=headTextColour,boxColour=(15,56,15),boxLineColours=((41,64,49),(41,64,49),(0,0,0),(0,0,0)) , paddingMultiplier=paddingList[c],minBoxWidth=4)
        
        rowXValues.append([xc,xW])

    yNextRow       = yRow + verticalGap
    yHeight2Bottom = windowHeight

    # PRINT EMPTY BIG TEXT BOXES
    for x in rowXValues:
        drawSimpleShadedBox(gui.screen,x[0]+ horizontalGap,yNextRow,x[1],yHeight2Bottom ,boxColour=boxColour,minLineWidth=3, boxLineColours=boxLineColours)

    # -----------PRINT AVAILABLE CONTRABAND OFFERS
    # ITERATES DICT, PRINTS A ROW FOR EACH ITEM
    yNextRow += 0.1*(yHeight2Bottom) # bring text below top of box


    # THRU ARRAY VERTICALLY
    for x in range(len(tableDictArray)):
        currentDict = tableDictArray[x]

        # CHECK IF MOUSE COLLIDES WITH HORIZONTAL STRIP, LIGHTEN
        defaultTextColour = textColour
        if(gui.mouseCollides(rowXValues[0][0],yNextRow,windowWidth,2*font.render('S', True, textColour).get_rect().height)):
            defaultTextColour = (139,224,198)
            if(gui.clicked):
                selected = currentDict
                gui.clicked = False
                gui.pressed = False


        # HIGHLIGHT THE IN MEMORY SELECTED ROW
        if(currentlySelected==currentDict):
            defaultTextColour = (255,255,255)

        # HIGHLIGHT A ROW FOR DEMO ONLY
        if(demoMe and x==1):
            defaultTextColour = (139,224,198)
            selected = tableDictArray[1]


        # THRU DICT HORIZONTALLY
        for y in range(len(rowXValues)):
            text = str(currentDict[str(itemNames[y])])
            textsurface = font.render(text, True, defaultTextColour)
            tw,th = textsurface.get_rect().width, textsurface.get_rect().height
            bx,bw = rowXValues[y][0],rowXValues[y][1]
            if((tw<0.9*bw)):
                gui.screen.blit(textsurface,(bx + 0.62*(bw-tw),yNextRow))
            else:
                gui.screen.blit(textsurface,(bx + 0.1*bw,yNextRow),(0,0,0.9*bw,th))


        yNextRow+= 2* th

    return(selected)





"""
FITS TEXT TO A BOX, ALLOWS PAGINATION
YOU NEED TO CAPTURE THE TWO RETURN NEXPAGE, NEXT INDEX
THEN RUN, IF NEXT PAGE, NEXTINDEX=THAT VALUE RETURNED
STORE IT AS STATE IN CLASS

"""
def fittedSentenceBox(gui,game,x,y,w,h,textBlob,leftoverWordIndex,font,textColour,textVerticalSpacing=1.5,boxColour=(15,56,15),boxLineColours=None,startYGap=None,autoPage=None):



    # GET THE WORDS INTO LIST, THEN MAKE THEM SURFACES
    wordList          =  [x + ' ' for x in textBlob.split(' ')]
    newLineIndexes    =  [i for i, x in enumerate(wordList) if 'TAKENEWLINE' in x]

    wordSurfaceList   =  [font.render(x, True, textColour) for x in wordList]
    textHeight        =  wordSurfaceList[0].get_rect().height
    textHeightSpacing = textVerticalSpacing * textHeight


    # TEXT STARTING POINT
    textX, textY = x + 0.05*w , y + 0.8*textHeightSpacing
    if(startYGap):
        textY = y + startYGap*textHeightSpacing

    maxWidthForText  = 0.9*w
    maxHeightforText = 0.85*h

    # DRAW BACKGROUND RECTANGLE
    if(boxLineColours==None):
        boxLineColours = ((0,0,0),((0,0,0)),((0,0,0)),((0,0,0)))
    drawSimpleShadedBox(gui.screen, x,y,w,h,boxColour=boxColour,boxLineColours=boxLineColours,     minLineWidth=4)

    # BUILD A FITTED ARRAY OF PRINT LINES
    line = []
    fullSentenceMatrix = []
    currentLineLen = 0
    
    xCurrent             = textX
    yCurrent             = textY

    # ADJUST DYNAMICALLY IF THIS HAS BEEN CALLED AGAIN WITH REMAINDER
    leftOverTriggered    = False
    wordSurfaceList = wordSurfaceList[leftoverWordIndex:]

    
    for wordIndex in range(len(wordSurfaceList)):
        word = wordSurfaceList[wordIndex]
        wordWidth = word.get_rect().width
            

        # HORIZONTAL
        if((currentLineLen+wordWidth < maxWidthForText) ):
            currentLineLen += wordWidth
            gui.screen.blit(word,(xCurrent,yCurrent))
            xCurrent += word.get_rect().width
        # VERTICAL
        elif(((yCurrent + textHeightSpacing + textHeight) < (y+maxHeightforText))):
            currentLineLen = 0
            xCurrent = textX
            yCurrent += textHeightSpacing

            currentLineLen += wordWidth
            gui.screen.blit(word,(xCurrent,yCurrent))
            xCurrent += word.get_rect().width
        else:
            leftoverWordIndex += wordIndex
            leftOverTriggered = True
            break

    # IF USER CLICKS, RETURN THE INDEX OF THE CHOPPED WORD

    userPaged = gui.clicked and gui.mouseCollides(x,y,w,h)
    
    if(userPaged and leftoverWordIndex!=0):
        # go to start again
        if(leftOverTriggered==False):
            leftoverWordIndex = 0
        return(True,leftoverWordIndex)
    else:
        return(False,leftoverWordIndex)


    



####################################################################################################
####################################################################################################



#                                BUTTONS


####################################################################################################
####################################################################################################




"""
simple button
"""
def simpleButton(x,y,text,gui,font,setTw=False,backColour=(0,0,0),borderColour=(255,255,255), textColour=(255,255,255),hoveredColour=None):
    
    # ------overridable----
    
    pad  = 20

    # --------------RENDER TEXT TO SET WIDTH
    
    selected = False 

    ts     = font.render(text, True, textColour)
    th     = ts.get_rect().height
    tw     = ts.get_rect().width
    if(setTw==False): setTw    = 1.1*tw
    # ------Set full width,height, text x,y poos

    w,h    = setTw,th+pad
    tx     = x + 0.5*(w-tw)
    ty     = y + 0.5*(h-th)

    # -----------draw box
    if(backColour!=None):
        pygame.draw.rect(gui.screen, (backColour), [x,y,w,h]) # background colour
    if(borderColour!=None):
        pygame.draw.rect(gui.screen, (borderColour), [x,y,w,h],2)               # border colour
    
    if(gui.mouseCollides(x,y,(w),(h))): 
        if(borderColour!=None):
            highlighedColour = borderColour
            if(hoveredColour!=None): 
                highlighedColour = hoveredColour

            pygame.draw.rect(gui.screen, (highlighedColour), [x,y,w,h])             # highlighted colour
        ts     = font.render(text, True, lighten(textColour,50))
        
        if(gui.clicked): 
            selected =True
            gui.clicked= False
            gui.pressed = False
    
    # ---- write text
    gui.screen.blit(ts,(tx,ty))


    return(selected,x+w,y+h)


"""
simple button
"""
def simpleButtonHovered(x,y,text,gui,font,setTw=False,backColour=(0,0,0),borderColour=(255,255,255), textColour=(255,255,255)):
    
    # ------overridable----
    
    pad  = 20

    # --------------RENDER TEXT TO SET WIDTH
    
    selected = False 

    ts     = font.render(text, True, textColour)
    th     = ts.get_rect().height
    tw     = ts.get_rect().width
    if(setTw==False): setTw    = 1.1*tw
    # ------Set full width,height, text x,y poos

    w,h    = setTw,th+pad
    tx     = x + 0.5*(w-tw)
    ty     = y + 0.5*(h-th)

    # -----------draw box
    if(backColour!=None):
        pygame.draw.rect(gui.screen, (backColour), [x,y,w,h]) # background colour
    if(borderColour!=None):
        pygame.draw.rect(gui.screen, (borderColour), [x,y,w,h],2)               # border colour
    
    hovered = False
    if(gui.mouseCollides(x,y,(w),(h))): 
        hovered = True
        if(borderColour!=None):
            pygame.draw.rect(gui.screen, (borderColour), [x,y,w,h])             # highlighted colour
        ts     = font.render(text, True, lighten(textColour,50))
        
        if(gui.clicked): 
            selected =True
            gui.clicked= False
            gui.pressed = False
    
    # ---- write text
    gui.screen.blit(ts,(tx,ty))


    return(selected,x+w,y+h,hovered)





####################################################################################################
####################################################################################################



#                                COLOURS


####################################################################################################
####################################################################################################





def approachColour(baseColour,targetColour,inc=2):
    complete = False
    if(baseColour[0]<targetColour[0]):
        baseColour = ((baseColour[0]+inc),(baseColour[1]),(baseColour[2]))
    if(baseColour[1]<targetColour[1]):
        baseColour = ((baseColour[0]),(baseColour[1]+inc),(baseColour[2]))
    if(baseColour[2]<targetColour[2]):
        baseColour = ((baseColour[0]),(baseColour[1]),(baseColour[2]+inc))

    if(baseColour==targetColour): complete=True

    return(complete,baseColour)






def darken(colour,darkenAmount = 20):
    c1 = colour[0] - darkenAmount
    if(c1<0):c1=0
    c2 = colour[1] - darkenAmount
    if(c2<0):c2=0
    c3 = colour[2] - darkenAmount
    if(c3<0):c3=0

    newColour = (c1,c2,c3)
    return(newColour)

def lighten(colour,lightenAmount=20):
    c1 = colour[0] + lightenAmount
    if(c1>255):c1=255
    c2 = colour[1] + lightenAmount
    if(c2>255):c2=255
    c3 = colour[2] + lightenAmount
    if(c3>255):c3=255

    newColour = (c1,c2,c3)
    return(newColour)

    




####################################################################################################
####################################################################################################



#                                IMAGE


####################################################################################################
####################################################################################################




def drawImage(screen,image,pos,trim=False):
    if(trim!=False):
        screen.blit(image,pos,trim)
    else:
        screen.blit(image,pos)

def drawSelectableImage(image,image2,pos,gui,trim=False):
    displayImage = image

    hover = gui.mouseCollides(pos[0],pos[1],image.get_rect().w,image.get_rect().h)
    if(hover): displayImage = image2

    if(trim!=False):
        gui.screen.blit(displayImage,pos,trim)
    else:
        gui.screen.blit(displayImage,pos)

    if(hover and gui.clicked):
        gui.clicked,gui.pressed = False, False
        return(True)

    return(False)


# returns image array iterating last filedigit
def loadImageFiles(firstFile,path,convert=False,log=False):
    imgFiles = []
    prefix = firstFile.split('.')[0][:-1]
    try:
        index  = int(firstFile.split('.')[0][-1])
    except:
        print('*Error* image file does not end with a numer' + str(firstFile))
    affix  = '.' + firstFile.split('.')[-1]
    for i in range(index,index+80):
        cf = prefix + str(index)
        tfile = path + cf + affix
        if(os.path.isfile(tfile)):
            if(convert):
                if(log):
                    print('converting ' + str(tfile))
                img = pygame.image.load(tfile).convert()
            else:
                img = pygame.image.load(tfile)
            imgFiles.append(img)
            index = index + 1
        else:
            break


    if(len(imgFiles)<1):
        print("Image file for " + str(path) + ' not loaded') 
        exit()

    return(imgFiles)








# WRAPS 360 OR 0 
def wrapAngle(facing):
    
    # ----WRAP ANGLE 
    if(facing>360): facing =  facing%360
    if(facing<0): facing = facing%360

    return(facing)







# --------SAVE FILE 

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




""""

  ____  _         _     ____   ____   _____  ____  
 / ___|| |       / |   / ___| / ___| | ____|/ ___| 
| |    | |      / _ |  |___ | |___ | |  _|  |___ | 
| |___ | |___  / ___ |  ___) | ___) || |___  ___) |
 |____||_____|/_/   |_||____/ |____/ |_____||____/ 
                                                   

"""





"""
button(X,W,W,H,'NAME',COLOUR,FONT,textColour=COLOUR)

IF BUTTON WIDTH/HEIGHT IS 0/0 IT WILL AUTO FIT


"""

# X,Y,W,H can be overriden
class button():
    def __init__(self, x,y,width,height,text,colour,font, thickness = 3,textColour=(200,200,200)):
        self.x            = x
        self.y            = y
        self.width        = width
        self.height       = height
        self.text         = text
        self.colour       = colour
        self.font         = font
        self.thickness    = thickness
        self.textColour   = textColour
        self.textsurface  = self.font.render(self.text, True, textColour)


    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

    def display(self,gui,textOverride=None, widthOverride=None,heightOverride=None,noBorder=False,fillColour=None,updatePos=None,hoverBoxCol=None,hoverTextCol=None,borderColour=(245,245,245),fontOverride=None):
        """
        # NEEDS UPGRADING TO FIX IT NOT CENTERING
        widthOverride = 'tight'  # if you want to have it dynamic

        updatePos - [X,Y] #override
        
        fillColour -  off by default
        """
        
        # SET TEXT
        if(textOverride!=None): self.text= textOverride
        text = self.text

        if(updatePos):
            self.x,self.y = updatePos[0],updatePos[1]
        
        textColour   = self.textColour
        hovered = self.isOver((gui.mx,gui.my))

        if(hovered): 
            textColour = (100,100,100)
            if(hoverTextCol):
                textColour= hoverTextCol
        if(hovered): 
            borderColour = (100,100,100)
            if(hoverBoxCol):
                borderColour = hoverBoxCol

        font = self.font
        if(fontOverride):
            font=fontOverride
        textsurface    = font.render(text, True, textColour)
        tw = textsurface.get_rect().width
        th = textsurface.get_rect().height
        letterSurfaceWidth = font.render('SS', True, textColour).get_rect().width


        # SOME BUTTONS HAVE WIDTH NOT CHANGING
        if(self.width==0): 
            self.width = 1.3*tw
        if(widthOverride =='tight'):
            self.width = tw + 1.5*(letterSurfaceWidth)
        elif(widthOverride!=None):
            self.width = widthOverride * tw + 1.5*(letterSurfaceWidth)
        
        if(self.height==0): 
            self.height = 1.3*th
        if(heightOverride!=None):
            self.height = heightOverride * th 

        

        # Draw box
        bx,by = self.x,self.y
        bw,bh = self.width,self.height

        if(fillColour):
            pygame.draw.rect(gui.screen,fillColour,[ bx,by,bw,bh],border_radius=4, border_top_left_radius=4, border_top_right_radius=4, border_bottom_left_radius=4, border_bottom_right_radius=4)

        if(noBorder): return(hovered,bw,bh)
        # draw Border
        pygame.draw.rect(gui.screen,borderColour,[bx,by,bw,bh], self.thickness,border_radius=4, border_top_left_radius=4, border_top_right_radius=4, border_bottom_left_radius=4, border_bottom_right_radius=4)

        # text at end
        gui.screen.blit(textsurface,(self.x + 0.5*(self.width-tw),self.y+ 0.5*(self.height-th)))

        selected = False
        if(hovered and gui.clicked): 
            selected = True
            gui.clicked,gui.pressed = False, False

        return(selected,bw,bh)

    # this works out the width you need before running
    # display function
    def displayReturnButtonDimensions(self,gui,textOverride=None, widthOverride=None,fontOverride=None):
        
        w,h = self.width,self.height
        
        # SET TEXT
        if(textOverride!=None): text= textOverride
        text = self.text

        textColour   = self.textColour

        font = self.font
        if(fontOverride):
            font=fontOverride
        textsurface    = font.render(text, True, textColour)
        tw = textsurface.get_rect().width
        th = textsurface.get_rect().height
        letterSurfaceWidth = font.render('SS', True, textColour).get_rect().width


        # SOME BUTTONS HAVE WIDTH NOT CHANGING
        if(self.width==0): 
            w = 1.3*tw
        if(widthOverride =='tight'):
            w = tw + 1.5*(letterSurfaceWidth)
        if(self.height==0): h = 1.3*th

        return(w,h)

        




    def displayCircle(self,gui,noBorder=False):
        textColour   = self.textColour
        borderColour = gui.themeColour
        hovered = self.isOver((gui.mx,gui.my))
        self.width,self.height=10,10
        if(hovered): borderColour = (160,20,20)


        # Draw box
        if(noBorder): return(hovered)
        pygame.draw.circle(gui.screen, borderColour, (self.x,self.y), 10, 0)
        
        return(hovered)











#-----------EXPANDS A MONITOR VISUAL ANIMATION
# INITIALISE THEN RUN epxand()
class monitorExpandAnimationClass():
    def __init__(self,x,y,w,h,increment,startColour):
        self.x    = x
        self.y    = y
        self.w    = w
        self.h    = h
        self.initialValues = [self.x,self.y,self.w,self.h]

        # increment x,y seperatly so it expands horizontally first
        self.increment     = 0.05 # EXPANDS BY % OF FULL SIZE (SO 20 FRAMEES IN THIS CASE)
        self.xscale        = self.increment
        self.yscale        = self.increment
        self.scaleComplete = False

        # change colour as expand
        self.colourStart = startColour
        self.colour      = startColour

    def reset(self):
        self.x,self.y,self.w,self.h = self.initialValues[0],self.initialValues[1],self.initialValues[2],self.initialValues[3]
        self.xscale = self.increment
        self.yscale = self.increment
        self.colour = self.colourStart
        self.scaleComplete = False

    def expand(self,gui):
        self.w = self.xscale * self.initialValues[2]
        self.h = self.yscale * self.initialValues[3]
        
        pygame.draw.rect(gui.screen, (self.colour), [self.x+ ((self.initialValues[2]-self.w)/2)  , self.y + ((self.initialValues[3]-self.h)/2),self.w ,self.h])
        
        if(not self.scaleComplete):
            # SCALE OUT HORIZONTALLY THEN VERTICALLY
            if(self.xscale>=1):
                self.xscale=1
                self.yscale += self.increment
                if(self.yscale>=1):
                    self.yscale=1
                    self.scaleComplete = True
            else:
                self.xscale += self.increment

            if(self.scaleComplete):
                self.reset()
                return(True)

        return(False)








"""
THIS WILL WORK BEAUTIFULLY IF YOU CHUNK BIG PARAGRAPHS INTO MORE LINES IN THE TEXTARRAY
TAKE NEXT BUTTON INTO ACCOUNT FOR HEIGHT
"""
class fullyWappedSelectableTextRowsPaginated():
    def __init__(self,gui):
        self.page          = 0
        self.nextButton    = button(500,500,0,0,'Next',gui.themeColour,gui.smallishFont, thickness = 3,textColour=(16,60,32))
        self.hoveredIndex  = None
        self.lastpageCheck = -1

    def printSelectableRows(self,gui,x,y,w,h,textArray,font,textColour,ySpacing=1.5,borderColour=(16,60,32),buttonFill=None,updateButtonPosition=[]):

        # THIS WILL GO THROUGH THE ARRAY, TREATING EACH AS A SENTENCE
        # THAT GOES INTO A MATRIX
        # WHICH THEN GOES INTO A LIST FOR PRINTING
        printList = [] # Contains print matrices
        
        # FOR EACH ELEMENT IN ARRAY
        for paragraph in textArray:
            wordList          =  [x + ' ' for x in paragraph.split(' ')]
            wordSurfaceList   =  [font.render(x, True, textColour) for x in wordList]
            hoverSurfaceList  =  [font.render(x, True, lighten(textColour,60)) for x in wordList]
            matrix            = [] # final object for printing (goes in printList)
            lineBuffer        = [] # fills up until w met
            currentLineLength = 0
            # FOR EACH WORD IN TOKENS
            for wordIndex in range(len(wordSurfaceList)):
                word = wordSurfaceList[wordIndex]
                wordWidth = word.get_rect().width
                
                # ADD TOKEN HORIZONTALLY
                if((currentLineLength+wordWidth < w) ):
                    currentLineLength += wordWidth
                    lineBuffer.append(word)    
                else:
                    # ADD TOKENS VERTICALLY
                    matrix.append(lineBuffer)
                    lineBuffer        = []
                    currentLineLength = 0
                    currentLineLength += wordWidth
                    lineBuffer.append(word)  

            # CATCH STRAGGLERS 
            if(len(lineBuffer)>0):
                matrix.append(lineBuffer)
            # append to printList
            printList.append(matrix)


        # WORK OUT A VERTICAL GAP WITH EXAMPLE
        verticalGap = ySpacing *  font.render('SS', True, textColour).get_rect().h


        # its the last index unless cut down
        lastMatrixIndex = len(printList)


        # A bit of jiggery pokery with flags to ensure
        # I get the index at which Y breaches height
        heightCheck= 0
        free = True   # just a simple flag to drop out 
        for mi in range(self.page,len(printList)):
            matrix = printList[mi]
            for r in matrix:
                if(free):
                    heightCheck += verticalGap
                    if(heightCheck>=h):
                        free=False
                        lastMatrixIndex = mi



        # UPDATE Y TO CENTER VERTICALLY
        # as matrix gets bigger, start y gets smaller 
        yStart = (y+ (h - verticalGap* (lastMatrixIndex+1))/2) 
        if(yStart< y+verticalGap):
            y = y+verticalGap
        else:
            y = yStart




        #PRINT THE TEXT
        xc,yc = x,y
        for m in range(self.page,lastMatrixIndex):
            hovered = False
            matrix = printList[m]
            if(m==self.hoveredIndex):
                hovered=True
            yp = yc
            for r in range(0,len(matrix)):
                row=matrix[r]
                for wrd in range(0,len(row)):
                    word = row[wrd]
                    gui.screen.blit(word,(xc,yc))
                    xc+= word.get_rect().w
                xc=x
                yc+=verticalGap

            if(gui.mouseCollides(x,yp,w,yc-yp)):
                pygame.draw.rect(gui.screen, (borderColour), [x-0.5*verticalGap, yp -0.1*verticalGap,w+1*verticalGap ,yc-yp+0.1*verticalGap],1)
                self.hoveredIndex = m
                if(gui.clicked):
                    gui.clicked,gui.pressed = False, False
                    return(True,m,yc+verticalGap)


        # NEXT BUTTON
        if(lastMatrixIndex<len(printList)):
            nextWidth    = font.render('next', True, textColour).get_rect().w
            xbutton,ybutton = x+(w-nextWidth)/2,yc
            if(updateButtonPosition):
                xbutton,ybutton = updateButtonPosition[0],updateButtonPosition[1]

            selected,bw,bh = self.nextButton.display(gui,textOverride='next', widthOverride='tight',fillColour=buttonFill,updatePos=(xbutton,ybutton),hoverBoxCol=lighten(borderColour,60),hoverTextCol=lighten(textColour,50),borderColour=borderColour,fontOverride=font)
            if(selected and lastMatrixIndex<len(printList)):
                self.page = lastMatrixIndex

                # WHEN LMI stops incrementing, its the end
                currentLastMatrixIndex  =lastMatrixIndex 
                if(currentLastMatrixIndex==self.lastpageCheck):
                    print('trigged')
                    print(currentLastMatrixIndex,self.lastpageCheck)
                    self.page=0
                else:
                    self.lastpageCheck = lastMatrixIndex


        return(False,None,yc+verticalGap)












class scrollingDialogueSimple():
    def __init__(self):
        self.initialised        = False
        self.trackedText        = ''

        # TIMER BETWEEN LETTERS
        self.scrollTimer        = stopTimer()
        self.scrollCount        = 0
        self.scrollInterval     = 0.03

        # STARTUP TIMER
        self.startupTimer       = stopTimer()
        self.startupDelay       = 1

        # TIMER TO END OUT
        self.closeOutTimer      = stopTimer()
        self.closeOutCount      = 0
        self.closeOutDelay      = 1.5

        self.textBuffer         = []
        self.baseArray          = []
        self.currentArrayIndex  = 0
        self.arrIndex           = 0
        self.senPos             = 0
        self.colour             = (255,2552,55)
        self.y                  = 0
        self.y2                 = 0


    def drawScrollingDialogue(self,gui,game,w,h,myfont, text, textStartingPos=(-1,-1),colour=None,interval=0,skipEnabled=False,closeOutDelay=True,startupDelay=True,vertInc= 1.2,maxLines=5):
        
        
        #---------DELAY STARTUP UP 

        if(startupDelay):
            startup = self.startupTimer.stopWatch(self.startupDelay, 'start up timer', str(text),game,silence=True)
            if(not startup):
                return(False)


        # SET STARTING POSITION

        if(textStartingPos==(-1,-1)):
            xStart,yStart      = gui.x + 500,gui.y+70
        else:
            xStart,yStart = textStartingPos[0],textStartingPos[1]
        x,y        = xStart,yStart
        maxWidth   = w
        maxHeight  = h

        clicked    = gui.clicked
        hovered    = gui.mouseCollides(x,y,maxWidth,maxHeight)
        
        
        if(colour==None): colour = self.colour
        
        # ONLY ENABLE SKIP IF SPECIFIED
        skip = False 
        if(skipEnabled):
            pass # ENABLE SKIP LATER

        #----------------------------------------------------------
        #
        #    INITIALISE DIALOGUE   REINITIALISE IF TEXT CHANGES OR SET EXTERNALLY 
        #
        #----------------------------------------------------------


        if(self.initialised== False or text!=self.trackedText):
            
            self.trackedText       = text
            # format paragraph into array of fitted sentences
            self.textBuffer        = []
            self.baseArray         = []
            self.y                 = yStart
            self.senPos            = 0
            self.currentArrayIndex = 0
            self.arrIndex          = 0
            self.finished          = False

            dialogueArray,para = [], ""
            for word in text.split(' '):
                pre   = para
                para += word + " "
                textsurface = myfont.render(para, True, colour)
                w = textsurface.get_rect().width
                if(w>= maxWidth):
                    dialogueArray.append(pre)
                    para = word + " "
            dialogueArray.append(para)

            self.baseArray       = dialogueArray   # Full Dialogue
            self.textBuffer      = dialogueArray   # Actual Dialogue being printed
            self.arrIndex        = 5        # array index is the last line of given array slice
            

            # SET TEMPORARY TEXT ARRAY BASED UPON LINE LIMIT 
            if(len(self.textBuffer)>maxLines): 
                self.textBuffer = self.baseArray[0:self.arrIndex]
            self.initialised  = True


        #----------------------------------------------------------
        #
        #    NEXT PAGE & SKIP
        #
        #----------------------------------------------------------
        if((hovered and clicked) or gui.input.returnedKey.upper()=='RETURN'): 
            
            # IF BEFORE THE LAST PAGE 
            # array index is the last line of given array slice
            if(self.arrIndex<len(self.baseArray)):
                self.textBuffer = self.baseArray[self.arrIndex:(self.arrIndex+maxLines)] # GO TO NEXT PAGE
                self.arrIndex  = self.arrIndex + maxLines
                self.currentArrayIndex     = 0
                self.senPos     = 0
                self.y          = yStart
            else:
                if(skip):
                    self.finished            = True
                    self.scrollSpeedOverride = None



        # -----------PRINT PRECEEDING ROWS

        self.y2 = yStart
        for row in range(0,self.currentArrayIndex):
            currentSentence = self.textBuffer[row]
            ts = myfont.render(currentSentence, True, colour)
            h = ts.get_rect().height
            gui.screen.blit(ts,(x,self.y2))
            self.y2=self.y2+ vertInc*h


        #----------------------------------------------------------
        #
        #    SCROLL CURRENT LINE
        #
        #----------------------------------------------------------

        currentSentence = self.textBuffer[self.currentArrayIndex]
        for word in (range(0,len(currentSentence[self.senPos]) )):
            printSentence = currentSentence[:self.senPos]
            ts = myfont.render(printSentence, True, colour)
            h = ts.get_rect().height
        gui.screen.blit(ts,(x,self.y))
        x=xStart


        # -----------PRINT SKIP IF NEED BE 

        if(skip and self.currentArrayIndex<(len(self.textBuffer)-1)): 
            self.currentArrayIndex = len(self.textBuffer)-1
            self.senPos=0
            self.y=self.y+vertInc *(len(self.textBuffer)-1)*h


        #----------------------------------------------------------
        #
        #    PROCESS NEXT WORD 
        #
        #----------------------------------------------------------


        nextWordReady = self.scrollTimer.stopWatch(self.scrollInterval, 'textScroll', str(self.scrollCount) + str(text),game,silence=True)
        if(nextWordReady):
            self.scrollCount +=1
            if(len(currentSentence)-2 >=self.senPos):
                self.senPos+=1
            else:
                if(len(self.textBuffer)-2>=self.currentArrayIndex):
                    self.currentArrayIndex +=1
                    self.y=self.y+vertInc *h
                    self.senPos=0
                else:
                    # If at end of array, end of elem and true end
                    if(self.arrIndex>=len(self.baseArray)):
                        self.finished    = True

        #---------DELAY CLOSING OUT 

        if(closeOutDelay and self.finished):
            closeOut = self.closeOutTimer.stopWatch(self.closeOutDelay, 'close out timer', str(self.closeOutCount) + str(text),game,silence=True)
            if(closeOut):
                self.closeOutCount +=1
                self.finished = True
            else:
                return(False)

        return(self.finished)






# -----BEST TO ASSIGN THIS TO SPECIFIC CLASS WITH THE IMAGES
# ----NOT GENERIC GUI BECAUSE THAT WOULD CLASH WITH MULTIPLE
# ----- JUST FEED ANIMATE THATS ENOUGH

class imageAnimate():
    def __init__(self,p,f,s,name=None):
        self.p           = 0       # page
        self.f           = 0       # count
        self.s           = 0       # reset
        self.initialised = False
        self.state       = None
        self.name        = None
    
    def animate(self,gui,gamestate,introSlides,pfs,blitPos):
        """p = page f = count s = reset count
        """

        # ------Initialise
        if(self.state!=gamestate): self.initialised=False
        if(self.initialised==False):
            self.p           = pfs[0]
            self.f           = pfs[1]
            self.s           = pfs[2]
            self.state       = gamestate
            self.initialised =True

        # last frame
        end = len(introSlides)
        self.f -=1
        if(self.f<1):
            self.f=self.s
            self.p +=1 
            if(self.p>=end): self.p = 0



        

        gui.screen.blit(introSlides[self.p],blitPos)



# LOOPS THRU IMAGE REEL

class imageAnimateAdvanced():
    def __init__(self,imageFrames,changeDuration):
        self.frameTimer      = stopTimer()
        self.changeDuration  = changeDuration
        self.changeCount     = 0

        self.currentFrame    = 0
        self.imageFrames     = imageFrames
        self.reelComplete    = False

    
    def animate(self,gui,trackedName,blitPos,game,rotation=None,centerOfRotation=(0.5,0.5),repeat=True, noseAdjust=False):
        # TIMER THAT ITERATES THROUGH A FRAME EACH GIVEN INTERVAL
        changeFrame = self.frameTimer.stopWatch(self.changeDuration,trackedName, str(self.changeCount) + trackedName, game,silence=True)
        
        if(changeFrame):
            self.changeCount +=1
            self.currentFrame +=1
            if(self.currentFrame>=len(self.imageFrames)):
                if(repeat==False):
                    self.currentFrame = len(self.imageFrames)-1
                else:
                    self.currentFrame = 0
                self.reelComplete = True
            else:
                # LATE ADDITION MIGHT NEED ROLLED BACK
                self.reelComplete = False

        if(rotation==None): rotation = 0
        rotation = wrapAngle(rotation)

        # GET ORIGINAL AND ROTATED LEN AND WIDTH
        rotated_image = pygame.transform.rotate(self.imageFrames[self.currentFrame], rotation)
        rotatedWidth,rotatedHeight     = rotated_image.get_width(),rotated_image.get_height()
        imgW,imgH = self.imageFrames[self.currentFrame].get_width(), self.imageFrames[self.currentFrame].get_height()

        # GET MUTATED COORDINATES
        blitx,blity         = blitPos[0]+centerOfRotation[0]*(imgW-rotatedWidth),blitPos[1]+centerOfRotation[1]*(imgH-rotatedHeight)
        

        if(noseAdjust):
            noseX,noseY = (blitPos[0]+0.5*imgW + imgW * 0.5*math.cos(wrapAngle(rotation+90)*math.pi/180),blitPos[1]+0.5*imgH  -imgH*0.5*math.sin(wrapAngle(rotation+90)*math.pi/180))
            bx,by = blitPos[0],blitPos[1]


            gui.screen.blit(rotated_image, (bx,by ))
        else:
            gui.screen.blit(rotated_image, (blitx,blity))

        # GET MUTATED COORDINATES
        midTopX,midTopY     = (blitPos[0]+0.5*imgW + imgW * 0.5*math.cos(wrapAngle(rotation+90)*math.pi/180),blitPos[1]+0.5*imgH  -imgH*0.5*math.sin(wrapAngle(rotation+90)*math.pi/180))
        # HORIZONTAL OFFSET OF MIDTOP
        offx = 30 * math.cos(math.radians(360-rotation))
        offy = 30 * math.sin(math.radians(360-rotation))
        rightTopX, rightTopY = midTopX + offx, midTopY + offy
        leftTopX, leftTopY   = midTopX - offx, midTopY - offy

        centerX,centerY   = (blitPos[0]+0.5*imgW + rotatedWidth*0.01*math.cos(wrapAngle(rotation+90)*math.pi/180),blitPos[1]+0.5*imgH -rotatedHeight*0.01*math.sin(wrapAngle(rotation+90)*math.pi/180))

        smallOx,smallOy = 20 * math.cos(math.radians(360-rotation)), 20 * math.sin(math.radians(360-rotation))
        centerRx,CenterRy = centerX + smallOx, centerY + smallOy
        centerLx,CenterLy = centerX - smallOx, centerY - smallOy

        behindX,behindY   = (blitPos[0]+0.5*imgW - imgW*1.3*math.cos(wrapAngle(rotation+90)*math.pi/180),blitPos[1]+0.5*imgH +imgH*1.3*math.sin(wrapAngle(rotation+90)*math.pi/180))
        

        #pygame.draw.circle(gui.screen, (220,100,100), (behindX,behindY), 10, 0)


        return(self.reelComplete,{'center':(centerX,centerY ), 'centerL':(centerLx,CenterLy ),'centerR':(centerRx,CenterRy ), 'midTop':(midTopX,midTopY),'leftTop':(leftTopX, leftTopY),'rightTop':(rightTopX, rightTopY),'behind':(behindX,behindY) , 'rotatedDims': (rotatedWidth,rotatedHeight)})



    def animateNoRotation(self,gui,trackedName,blitPos,game,repeat=True):
        # TIMER THAT ITERATES THROUGH A FRAME EACH GIVEN INTERVAL
        changeFrame = self.frameTimer.stopWatch(self.changeDuration,trackedName, str(self.changeCount) + trackedName, game,silence=True)
        
        if(changeFrame):
            self.changeCount +=1
            self.currentFrame +=1
            if(self.currentFrame>=len(self.imageFrames)):
                if(repeat==False):
                    self.currentFrame = len(self.imageFrames)-1
                else:
                    self.currentFrame = 0
                self.reelComplete = True
            else:
                # LATE ADDITION MIGHT NEED ROLLED BACK
                self.reelComplete = False


        # GET ORIGINAL AND ROTATED LEN AND WIDTH
        imgW,imgH = self.imageFrames[self.currentFrame].get_width(), self.imageFrames[self.currentFrame].get_height()
        gui.screen.blit(self.imageFrames[self.currentFrame], (blitPos[0],blitPos[1]))

        return(self.reelComplete)









class imageWithTimer():
    def __init__(self,changeDuration):
        self.imageTimer      = stopTimer()
        self.changeDuration  = changeDuration
        self.changeCount     = 0

    
    def display(self,image,gui,trackedName,blitPos,game,rotation=None,centerOfRotation=(0.5,0.5)):
        timeUp = self.imageTimer.stopWatch(self.changeDuration,trackedName,trackedName + str(image), game,silence=True)

        if(rotation):
            rotation      = wrapAngle(rotation)
            rotated_image = pygame.transform.rotate(image, rotation)
            rw,rh         = rotated_image.get_width(),rotated_image.get_height()
            fw,fh         = image.get_width(), image.get_height()

            blitx,blity = blitPos[0]+centerOfRotation[0]*(fw-rw),blitPos[1]+centerOfRotation[1]*(fh-rh)
            gui.screen.blit(rotated_image, (blitx,blity))
            return(timeUp,(blitx,blity),rw,rh)

        else:
            gui.screen.blit(image, blitPos)
            w,h = image.get_width(),image.get_height()
            return(timeUp,blitPos,w,h)




class animateMouseCursor():
    def __init__(self,cursorName,cursorImageList):
        self.cursorName       = cursorName
        self.cursorIndex      = 0
        self.cursorTimer      = stopTimer()
        self.cursorImageList  = cursorImageList
        self.cursorActive     = False 


    def animate(self,gui,game,delayRate):
        pygame.mouse.set_visible(False)
        changeIndex = self.cursorTimer.stopWatch(delayRate,'cursor',str(self.cursorIndex) + str(self.cursorName),game,silence=True)
        if(changeIndex):
            self.cursorIndex+=1
            if(self.cursorIndex>=len(self.cursorImageList)-1):
                self.cursorIndex = 0
        
        drawImage(gui.screen,self.cursorImageList[self.cursorIndex],(gui.mx,gui.my))
        self.cursorActive     = True 


"""
IF SOURCE CHANGES
OR TRACKED OBJECT CHANGES 
OR SPECIFIED TIME CHANGES
STOPWATCH WILL RE-INITIALISE

"""
class stopTimer():
    def __init__(self):
        self.stopWatchInitialised  = False
        self.stopWatchState        = None

    def stopWatch(self,countValue,source,trackedObject,gs,silence=False):
        complete = False
        
        # Re-Initialise automatically
        if(self.stopWatchInitialised):
            if(self.stopWatchState['source']!= source or self.stopWatchState['endCount']!= countValue or self.stopWatchState['trackedObject']!= trackedObject):
                if(silence!=True):
                    print('***initialising counter**** for : ' + str(source))

                self.stopWatchInitialised=False

        # Initialise stop watch 
        if(self.stopWatchInitialised==False):
            self.stopWatchState = {'elapsed': 0,'endCount':countValue,'source':source,'trackedObject':trackedObject}
            self.stopWatchInitialised=True

        if(self.stopWatchInitialised):
            self.stopWatchState['elapsed'] += gs.dt/1000
            #print('Iter: ' + str(self.itercount) + '  elapsed: ' + str(self.stopWatchState['elapsed']))
            if(self.stopWatchState['elapsed']>self.stopWatchState['endCount']):
                complete=True

        return(complete)

    def reset(self):
        self.stopWatchInitialised  = False
        self.stopWatchState        = None






class countDownTimer():
    def __init__(self):
        self.counter = None

    def countDownReal(self,count,game):
        if(self.counter==None): self.counter = count

        self.counter-=game.dt/1000
        if(self.counter<1):
            self.counter= None
            return(True,self.counter)

        return(False,self.counter)



class countUpTimer():
    def __init__(self):
        self.counter   = 0
        self.alarmTime = None
    
    def reset(self,alarmTime):
        self.alarmTime = alarmTime
        self.counter   = 0
    
    def countRealSeconds(self,alarmTime,game):
        # INIT
        if(self.alarmTime==None): 
            self.alarmTime = alarmTime

        try:
            self.counter+=game.dt/1000
        except:
            print("Failed to add to counter in countUpTimer, likely you didn't reset it ")
            exit()
        
        # RESET COUNTER, RETURN TRUE
        if(self.counter>self.alarmTime):
            self.counter= None
            return(True,self.counter)

        return(False,self.counter)








class loadingBarClass():
    def __init__(self,w,h,fillingColour,emptyColour,borderColour):
        self.w              = w
        self.h              = h 
        self.fillingColour  = fillingColour
        self.emptyColour    = emptyColour
        self.borderColour   = borderColour
        self.fillingPercent = 0

        self.fillingIncrement = 0.01
        self.loadComplete     = False

        # For a timed load, it works out the increments as %100
        self.startTime       = None
        self.endTime         = None
        self.duration        = None


    # BEST TO RESET EXTERNALLY TO BE SURE
    def reset(self):
        self.fillingPercent  = 0
        self.loadComplete    = False
        # timed
        self.startTime       = None
        self.endTime         = None
        self.duration        = None


    # FOR SHOW ONLY LOAD
    def erraticLoad(self,x,y,gui,borderThickness=2):
        
        #DRAW MAIN EMPTY BACKBAR
        pygame.draw.rect(gui.screen,(self.emptyColour),[x,y,self.w,self.h])
        
        # FILL UP THE BAR
        self.fillingPercent += self.fillingIncrement
        if(self.fillingPercent>=1):
            self.fillingPercent=1
            self.loadComplete = True

        #DRAW MAIN BAR
        pygame.draw.rect(gui.screen,(self.fillingColour),[x,y,self.fillingPercent*self.w,self.h])
        
        # DRAW OUTER BORDER
        if(self.borderColour!=None):
            pygame.draw.rect(gui.screen,(self.borderColour),[x,y,self.w,self.h],borderThickness)

        return(self.loadComplete)

    
    # you externally set the increment based on a percentage completion
    def load(self,x,y,gui,sourceDefinedIncrement,borderThickness=2,fillColour=None,emptyColour=None,cameraOffset=False):
        if(cameraOffset!=False):
            x = x - cameraOffset[0]
            y = y - cameraOffset[1]

        if(emptyColour==None):  emptyColour = self.emptyColour
        if(fillColour==None): fillColour = self.fillingColour
       


        #DRAW MAIN EMPTY BACKBAR
        pygame.draw.rect(gui.screen,(emptyColour),[x,y,self.w,self.h])
        
        # FILL UP THE BAR
        self.fillingPercent = sourceDefinedIncrement
        if(self.fillingPercent>=1):
            self.fillingPercent=1
            self.loadComplete = True

        #DRAW MAIN BAR
        pygame.draw.rect(gui.screen,(fillColour),[x,y,self.fillingPercent*self.w,self.h])
        
        # DRAW OUTER BORDER
        if(self.borderColour!=None):
            pygame.draw.rect(gui.screen,(self.borderColour),[x,y,self.w,self.h],borderThickness)

        return(self.loadComplete)

    def loadTimeIncrement(self,x,y,gui,game,duration,borderThickness=2):
        if(self.startTime== None):
            self.startTime = game.gameElapsed
            if(self.startTime==0):
                self.startTime = 0.00001
            self.duration  = duration
            self.endTime   = game.gameElapsed + duration
        

        increment = 1- (self.endTime - game.gameElapsed)/duration
        increment = round(increment,2)

        #DRAW MAIN EMPTY BACKBAR
        pygame.draw.rect(gui.screen,(self.emptyColour),[x,y,self.w,self.h])
        
        # FILL UP THE BAR
        self.fillingPercent = increment
        if(self.fillingPercent>=1):
            self.fillingPercent=1
            self.loadComplete = True

        #DRAW MAIN BAR
        pygame.draw.rect(gui.screen,(self.fillingColour),[x,y,self.fillingPercent*self.w,self.h])
        
        # DRAW OUTER BORDER
        if(self.borderColour!=None):
            pygame.draw.rect(gui.screen,(self.borderColour),[x,y,self.w,self.h],borderThickness)

        return(self.loadComplete)




class dynamicBorder():
    def __init__(self,borderColour = (200,0,0),changeDuration=0.15,noShadeShifts=6):
        self.borderTimer     = stopTimer()
        self.changeDuration  = changeDuration
        self.calledBy        = 'external'
        self.sbDirection     = 'lighten'
        self.borderColour    = borderColour
        self.summaryBChanges = 0
        self.noShadeShifts   = noShadeShifts


    def animateBorder(self,trackedName,game,gui):

        pygame.draw.rect(gui.screen, self.borderColour, [0.05*gui.w, 0.05*gui.h,0.9*gui.w ,0.9*gui.h],4)

        borderChange = self.borderTimer.stopWatch(self.changeDuration,trackedName, str(self.calledBy) + trackedName, game,silence=True)
        if(borderChange):
            if(self.sbDirection=='lighten'):
                self.borderColour = lighten(self.borderColour,lightenAmount=10)
            else:
                self.borderColour = darken(self.borderColour,darkenAmount=10)
            
            self.borderTimer.stopWatchInitialised = False
            self.summaryBChanges +=1
            if(self.summaryBChanges>self.noShadeShifts):
                self.summaryBChanges = 0
                if(self.sbDirection=='lighten'):
                    self.sbDirection = 'darken'
                else:
                    self.sbDirection = 'lighten'
        



def buttonWrap(x,y,text,core,w=None,textColour=None,buttonColour=None,font=None,fillColour=None):
    
    # ------OVERRIDES----

    tc,bc = (255,255,255),(40,40,200)
    if(textColour):
        tc=textColour
    if(buttonColour):
        bc = buttonColour
    if(font==None):
        font= core.font


    # ------TEXT------

    pad  = 20
    selected = False 
    ts     = font.render(text, True, tc)

    th     = ts.get_rect().height
    tw     = ts.get_rect().width

    if(w==None): w = tw+pad
    h      = th+pad
    tx     = x + 0.5*(w-tw)
    ty     = y + 0.5*(h-th)


    # -----------draw box
    if(fillColour):
        pygame.draw.rect(core.screen, (fillColour), [x,y,w,h])

    pygame.draw.rect(core.screen, (bc), [x,y,w,h],2)

    # HIGHLIGHT IF SELECTED
    if(core.mouseCollides(x,y,(w),(h))): 
        pygame.draw.rect(core.screen, (bc), [x,y,w,h])
        if(core.clicked): 
            core.pressed = False
            selected     = True
            core.clicked = False # RESET CLICKED BUTTON
    
    # ---- write text
    core.screen.blit(ts,(tx,ty))


    return(selected,x+w,y+h)


class stretchBox():
    def __init__(self,gui):
        self.x = 0.4*gui.w
        self.y = 0.4*gui.h
        self.w = 0.1*gui.w
        self.h = 0.1*gui.h

        self.borderColour    = gui.colourB
        self.borderThickness = 10


        self.expandRight       = False
        self.expandLeft        = False
        self.expandTop         = False
        self.expandBottom      = False

    def drawbox(self,gui):
        borderColour = self.borderColour

        # RIGHT SIDE SELECTED
        if(gui.mouseCollides(self.x+self.w-self.borderThickness,self.y,self.borderThickness,self.h)):
            borderColour = lighten(borderColour)
            if(gui.clicked):
                if(self.expandRight==False):
                    self.expandRight = True
                    gui.clicked = False
                    gui.pressed = False

        # LEFT SIDE SELECTED
        if(gui.mouseCollides(self.x,self.y,self.borderThickness,self.h)):
            borderColour = lighten(borderColour)
            if(gui.clicked):
                if(self.expandLeft==False):
                    self.expandLeft = True
                    gui.clicked = False
                    gui.pressed = False

        # TOP SELECTED
        if(gui.mouseCollides(self.x,self.y,self.w,self.borderThickness)):
            borderColour = lighten(borderColour)
            if(gui.clicked):
                if(self.expandTop==False):
                    self.expandTop = True
                    gui.clicked = False
                    gui.pressed = False

        # BOTTOM SELECTED
        if(gui.mouseCollides(self.x,self.y + self.h- self.borderThickness,self.w,self.borderThickness)):
            borderColour = lighten(borderColour)
            if(gui.clicked):
                if(self.expandBottom==False):
                    self.expandBottom = True
                    gui.clicked = False
                    gui.pressed = False




        # EXPAND BOX  

        if(self.expandRight):
            self.w = gui.mx - self.x
            if(gui.clicked):
                self.expandRight = False
                gui.clicked = False 
                gui.pressed = False

        if(self.expandLeft):
            rightXPoint = self.x + self.w
            self.x = gui.mx
            self.w = rightXPoint - self.x
            if(gui.clicked):
                self.expandLeft = False
                gui.clicked = False 
                gui.pressed = False

        if(self.expandTop):
            bottomPoint = self.y + self.h
            self.y = gui.my
            self.h = bottomPoint - self.y
            if(gui.clicked):
                self.expandTop = False
                gui.clicked = False
                gui.pressed = False

        if(self.expandBottom):
            self.h = gui.my - self.y
            if(gui.clicked):
                self.expandBottom = False
                gui.clicked = False 
                gui.pressed = False




        pygame.draw.rect(gui.screen, (borderColour), [self.x,self.y,self.w,self.h],self.borderThickness)


        printMe = buttonWrap(self.x + 30, self.y + self.h + 20,'P', gui,w=None)
        if(printMe[0]):
            print("""



                pygame.draw.rect(gui.screen, (borderColour), [x,y,w,h],borderThickness)
                x = {}
                y = {}
                w = {}
                h = {}
                borderColour = {}
                borderThickness = {}


                """.format(self.x,self.y,self.w,self.h,self.borderColour, self.borderThickness))




class dragSelector():
    def __init__(self):
        self.selecting       = False
        self.selectedX       = None
        self.selectedY       = None
        self.selectedW       = None
        self.selectedH       = None
        self.set             = False

        self.borderC         = (20,20,120)
        self.borderThickness = 3


    def dragSelect(self,gui,bm,camx,camy):

        # IF NOTHIGN SELECTED AND BUTTON HELD DOWN
        if(self.selecting==False):
            if(gui.pressed==True and self.set ==False):
                self.selecting = True
                self.selectedX = gui.mx
                self.selectedY = gui.my
                self.set = True


        # GET THE X AND Y POS
        if(self.selecting):
            self.selectedW = gui.mx - self.selectedX # MOUSE DIFF FROM FIRST CLICK TO AFTER
            self.selectedH = gui.my - self.selectedY

            # DEPENDING ON MOUSE ORIENTATION, ADJUST RECT TO MAKE IT WORK
            selected = None
            if(self.selectedW <0 and self.selectedH <0):
                 pygame.draw.rect(gui.screen, (self.borderC), [gui.mx,gui.my ,-self.selectedW,-self.selectedH],self.borderThickness)
                 selected = [gui.mx,gui.my ,-self.selectedW,-self.selectedH]
            elif(self.selectedW <0):
                pygame.draw.rect(gui.screen, (self.borderC), [gui.mx,self.selectedY ,-self.selectedW,self.selectedH],self.borderThickness)
                selected = [gui.mx,self.selectedY ,-self.selectedW,self.selectedH]
            elif(self.selectedH <0):
                pygame.draw.rect(gui.screen, (self.borderC), [self.selectedX,gui.my ,self.selectedW, -self.selectedH],self.borderThickness)
                selected = [self.selectedX,gui.my ,self.selectedW, -self.selectedH]
            else:
                pygame.draw.rect(gui.screen, (self.borderC), [self.selectedX,self.selectedY ,self.selectedW,self.selectedH],self.borderThickness)
                selected = [self.selectedX,self.selectedY ,self.selectedW,self.selectedH]

            # RETURN ARRAY ADJUSTED BY CAM
            if(gui.pressed==False):
                self.selecting = False
                self.set = False
                selected =[ selected[0] + camx, selected[1] + camy, selected[2], selected[3] ]
                return(selected)


        return(None)














#----------------------------------------
#    FOR TEXT THAT FLICKS LEFT TO RIGHT
#----------------------------------------

class scrollingDilaogue():

    def __init__(self,gui,x,y,w,h,borderColour):
        self.x                      = x
        self.y                      = y
        self.w                      = w
        self.h                      = h
        self.scrollInitialised      = False
        self.origText               = ''
        self.tempWriterArray        = []
        self.colour                 = (0,0,0)
        self.y                      = 0
        self.y2                     = 0
        
        self.timer                  = 15
        self.senPos                 = 0
        self.arrPos                 = 0
        self.arrIndex               = 0
        self.scrollSpeedOverride    = None
        self.finished               = False
        self.stopTimer              = stopTimer()
        self.borderColour           = borderColour

        #-----INITIALISE RESPONSE
        self.requiresResponse = False 
        self.responseOptions  = ["Yes.", "No."]
        self.buttonFillColour = (0,0,0)
        self.buttonTxtColour  = (255,255,255)
        self.response1        = button(200,30,0,0,self.responseOptions[0],self.buttonFillColour,gui.font,textColour=self.buttonTxtColour)
        self.response2        = button(200,30,0,0,self.responseOptions[1],self.buttonFillColour,gui.font,textColour=self.buttonTxtColour )
        self.response3        = button(200,30,0,0,self.responseOptions[1],self.buttonFillColour,gui.font,textColour=self.buttonTxtColour)

        self.cutOutDuration   = 'normal' # Time to pause when cutting out
    
    # POS[X,Y] ARE LEFT SIDE AND BOTTOM OF AVATAR
    def drawScrollingDialogue(self,gui, game,myfont, text,maxWidth,maxHeight,textStartingPos=(-1,-1),colour=None,scrollSpeed=10,vertInc=1.2,maxLines=5,cutOutWaitTime=5,skip=False):
        """
        function to scroll text, top/bottom with paging.
        """
        

        #   - starting text positions
        sx,sy      = textStartingPos[0],textStartingPos[1]
        x,y        = sx,sy
        
        clicked    = gui.clicked
        hovered    = gui.mouseCollides(x,y,maxWidth,maxHeight)
        
        # OVERRIDE COLOUR FROM CALLING FUNCTION
        if(colour!=None):
            self.colour = colour

        # RESET IF THE TEXT CHANGES FROM THE TEXT STORED IN STATE 
        if(self.origText!= text):

            self.scrollInitialised =False
            self.origText = text






        #----------------------------------------------------------
        #
        #    INITIALISE DIALOGUE
        #
        #----------------------------------------------------------

        if(self.scrollInitialised == False):
            self.colour      = (0,0,0)       # reset colour
            self.timer       = 15

            self.origText   = text
            # format paragraph into array of fitted sentences
            self.tempWriterArray   = []
            self.baseArray   = []
            self.y           = sy
            self.senPos      = 0
            self.arrPos      = 0
            self.arrIndex    = 0
            self.finished    = False
            

            #  BUILDING FULL DIALOGUE ARRAY FOR TEXT
            print('******************************************')
            print('BUILDING FULL DIALOGUE ARRAY FOR ' + str(text))
            print('******************************************')
            dialogueArray,para = [], ""
            for word in text.split(' '):
                pre   = para
                para += word + " "
                textsurface = myfont.render(para, True, self.colour)
                w = textsurface.get_rect().width
                if(w>= maxWidth):
                    dialogueArray.append(pre)
                    para = word + " "
            dialogueArray.append(para)

            
            self.baseArray       = dialogueArray   # Full Dialogue
            self.tempWriterArray = dialogueArray   # Actual Dialogue being printed
            self.arrIndex  = 5               # array index is the last line of given array slice
            

            # SET TEMPORARY TEXT ARRAY BASED UPON LINE LIMIT 
            if(len(self.tempWriterArray)>maxLines): 
                self.tempWriterArray = self.baseArray[0:self.arrIndex]
            self.scrollInitialised  = True




        #----------------------------------------------------------
        #
        #    OVERRIDE SPEED (SET EXTERNALLY VIA PLOT->MESSAGEUPDATE->HERE)
        #
        #----------------------------------------------------------
        if(self.scrollSpeedOverride=='fast'):
            scrollSpeed    = 0
        if(self.scrollSpeedOverride=='normal'):
            scrollSpeed    = 1
        if(self.scrollSpeedOverride=='slow'):
            scrollSpeed    = 3

        if(self.cutOutDuration=='instant'):
            cutOutWaitTime = 0
        if(self.cutOutDuration=='fast'):
            cutOutWaitTime = 1
        if(self.cutOutDuration=='normal'):
            cutOutWaitTime = 3
        if(self.cutOutDuration=='slow'):
            cutOutWaitTime = 4
        if(self.cutOutDuration=='verySlow'):
            cutOutWaitTime = 7
        if(self.cutOutDuration=='untilClicked'):
            cutOutWaitTime = 3




        #----------------------------------------------------------
        #
        #    NEXT PAGE & SKIP
        #
        #----------------------------------------------------------
        if((hovered and clicked) or gui.input.returnedKey.upper()=='RETURN'): 
            
            # IF BEFORE THE LAST PAGE 
            # array index is the last line of given array slice
            if(self.arrIndex<len(self.baseArray)):
                self.tempWriterArray = self.baseArray[self.arrIndex:(self.arrIndex+maxLines)] # GO TO NEXT PAGE
                self.arrIndex  = self.arrIndex + maxLines
                self.arrPos     = 0
                self.senPos     = 0
                self.y          = sy
            else:
                if(skip):
                    self.finished            = True
                    self.scrollSpeedOverride = None


        

        #----------------------------------------------------------
        #
        #    PRINT ALL PREVIOUS LINES
        #
        #----------------------------------------------------------
        
        self.y2 = sy
        for row in range(0,self.arrPos):
            currentSentence = self.tempWriterArray[row]
            ts = myfont.render(currentSentence, True, self.colour)
            h = ts.get_rect().height
            gui.screen.blit(ts,(x,self.y2))
            self.y2=self.y2+ vertInc*h


        #----------------------------------------------------------
        #
        #    SCROLL CURRENT LINE
        #
        #----------------------------------------------------------

        currentSentence = self.tempWriterArray[self.arrPos]
        for word in (range(0,len(currentSentence[self.senPos]) )):
            printSentence = currentSentence[:self.senPos]
            ts = myfont.render(printSentence, True, self.colour)
            h = ts.get_rect().height
        gui.screen.blit(ts,(x,self.y))
        x=sx


        #--------------increment sen/array
        self.timer-=1
        if(self.timer<1):
            self.timer=scrollSpeed

            # Increment sentence print position
            if(len(currentSentence)-2 >=self.senPos):
                self.senPos+=1
            else:
                # Increment array Position
                if(len(self.tempWriterArray)-2>=self.arrPos):
                    self.arrPos +=1
                    self.y=self.y+vertInc*h
                    self.senPos=0
                else:
                    # If at end of array, end of elem and true end
                    if(self.arrIndex>=len(self.baseArray)):
                        self.finished    = 'End of Text'
        

        #================================================
        #
        #               FINISH UP
        #       
        #   ADD DELAY BEFORE FINISHING (DEFINED BY cutOutWaitTime 
        #   WHICH IS SCROLLOVERRIDE VALUE)
        #
        #   IF REQUIRES RESPONSE SET THEN THAT HAPPENS FIRST
        #
        #================================================

        # WRAP UP AND WAIT FOR CUTOUT TIME
        if(self.finished=='End of Text' and self.requiresResponse==False and self.cutOutDuration!='untilClicked'):
            swComplete = self.stopTimer.stopWatch(cutOutWaitTime,'displayAlert',text,game)
            if(swComplete):
                self.scrollSpeedOverride = None
                self.finished            = True
        # OR WAIT UNTIL RESPONSE GIVEN
        elif(self.finished=='End of Text' and self.requiresResponse==True):
            
            # GET DIMENSIONS TO POSITION BUTTON BETTER
            rw1,rh1      = self.response1.displayReturnButtonDimensions(gui,textOverride=self.responseOptions[0], widthOverride='tight',fontOverride=self.response1.font)
            rw2,rh2      = self.response2.displayReturnButtonDimensions(gui,textOverride=self.responseOptions[1], widthOverride='tight',fontOverride=self.response2.font)

            horizontalGap = 0.05*self.w
            x_response   = self.x + 0.5*(self.w-(rw1+rw2+horizontalGap))
            y_response   = self.y+self.h - 1.5*rh1 - 7 # 7 is border 
            optionOne,bw,bh = self.response1.display(gui,textOverride=self.responseOptions[0], widthOverride='tight',noBorder=False,fillColour=darken(self.buttonFillColour),updatePos=[x_response,y_response],                             hoverBoxCol=lighten(self.buttonFillColour),hoverTextCol=self.buttonTxtColour,borderColour=self.borderColour)
            optionTwo,bw,bh = self.response2.display(gui,textOverride=self.responseOptions[1], widthOverride='tight',noBorder=False,fillColour=darken(self.buttonFillColour),updatePos=[x_response + bw + horizontalGap,y_response],        hoverBoxCol=lighten(self.buttonFillColour),hoverTextCol=self.buttonTxtColour,borderColour=self.borderColour)

            
            # --- wrap up once response captured
            if(optionOne):
                game.plotTracker[game.state]['response'] = self.responseOptions[0]
                self.requiresResponse = False
                self.responseOptions = ['Yes','No']
            if(optionTwo):
                game.plotTracker[game.state]['response'] = self.responseOptions[1]
                self.requiresResponse = False
                self.responseOptions = ['Yes','No']
        # OR WAIT UNTIL CLICKED
        elif(self.finished=='End of Text' and self.requiresResponse==False and self.cutOutDuration=='untilClicked'):
            swComplete = self.stopTimer.stopWatch(cutOutWaitTime,'displayAlert',text,game)
            if(swComplete):
                if( (hovered and clicked) or gui.user_input.returnedKey=='return'):
                    self.scrollSpeedOverride = None
                    self.finished            = True


        return(self.finished)







