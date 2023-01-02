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
gui.smallishFont   = pygame.font.Font(FONTPATH + '/Orbitron-Regular.ttf', 23)
gui.smallFont      = pygame.font.Font(FONTPATH + '/Orbitron-Regular.ttf', 20)
gui.nanoFont       = pygame.font.Font(FONTPATH + '/Orbitron-Regular.ttf', 14)
gui.vSmallFont     = pygame.font.Font(FONTPATH + '/Orbitron-Regular.ttf', 14)
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
gui.kira              = pygame.image.load(IMAGEASSETPATH + 'cover/kira.png')
gui.madge             = pygame.image.load(IMAGEASSETPATH + 'cover/madge.png')
gui.madgeInv          = pygame.image.load(IMAGEASSETPATH + 'cover/madgeInv.png')
gui.bunnyTank         = pygame.image.load(IMAGEASSETPATH + 'cover/bunnyTank.png')
gui.cherry            = pygame.image.load(IMAGEASSETPATH + 'cover/cherry.png')
gui.sarah             = pygame.image.load(IMAGEASSETPATH + 'cover/sarah.png')
gui.apacheJack        = pygame.image.load(IMAGEASSETPATH + 'cover/apacheJack.png')
gui.cyborgCover       = pygame.image.load(IMAGEASSETPATH + 'cover/cyborgGirl.png')
gui.bunnyGirlYCover   = pygame.image.load(IMAGEASSETPATH + 'cover/bunnyGirlYellowCover.png')


# ----- UNITS AND PLAYER 

gui.player            = loadImageFiles('fighter1.png',IMAGEASSETPATH + 'fighter/',convert=False)
gui.playerShooting    = loadImageFiles('fighterShooting1.png',IMAGEASSETPATH + 'fighter/',convert=False)
gui.playerBoost       = loadImageFiles('fighterBoost1.png',IMAGEASSETPATH + 'fighter/',convert=False)
gui.playerShadow      = loadImageFiles('shadow1.png',IMAGEASSETPATH + 'fighter/',convert=False)
gui.playerHit         = loadImageFiles('playerHit1.png',IMAGEASSETPATH + 'fighter/',convert=False)


gui.player            = loadImageFiles('g12_1.png',IMAGEASSETPATH + 'fighter/',convert=False)
gui.playerShooting    = loadImageFiles('g12_Shooting1.png',IMAGEASSETPATH + 'fighter/',convert=False)
gui.playerBoost       = loadImageFiles('g12_boost1.png',IMAGEASSETPATH + 'fighter/',convert=False)
gui.playerShadow      = loadImageFiles('g12_Shadow1.png',IMAGEASSETPATH + 'fighter/',convert=False)
gui.playerHit         = loadImageFiles('g12_Hit1.png',IMAGEASSETPATH + 'fighter/',convert=False)





gui.scoutRed          = loadImageFiles('crabRed1.png',IMAGEASSETPATH + 'units/crab/',convert=False)
gui.scoutRedHit       = loadImageFiles('crabRedhit1.png',IMAGEASSETPATH + 'units/crab/',convert=False)

gui.tank              = loadImageFiles('sandTank1.png',IMAGEASSETPATH + 'units/tank/',convert=False)
gui.tankHit           = loadImageFiles('sandTankHit1.png',IMAGEASSETPATH + 'units/tank/',convert=False)
gui.turret            = [pygame.image.load(IMAGEASSETPATH + 'units/tank/turret.png')]
gui.turretHit         = loadImageFiles('sandTankTurretHit1.png',IMAGEASSETPATH + 'units/tank/',convert=False)
gui.tankStatic        = pygame.image.load(IMAGEASSETPATH + 'units/tank/sandTankStatic.png')
gui.tankRemains       = loadImageFiles('tankCarcass1.png',IMAGEASSETPATH + 'units/tank/',convert=False)


gui.greenTank              = loadImageFiles('greenTank1.png',IMAGEASSETPATH + 'units/tank/',convert=False)
gui.greenTankHit           = loadImageFiles('greenTankhit1.png',IMAGEASSETPATH + 'units/tank/',convert=False)
gui.greenTurret            = [pygame.image.load(IMAGEASSETPATH + 'units/tank/greenTurret.png')]
gui.greenTurretHit         = loadImageFiles('greenTankTurretHit1.png',IMAGEASSETPATH + 'units/tank/',convert=False)
gui.greenTankStatic        = pygame.image.load(IMAGEASSETPATH + 'units/tank/greenTankStatic.png')
gui.greenTankRemains       = loadImageFiles('greenTankCarcass1.png',IMAGEASSETPATH + 'units/tank/',convert=False)


gui.attackBoat              = loadImageFiles('attackBoat1.png',IMAGEASSETPATH + 'units/attackBoat/',convert=False)
gui.attackBoatHit           = loadImageFiles('attackBoatHit1.png',IMAGEASSETPATH + 'units/attackBoat/',convert=False)
gui.attackBoatTurret        = [pygame.image.load(IMAGEASSETPATH + 'units/attackBoat/attackBoatTurret.png')]
gui.attackBoatTurretHit     = loadImageFiles('attackBoatTurretHit1.png',IMAGEASSETPATH + 'units/attackBoat/',convert=False)
gui.attackBoatStatic        = pygame.image.load(IMAGEASSETPATH + 'units/attackBoat/attackBoatStatic.png')


