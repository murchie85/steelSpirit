# STEEL SPIRIT

![steel spirit cover](scenes/cover.png)  



# JUMP_CONTENTS 


- SCENE_MECHANICS


- MEDIA_TRACTION


- FEATURES_BACKLOG



- INSPIRATION



- FEEDBACK_FROM_PEOPLE



- ACCEPTANCE_CRITERIA



# SCENE_MECHANICS 

JUMP_CONTENTS


It's a FAST DESERT STRIKE like shooter.

With SHMUP TRANSITION scenes

Heavily PLOT DRIVEN with ingame VIDEO GUI (and talk audio)


STRETCH: Possible chronotrigger like Magic abilities
STRETCH: Possible merged turnbase background objectives whilst you fight


QUALITY CONTROL - Does it still have slug throwing SHmup feel?



# MEDIA_TRACTION: 

JUMP_CONTENTS

gamedev.net, 

linkedin, 

reddit pygame, 

indiedev, 

fungames, 

twitter, 

tiktok




## FEATURES_BACKLOG 
JUMP_CONTENTS



JINK-DASH IN NEW LOCKON MODE


SHOW LOCKON MODE

SHOW SEARCH BEAM

NGUNI ENEMY 

GRASS L2 DARKENED OVERLAY

BONUS MULTIPLIER 
			to prevent me snipping from a distance.  Use a timer 
			- kill enemy, timer starts
			- 1.2 * points for each kill
			- BONUS COLOUR FLOAT says BONUS 200 PTS
			- 1.4 at 6 enemies
			- SCORE TOP LEFT FLASHES
			- SPAWN POWER UP IF YOU KILL 10

			GOLDEN X2 , X3 and score flashes that colour


MISSILE POWERUPS

BURNING ANIMATION

RUNWAY

SPIDER CRAWLER - SHOOTER BOT

CHAIN GUN ENEMY

SETTINGS : DPAD

ANIMATION: NOT ALL STUFF SHOULD EXPLODE: FIRE AND CRASH DEBRIS LEAVES POT HOLE (L2): slower flipping debris 

Frame work for allies and huge fight plus insta shield

ANIMATED POND

BETTER L2 - CRATES, CONTAINERS LIKE RAIDEN II



BULLET: bullet flash https://duckduckgo.com/?va=o&t=ha&q=shmup+sprites+powerups&iax=images&ia=images&iai=https%3A%2F%2Fimages.squarespace-cdn.com%2Fcontent%2Fv1%2F551a19f8e4b0e8322a93850a%2F1607969224266-KWX66VFLV66TT276HVRM%2F83-Projectiles_P.gif

ANIMATED POND


ART: Improve art https://opengameart.org/art-search-advanced?keys=&field_art_type_tid%5B%5D=14&sort_by=count&sort_order=DESC

LOWER 



BETTER MAP TEXTURES example https://youtu.be/XqinwSr2yD8?si=IRvjGLWmDKA3l6UA&t=664





Turret blow off
CLEARLY SIGNPOST: FREE MODE <-->LOCKON MODE
CLEARLY SIGNPOST: Boosting, side dodge etc
NOTES: Use a single frame pic (ace combat style) to speed up dev
GUI: display panel slides up
GUI: gui must include current objective (can show on pause menu)
GUI: Game timer
GUI: full sidebar might be best
GUI: **KEY** XP/Points tick up on the Gui
GUI: Minimap bottom right?
GUI: GUI LAYOUT: HEALTH, INFO PANEL like DC
GUI: GUI LAYOUT: RIGHT VIDEO SCREEN FOR FAST, INGAME POPUP SCREEN FOR BLUR
GUI: Video phase in animation - telegraph it


CODE:Third layer with paralax canv Speed (possibly cloud cover) - canvas transparent. MOD to pick layer size
CODE: PROPER SCREEN PANNING so north,south gets more coverage in facing dir
CODE: ANIMATED TILES
H - shoot in lockon J - strafe mode JJ - clockwise mode  J hold - break off K - missile

ART: Redo unit art, better colour, look at tank from shmup
ART: Billowing black smoke
ART: Shockwave for barell, include shrapnell
ART: Backgrounds, cram more stuff into a 100/100 tile 
ART: More raiden explosions (check stuff falling, lv 1)
ART: Draw a bunch of stuff (Candc3 sprites long laser sect)
ART: INCINERY FLARE EXPLOSIONS https://youtu.be/zXjBS382P2k?t=224
ART: Special, Nuke Mussile
ART: Use contrast for background

