from pathlib import Path
import pygame
import os
from utils._gui import *
from utils._input import *
from utils._game import *
from utils._utils import imageAnimate
from utils._utils import loadImageFiles

width, height  = 1500 ,850                 # Can be adjusted
FPS            = 90                        # Frame rate
state          = 'START'    # This determines what part of the plot

pygame.init()
pygame.display.set_caption("Steel Spirit")
clock          = pygame.time.Clock()
nextFrame      = pygame.time.get_ticks()
monitorSize    = [pygame.display.Info().current_w,pygame.display.Info().current_h]
screen         = pygame.display.set_mode((width,height),pygame.DOUBLEBUF)




#------------PATH STUFF 

BASEPATH       = str(Path(os.getcwd() ).parent.absolute()) + '/'
ASSETSPATH     = '/Users/adammcmurchie/Pictures/aseprite_myProjects/Steel_Spirit/assets/'
FONTPATH       = ASSETSPATH   + 'fonts/'
IMAGEASSETPATH = ASSETSPATH   + ''


# THIS CAN BE SET AND ADDED TO THE FUNCTION IN GUI TO ADD DIFFERENT COLOUR SCHEMES
guiTheme       = 'main'  


gui                = gui(screen,width,height,guiTheme, IMAGEASSETPATH=IMAGEASSETPATH)

#------------FONTS 

gui.nokiaFont      = pygame.font.Font(FONTPATH + '/nokiafc22.ttf', 25)
gui.nanoNokiaFont  = pygame.font.Font(FONTPATH + '/nokiafc22.ttf', 14)
gui.smallNokiaFont = pygame.font.Font(FONTPATH + '/nokiafc22.ttf', 18)
gui.bigNokiaFont   = pygame.font.Font(FONTPATH + '/nokiafc22.ttf', 37)
gui.hugeNokiaFont   = pygame.font.Font(FONTPATH + '/nokiafc22.ttf', 45)

gui.font           = pygame.font.Font(FONTPATH + '/Orbitron-Regular.ttf', 25)
gui.nanoFont       = pygame.font.Font(FONTPATH + '/Orbitron-Regular.ttf', 14)
gui.vSmallFont     = pygame.font.Font(FONTPATH + '/Orbitron-Regular.ttf', 14)
gui.smallishFont   = pygame.font.Font(FONTPATH + '/Orbitron-Regular.ttf', 18)
gui.smallFont      = pygame.font.Font(FONTPATH + '/Orbitron-Regular.ttf', 20)
gui.largeFont      = pygame.font.Font(FONTPATH + '/Orbitron-Regular.ttf', 26)
gui.bigFont        = pygame.font.Font(FONTPATH + '/Orbitron-Regular.ttf', 32)
gui.hugeFont       = pygame.font.Font(FONTPATH + '/Orbitron-Regular.ttf', 40)
gui.jumboFont      = pygame.font.Font(FONTPATH + '/Orbitron-Regular.ttf', 50)



gui.fontTerminator      = pygame.font.Font(FONTPATH + '/future-earth.ttf', 25)
gui.fontTerminatorL     = pygame.font.Font(FONTPATH + '/future-earth.ttf', 30)


gui.sizeFont           = gui.font.size("S")
gui.sizeNanoFont       = gui.nanoFont.size("S")
gui.sizeVSmallFont     = gui.vSmallFont.size("S")
gui.sizeSmallishFont   = gui.smallishFont.size("S")
gui.sizeSmallFont      = gui.smallFont.size("S")
gui.sizeBigFont        = gui.bigFont.size("S")
gui.sizeHugeFont       = gui.hugeFont.size("S")
gui.sizeJumboFont      = gui.jumboFont.size("S")


gui.squareFont       = pygame.font.Font(FONTPATH + 'FORCEDSQUARE.ttf', 28)
gui.squareFontNano   = pygame.font.Font(FONTPATH + 'FORCEDSQUARE.ttf', 20)
gui.squareFontSmall  = pygame.font.Font(FONTPATH + 'FORCEDSQUARE.ttf', 22)
gui.squareFontMed    = pygame.font.Font(FONTPATH + 'FORCEDSQUARE.ttf', 26)
gui.squareFontH      = pygame.font.Font(FONTPATH + 'FORCEDSQUARE.ttf', 28)


gui.titleFont         = pygame.font.Font(FONTPATH + 'squids.ttf', 60)
gui.titleFontB        = pygame.font.Font(FONTPATH + 'squids.ttf', 90)



# ------ IMAGES   


# -----MENU/STARTUP

