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


gui.tilePath       = ASSETSPATH + 'tilesets/'
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
gui.picoFont       = pygame.font.Font(FONTPATH + '/Orbitron-Regular.ttf', 8)
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


# -----MAP EDITOR

gui.saveIcon          = pygame.image.load(IMAGEASSETPATH + 'gui/save1.png')
gui.saveIcon2          = pygame.image.load(IMAGEASSETPATH + 'gui/save2.png')
gui.loadIcon           = pygame.image.load(IMAGEASSETPATH + 'gui/load1.png')
gui.loadIcon2          = pygame.image.load(IMAGEASSETPATH + 'gui/load2.png')
gui.openTileWindow     = pygame.image.load(IMAGEASSETPATH + 'gui/tileWindow1.png')
gui.openTileWindow2    = pygame.image.load(IMAGEASSETPATH + 'gui/tileWindow2.png')
gui.L1_1               = pygame.image.load(IMAGEASSETPATH + 'gui/L1_1.png')
gui.L1_2		       = pygame.image.load(IMAGEASSETPATH + 'gui/L1_2.png')
gui.L2_1               = pygame.image.load(IMAGEASSETPATH + 'gui/L2_1.png')
gui.L2_2		       = pygame.image.load(IMAGEASSETPATH + 'gui/L2_2.png')
gui.Anim_1             = pygame.image.load(IMAGEASSETPATH + 'gui/Anim_1.png')
gui.Anim_2		       = pygame.image.load(IMAGEASSETPATH + 'gui/Anim_2.png')
gui.E_1                = pygame.image.load(IMAGEASSETPATH + 'gui/E_1.png')
gui.E_2		           = pygame.image.load(IMAGEASSETPATH + 'gui/E_2.png')
gui.S_1                = pygame.image.load(IMAGEASSETPATH + 'gui/S_1.png')
gui.S_2		           = pygame.image.load(IMAGEASSETPATH + 'gui/S_2.png')
gui.Q_1                = pygame.image.load(IMAGEASSETPATH + 'gui/Q_1.png')
gui.Q_2		           = pygame.image.load(IMAGEASSETPATH + 'gui/Q_2.png')
gui.openTileWindow     = pygame.image.load(IMAGEASSETPATH + 'gui/tileWindow1.png')
gui.openTileWindow2    = pygame.image.load(IMAGEASSETPATH + 'gui/tileWindow2.png')
gui.next               = pygame.image.load(IMAGEASSETPATH + 'tilesets/50/template/base100_5.png')
gui.next2              = pygame.image.load(IMAGEASSETPATH + 'tilesets/50/template/base100_6.png')


# -----MENU/STARTUP
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



# ----- GUI

gui.objectiveArrow         = loadImageFiles('directionArrow1.png',IMAGEASSETPATH + 'gui/')
gui.shipHealthDisplay      = {"100": pygame.image.load(IMAGEASSETPATH + 'gui/guibox/playerIcon_100percent.png'),
							  "10": pygame.image.load(IMAGEASSETPATH + 'gui/guibox/playerIcon_10percent.png')}

gui.weaponsLoadout         = {"missiles_1hot": pygame.image.load(IMAGEASSETPATH + 'gui/guibox/loadOut_missles_1HotRounds.png'),
							  "missiles_2hot": pygame.image.load(IMAGEASSETPATH + 'gui/guibox/loadOut_missles_2HotRounds.png'),
							  "missiles_3hot": pygame.image.load(IMAGEASSETPATH + 'gui/guibox/loadOut_missles_3HotRounds.png'),
							  "missiles_angleRound": pygame.image.load(IMAGEASSETPATH + 'gui/guibox/loadOut_missles_angleRound.png'),
							  "missiles_angleRoundFaster": pygame.image.load(IMAGEASSETPATH + 'gui/guibox/loadOut_missles_angleRoundFaster.png'),
							  "missiles_angleRoundFullSpeed": pygame.image.load(IMAGEASSETPATH + 'gui/guibox/loadOut_missles_angleRoundFullSpeed.png'),
							  "missiles_angleRound3": pygame.image.load(IMAGEASSETPATH + 'gui/guibox/loadOut_missles_angleRound3.png'),
							  }

