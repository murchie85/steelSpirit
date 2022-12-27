# STEEL SPIRIT

![steel spirit cover](scenes/cover.png)  

# A TwinStick,Shmup RPG hybrid    

In progress, lots yet to be done. 



# FEATURES

## PRIMARY 

- MOVEMENT EXPERIMENT
 	- LOCKON SHOULDN'T FACE TARGET, cus you plough into it, should put you into jink mode, which you can swivel holding jink button
	- Maybe just slow down when enemies are in range (unless you boost)
	- Consider shooting puts you in Jink mode to strafe like under defeat
	- Consider holding down lockon, when you let go, you are just in jink mode
	- Make dodging a big element too zipping past until you get to a good part
	- Jinkshoot spray and pray by slowing forward motion is a must.. to make chaff dodge work it should be in non shooting mode..you can lob missiles maybe

- GROUND AA with bullets
- GROUND AA With missiles
- GROUND damagable structures

- ANIMATED TILES
- MISSILE
- CHAFF
- Enemy placer
- Next objective arrow to speed to objective
- Canvas second layer
- canvas transparent
- ++ CANVAS SPEED
- Camera shake
- ADD ALLY
- ADD ALLY LOGIC
- ALLY COMMAND
- INCINERY FLARE EXPLOSIONS https://youtu.be/zXjBS382P2k?t=224
- Want to be able to dodge enemy in shmup style, lockon camera centering clamp may be needed
	- this makes jink manual
	- more thinking required, because to get that flow, its hard if there are enemies in front and beside
- dont allow multiple selects of enemy on one tile

ENEMIES: 

GIGA TANK - COME FROM UNDER GROUND
GIGA TURRET / CANNON 
SHIPS IN PORTS


## SECONDARY 

- Fine control, so rotation is inversed if facing down, (but only if r,l isn't already pressed)
- Check Godzilla for human type ideas
- Shmup into open world
- Redo omega storm including canvas
- Redo title text explaination with ai art gen - move to after game
- UPGRADE TREE
	- MAINMENU UNLOCK
	- LONGER BOOST TIME - Dual fire
- Boss target-points flash/Highlight
- Shmup maybe not needed not for a long time anyway
- GUI LAYOUT: HEALTH, INFO PANEL like DC
- GUI LAYOUT: RIGHT VIDEO SCREEN FOR FAST, INGAME POPUP SCREEN FOR BLUR
- release with twitter acc, automate reshares..adds, get list of shmups
- load assets by lv
- clean map editor, so it always checks number of rows, cols match actual in metaTiles 


## UNDER CONSIDERATOIN

[`JOINT SPECIAL ATTACK`, `Shmup intro`, `slow Underdefeat shmup levels`,   ]


## DONE 

DONE: make and render player DONE: Do a simple map DONE: Navigate with aswd DONE: Camera Nav
DONE - Map maker, Midjourney images, Fix camera, HIT DAMAGE, player explosion animation, allow player to die, Thinner fire, Double fire, radar cone, LOCK ON
DONE: Finish isonscreen function - test using a viewport, TRISHOT - Like in Underdefeat, Multi-tile edit
DONE: - JINK IF NOT IN PIVOT, LOCKON TOGGLE (left/right to scroll), LOCKON LIMIT 3, FACE ENEMY DURING LOCKON, PIVOT CLOCKWISE DURING LOCKON GROUND UNIT

# ACCEPTANCE CRITERIA GLOBAL

- Lots of variety on screen, AA, planes, ATB, etc
- Good Map Detail 




 

# REFS 


https://www.reddit.com/user/KrahsteertS/

https://twitter.com/dantemendes/status/1605888637534707717

shmup maker https://twitter.com/bulostudio/status/1606030117133815808

Gyro Blade
https://twitter.com/HTProject073/status/1600464060428222464

https://twitter.com/HTProject073/status/1601422278054449153





================================
| 							   |
| 							   |
|       CHECKPOINT 			   |
| 							   |
| 		**DO NOT PASS**		   |
| 							   |
| 							   |
| 							   |
================================


**ACCEPTANCE** don't start until DOGFIGHT, CHAFF, 5 ENEMIES, 5 GROUND AA COMPLETE



# SCENE MECHANISMS 

- Scene accepance criteria.. slow blur then pop up or in game side bar scene
- Both.. side/bott/top for fast alert slow blur for story scene

## BIG SCENES


## 0 - INTRO

BUNNIES, FOX, CATS on Mars, Venus and outposts
Parallel world where we gen altered ourselves. Solar system has 40 billion peeps


## 1 - TRAINING VR / THE BIG FURBALL

---CHATER 0 THE BIG FURBALL---

'Takes the keys', your GROUNDED, BACK TO VR
- Team break! (Ling ling, Raj, Simon...) 
- Race them to clearing objective points
- Roxy goes - 'YESSSSS!' in quick pop up once she takes out sth
- Chase each other with Lockon fights




## 2 - DREADNOUGHT

## MECHANISM: 

battlship preview before coming to you
Dreadaught restrict sections and slow scroll speed
Dreadnaught regens...hence timed to take out at mars
Boss target points flash


# STORY 

Timer in big, 'x until end of Earth...or the sun, **shrinks to top right**'
MASSIVE EXPLOSIONS, AIM BIGGER THAN THE REST
Beat the ship, then give a triumphant intro..Adam proudly presents etc
Use UDM names, Turov etc, make a big tutorial
go here shoot this use chaff repeat



## OTHER 

- mild plot about slipgates
- BREAK RIGHT
- Pop up view box (Consider spinning out of power x302s)
- Meeting an alien skrill for the first time 'your ship is junk'...fight me
- VR intro scene, 4 different sides... go go go, split up



# Music Notes

Snippets: https://youtu.be/H6kvP0h0g9M?t=5







# Notes  





# GAME FLOW 


## SIMPLIFIED  Game Logic: 

- [MAIN] - [GAME] - [LEVEL] - [PLAYER OBJ, ENEMY OBJ, BULLET OBJ, TILEMAPS]


## FULL FLOW 


- main 
	
	- setup ---- (importing images and setting up the main gui, game and other classes)
	
	- Coordinator [GAME CLASS] (managing the main scenes/phease of the game)

		- Intro 

		- Title screen

		- Start Menu

		-  Game Logic [LEVEL CLASS]

			- Two main states: 

				- Init
					- Setup background, add enemies to the field
				- Run
					- Runs the bullets, map, enemies, players functions

		- Map editor ***(Complete)***

			- Create new map

			- Load Map

				- Edit map

		- (settings, profile...)



## STORY BOARDING


- EARTH HAS COME A LONG WAY SINCE THE FORMATION OF A WEIGHED FEDERATED ALLIANCE
  (SPACE SHIPS, MANS SHAKING HANDS)

- EARTH EXPANDED OUT FURTHER INTO THE HEAVENS 
	 - PICTURES OF SHIPS BUILDING HABBITATES

- FINALLY THE GREATEST BREAKTHROUGH CAME AT OUR FEET AND NOT IN THE STARS
	- GENETIC ENGINEEERING , BABY HYBRIDS

- NEW VARIATIONS TOOK OFF IN THE NEW PLANETS, 
	- MARTIAN FOX LIKE CREATIONS
	- VENUSIAN RABBIT GIRLS
	- TITAN CAT GIRLS etc

- The population of the solar system grew to 50 billion 

- New racial tensions soon fueled civil wars

- Nation leaders nearly brought us to the brink until the 'veterans' stood in and brought about the peace

- Now we stand at a new dawn, the veterans have retired, with a gap for the new breed



