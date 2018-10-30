"""
contains game board and functions which effect the board
and involve any change to the board
"""

import os
import time
import sys
import numpy as np
import board
import color

# for maintaining timer
from main import BASETIME

# to print in a good way
np.set_printoptions(linewidth=1000, threshold=np.nan)

#global variables
E1_ARR = []
E2_ARR = []


class MainsceneBoard:
    """
    contains methods affecting the game board
    """

    def __init__(self):

        # basic structure
        self.__grid = np.chararray((40, 100*10))
        self.__grid[:] = "-"
        self.__grid[36:40:1, :] = "#"

        # gaps
        # also in moveflag func
        self.__grid[36:40:1, 180:190:1] = "~"
        self.__grid[36:40:1, 485:490:1] = "~"

        # clouds
        for i in range(7, 600, 100):
            self.__grid = board.addcloud(self.__grid, 5, i)
        for i in range(60, 600, 100):
            self.__grid = board.addcloud(self.__grid, 7, i)

        # hills
        for i in range(40, 600, 100):
            self.__grid = board.addhill(self.__grid, 28, i)

        # tunnels
        for i in range(100, 540, 150):
            self.__grid = board.addtunnel(self.__grid, 32, i)

        # mario
        self.__grid = board.addmario(self.__grid, 33, 6)

        # blocks
        for i in range(40, 400, 57):
            self.__grid = board.addblock(self.__grid, 27, i)

        # random blocks

        # type1
        self.__grid = board.addblock(self.__grid, 23, 230)
        self.__grid = board.addblock(self.__grid, 23, 240)
        self.__grid = board.addblock(self.__grid, 23, 290)
        self.__grid = board.addblock(self.__grid, 23, 300)
        self.__grid = board.addblock(self.__grid, 19, 520)
        self.__grid = board.addblock(self.__grid, 19, 530)

        # type2
        self.__grid = board.addsblock(self.__grid, 15, 233)
        self.__grid = board.addsblock(self.__grid, 15, 239)
        self.__grid = board.addsblock(self.__grid, 15, 245)
        self.__grid = board.addsblock(self.__grid, 19, 159)

        # enemies

        # enemy1 y=even

        self.__grid = board.adde1(self.__grid, 35, 160)
        self.__grid = board.adde1(self.__grid, 35, 166)
        self.__grid = board.adde1(self.__grid, 35, 300)
        self.__grid = board.adde1(self.__grid, 35, 310)
        self.__grid = board.adde1(self.__grid, 35, 424)

        # enemy2
        self.__grid = board.adde2(self.__grid, 35, 220)
        self.__grid = board.adde2(self.__grid, 35, 390)
        # self.__grid=board.adde2(self.__grid,35,425)
        self.__grid = board.adde2(self.__grid, 35, 529)

        # random tunnels
        self.__grid = board.addtunnel(self.__grid, 32, 350)

        # level ender
        self.__grid = board.addler(self.__grid, 35, 450)
        self.__grid = board.addlel(self.__grid, 16, 490)

        # flag
        self.__grid = board.addflag(self.__grid, 35, 550)

        # castle
        self.__grid = board.addcastle(self.__grid, 35, 600)

        # bullets
        self.__grid[27, 215:220:1] = "?"
        self.__grid[27, 51] = "?"

    def printboard(self, printobj):
        """
        for printing the game scene
        """
        index = printobj[0]
        coor = printobj[1]
        life = printobj[2]
        score = printobj[3]
        bullet = printobj[4]

        os.system('clear')

        sys.stdout.flush()
        for row in range(40):
            for column in range(0+index, 100+index, 1):
                sys.stdout.write(color.getcolor(
                    self.__grid[row, column].decode()))
            sys.stdout.write("\n")

        print()
        global BASETIME
        print("TIME->", int(time.time()-BASETIME))
        print("LIFE->", life, "BULLET->", bullet)  # bullet 1 means yes
        print("COINS:", score, "MARIO:", coor)
        print()

        # making easy to avoid enemies
        if life < 3:
            print("ENEMY1->", E1_ARR, "ENEMY2->", E2_ARR)
        # printing controls
        print("d->right\na->left\nf->bullet\n\nsw->jump\ndw->rjump\naw->ljump\n\nq->quit")


# ---------------mario-------------------------------------


    def updateboardf(self, present, prev):
        """
        help make mario move forward
        """
        self.__grid[present[0], present[1]] = prev[0]
        self.__grid[present[0]+1, present[1]-2] = prev[1]
        self.__grid[present[0]+1, present[1]-1] = prev[2]
        self.__grid[present[0]+2, present[1]-1] = prev[6]

        # to update start position of mario
        if present[1] < 30:
            self.__grid[33:36:1, 2:15:1] = "-"

        return()

    def updateboardb(self, present, prev):
        """
        help make mario move backward
        """
        self.__grid[present[0], present[1]] = prev[0]
        self.__grid[present[0]+1, present[1]+1] = prev[4]
        self.__grid[present[0]+1, present[1]+2] = prev[5]
        self.__grid[present[0]+2, present[1]+1] = prev[7]

        # to update start position of mario
        if present[1] < 10:
            self.__grid[33:36:1, 2:15:1] = "-"

        return()

    def updateboardbjump(self, present, prev):
        """
        help make mario move on jump
        """
        self.__grid[present[0], present[1]] = prev[0]
        self.__grid[present[0]+1, present[1]-2] = prev[1]
        self.__grid[present[0]+1, present[1]-1] = prev[2]
        self.__grid[present[0]+1, present[1]] = prev[3]
        self.__grid[present[0]+1, present[1]+1] = prev[4]
        self.__grid[present[0]+1, present[1]+2] = prev[5]
        self.__grid[present[0]+2, present[1]-1] = prev[6]
        self.__grid[present[0]+2, present[1]+1] = prev[7]
        return()

    def updatemario(self, x_cor, y_cor):
        """
        to print mario
        """
        self.__grid = board.addmario(self.__grid, x_cor, y_cor)

    def clean(self, present, prev):
        """
        to remove mario from screen
        """
        self.__grid[present[0], present[1]] = prev[0]
        self.__grid[present[0]+1, present[1]-2] = prev[1]
        self.__grid[present[0]+1, present[1]-1] = prev[2]
        self.__grid[present[0]+1, present[1]] = prev[3]
        self.__grid[present[0]+1, present[1]+1] = prev[4]
        self.__grid[present[0]+1, present[1]+2] = prev[5]
        self.__grid[present[0]+2, present[1]-1] = prev[6]
        self.__grid[present[0]+2, present[1]+1] = prev[7]

