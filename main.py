
# -----ALL VARIABLES & CLASSES IMPORTED FROM SETUP
import pygame
import time
import math
import random
import json
import os, sys

# -----ALL VARIABLES & CLASSES IMPORTED FROM SETUP

from utils.setup import *

while game.running:

	# -------------NEXT CYCLE 

    game.itercount                +=1                          # INCREMENT LOOP COUNT
    gui.resetMouseInputs()
    gui.screen.fill((0, 0, 0))                                 # DRAW BLACK BG
    user_input.returnedKey =''
    gui.mx, gui.my = pygame.mouse.get_pos()

    

    # -------------PROCESS STANDARD INPUT EVENTS

    for event in pygame.event.get():
        pos            = pygame.mouse.get_pos()
        if event.type == pygame.QUIT: game.running = False

        if pygame.mouse.get_pressed()[0]:
            gui.pressed = True

        
        if(event.type==pygame.MOUSEBUTTONUP):
            gui.pressed = False
        if event.type == pygame.MOUSEBUTTONDOWN: 
            if(event.button==1):
                gui.clicked  = True
            if(event.button==3):
                gui.rightClicked = True
            
            if(event.button==4):
                gui.scrollUp  = True
            if(event.button==5):
                gui.scrollDown = True
                
        gui.input              = user_input.getButtonInputs(event)

    gui.mx, gui.my             = pygame.mouse.get_pos()        # GET MOUSE POS

    
    # -----------MANAGE EVENTS AND PLOT 
    game.coordinateGame(gui)

    # Flip the display
    pygame.display.flip() 
    
    # TICK

    game.dt           = clock.tick(game.FPS)     # GET TIME INCREMENT
    game.elapsed     += game.dt/1000        # UPDATE TIME ELAPSED
    continue



pygame.quit()   # END GAME WHEN LOOP EXITS