gui.aaSmall           = loadImageFiles('aaSmall1.png',IMAGEASSETPATH + 'units/AA_burst/',convert=False)
gui.aaSmallHit        = loadImageFiles('aaSmallHit1.png',IMAGEASSETPATH + 'units/AA_burst/',convert=False)
gui.aaSmallTurret     = [pygame.image.load(IMAGEASSETPATH + 'units/AA_burst/aaSmallTurret.png')]
gui.aaSmallTurretHit  = loadImageFiles('aaSmallTurretHit1.png',IMAGEASSETPATH + 'units/AA_burst/',convert=False)
gui.aaSmallStatic     = pygame.image.load(IMAGEASSETPATH + 'units/AA_burst/aaSmall.png')
gui.aaSmallRemains    = loadImageFiles('aaSmallCarcass1.png',IMAGEASSETPATH + 'units/AA_burst/',convert=False)

gui.mlrs              = loadImageFiles('mlrs1.png',IMAGEASSETPATH + 'units/MLRS/',convert=False)
gui.mlrsHit           = loadImageFiles('mlrsHit1.png',IMAGEASSETPATH + 'units/MLRS/',convert=False)
gui.mlrsTurret        = [pygame.image.load(IMAGEASSETPATH + 'units/MLRS/mlrsTurret1.png')]
gui.mlrsTurretHit     = loadImageFiles('mlrsTurretHit1.png',IMAGEASSETPATH + 'units/MLRS/',convert=False)
gui.mlrsStatic        = pygame.image.load(IMAGEASSETPATH + 'units/MLRS/mlrsStatic.png')
gui.mlrsRemains       = loadImageFiles('mlrsRemains1.png',IMAGEASSETPATH + 'units/MLRS/',convert=False)



# ---------BUILDINGS INTERACTABLE


gui.bioLab                    = [pygame.image.load(IMAGEASSETPATH + 'buildings/biolab/bioLab.png')]
gui.bioLabHit                 = loadImageFiles('bioLabHit1.png',IMAGEASSETPATH + 'buildings/biolab/',convert=False)
gui.bioLabRemains             = loadImageFiles('bioLabRemains1.png',IMAGEASSETPATH + 'buildings/biolab/',convert=False)


gui.barrelGroupRed            = [pygame.image.load(IMAGEASSETPATH + 'buildings/barrel/barrelGroupRed.png')]
gui.barrelGroupRedHit         = loadImageFiles('barrelGroupRedHit1.png',IMAGEASSETPATH + 'buildings/barrel/',convert=False)
gui.barrelGroupRedRemains     = loadImageFiles('barellGroupRedRemains1.png',IMAGEASSETPATH + 'buildings/barrel/',convert=False)



# ---------BULLETS AND WEAPONS

gui.slitherShot            = loadImageFiles('slither1.png',IMAGEASSETPATH + 'ordinance/',convert=False)
gui.triBlast               = loadImageFiles('triBlast1.png',IMAGEASSETPATH + 'ordinance/',convert=False)
gui.yellowPlasma           = loadImageFiles('yellowPlasmaBall1.png',IMAGEASSETPATH + 'ordinance/',convert=False)
gui.hotRound               = loadImageFiles('hotRound1.png',IMAGEASSETPATH + 'ordinance/hotRound/',convert=False)

gui.streakerMissile        = loadImageFiles('missile1.png',IMAGEASSETPATH + 'ordinance/missiles/',convert=False)
gui.streakerGray           = loadImageFiles('grayMissile1.png',IMAGEASSETPATH + 'ordinance/missiles/',convert=False)
gui.missilePlume           = loadImageFiles('missilePlume1.png',IMAGEASSETPATH + 'ordinance/plumes/',convert=True)

# SETTING TRANS
#[x.set_colorkey((0, 0, 0)) for x in gui.missilePlume]
[x.set_alpha(130) for x in gui.missilePlume]


#gui.missilePlumeLong       = loadImageFiles('missilePlumeLong1.png',IMAGEASSETPATH + 'ordinance/plumes/',convert=False)
gui.missileExplosion       = loadImageFiles('missileExplosion1.png',IMAGEASSETPATH + 'explosions/missileExplosion/',convert=False)

gui.chaffHead              = loadImageFiles('chaffHead1.png',IMAGEASSETPATH + 'ordinance/flares/',convert=False)


gui.lockOn                 = loadImageFiles('lockon1.png',IMAGEASSETPATH + 'gui/',convert=False)
gui.lockOnStill            = pygame.image.load(IMAGEASSETPATH + '/gui/stillLockedOn.png')

