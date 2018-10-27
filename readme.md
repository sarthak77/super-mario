# Pythen terminal mario

##Running the program

- Install requirements:
 - `pip install -r requirements.txt`
- Run the program:
 - `python3 main.py`

## Controls:

- d->right
- a->left
- f->bullet
- sw->up jump
- aw->back jump
- dw->forward jump
- ctrl+c->to quit

## Required_Features
 # OO concepts
 - INHERITANCE:Objetcs are derived from `Object` class
 - POLYMORPHISM:To check movements of the enemy and mario
 - ENCAPSULATION:Class based approach to construct the game
 - ABSTRACTION:Private variables of the objects prevent any change from outside 

 #Movement
 - left,right,jump
 - gravity effect jump
 - jump on blocks pops them out

 #Obstacles
 - enemies move left,right,automatically
 - enemies with different speed
 - enemies chase the player
 - time,life,bullet,coins and coordinates of mario displayed
 - controls of the game displayed
 #Score
 - time score
 - life score
 - coin score
 - enemy killing score


 #Background
 - scenery changes when mario about to move out of the window
 - different scenes in the background containing clouds,mountains,tunnels,bridges,rivers,flags,walls etc

 #Bonus
 - color using ANSI colour codes for terminal
 - sound
 - smart enemies which chase the player, move fast, invincible etc

##Extra_Features

#Basic
- additional start screen
- shows prev dead location of mario
- at the end mario enters into the castle and fireworks begin
- score calculated at the end of the game

#Enemies
- enemy2:
- walk on water
- walk faster
- cannot kill by jumping(but will get points for it) or by firing

- enemy1:
- random follow
- difficult to kill by jump
- can be killed by bullet

- enemy2 and enemy1 can block each other
- use enemies wisely to avoid being killed
- 
#Coins
- generated randomly
- 3 types
- ? 1 points
- C 10 points
- $ 50 points
- imaginary coin block

#Power_ups
- power ups go away if jumped again on same block
- random power ups throughout the level
- pop out on jumping

#Imaginary_blocks
- imaginary block at ycoor=75

#Bullet
- pass through the flower slowly to get the bullet
- once flower plucked its stem will disappear

#Level
- speed of enemies increases as mario progresses

## file structure

.
├── board.py
├── color.py
├── func.py
├── main.py
├── mainscene.py
├── __pycache__
│   ├── board.cpython-36.pyc
│   ├── color.cpython-36.pyc
│   ├── func.cpython-36.pyc
│   ├── infoscreen.cpython-36.pyc
│   ├── inputeg.cpython-36.pyc
│   ├── main.cpython-36.pyc
│   ├── mainscene.cpython-36.pyc
│   └── start.cpython-36.pyc
├── readme.md
├── requirements.txt
├── sounds
│   ├── background.wav
│   ├── smb_1-up.wav
│   ├── smb_bump.wav
│   ├── smb_coin.wav
│   ├── smb_fireball.wav
│   ├── smb_fireworks.wav
│   ├── smb_flagpole.wav
│   ├── smb_gameover.wav
│   ├── smb_jump-small.wav
│   ├── smb_jump-super.wav
│   ├── smb_kick.wav
│   ├── smb_mariodie.wav
│   ├── smb_powerup_appears.wav
│   ├── smb_powerup.wav
│   ├── smb_stage_clear.wav
│   ├── smb_stomp.wav
│   ├── smb_vine.wav
│   ├── smb_warning.wav
│   └── smb_world_clear.wav
└── start.py

2 directories, 35 files
