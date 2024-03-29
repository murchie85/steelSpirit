import pygame
import os
from buildings.nonInteractable import *
from levels.level_ruralAssault import *
from levels.sandbox import *




def loadUnconverted(mapPath):

    map_data       = []
    map_l2_data    = []
    animated_data  = []
    map_enemy_data = []
    spawn_zones    = []
    quadrants      = []

    with open(mapPath, 'r') as file:
        section = None  # This will keep track of which section we're in
        for line in file:
            line = line.strip()  # Remove any leading/trailing whitespace
            if line == "*L1":
                section = "L1"
                continue  # Skip to the next line
            elif line == "*L2":
                section = "L2"
                continue
            elif line == "*ANIMATED":
                section = "ANIMATED"
                continue
            elif line == "*ENEMY":
                section = "ENEMY"
                continue
            elif line == "*SPAWN":
                section = "SPAWN"
                continue
            elif line == "*QUADRANT":
                section = "QUADRANT"
                continue
            elif not line:  # If the line is empty, skip it
                continue

            # Split the line on commas and remove empty strings
            data = list(filter(None, line.split(',')))

            # Append the data to the appropriate list based on the section
            if section == "L1":
                map_data.append(data)
            elif section == "L2":
                map_l2_data += data
            elif section == "ANIMATED":
                animated_data += data
            elif section == "ENEMY":
                map_enemy_data += data
            elif section == "SPAWN":
                spawn_zones += data
            elif section == "QUADRANT":
                quadrants += data




    print('----------------------------------------------------------------')
    print('                        MAP DATA LOADED ')
    print(map_data)
    print(len(map_data))
    print(len(map_data[0]))
    print("L2 MAP DATA LOADED")
    print(map_l2_data)
    print("ENEMY MAP DATA LOADED")
    print(map_enemy_data)
    print('----------------------------------------------------------------')
    print('\n\n\n\n\n\n\n\n\n')

    return(map_data,map_l2_data,animated_data,map_enemy_data,spawn_zones,quadrants)


def loadMapRefData(gui,game):
    """
    populates activeL1Data and returns ref dict
    """
    templateTiles = get_png_files(gui,'/50/template/') 
    grassTiles    = get_png_files(gui,'/50/grass/grassV1/')
    concrete      = get_png_files(gui,'/50/concrete/') 
    sand          = get_png_files(gui,'/50/sand/sandv1/')
    snow          = get_png_files(gui,'/50/snow/') 
    snowLake      = get_png_files(gui,'/50/snowLake/') 
    water         = get_png_files(gui,'/50/water/') 
    port          = get_png_files(gui,'/50/port/') 
    
    for k in templateTiles:
        templateTiles[k] = pygame.Surface.convert_alpha(templateTiles[k])
    for k in grassTiles:
        grassTiles[k] = pygame.Surface.convert_alpha(grassTiles[k])
    for k in concrete:
        concrete[k] = pygame.Surface.convert_alpha(concrete[k])
    for k in sand:
        sand[k] = pygame.Surface.convert_alpha(sand[k])
    for k in snow:
        snow[k] = pygame.Surface.convert_alpha(snow[k])
    for k in snowLake:
        snowLake[k] = pygame.Surface.convert_alpha(snowLake[k])
    for k in water:
        water[k] = pygame.Surface.convert_alpha(water[k])
    for k in port:
        port[k] = pygame.Surface.convert_alpha(port[k])


    tileDict = {}
    tileDict['template']    = templateTiles
    tileDict['grassV1']     = grassTiles
    tileDict['concrete']    = concrete
    tileDict['sand']        = sand
    tileDict['snow']        = snow
    tileDict['snowlake']    = snowLake
    tileDict['water']       = water
    tileDict['pier']        = port


    # CONVERTING MAP DATA TO GAME OBJECT DATA
    print('----------------------------------------------------------------')
    print('                        LOADING MAP DATA INTO OBJECTS ')

    # ----create empty list of right size to populate objects 
    
    game.activeL1Data = [[None for _ in row] for row in game.rawL1Data]

    rows = len(game.rawL1Data)
    cols = len(game.rawL1Data[0])
    print("Rows: " + str(rows))
    print("Cols: " + str(cols))

    for r in range(rows):
        for c in range(cols):
            keys = game.rawL1Data[r][c]
            libraryKey = keys.split('/')[0].strip()
            mapKey     = keys.split('/')[1].strip()

            game.activeL1Data[r][c] = tileDict[libraryKey][mapKey]




    return(tileDict,game.activeL1Data)




