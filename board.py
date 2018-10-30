"""
contains info about the board
contains functions about the board
starting board
do not change(change at your own risk)
"""

import random


DIMY = 40
DIMX = 100
WORD = "*"
CLOUD = "^"


def addcloud(grid, xcor, ycor):
    """
    adding clouds
    """
    grid[xcor:xcor+2:1, ycor:ycor+13:1] = CLOUD
    grid[xcor-1:xcor+3:3, ycor+1:ycor+12:1] = CLOUD
    grid[xcor-2, ycor+2:ycor+11:1] = CLOUD
    grid[xcor-2, ycor+5:ycor+8:1] = "-"
    grid[xcor-1, ycor+6] = "-"
    return grid


HILL = "/"


def addhill(grid, xcor, ycor):
    """
    adding hills
    """
    grid[xcor, ycor] = HILL
    count = 1
    xcor += 1
    while count != 8:
        grid[xcor, ycor-count:ycor+count+1:1] = HILL
        count += 1
        xcor += 1
    return grid


TUNNEL = "|"


def addtunnel(grid, xcor, ycor):
    """
    adding tunnels
    """
    grid[xcor, ycor:ycor+9:8] = TUNNEL
    grid[xcor:xcor+4:1, ycor+1:ycor+8:1] = TUNNEL
    return grid


def addmario(grid, xcor, ycor):
    """
    adding mario
    """
    grid[xcor, ycor] = "@"
    grid[xcor+1, ycor-2:ycor+3:1] = ["<", "-", "|", "-", ">"]
    grid[xcor+2, ycor-1:ycor+2:2] = "^"
    return grid


BLOCK = "O"


def addblock(grid, xcor, ycor):
    """
    adding blocks
    """
    grid[xcor-1:xcor+2:1, ycor:ycor+15:1] = BLOCK

    # random coins
    for i in range(15):
        ptr = random.randint(0, 4)
        if ptr == 1:
            grid[xcor, ycor+i] = "?"

    # randomly spawn power ups
    ptr = random.randint(0, 20)
    if ptr < 12:
        grid[xcor, ycor+ptr:ycor+ptr+2:1] = "P"
    return grid


def addsblock(grid, xcor, ycor):
    """
    adding single blocks
    """
    grid[xcor-1:xcor-4:-1, ycor:ycor+6:1] = BLOCK

    # coins
    for i in range(6):
        ptr = random.randint(0, 1)
        if ptr == 1:
            grid[xcor-2, ycor+i] = "C"

    # super coins
    ptr = random.randint(0, 5)
    grid[xcor-2, ycor+ptr] = "$"
    return grid


LE = "@"


def addler(grid, xcor, ycor):
    """
    adding bricks at the end
    """
    grid[xcor:xcor-4:-1, ycor:ycor+35:1] = LE
    grid[xcor-4:xcor-8:-1, ycor+7:ycor+35:1] = LE
    grid[xcor-8:xcor-12:-1, ycor+14:ycor+35:1] = LE
    grid[xcor-12:xcor-16:-1, ycor+21:ycor+35:1] = LE
    grid[xcor-16:xcor-20:-1, ycor+28:ycor+35:1] = LE
    return grid


def addlel(grid, xcor, ycor):
    """
    add level ender
    """
    grid[xcor:xcor+4:1, ycor:ycor+7:1] = LE
    grid[xcor+4:xcor+8:1, ycor:ycor+14:1] = LE
    grid[xcor+8:xcor+12:1, ycor:ycor+21:1] = LE
    grid[xcor+12:xcor+16:1, ycor:ycor+28:1] = LE
    grid[xcor+16:xcor+20:1, ycor:ycor+35:1] = LE
    return grid


FLAG = "M"
FLAGH = "|"


def addflag(grid, xcor, ycor):
    """
    adding flag
    """
    grid[xcor:xcor-16:-1, ycor:ycor+2:1] = FLAGH
    grid[xcor-15:xcor-12:1, ycor+2:ycor+10:1] = FLAG
    return grid


CASTLE = "H"


def addcastle(grid, xcor, ycor):
    """
    adding CASTLE
    """
    grid[xcor:xcor-6:-1, ycor:ycor+20:1] = CASTLE
    grid[xcor-6:xcor-10:-1, ycor+5:ycor+15:1] = CASTLE
    grid[xcor:xcor-3:-1, ycor+8:ycor+12:1] = "."
    return grid


E1T = "Q"
E1B = "x"


def adde1(grid, xcor, ycor):
    """
    adding enemy1
    """
    grid[xcor, ycor:ycor+3:1] = E1B
    grid[xcor-1, ycor+1] = E1T
    return grid


E2T = "Q"
E2B = "x"


def adde2(grid, xcor, ycor):
    """
    adding enemy2
    """
    grid[xcor, ycor+1:ycor+4:1] = E2B
    grid[xcor-1, ycor:ycor+2:1] = E2T
    return grid