# ---------TILE SETS
gui.grassTiles         = loadImageFiles('grass1.png',IMAGEASSETPATH + 'tilesets/grassV1/',convert=True)
gui.grassLight         = loadImageFiles('grass1.png',IMAGEASSETPATH + 'tilesets/grassLight/',convert=True)
gui.concreteTiles      = loadImageFiles('concrete1.png',IMAGEASSETPATH + 'tilesets/concrete/',convert=True)
gui.sandTiles          = loadImageFiles('sand1.png',IMAGEASSETPATH + 'tilesets/sandv1/',convert=True)
gui.base100            = loadImageFiles('base100_1.png',IMAGEASSETPATH + 'tilesets/template/',convert=True)
gui.water              = loadImageFiles('water1.png',IMAGEASSETPATH + 'tilesets/water/',convert=True)
gui.pilonDR            = loadImageFiles('pilon1.png',IMAGEASSETPATH + 'tilesets/pilonDiagonalRight/',convert=False)
gui.pilonDL            = loadImageFiles('pilon1.png',IMAGEASSETPATH + 'tilesets/pilonDiagonalLeft/',convert=False)

gui.tileDict           = {'Grass': gui.grassTiles,
						  'grassLight': gui.grassLight,
						  'Concrete': gui.concreteTiles,
						  'sand': gui.sandTiles,
						  'base': gui.base100,
						  'water': gui.water,
						  }

gui.layer2Dict           = {'Grass': gui.grassTiles,
						  'grassLight': gui.grassLight,
						  'Concrete': gui.concreteTiles,
						  'sand': gui.sandTiles,
						  'base': gui.base100,
						  'water': gui.water,
						  'pilonDR': gui.pilonDR,
						  'pilonDL:': gui.pilonDL,
						  }



gui.enemyDict          = {'scout':{'special':['command1','command2'],'image': gui.scoutRed[0]}, 
						  'tank':{'special':['command1','command2'],'image': gui.tankStatic},
						  'greenTank':{'special':['command1','command2'],'image': gui.greenTankStatic},
						  'attackBoat':{'special':['command1','command2'],'image': gui.attackBoatStatic},
						  'mlrs':{'special':['command1','command2'],'image': gui.mlrsStatic},
						  'aaSmall':{'special':['command1','command2'],'image': gui.aaSmallStatic}, 
						  'bioLab':{'special':['command1','command2'],'image': gui.bioLab[0]},
						  'barrelRed':{'special':['command1','command2'],'image': gui.barrelGroupRed[0]}, 

							}



gui.smallRedExplosion      = loadImageFiles('explosion1.png',IMAGEASSETPATH + 'explosions/smallExplosion/')
gui.redExplosion          = loadImageFiles('explosion1.png',IMAGEASSETPATH + 'explosions/explosion/')
gui.bigCloudyExplosion     = loadImageFiles('explosion1.png',IMAGEASSETPATH + 'explosions/bigCloud/')
gui.smallCloudyExplosion   = loadImageFiles('explosion1.png',IMAGEASSETPATH + 'explosions/cloudExplosion/')
gui.smallYellowExplosion   = loadImageFiles('explosion1.png',IMAGEASSETPATH + 'explosions/explosionParticle/')







#---------------------CUTSCENE

# CHARACTERS 

#gui.gainsborough = pygame.image.load(IMAGEASSETPATH + 'characters/gainsborough.png')
gui.allyCodec         = loadImageFiles('allyCodec1.png',IMAGEASSETPATH + 'characters/mask/')
gui.enemyCodec        = loadImageFiles('enemyCodec1.png',IMAGEASSETPATH + 'characters/mask/')
gui.allyBorder        = pygame.image.load(IMAGEASSETPATH + 'characters/mask/maskAlly.png')
gui.enemyBorder       = pygame.image.load(IMAGEASSETPATH + 'characters/mask/maskEnemy.png')

gui.allyUnderlay      = pygame.image.load(IMAGEASSETPATH + 'characters/mask/allyUnderlay.png')
gui.enemyUnderlay     = pygame.image.load(IMAGEASSETPATH + 'characters/mask/enemyUnderlay.png')

# CLAIRE
gui.claire            = pygame.image.load(IMAGEASSETPATH + 'characters/claire/claireNeutral.png')
gui.claireBlink       = pygame.image.load(IMAGEASSETPATH + 'characters/claire/claireBlink.png')
gui.claireTalk        = loadImageFiles('claireTalk1.png',IMAGEASSETPATH + 'characters/claire/')
gui.claireShocked     = loadImageFiles('claireShocked1.png',IMAGEASSETPATH + 'characters/claire/')
talkFrames            = 3* gui.claireTalk + [gui.claireBlink]
gui.claireTalking     = imageAnimateAdvanced(talkFrames,0.2)




# ------ CLASS ATTRS

gui.animate = imageAnimate(0,10,10,name='guiAnimationObj')
game        = gameObject(ASSETSPATH,gui)
user_input  = userInputObject("","", gui)
game.input  = user_input

#gui.statusButton  = button(0.15*width,0.05*height,width/17,height/13,'ST',(0,128,0),gui.bigNokiaFont,textColour=(97,165,93))