gui.bombIcons               = {"nuke": pygame.image.load(IMAGEASSETPATH + 'gui/guibox/nuke.png')
							  }

# ----- UNITS AND PLAYER 

gui.player            = loadImageFiles('fighter1.png',IMAGEASSETPATH + 'units/fighter/',convert=False)
gui.playerShooting    = loadImageFiles('fighterShooting1.png',IMAGEASSETPATH + 'units/fighter/',convert=False)
gui.playerBoost       = loadImageFiles('fighterBoost1.png',IMAGEASSETPATH + 'units/fighter/',convert=False)
gui.playerShadow      = loadImageFiles('shadow1.png',IMAGEASSETPATH + 'units/fighter/',convert=False)
gui.playerHit         = loadImageFiles('playerHit1.png',IMAGEASSETPATH + 'units/fighter/',convert=False)


gui.player            = loadImageFiles('g12_1.png',IMAGEASSETPATH + 'units/fighter/',convert=False)
gui.playerShooting    = loadImageFiles('g12_Shooting1.png',IMAGEASSETPATH + 'units/fighter/',convert=False)
gui.playerBoost       = loadImageFiles('g12_boost1.png',IMAGEASSETPATH + 'units/fighter/',convert=False)
gui.playerShadow      = loadImageFiles('g12_Shadow1.png',IMAGEASSETPATH + 'units/fighter/',convert=False)
gui.playerHit         = loadImageFiles('g12_Hit1.png',IMAGEASSETPATH + 'units/fighter/',convert=False)





gui.scoutRed          = loadImageFiles('crabRed1.png',IMAGEASSETPATH + 'units/crab/',convert=False)
gui.scoutRedHit       = loadImageFiles('crabRedhit1.png',IMAGEASSETPATH + 'units/crab/',convert=False)
gui.scoutShadow       = [pygame.image.load(IMAGEASSETPATH + 'units/crab/crabShadow.png')]


gui.powerDrone        = {"ready":loadImageFiles('powerDrone1.png',IMAGEASSETPATH + 'powerups/drone/',convert=False),
						 "3":loadImageFiles('powerDroneThree1.png',IMAGEASSETPATH + 'powerups/drone/',convert=False),
						 "2":loadImageFiles('powerDroneTwo1.png',IMAGEASSETPATH + 'powerups/drone/',convert=False),
						 "1":loadImageFiles('powerDroneOne1.png',IMAGEASSETPATH + 'powerups/drone/',convert=False),
						 "0":loadImageFiles('powerDroneZero1.png',IMAGEASSETPATH + 'powerups/drone/',convert=False),
						 "shadow":[pygame.image.load(IMAGEASSETPATH + 'powerups/drone/powerDroneShadow.png')],
						 "static":loadImageFiles('powerDrone1.png',IMAGEASSETPATH + 'powerups/drone/',convert=False)[0],
						 "hit":loadImageFiles('pdHit1.png',IMAGEASSETPATH + 'powerups/drone/',convert=False), 
						 "destroyed":loadImageFiles('pdHitDestroyed1.png',IMAGEASSETPATH + 'powerups/drone/',convert=False), }
gui.pdAmmo            = { "angleRound": pygame.image.load(IMAGEASSETPATH + 'powerups/powerDroneAmmo/angle1.png'),
						 "angleRoundFaster": pygame.image.load(IMAGEASSETPATH + 'powerups/powerDroneAmmo/angle2.png'),
						 "angleRoundFullSpeed": pygame.image.load(IMAGEASSETPATH + 'powerups/powerDroneAmmo/angle3.png'),
						 "angleRound3": pygame.image.load(IMAGEASSETPATH + 'powerups/powerDroneAmmo/angle4.png'),
						 "hotRound": pygame.image.load(IMAGEASSETPATH + 'powerups/powerDroneAmmo/hotRound1.png'),
						 "hotDouble": pygame.image.load(IMAGEASSETPATH + 'powerups/powerDroneAmmo/hotRound2.png'),
						 "hotTripple": pygame.image.load(IMAGEASSETPATH + 'powerups/powerDroneAmmo/hotRound3.png'),}