SHOW:
- More colourful weapons (missiles,shields), dodge move
- A boss to show, objectives, allies, levels, and GUI scenes
- Tech Tree, flirt scene, weapons loadout
- Smoke, and progressive enemy damage
- TURRET COOKOFF
- Make no go zones on map
- GUI TEXT SCROLL TIMER
- When flying ships get hit, they crash and leave a crater
- Big cannons you destroy and black smoke pours out
- GROUND AA LASER CANNON builds up
- Propaganda stations
- Next ENEMY Arrow/s (red) this will help when vision is down..make it bigger as nearer
- Bullet blast animation, bullet impact animation
- Big power generators for laser, manufac facility, super conduct towers... (include obj acrrow)
 if time downloading objective with loading bar, otherwise put to later
- Next OBJECTIVE (green/yellow) arrow to speed to objective
	- Start making objectives
- Missiles are on timer, tick up to five, launch as many as targetted
- ADD ALLY
- ADD ALLY LOGIC
- ALLY COMMAND
- improved explosion animations
- APC
- Procedural level generator (start with enemy)
- raidal lockon speed is unlockable boost
- Delta time to keep speed constant
- DOUBLE BARREL 2 SHOTS SAME TIME
- Shrapnell flying out should land and puff
- Surfacing submarine
UNIT: Tanks can only move in 12 directions maybe 18 making animations look more 3d
bomb self frag

CONTROLER: Hold button to lock on and turn otherwise free roam
CONTROLER: Facing south when shooting inverts u/d
CONTROLER: Probably want lockon/lockoff buttons all to be the same - controll still feels offf, storyboard

- Tank bumping over - gives realistic feel, with dust thrown up by treds
BETA TESTING
- Add movement pivot around center point when not in lockon mode/ OR MODIFY LOCKON to pivot around center mass...adding more 
	 - Add variations as schemas to test for beta testing


ENEMIES TO ADD: 

GIGA TANK - COME FROM UNDER GROUND
GIGA TURRET / CANNON 
SHIPS IN PORTS

- BOSS Slog it battles, that is slugfest and boss chases you about screen
- BOSS all aim for his core at the same time

- Consider reducing sizes of sprites to make it more realistic (tanks,mlrs especially)
- UPGRADE TREE
	- MAINMENU UNLOCK
	- LONGER BOOST TIME - Dual fire
- Might wanna use the camToLocation from droneCommander
- tanks to be smaller, so they can roll out as a pack
- stretch - 'GOOD JOB' when enemy count ticks to zero in sector
- Check Godzilla for human type ideas
- Shmup into open world
- Redo omega storm including canvas
- Redo title text explaination with ai art gen - move to after game
- Boss target-points flash/Highlight
- Shmup maybe not needed not for a long time anyway
- release with twitter acc, automate reshares..adds, get list of shmups
- load assets by lv
- clean map editor, so it always checks number of rows, cols match actual in metaTiles 
- Light source
	- all shadows must change respectively
	- Shadow wonky fix
	- shadow that rotates about an origin point and not revolve around the player?