def loadLayer2RefData(gui,game):
    """
    populates activeL2Data and returns ref dict
    """
    objectTiles = get_png_files(gui,'/L2/objects/') 
    pilonLeft   = get_png_files(gui,'/L2/objects/pilonDiagonalLeft/') 
    pilonRight  = get_png_files(gui,'/L2/objects/pilonDiagonalRight/')
    barracks    = get_png_files(gui,'/L2/buildings/barracks/')
    lv1         = get_png_files(gui,'/L2/lv1/')

    
    for k in objectTiles:
        objectTiles[k] = pygame.Surface.convert_alpha(objectTiles[k])
    for k in pilonLeft:
        pilonLeft[k] = pygame.Surface.convert_alpha(pilonLeft[k])
    for k in pilonRight:
        pilonRight[k] = pygame.Surface.convert_alpha(pilonRight[k])
    for k in barracks:
        barracks[k] = pygame.Surface.convert_alpha(barracks[k])
    for k in lv1:
        lv1[k] = pygame.Surface.convert_alpha(lv1[k])



    l2Dict = {}
    l2Dict['lv1']          = lv1
    l2Dict['pilonLeft']    = pilonLeft
    l2Dict['pilonRight']   = pilonRight
    l2Dict['barracks']     = barracks
    l2Dict['objectTiles']  = objectTiles


    game.activeL2Data = []
    for item in game.rawL2Data:
        # objectTiles/obj1/200/420
        if(item.count('/')==3):
            xpos       = item.split('/')[0].strip()
            ypos       = item.split('/')[1].strip()
            libraryKey = item.split('/')[2].strip()
            mapKey     = item.split('/')[3].strip()

            # x,y, image, key,subkey
            game.activeL2Data.append([int(xpos),int(ypos),l2Dict[libraryKey][mapKey],libraryKey,mapKey])

    l2DictScaled = {key: {sub_key: pygame.transform.scale(image, (70, 70)) 
                          for sub_key, image in value.items()} 
                    for key, value in l2Dict.items()}
    return(l2Dict,game.activeL2Data,l2DictScaled)


def loadAnimatedData(gui,game):
    """
    populates activeL2Data and returns ref dict
    """
    animatedDict = {}
    changeDurationDict   = {"fast": 0.2,"medium": 0.4,"slow":0.6}


    conveyor = get_png_files_list(gui,'/L3_Animated/conveyor/') 
    for k in range(len(conveyor)):
        conveyor[k] = pygame.Surface.convert_alpha(conveyor[k])


    animatedDict['conveyor']     = {"images": conveyor, "thumbnail":  pygame.transform.scale(conveyor[0], (70, 70)), 'cursorImage':conveyor[0]}
    


    game.activeAnimatedData = []
    for item in game.rawAnimData:
        # conveyor/90/200/420/fast
        if(item.count('/')==4):
            libraryKey          = item.split('/')[0].strip()
            rotation            = item.split('/')[1].strip()
            xpos                = item.split('/')[2].strip()
            ypos                = item.split('/')[3].strip()
            changeDuration      = item.split('/')[4].strip()


            images      = animatedDict[libraryKey]['images']
            terrainObj  = nonInteractable(int(xpos),int(ypos),images,imageAnimateAdvanced(images,changeDurationDict[changeDuration]),gui)
            terrainObj.facing = int(rotation)


            # ACTIVEANIMATEDDATA MUST HAVE Lib key, rotation, x,y, animationClass
            # x,y, image, key,subkey
            game.activeAnimatedData.append({"x":int(xpos) ,"y": int(ypos),"libraryKey": libraryKey,"speed":changeDuration, "classObject": terrainObj})

    return(animatedDict,game.activeAnimatedData)