gui.hind              = loadImageFiles('hind1.png',IMAGEASSETPATH + 'units/hind/',convert=False)
gui.hindHit           = loadImageFiles('hindHit1.png',IMAGEASSETPATH + 'units/hind/',convert=False)
gui.hindShadow        = loadImageFiles('hindShadow1.png',IMAGEASSETPATH + 'units/hind/',convert=False)



gui.tank              = loadImageFiles('sandTank1.png',IMAGEASSETPATH + 'units/tank/sandTank/',convert=False)
gui.tankHit           = loadImageFiles('sandTankHit1.png',IMAGEASSETPATH + 'units/tank/sandTank/',convert=False)
gui.turret            = [pygame.image.load(IMAGEASSETPATH + 'units/tank/sandTank/turret.png')]
gui.turretHit         = loadImageFiles('sandTankTurretHit1.png',IMAGEASSETPATH + 'units/tank/sandTank/',convert=False)
gui.tankStatic        = pygame.image.load(IMAGEASSETPATH + 'units/tank/sandTank/sandTankStatic.png')
gui.tankRemains       = loadImageFiles('tankCarcass1.png',IMAGEASSETPATH + 'units/tank/',convert=False)
gui.tankShadow        = [pygame.image.load(IMAGEASSETPATH + 'units/tank/sandTank/sandTankShadow.png')]

gui.greenTank              = loadImageFiles('greenTank1.png',IMAGEASSETPATH + 'units/tank/greenTank/',convert=False)
gui.greenTankHit           = loadImageFiles('greenTankhit1.png',IMAGEASSETPATH + 'units/tank/greenTank/',convert=False)
gui.greenTurret            = [pygame.image.load(IMAGEASSETPATH + 'units/tank/greenTank/greenTurret.png')]
gui.greenTurretHit         = loadImageFiles('greenTankTurretHit1.png',IMAGEASSETPATH + 'units/tank/greenTank/',convert=False)
gui.greenTankStatic        = pygame.image.load(IMAGEASSETPATH + 'units/tank/greenTank/greenTankStatic.png')
gui.greenTankRemains       = loadImageFiles('greenTankCarcass1.png',IMAGEASSETPATH + 'units/tank/greenTank/',convert=False)
gui.greenTankShadow        = [pygame.image.load(IMAGEASSETPATH + 'units/tank/greenTank/greenTankShadow.png')]



gui.snowTank               = loadImageFiles('snowTank1.png',IMAGEASSETPATH + 'units/tank/snowTank/',convert=False)
gui.snowTankHit            = loadImageFiles('snowTankhit1.png',IMAGEASSETPATH + 'units/tank/snowTank/',convert=False)
gui.snowTurret             = [pygame.image.load(IMAGEASSETPATH + 'units/tank/snowTank/snowTurret.png')]
gui.snowTurretHit          = loadImageFiles('snowTurretHit1.png',IMAGEASSETPATH + 'units/tank/snowTank/',convert=False)
gui.snowTankStatic         = pygame.image.load(IMAGEASSETPATH + 'units/tank/snowTank/snowTankStatic.png')
gui.snowTurretRemains      = loadImageFiles('tankCarcass1.png',IMAGEASSETPATH + 'units/tank/',convert=False)
gui.snowTankShadow         = [pygame.image.load(IMAGEASSETPATH + 'units/tank/snowTank/snowTankShadow.png')]


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
gui.aaShadow          = [pygame.image.load(IMAGEASSETPATH + 'units/AA_burst/aaShadow.png')]