# -----MENU/STARTUP
gui.titleLogo        = pygame.image.load(IMAGEASSETPATH + '/scenes/title/titleLogo.png')
gui.blueFire         = [pygame.image.load(IMAGEASSETPATH + 'scenes/title/bluefire1.png'),pygame.image.load(IMAGEASSETPATH + 'scenes/title/bluefire2.png') ,pygame.image.load(IMAGEASSETPATH + 'scenes/title/bluefire3.png') ,pygame.image.load(IMAGEASSETPATH + 'scenes/title/bluefire4.png')]
gui.bluefireEntry    = loadImageFiles('blueFireEntry1.png',IMAGEASSETPATH + 'scenes/title/',convert=False)
gui.planet           = pygame.image.load(IMAGEASSETPATH + 'scenes/title/planet.png')
gui.coverLogo         = pygame.image.load(IMAGEASSETPATH + 'cover/logo.png')
gui.cover1            = pygame.image.load(IMAGEASSETPATH + 'cover/altCover.png')
gui.cover2            = pygame.image.load(IMAGEASSETPATH + 'cover/altCover2.png')
gui.cover3            = pygame.image.load(IMAGEASSETPATH + 'cover/altCover3.png')
gui.cyborgCover       = pygame.image.load(IMAGEASSETPATH + 'cover/cyborgGirl.png')
gui.bunnyGirlYCover   = pygame.image.load(IMAGEASSETPATH + 'cover/bunnyGirlYellowCover.png')


# ----- UNITS AND PLAYER 

gui.player            = loadImageFiles('fighter1.png',IMAGEASSETPATH + 'fighter/',convert=False)
gui.playerBoost       = loadImageFiles('fighterBoost1.png',IMAGEASSETPATH + 'fighter/',convert=False)
gui.playerShadow      = loadImageFiles('shadow1.png',IMAGEASSETPATH + 'fighter/',convert=False)
gui.playerHit         = loadImageFiles('playerHit1.png',IMAGEASSETPATH + 'fighter/',convert=False)

gui.scoutRed          = loadImageFiles('crabRed1.png',IMAGEASSETPATH + 'enemies/crab/',convert=False)
gui.scoutRedHit       = loadImageFiles('crabRedhit1.png',IMAGEASSETPATH + 'enemies/crab/',convert=False)

gui.tank              = loadImageFiles('sandTank1.png',IMAGEASSETPATH + 'enemies/tank/',convert=False)
gui.tankHit           = loadImageFiles('sandTankHit1.png',IMAGEASSETPATH + 'enemies/tank/',convert=False)
gui.turret            = [pygame.image.load(IMAGEASSETPATH + 'enemies/tank/turret.png')]




# ---------BULLETS AND WEAPONS

gui.slitherShot            = loadImageFiles('slither1.png',IMAGEASSETPATH + 'ordinance/',convert=False)
gui.triBlast               = loadImageFiles('triBlast1.png',IMAGEASSETPATH + 'ordinance/',convert=False)

gui.lockOn                 = loadImageFiles('lockon1.png',IMAGEASSETPATH + 'gui/',convert=False)
gui.lockOnStill            = pygame.image.load(IMAGEASSETPATH + '/gui/stillLockedOn.png')

# ---------TILE SETS
gui.grassTiles         = loadImageFiles('grass1.png',IMAGEASSETPATH + 'tilesets/grassV1/',convert=True)
gui.concreteTiles      = loadImageFiles('concrete1.png',IMAGEASSETPATH + 'tilesets/concrete/',convert=True)
gui.sandTiles          = loadImageFiles('sand1.png',IMAGEASSETPATH + 'tilesets/sandv1/',convert=True)
gui.base100            = loadImageFiles('base100_1.png',IMAGEASSETPATH + 'tilesets/template/',convert=True)
gui.water              = loadImageFiles('water1.png',IMAGEASSETPATH + 'tilesets/water/',convert=True)
gui.tileDict           = {'Grass': gui.grassTiles,
						  'Concrete': gui.concreteTiles,
						  'sand': gui.sandTiles,
						  'base': gui.base100,
						  'water': gui.water
						  }


gui.smallRedExplosion      = loadImageFiles('explosion1.png',IMAGEASSETPATH + 'explosions/smallExplosion/')
gui.smallYellowExplosion   = loadImageFiles('explosion1.png',IMAGEASSETPATH + 'explosions/explosionParticle/')

# ------ CLASS ATTRS

gui.animate = imageAnimate(0,10,10,name='guiAnimationObj')
game        = gameObject(ASSETSPATH,gui)
user_input  = userInputObject("","", gui)
game.input  = user_input

#gui.statusButton  = button(0.15*width,0.05*height,width/17,height/13,'ST',(0,128,0),gui.bigNokiaFont,textColour=(97,165,93))