def loadEnemyRefData(gui,game,debug=True):
    """

    X,Y, enemyKeyName,enemySubKeyName, ROTATION, PATROL_ROUTE, POWERLEVEL
    200/300/ground/tank/30/200-300:400-320:200-250:500-220/3,400/700/air/scout/30/400-700:400-320/3

    """


    enemyDict = {}
    enemyDict['ground'] = {
                          'tank':{'image': gui.tankStatic},
                          'greenTank':{'image': gui.greenTankStatic},
                          'snowTank':{'image': gui.snowTankStatic},
                          'mlrs':{'image': gui.mlrsStatic},
                          'aaSmall':{'image': gui.aaSmallStatic}, 
                          'barrelRed':{'image': gui.barrelGroupRed[0]}
                          }
    enemyDict['air']   = {'scout':{'image': gui.scoutRed[0]}, 
                          'hind':{'image': gui.hind[0]},
                          'comanche':{'image': gui.comanche[0]}
                          }
    enemyDict['buildings'] = {
                          'bioLab':{'image': gui.bioLab[0]},
                          'samSite':{'image': gui.samSite[0]},
                          'tankBarracks':{'image':gui.tankBarracks[0]},
                          'greenBarracks':{'image':gui.greenBarracks[0]},
                          }
    enemyDict['sea'] = {
                          'attackBoat':{'image': gui.attackBoatStatic},
                          }

    enemyDict['passive'] = {
                          'powerDrone':{'image': gui.powerDrone['static']},
                          }




    game.activeEnemyData = []
    for item in game.rawEnemyData:
        # objectTiles/obj1/200/420

        xpos            = item.split('/')[0].strip()
        ypos            = item.split('/')[1].strip()
        enemyKeyName    = item.split('/')[2].strip()
        enemySubKeyName = item.split('/')[3].strip()
        rotation        = item.split('/')[4].strip()
        patrol          = item.split('/')[5].strip()
        patrolU         = patrol.split(':')
        patrolRoute     = []
        if(debug):
            print('Patrol route is : ' + str(patrolU))
        for r in patrolU:
            patrolRoute.append((int(r.split('-')[0]),int(r.split('-')[1])))
        lv              = item.split('/')[6].strip()
        
        try:
            objectiveKey    = item.split('/')[7].strip()
        except:
            print("Enemy does not have objective key, adding default value")
            objectiveKey = 'no objective'
        
        try:
            itemDrop    = item.split('/')[8].strip()
        except:
            print("Enemy does not have itemDrop key, adding default value")
            itemDrop = 'None'

        try:
            spawnMe             = item.split('/')[9].strip()
            spawn_wave_num      = item.split('/')[10].strip()
            spawn_wave_Interval = item.split('/')[11].strip()
            spawn_area          = item.split('/')[12].strip()
            spawn_range         = item.split('/')[13].strip()
            spawn_periphery     = item.split('/')[14].strip()
            spawn_objective     = item.split('/')[15].strip()


        except:
            print("Enemy does not have itemDrop key, adding default value")
            spawnMe             = 'False'
            spawn_wave_num      = '0'
            spawn_wave_Interval = '0.2'
            spawn_area          = 'small'
            spawn_range         = 'small'
            spawn_periphery     = 'False'
            spawn_objective     = 'No Objective'

        rotatedImage = pygame.transform.rotate(enemyDict[enemyKeyName][enemySubKeyName]['image'],int(rotation))
        if(spawnMe=='True'):
            rotatedImage.set_alpha(100)
        game.activeEnemyData.append({'x':int(xpos) ,
                                     'y':int(ypos) ,
                                    'image':rotatedImage ,
                                    'enemyKeyName':enemyKeyName ,
                                    'enemySubKeyName':enemySubKeyName ,
                                    'rotation':int(rotation) ,
                                    'patrolRoute':patrolRoute ,
                                    'lv':lv,
                                    'assignedObjective':objectiveKey,
                                    'itemDrop': itemDrop, 
                                    'spawnMe': spawnMe,
                                    'numberOfWaves': int(spawn_wave_num), 
                                    'waveInterval': float(spawn_wave_Interval), 
                                    'spawnArea': spawn_area, 
                                    'enemyRange': spawn_range, 
                                    'spawnAtPeriphery': spawn_periphery=='True', 
                                    'spawnObjective': spawn_objective

                                    })


    # Create a new dict with the images scaled
    for category, items in enemyDict.items():
        for key, value in items.items():
            original_image = value['image']
            scaled_image = pygame.transform.scale(original_image, (70, 70))
            enemyDict[category][key]['scaled_image'] = scaled_image


    return(enemyDict,game.activeEnemyData)



def loadSpawnZones(gui,game):
    game.activeSpawnZones = []
    """
    [[588, 157, 353, 213], [336, 514, 710, 246]]
    588/157/353/213,
    """
    for item in game.rawSpawnData:
        # []
        if(item.count('/')==3):
            x            = item.split('/')[0].strip()
            y            = item.split('/')[1].strip()
            w            = item.split('/')[2].strip()
            h            = item.split('/')[3].strip()
            quad         = [int(x),int(y),int(w),int(h)]
            game.activeSpawnZones.append(quad)
    return(game.activeSpawnZones)

def loadQuadrants(gui,game):
    game.activeQuadrants= []
    """
    [[588, 157, 353, 213], [336, 514, 710, 246]]
    588/157/353/213,
    """
    for item in game.rawQuadrantData:
        # []
        if(item.count('/')==3):
            x            = item.split('/')[0].strip()
            y            = item.split('/')[1].strip()
            w            = item.split('/')[2].strip()
            h            = item.split('/')[3].strip()
            quad         = [int(x),int(y),int(w),int(h)]
            game.activeQuadrants.append(quad)
    return(game.activeQuadrants)







def get_png_files(gui,subdir):
    path = gui.tilePath +  subdir
    pngFiles = []
    with os.scandir(path) as entries:
        pngFiles = [entry.name for entry in entries if entry.is_file() and entry.name.endswith('.png')]

    tilesDict = {}

    for pngFile in pngFiles:
        tilesDict[pngFile.replace('.png','')] = pygame.image.load(path + pngFile)

    print("Getting images for " + str(path))
    print(tilesDict)
    return(tilesDict)

def get_png_files_list(gui, subdir):
    path = gui.tilePath + subdir
    pngFiles = []
    with os.scandir(path) as entries:
        pngFiles = [entry.name for entry in entries if entry.is_file() and entry.name.endswith('.png')]

    tilesList = []

    for pngFile in pngFiles:
        tilesList.append(pygame.image.load(path + pngFile))

    print("Getting images for " + str(path))
    print(tilesList)
    return tilesList