gui.mlrs              = loadImageFiles('mlrs1.png',IMAGEASSETPATH + 'units/MLRS/',convert=False)
gui.mlrsHit           = loadImageFiles('mlrsHit1.png',IMAGEASSETPATH + 'units/MLRS/',convert=False)
gui.mlrsTurret        = [pygame.image.load(IMAGEASSETPATH + 'units/MLRS/mlrsTurret1.png')]
gui.mlrsTurretHit     = loadImageFiles('mlrsTurretHit1.png',IMAGEASSETPATH + 'units/MLRS/',convert=False)
gui.mlrsStatic        = pygame.image.load(IMAGEASSETPATH + 'units/MLRS/mlrsStatic.png')
gui.mlrsRemains       = loadImageFiles('mlrsRemains1.png',IMAGEASSETPATH + 'units/MLRS/',convert=False)
gui.mlrsShadow        = [pygame.image.load(IMAGEASSETPATH + 'units/MLRS/mlrsShadow.png')]


gui.frigate           = [pygame.image.load(IMAGEASSETPATH + 'units/navalFrigate/frigate1.png')]
gui.frigateRemains    = [pygame.image.load(IMAGEASSETPATH + 'units/navalFrigate/frigateRemains.png')]
gui.frigateHit        = loadImageFiles('frigateHit1.png',IMAGEASSETPATH + 'units/navalFrigate/',convert=False)
gui.frigateTurret     = [pygame.image.load(IMAGEASSETPATH + 'units/navalFrigate/turret.png')]
gui.frigateTurretRemains     = [pygame.image.load(IMAGEASSETPATH + 'units/navalFrigate/turretRemains.png')]
gui.frigateTurretHit  = loadImageFiles('turretHit1.png',IMAGEASSETPATH + 'units/navalFrigate/',convert=False)
gui.frigateMulti      = [pygame.image.load(IMAGEASSETPATH + 'units/navalFrigate/multiTurret.png')]
gui.frigatMultiHit    = loadImageFiles('multiTurretHit1.png',IMAGEASSETPATH + 'units/navalFrigate/',convert=False)
gui.frigateMultiRemains = [pygame.image.load(IMAGEASSETPATH + 'units/navalFrigate/multiTurretRemains.png')]



# ---------BUILDINGS INTERACTABLE


gui.bioLab                    = [pygame.image.load(IMAGEASSETPATH + 'tilesets/L2/interactable/biolab/bioLab.png')]
gui.bioLabHit                 = loadImageFiles('bioLabHit1.png',IMAGEASSETPATH + 'tilesets/L2/interactable/biolab/',convert=False)
gui.bioLabRemains             = loadImageFiles('bioLabRemains1.png',IMAGEASSETPATH + 'tilesets/L2/interactable/biolab/',convert=False)


gui.barrelGroupRed            = [pygame.image.load(IMAGEASSETPATH + 'tilesets/L2/interactable/barrel/barrelGroupRed.png')]
gui.barrelGroupRedHit         = loadImageFiles('barrelGroupRedHit1.png',IMAGEASSETPATH + 'tilesets/L2/interactable/barrel/',convert=False)
gui.barrelGroupRedRemains     = loadImageFiles('barellGroupRedRemains1.png',IMAGEASSETPATH + 'tilesets/L2/interactable/barrel/',convert=False)


#----TERRAIN TILELESS

gui.volcano					  = [pygame.image.load(IMAGEASSETPATH + 'tilesets/L2/unfinished/terrain/volcano.png')]
gui.snowTrees  				  = [pygame.image.load(IMAGEASSETPATH + 'tilesets/L2/unfinished/trees/snowTrees.png')]
gui.snowTreesLeft  			  = [pygame.image.load(IMAGEASSETPATH + 'tilesets/L2/unfinished/trees/snowTreesLeft.png')]
gui.snowTreesRight  		  = [pygame.image.load(IMAGEASSETPATH + 'tilesets/L2/unfinished/trees/snowTreesRight.png')]



# ---------BULLETS AND WEAPONS