# --------------------------------------------------------------

# ----------------------enemies-------------------------------

    def searchenemy(self, i):
        """
        finds enemies on the board
        """
        for j in range(80+i, 100+i, 1):  # max=100+i and difference = increment in i
            if self.__grid[34, j] == b'Q':
                if self.__grid[34, j+1] == b'Q':
                    global E2_ARR
                    try:
                        E2_ARR.index(j)
                    except:
                        E2_ARR.append(j)
                elif self.__grid[34, j-1] != b'Q':
                    global E1_ARR
                    try:
                        E1_ARR.index(j)
                    except:
                        E1_ARR.append(j)

        return(E1_ARR, E2_ARR)

    def updateenemy1b(self, y_i, arr):
        """
        helps move enemy1 back
        """
        self.__grid[34, y_i] = arr[0]
        self.__grid[35, y_i] = arr[2]
        self.__grid[35, y_i+1] = arr[3]

    def updateenemy1f(self, y_i, arr):
        """
        helps move enemy1 forward
        """
        self.__grid[34, y_i] = arr[0]
        self.__grid[35, y_i-1] = arr[1]
        self.__grid[35, y_i] = arr[2]

    def updateenemy1(self, x_cor, y_cor):
        """
        to add enemy1
        """
        self.__grid = board.adde1(self.__grid, x_cor+1, y_cor-1)

    def updateenemy2b(self, y_i, arr):
        """
        helps move enemy2 back
        """
        self.__grid[34, y_i] = arr[0]
        self.__grid[34, y_i+1] = arr[1]
        self.__grid[35, y_i+2] = arr[3]
        self.__grid[35, y_i+3] = arr[4]

    def updateenemy2(self, x_cor, y_cor):
        """
        to add enemy2
        """
        self.__grid = board.adde2(self.__grid, x_cor+1, y_cor)

    def cleane1a(self, y_cor, prev):
        """
        to remove enemy1 from screen if dead
        """
        self.__grid[34, y_cor] = prev[0]
        self.__grid[35, y_cor-1] = prev[1]
        self.__grid[35, y_cor] = prev[2]
        self.__grid[35, y_cor+1] = prev[3]

# ------------------------------------------------


# ------------coins-----------------------------



    def jumpupc(self, x_cor, y_cor):
        """
        when jumping up on blocks
        """
        self.__grid[x_cor, y_cor] = "-"
        self.__grid[x_cor-3, y_cor] = "O"
        if self.__grid[x_cor-1, y_cor].decode() == "?":
            os.system('aplay ./sounds/smb_coin.wav&')
            return 1
        elif self.__grid[x_cor-1, y_cor].decode() == "C":
            os.system('aplay ./sounds/smb_coin.wav&')
            return 10
        elif self.__grid[x_cor-1, y_cor].decode() == "$":
            os.system('aplay ./sounds/smb_coin.wav&')
            return 50
        elif self.__grid[x_cor-1, y_cor].decode() == "P":
            os.system('aplay ./sounds/smb_powerup_appears.wav&')
            return 11
        else:
            os.system('aplay ./sounds/smb_bump.wav&')
            return 0

    def jumpdownc(self, x_cor, y_cor):
        """
        for "coin coming out" effect
        """
        self.__grid[x_cor, y_cor] = "O"
        self.__grid[x_cor-1, y_cor] = "O"
        self.__grid[x_cor-3, y_cor] = "-"

# ---------------------------------------------------

    def updatecell(self, x_cor, y_cor, value):
        """
        to update the value at any cell
        """
        self.__grid[x_cor, y_cor] = value

    def addflower(self, x_cor, y_cor):
        """
        make flower come out of the brick
        """
        self.__grid[x_cor-1, y_cor] = "I"
        self.__grid[x_cor-2, y_cor] = "*"
        self.__grid[x_cor-2, y_cor-1] = "*"
        self.__grid[x_cor-2, y_cor+1] = "*"

    def addfireworks(self, x_cor, y_cor):
        """
        to add fireworks at the end of game
        """
        self.__grid[x_cor, y_cor-1:y_cor+2:1] = "*"
        self.__grid[x_cor-1, y_cor] = "*"
        self.__grid[x_cor+1, y_cor] = "*"

    def getgrid(self, x_cor, y_cor):
        """
        to get character at any point
        """
        return self.__grid[x_cor, y_cor].decode()

    def moveflag(self, i):
        """
        moves flag down at the end
        """
        self.__grid[i, 552:560:1] = "-"
        self.__grid[i+3, 552:560:1] = board.FLAG