- chaff efficiency (limit number of chaff on screen) or just go with a ball of particles (save trans)
- movement wind/streak effect
- More ground damagable structs
- NAVI ALLY, include story etc
UNIT: JEEP (https://www.youtube.com/watch?v=uX9r5J1WYko)
ART: IMPROVE CONCRETE
UNSURE: Terrain should be smaller...maybe...think about it (small view like raiden or big like under attack)


# FEATURES: NAVAL BASE LEVEL 

- Medium sized ships
- SNOW ( a weeks work)
	- DRAW Carrier jets come at you
	-  Draw trees, muddy paths, mountains
	- AA in shell, 
	- small copters 10 attack if in area (raiden AI), 
	- Big copter volley of 4
	- tribarreled tanks (for later stages)
	- 4 Loaders, 
	- Guard towers
	- blizzard effect
	- toggle lockon view
	- units chase you a bit
	- groups of enemies (tanks roll out, copters group attack...etc)
	- Carrier must have jets that come attack you and fly back





# INSPIRATION


https://twitter.com/DonPachi003/status/1615725706918469634 baddy example

Level ideas https://twitter.com/dantemendes/status/1625699195289042945
https://twitter.com/HTProject073/status/1603999213138116609


https://www.youtube.com/watch?v=cD_n6TA2VXw

https://youtu.be/e6RqIcdMlPc

power of 10 artwork ideas https://store.steampowered.com/app/1319550/Power_of_Ten/ 

Unity game https://www.reddit.com/user/KrahsteertS/

saturn game https://twitter.com/dantemendes/status/1605888637534707717

shmup maker https://twitter.com/bulostudio/status/1606030117133815808

Gyro Blade
https://twitter.com/HTProject073/status/1600464060428222464

https://twitter.com/HTProject073/status/1601422278054449153

music making https://www.youtube.com/watch?v=l61EBjVd9tw

https://www.youtube.com/watch?v=-10qqJ_f8ak













## FEEDBACK_FROM_PEOPLE
JUMP_CONTENTS


LEVEL DESIGN TRICK: FOR CONCRETE BASE, BREAK THINGS UP SO ITS NOT CONTINUOUS, HAVE HOLES IN THE FLOOR


Looking good! Some improvements if I may: Tile variants in the grass, it would break up the repetition, you can see a grid.
Shadows for everything.
The player movement seems a little stiff, could be a little slower to stop when the player stops moving.




```


User avatar
level 1
Adventurous_Jacket64
·
14 hr. ago
The way I solved this was by splitting the tiles into chunks, then pre render the chunks and blit the ones that are shown to the screen right now. This will make the tile rendering time so insignificant you won't notice it.

Also, you probably don't want to use a dictionary, a list (or an array) is much more suitable for such cases, especially if the keys are ints anyways.

In your case, since the map doesn't even change, the chunks can be arbitrarily large so just try different sizes and see what works best
```





# ACCEPTANCE_CRITERIA 
JUMP_CONTENTS

KEEP: Currently, tank battles feel shmupy, lots of damage, carnage. 

LOTS TO DODGE 

LOTS TO SHOOT 

2. Must have MULTIPLE LAYERS
3. MUST BE differentiable from the 10000 other Shmups (RPG element, Summon attack, Gameplay mechanics???). Joint teams.Shmup/Open pivot
4. Dodging huge boss like bullet hell stream
5. Review videos
- QUALITY CONTROL - Does it still have slug throwing Shmup feel? Are graphics isometric a bit
- Keep it different from Gyro blade, it should be fast, manic and fun. Not desert strike
- Lots of variety on screen, AA, planes, ATB, etc
- Good Map Detail 
- FLOW FUGE MODE: Zoom to area with dog fight tailers...jump into lockon mode..clean up
- Visuals still FAR below par - have they been improved to look nice? Think is a boss fight got that proboctor feel?








## UNDER CONSIDERATOIN

[`JOINT SPECIAL ATTACK`, `Shmup intro`, `slow Underdefeat shmup levels`,   ]


 

# REFS 







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





## BIG SCENES


## 0 - INTRO

BUNNIES, FOX, CATS on Mars, Venus and outposts
Parallel world where we gen altered ourselves. Solar system has 40 billion peeps
 - "Your earth isnt the same as ours"
 - "Ssw the solar system wars"


 AMU A ROGUE FROM THE AI PERIMETER

## MUST 
- LV 1 TUTORIAL, SHOWING EACH MOVE WITH SLOWDOWN...TAP C FOR CHAFF, TO MUSIC RYTHM REALLY MATTERS


## 1 - TRAINING VR / THE BIG FURBALL

---CHATER 0 THE BIG FURBALL---

'Takes the keys', your GROUNDED, BACK TO VR
- Team break! (Ling ling, Raj, Simon...) 
- Race them to clearing objective points
- Roxy goes - 'YESSSSS!' in quick pop up once she takes out sth
- Chase each other with Lockon fights
- Vr first has level bars rapidly changjng also show who captures objectives

--TUTORIAL 

	---- STEER
	----- SHOW LOCKON RADARD AND LOCKON
	----- DODGE A SHOT BY PUSHING CHAFF BUTTON, TIME SLOWS DOWN
	----- DODGE BY BOOST WHICH BREAKS LOCKON 'GET THE HELL OUT OF THERE '


## 2 - DREADNOUGHT


THE DREADNOUGHT IS COMING TO DESTROY THE SUN

THE DRONE QUEEN DOES ALL SHE CAN TO STOP THEM AT THE OUTER SOLAR SYSTEM

FIGHT BEGINS, YOU APPROACH FROM REAR

TIMER STARTS; TICK DOWN TOP RIGHT + SHIP HEALTH BAR

PERIMETER 5: THE AI RING

DESTROY PART OF SHIP WITH THEIR HELP

PERIMETER 4: ASTEROID 

SAME

PERIMETER 3: MARS

GIANT PULSE CANNONS DESTROY ANOTHER SEGMENT
(Multiple allies with you now)

PERIMETER 2: EARTH

MULTIPLE SMALLER PERIMETERS, USA, CHINA, UK ETC

NUKES

PERIMETER 1: VENUS

THE FOXES AND THEIR SWARM FLEETS 

PERIMETER 0: MERCURY

FINAL STAND THE ROGUE ALLIANCE OF ALL THE OTHERS






implementation 

battlship preview before coming to you
Dreadaught restrict sections and slow scroll speed
Dreadnaught regens...hence timed to take out at mars
Boss target points flash

show jupiter sphere, mars sphere, earth sphere, venus sphere


story

Timer in big, 'x until end of Earth...or the sun, **shrinks to top right**'
MASSIVE EXPLOSIONS, AIM BIGGER THAN THE REST
Beat the ship, then give a triumphant intro..Adam proudly presents etc
Use UDM names, Turov etc, make a big tutorial
go here shoot this use chaff repeat



## 3  - protecting carrier group

- China, USA ships destroyed, carriers retreating from shielded mothership
- You blast in, using FLASH to break its shields
- Short dialogue before Red and Blue jets join behind you
- Big fight to take it apart, it fleets
- Chase it about the map

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



		- (settings, profile...)



## STORY BOARDING



....One ship... just one ship, thats all it takes to destroy a system
fermi paradox
we know its coming, other planets already destroyed
immune system, turns them on to each other
earth is so yesterday.. (make it in game jibes)


- EARTH HAS COME A LONG WAY SINCE THE FORMATION OF A WEIGHED FEDERATED ALLIANCE
  (SPACE SHIPS, MANS SHAKING HANDS)
  - SSW 1 SSW 2
  - propoganda, 

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








## MOVEMENT STRETCH CONSIDERATIONS 

- MOVEMENT EXPERIMENT CONSIDERATIONS
 	- LOCKON SHOULDN'T FACE TARGET, cus you plough into it, should put you into jink mode, which you can swivel holding jink button
	- Maybe just slow down when enemies are in range (unless you boost)
	- Consider shooting puts you in Jink mode to strafe like under defeat
	- Consider holding down lockon, when you let go, you are just in jink mode
	- Make dodging a big element too zipping past until you get to a good part
	- Jinkshoot spray and pray by slowing forward motion is a must.. to make chaff dodge work it should be in non shooting mode..you can lob missiles maybe
	- Fine control, so rotation is inversed if facing down, (but only if r,l isn't already pressed)
	- Want to be able to dodge enemy in shmup style, lockon camera centering clamp may be needed
		- this makes jink manual
		- more thinking required, because to get that flow, its hard if there are enemies in front and beside


## PIXEL ART 

- SCULPT not draw
- DEFINE A LIGHT SOURCE
- start simple
- ask why i'm adding another colour

## DONE 

DONE: Enemy Respawn
DONE: make and render player DONE: Do a simple map DONE: Navigate with aswd DONE: Camera Nav
DONE - Map maker, Midjourney images, Fix camera, HIT DAMAGE, player explosion animation, allow player to die, Thinner fire, Double fire, radar cone, LOCK ON
DONE: Finish isonscreen function - test using a viewport, TRISHOT - Like in Underdefeat, Multi-tile edit
DONE: - JINK IF NOT IN PIVOT, LOCKON TOGGLE (left/right to scroll), LOCKON LIMIT 3, FACE ENEMY DURING LOCKON, PIVOT CLOCKWISE DURING LOCKON GROUND UNIT, Jink button switches lockon, or moves direction if held
DONE: Enemy placer, Remove jink timer, especially if lockon disabled,dont allow multiple selects of enemy on one tile, MISSILE, Missiles- homin & horizontal jink only. need plume, contact explosion
GROUND AA with bullets   [5], GROUND AA With missiles (MLRS), In lockoff 1. Shoot init X,Y. left/Right should always move you in that dir. , in lockoff 2. limit spray angle to 45
- Camera shake - Split out controls - CHAFF - BOAT enemy - GROUND damagable structures - Destroyed tanks, ground units leave husks - Buildings as second layer non-interactable 
ISOMETRIC MISSILE BASE  - PLACE ME ANYWHERE LAYER
- Objective class and automated progressor
- objective arrow flashes to next objective.
- Limit sectors until objectives complete
- pointer times out after 3 seconds, B to show it
 - keep enemies in quandrant
- DRAW L2 ABOVE GROUND AND ENEMIES BELOW TREES

 isometric base (build parts like fence) 
 	- Bomb
- bomb
- change selection criteria to be simply a square  
- create spawn point placer, drag/drop perimeter (toggle box one more-  it should show a number)
- Make select enemy objective
Consider making units smaller
- snow tank, 
- Fix frigate
2. Add blue laser
Destroyable Barracks
SQUARE SAMS
HEALTH POWER UP DRONE
WIREFRAME GUI
MAP OVERHAUL
ANGLE BULLETS
POWER UPs [from box, basic gui to show what i'm shooting with
- Trees (so they cluster as group too)
Enemy power up spawner

Add option on map selector for unit
Or in level code i.e. every 5th tank
Adds spawn power up to class attr

Add check at death
Adds PD to enemy list

---self kill

Kill timer
Start once seen
Animate all slides but slowly
Terninate

---Pd- cycle different weapon

Random chance at spawn
Have it cycle between weap types 
Cycle timer
Need a switch dict
If timer met switch to same level tho
6. SCORE SYSTEM - Extra life at 1k
7. SPAWN POWERUP OPTION (RANDOM POWERUP - BUT IT STEPS YOU UP NOT JUMPS TO THREE SHOT)