gui.slitherShot            = loadImageFiles('slither1.png',IMAGEASSETPATH + 'ordinance/slither/',convert=False)
gui.triBlast               = loadImageFiles('triBlast1.png',IMAGEASSETPATH + 'ordinance/',convert=False)
gui.yellowPlasma           = loadImageFiles('yellowPlasmaBall1.png',IMAGEASSETPATH + 'ordinance/plasma/yellowPlasma/',convert=False)
gui.redPlasma              = loadImageFiles('redPlasmaBall1.png',IMAGEASSETPATH + 'ordinance/plasma/redPlasma/',convert=False)
gui.lightRedPlasma         = loadImageFiles('lightRedPlasmaBall1.png',IMAGEASSETPATH + 'ordinance/plasma/lightRedPlasma/',convert=False)
gui.hotRound               = loadImageFiles('hotRound1.png',IMAGEASSETPATH + 'ordinance/hotRound/',convert=False)
gui.angleRound             = loadImageFiles('angleRounds1.png',IMAGEASSETPATH + 'ordinance/angleRounds/',convert=False)
gui.beamPart               = loadImageFiles('beamPart1.png',IMAGEASSETPATH + 'ordinance/beam/',convert=False)
gui.beamHead               = loadImageFiles('beamHead1.png',IMAGEASSETPATH + 'ordinance/beam/',convert=False)




gui.streakerMissile        = loadImageFiles('missile1.png',IMAGEASSETPATH + 'ordinance/missiles/',convert=False)
gui.streakerGray           = loadImageFiles('grayMissile1.png',IMAGEASSETPATH + 'ordinance/missiles/',convert=False)
gui.nukeMissile            = loadImageFiles('nuke1.png',IMAGEASSETPATH + 'ordinance/missiles/',convert=False)
gui.missilePlume           = loadImageFiles('missilePlume1.png',IMAGEASSETPATH + 'ordinance/plumes/',convert=False,alphaConvert=True)


gui.bombShockFrames        = loadImageFiles('bombShock1.png',IMAGEASSETPATH + 'ordinance/bomb/',convert=False,alphaConvert=True)
gui.bombBlastFrames        = loadImageFiles('bomb1.png',IMAGEASSETPATH + 'ordinance/bomb/',convert=False,alphaConvert=True)




# SETTING TRANS
#[x.set_colorkey((0, 0, 0)) for x in gui.missilePlume]
#[x.set_alpha(130) for x in gui.missilePlume]


#gui.missilePlumeLong       = loadImageFiles('missilePlumeLong1.png',IMAGEASSETPATH + 'ordinance/plumes/',convert=False)
gui.missileExplosion       = loadImageFiles('missileExplosion1.png',IMAGEASSETPATH + 'ordinance/explosions/missileExplosion/',convert=False)

gui.chaffHead              = loadImageFiles('chaffHead1.png',IMAGEASSETPATH + 'ordinance/flares/',convert=False)


gui.lockOn                 = loadImageFiles('lockon1.png',IMAGEASSETPATH + 'gui/',convert=False)
gui.lockOnStill            = pygame.image.load(IMAGEASSETPATH + '/gui/stillLockedOn.png')

#-----------BIG 

gui.grassTiles         = loadImageFiles('grass1.png',IMAGEASSETPATH + 'tilesets/100/grass/grassV1/',convert=True)
gui.grassLight         = loadImageFiles('grass1.png',IMAGEASSETPATH + 'tilesets/100/grass/grassLight/',convert=True)
gui.concreteTiles      = loadImageFiles('concrete1.png',IMAGEASSETPATH + 'tilesets/100/concrete/',convert=True)
gui.sandTiles          = loadImageFiles('sand1.png',IMAGEASSETPATH + 'tilesets/100/sand/sandv1/',convert=True)
gui.base100            = loadImageFiles('base100_1.png',IMAGEASSETPATH + 'tilesets/100/template/',convert=True)
gui.water              = loadImageFiles('water1.png',IMAGEASSETPATH + 'tilesets/100/water/',convert=True)
gui.snow               = loadImageFiles('snow1.png',IMAGEASSETPATH + 'tilesets/100/snowlv/snow/',convert=True)
gui.snowLake           = loadImageFiles('snowlake1.png',IMAGEASSETPATH + 'tilesets/100/snowlv/snowLake/',convert=True)

#-----------SMALL 

