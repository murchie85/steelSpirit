import pygame
import os



def loadUnconverted(mapPath):

    map_data       = []
    map_l2_data    = []
    map_enemy_data = []
    spawn_zones    = []

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
            elif line == "*ENEMY":
                section = "ENEMY"
                continue
            elif line == "*SPAWN":
                section = "SPAWN"
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
            elif section == "ENEMY":
                map_enemy_data += data
            elif section == "SPAWN":
                spawn_zones += data




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

    return(map_data,map_l2_data,map_enemy_data,spawn_zones)


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

    
    for k in objectTiles:
        objectTiles[k] = pygame.Surface.convert_alpha(objectTiles[k])
    for k in pilonLeft:
        pilonLeft[k] = pygame.Surface.convert_alpha(pilonLeft[k])
    for k in pilonRight:
        pilonRight[k] = pygame.Surface.convert_alpha(pilonRight[k])
    for k in barracks:
        barracks[k] = pygame.Surface.convert_alpha(barracks[k])



    l2Dict = {}
    l2Dict['objectTiles']  = objectTiles
    l2Dict['pilonLeft']    = pilonLeft
    l2Dict['pilonRight']   = pilonRight
    l2Dict['barracks']     = barracks


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


def loadEnemyRefData(gui,game):
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
                          'hind':{'image': gui.hind[0]}
                          }
    enemyDict['buildings'] = {
                          'bioLab':{'image': gui.bioLab[0]}
                          }
    enemyDict['sea'] = {
                          'attackBoat':{'image': gui.attackBoatStatic},
                          }

  


    game.activeEnemyData = []
    for item in game.rawEnemyData:
        # objectTiles/obj1/200/420
        if(item.count('/')==6):
            xpos            = item.split('/')[0].strip()
            ypos            = item.split('/')[1].strip()
            enemyKeyName    = item.split('/')[2].strip()
            enemySubKeyName = item.split('/')[3].strip()
            rotation        = item.split('/')[4].strip()
            patrol          = item.split('/')[5].strip()
            patrolU         = patrol.split(':')
            patrolRoute     = []
            print(patrol)
            print(patrolU)
            for r in patrolU:
                patrolRoute.append([r.split('-')[0],r.split('-')[1]])
            lv           = item.split('/')[6].strip()

            # x,y, image, rotation, patrol,powerlevel
            # 200/300/ground/tank/30/200-300:400-320:200-250:500-220/3,400/700/air/scout/30/400-700:400-320/3
            #{'x':200,'y':300,'enemyKeyName':'ground','enemySubKeyName':'tank','patrolRoute':[(200,300),(400-320),(200-250),(500-220)],'lv':3}
            rotatedImage = pygame.transform.rotate(enemyDict[enemyKeyName][enemySubKeyName]['image'],int(rotation))
            game.activeEnemyData.append({'x':int(xpos) ,'y':int(ypos) ,'image':rotatedImage ,'enemyKeyName':enemyKeyName ,'enemySubKeyName':enemySubKeyName ,'rotation':int(rotation) ,'patrolRoute':patrolRoute ,'lv':lv})

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






def get_png_files(gui,subdir):
    path = gui.tilePath +  subdir
    pngFiles = []
    with os.scandir(path) as entries:
        pngFiles = [entry.name for entry in entries if entry.is_file() and entry.name.endswith('.png')]

    tilesDict = {}

    for pngFile in pngFiles:
        tilesDict[pngFile.replace('.png','')] = pygame.image.load(path + pngFile)

    print(tilesDict)
    return(tilesDict)


