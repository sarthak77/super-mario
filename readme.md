# Pythen terminal mario

## Running the program

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
 ### OO concepts
 - INHERITANCE:Objetcs are derived from `Object` class
 - POLYMORPHISM:To check movements of the enemy and mario
 - ENCAPSULATION:Class based approach to construct the game
 - ABSTRACTION:Private variables of the objects prevent any change from outside 

 ### Movement
 - left,right,jump
 - gravity effect jump
 - jump on blocks pops them out

 ### Obstacles
 - enemies move left,right,automatically
 - enemies with different speed
 - enemies chase the player
 - time,life,bullet,coins and coordinates of mario displayed
 - controls of the game displayed
 
 ### Score
 - time score
 - life score
 - coin score
 - enemy killing score

 ### Background
 - scenery changes when mario about to move out of the window
 - different scenes in the background containing clouds,mountains,tunnels,bridges,rivers,flags,walls etc

 ### Bonus
 - color using ANSI colour codes for terminal
 - sound
 - smart enemies which chase the player, move fast, invincible etc

## Extra_Features

### Basic
- additional start screen
- shows prev dead location of mario
- at the end mario enters into the castle and fireworks begin
- score calculated at the end of the game

### Enemies
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

### Coins
- generated randomly
- 3 types
- ? 1 points
- C 10 points
- $ 50 points
- imaginary coin block

### Power_ups
- power ups go away if jumped again on same block
- random power ups throughout the level
- pop out on jumping

### Imaginary_blocks
- imaginary block at ycoor=75

### Bullet
- pass through the flower slowly to get the bullet
- once flower plucked its stem will disappear

### Level
- speed of enemies increases as mario progresses

## file structure

<br>.
<br>├── board.py
<br>├── color.py
<br>├── func.py
<br>├── main.py
<br>├── mainscene.py
<br>├── __pycache__
<br>│   ├── board.cpython-36.pyc
<br>│   ├── color.cpython-36.pyc
<br>│   ├── func.cpython-36.pyc
<br>│   ├── infoscreen.cpython-36.pyc
<br>│   ├── inputeg.cpython-36.pyc
<br>│   ├── main.cpython-36.pyc
<br>│   ├── mainscene.cpython-36.pyc
<br>│   └── start.cpython-36.pyc
<br>├── readme.md
<br>├── requirements.txt
<br>├── sounds
<br>│   ├── background.wav
<br>│   ├── smb_1-up.wav
<br>│   ├── smb_bump.wav
<br>│   ├── smb_coin.wav
<br>│   ├── smb_fireball.wav
<br>│   ├── smb_fireworks.wav
<br>│   ├── smb_flagpole.wav
<br>│   ├── smb_gameover.wav
<br>│   ├── smb_jump-small.wav
<br>│   ├── smb_jump-super.wav
<br>│   ├── smb_kick.wav
<br>│   ├── smb_mariodie.wav
<br>│   ├── smb_powerup_appears.wav
<br>│   ├── smb_powerup.wav
<br>│   ├── smb_stage_clear.wav
<br>│   ├── smb_stomp.wav
<br>│   ├── smb_vine.wav
<br>│   ├── smb_warning.wav
<br>│   └── smb_world_clear.wav
<br>└── start.py

2 directories, 35 files