gui.smallGrassTiles         = loadImageFiles('grass1.png',IMAGEASSETPATH + 'tilesets/50/grass/grassV1/',convert=True)
gui.smallConcreteTiles      = loadImageFiles('concrete1.png',IMAGEASSETPATH + 'tilesets/50/concrete/',convert=True)
gui.smallSandTiles          = loadImageFiles('sand1.png',IMAGEASSETPATH + 'tilesets/50/sand/sandv1/',convert=True)
gui.smallBase100            = loadImageFiles('base100_1.png',IMAGEASSETPATH + 'tilesets/50/template/',convert=True)
gui.smallWater              = loadImageFiles('water1.png',IMAGEASSETPATH + 'tilesets/50/water/',convert=True)
gui.smallSnow               = loadImageFiles('snow1.png',IMAGEASSETPATH + 'tilesets/50/snow/',convert=True)
gui.smallSnowLake           = loadImageFiles('snowlake1.png',IMAGEASSETPATH + 'tilesets/50/snowLake/',convert=True)
gui.pier 					= loadImageFiles('pier1.png',IMAGEASSETPATH + 'tilesets/50/port/',convert=True)

# TILELESS
gui.pilonDR            = loadImageFiles('pilon1.png',IMAGEASSETPATH + 'tilesets/L2/objects/pilonDiagonalRight/',convert=False)
gui.pilonDL            = loadImageFiles('pilon1.png',IMAGEASSETPATH + 'tilesets/L2/objects/pilonDiagonalLeft/',convert=False)
gui.backObjects        = loadImageFiles('obj1.png',IMAGEASSETPATH + 'tilesets/L2/objects/',convert=False)
gui.barracks           = loadImageFiles('barracks1.png',IMAGEASSETPATH + 'tilesets/L2/buildings/barracks/',convert=False)
gui.conveyorV          = loadImageFiles('vBelt1.png',IMAGEASSETPATH + 'tilesets/L2/buildings/conveyor/',convert=False)
gui.conveyorH          = loadImageFiles('hBelt1.png',IMAGEASSETPATH + 'tilesets/L2/buildings/conveyor/',convert=False)
gui.space              = [pygame.image.load(IMAGEASSETPATH + 'tilesets/50/space/spaceBack.png').convert()]



# TILELESS LAYER 
gui.missileBase        =loadImageFiles('missileBase1.png',IMAGEASSETPATH + 'tilesets/ISOMETRIC/missileBase/',convert=False,alphaConvert=True)
gui.missileBaseBldings =loadImageFiles('buildings1.png',IMAGEASSETPATH + 'tilesets/ISOMETRIC/missileBase/',convert=False,alphaConvert=True)
#gui.snowBase           =loadImageFiles('snowbase1.png',IMAGEASSETPATH + 'tilesets/snowlv/snowBase/',convert=False,alphaConvert=True)

gui.isoMetric           =loadImageFiles('iso1.png',IMAGEASSETPATH + 'tilesets/ISOMETRIC/',convert=True,alphaConvert=False)
[x.set_colorkey((0, 0, 0)) for x in gui.isoMetric]
[x.set_alpha(130) for x in gui.isoMetric]


gui.tileDict           = {'Grass': gui.grassTiles,
						  'grassLight': gui.grassLight,
						  'Concrete': gui.concreteTiles,
						  'sand': gui.sandTiles,
						  'base': gui.base100,
						  'water': gui.water,
						  'snow': gui.snow,
						  'snowLake':gui.snowLake,
						  
						  'smallGrass': gui.smallGrassTiles,
						  'smallConcrete': gui.smallConcreteTiles,
						  'smallsand': gui.smallSandTiles,
						  'smallbase': gui.smallBase100,
						  'smallwater': gui.smallWater,
						  'smallsnow': gui.smallSnow,
						  'smallsnowLake':gui.smallSnowLake,
						  'snowPier': gui.pier


						  }

gui.smallTileDict        = {
						  'smallGrass': gui.smallGrassTiles,
						  'smallConcrete': gui.smallConcreteTiles,
						  'smallsand': gui.smallSandTiles,
						  'base': gui.smallBase100,
						  'smallwater': gui.smallWater,
						  'smallsnow': gui.smallSnow,
						  'smallsnowLake':gui.smallSnowLake,
						  'snowPier': gui.pier
						  }

