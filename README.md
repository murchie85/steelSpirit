# STEEL SPIRIT

![steel spirit cover](scenes/cover.png)
## A TwinStick,Shmup RPG hybrid    

In progress, lots yet to be done. 



## TODO   



- Finish isonscreen function - test using a viewport
- JINK
- MISSILE
- LOCK ON
- CHAFF
- UDLR + ROTATE 
- ++ HOR SPEED
- ++ VER SPEED
- ++ CANVAS SPEED

DONE: make and render player DONE: Do a simple map DONE: Navigate with aswd DONE: Camera Nav
DONE - Map maker, Midjourney images, Fix camera, HIT DAMAGE, player explosion animation, allow player to die, 
DONE Thinner fire
DONE Double fire


- UPGRADE TREE
- MAINMENU UNLOCK
	- LONGER BOOST TIME - Dual fire

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

# SCENES 

**ACCEPTANCE** don't start until DOGFIGHT, CHAFF, 5 ENEMIES, 5 GROUND AA COMPLETE

- Pop up view box (Consider spinning out of power x302s)
- Meeting an alien skrill for the first time 'your ship is junk'...fight me
- VR intro scene, 4 different sides... go go go, split up


 

# REFS 


https://www.reddit.com/user/KrahsteertS/

https://twitter.com/dantemendes/status/1605888637534707717

shmup maker https://twitter.com/bulostudio/status/1606030117133815808

Gyro Blade
https://twitter.com/HTProject073/status/1600464060428222464

https://twitter.com/HTProject073/status/1601422278054449153


# Notes  


DRAW MORE UNITS

GOAL: NO STORY until game is playable and fun GOAL: Do 2 way pivot, shmup to open

SCENE

FEATURES:



fire weapon

make enemy

make enemy simple logic

make enemy fire

destroy enemy scene

Deduct Health

Helicopter mode in atmo

MUST HAVE: After burners

MUST HAVE: Jink DODGE

Shmup into open world

Redo omega storm including canvas

Camera shake

later
Team ally players
BIG SCENE 0 - FURBALL

Training/competition scene

cats, dogs, apes
They have sleek fast ships, chase em to locations and clean up before them

mild plot about slipgates

Lock on fights

## BIG SCENE 1 - DREADNAUGHT

Timer in big, 'x until end of earht, shrinks to top right'
battlship preview before coming to you
MASSIVE EXPLOSIONS, AIM BIGGER THAN THE REST
Beat the ship, then give a triumphant intro..Adam proudly presents etc
Use UDM names, Turov etc
make a big tutorial
go here
shoot this
use chaff
repeat