gui.layer2Dict           = {
						  'base': gui.base100,
						  'pilonDR': gui.pilonDR,
						  'pilonDL:': gui.pilonDL,
						  'objects': gui.backObjects,
						  'smallbase': gui.smallBase100
						  }


# IF THE WORD HAS ANIMATED
# IT WILL BE ADDED TO TERRAIN LIST AND RENDERED AS AN OBJECT
gui.tilelessL1Dict      = {
						  'pilonDR': gui.pilonDR,
						  'pilonDL': gui.pilonDL,
						  'objects': gui.backObjects,
						  'barracks': gui.barracks,
						  'conveyor_animated_v': gui.conveyorV,
						  'conveyor_animated_h': gui.conveyorH,
						  'volcano': gui.volcano,
						  'snowTrees': gui.snowTrees,
						  'snowTreesLeft':gui.snowTreesLeft,
						  'snowTreesRight':gui.snowTreesRight,
						  'space':gui.space

						  }

"""
						  'missileBase': gui.missileBase,
						  'buildings': gui.missileBaseBldings,
						  'snowBase': gui.snowBase
"""

gui.enemyDict          = {'scout':{'image': gui.scoutRed[0]}, 
						  'tank':{'image': gui.tankStatic},
						  'greenTank':{'image': gui.greenTankStatic},
						  'snowTank':{'image': gui.snowTankStatic},
						  'attackBoat':{'image': gui.attackBoatStatic},
						  'mlrs':{'image': gui.mlrsStatic},
						  'aaSmall':{'image': gui.aaSmallStatic}, 
						  'bioLab':{'image': gui.bioLab[0]},
						  'barrelRed':{'image': gui.barrelGroupRed[0]}, 
						  'hind':{'image': gui.hind[0]}, 
						  'frigate':{'image': gui.frigate[0]}

							}



gui.smallRedExplosion      = loadImageFiles('explosion1.png',IMAGEASSETPATH + 'ordinance/explosions/smallExplosion/')
gui.redExplosion           = loadImageFiles('explosion1.png',IMAGEASSETPATH + 'ordinance/explosions/explosion/')
gui.barrelExplosion        = loadImageFiles('barrelExplosion1.png',IMAGEASSETPATH + 'ordinance/explosions/barrellExplosion/')
gui.bigCloudyExplosion     = loadImageFiles('explosion1.png',IMAGEASSETPATH + 'ordinance/explosions/bigCloud/')
gui.smallCloudyExplosion   = loadImageFiles('explosion1.png',IMAGEASSETPATH + 'ordinance/explosions/cloudExplosion/')
gui.smallYellowExplosion   = loadImageFiles('explosion1.png',IMAGEASSETPATH + 'ordinance/explosions/explosionParticle/')

gui.smallSmoke             = loadImageFiles('smallTrail1.png',IMAGEASSETPATH + 'SFX/smoke/')
gui.medSmoke               = loadImageFiles('belching1.png',IMAGEASSETPATH + 'SFX/smoke/')

gui.shrapnellA             =  loadImageFiles('shrapnell1.png',IMAGEASSETPATH + 'SFX/shrapnell/')      
gui.shrapnellPlume         =  loadImageFiles('plume1.png',IMAGEASSETPATH + 'SFX/shrapnellPlume/')      



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
gui.claireSmileFrames = loadImageFiles('claireSmiling1.png',IMAGEASSETPATH + 'characters/claire/')
gui.claireTalking     = imageAnimateAdvanced(talkFrames,0.2)
gui.clareSmiling      = imageAnimateAdvanced(gui.claireSmileFrames,0.2)
gui.talkScreenW       = gui.claireTalk[0].get_width()
gui.talkScreenH       = gui.claireTalk[0].get_height()




# ------ CLASS ATTRS
game          = gameObject(ASSETSPATH,gui)
game.mapPaths = 'state/txtMaps/'
user_input    = userInputObject("","", gui)
game.input    = user_input

#gui.statusButton  = button(0.15*width,0.05*height,width/17,height/13,'ST',(0,128,0),gui.bigNokiaFont,textColour=(97,165,93))
