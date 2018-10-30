"""
contains starting board
"""
import os
import numpy as np
import board

# to print in a good way
np.set_printoptions(linewidth=1000, threshold=np.nan)


class StartBoard:
    """
    initializes starting board
    """
    def __init__(self):

        # basic structure
        self.__grid = np.chararray((board.DIMY, board.DIMX))
        self.__grid[:] = "@"
        self.__grid[3:board.DIMY-3:1, 6:board.DIMX-6:1] = ""
        self.__grid[3:board.DIMY-3:1, 6:board.DIMX-6:1] = "-"
        self.__grid[5:20:1, 30:62:1] = "@"
        self.__grid[6:11:2, 33:36] = board.WORD
        self.__grid[7, 33] = board.WORD
        self.__grid[9, 35] = board.WORD

        # words
        self.__grid[23, 43:48:1] = ["S", "T", "A", "R", "T"]
        self.__grid[25, 43:47:1] = ["Q", "U", "I", "T"]

        # pointer
        self.__grid[23, 41] = ">"

        # super
        self.__grid[6:11:1, 37:41:3] = board.WORD
        self.__grid[10, 38:40:1] = board.WORD
        self.__grid[6:11:1, 42] = board.WORD
        self.__grid[6:9:2, 43:46:1] = board.WORD
        self.__grid[7, 45] = board.WORD
        self.__grid[6:11:1, 47] = board.WORD
        self.__grid[6:11:2, 48:51:1] = board.WORD
        self.__grid[6:11:1, 52] = board.WORD
        self.__grid[6:9:2, 53:56:1] = board.WORD
        self.__grid[7, 56] = board.WORD
        self.__grid[9, 53] = board.WORD
        self.__grid[10, 54:56:1] = board.WORD

        # mario
        self.__grid[13:18:1, 37:42:4] = board.WORD
        self.__grid[13, 38:41:2] = board.WORD
        self.__grid[14, 39] = board.WORD
        self.__grid[13:18:1, 43:46:2] = board.WORD
        self.__grid[13:16:2, 44] = board.WORD
        self.__grid[13:18:1, 47] = board.WORD
        self.__grid[13:18:2, 47:51:1] = board.WORD
        self.__grid[14, 50] = board.WORD
        self.__grid[16, 48] = board.WORD
        self.__grid[17, 48] = '@'
        self.__grid[13:18:1, 52:54:1] = board.WORD
        self.__grid[13:18:1, 55:59:3] = board.WORD
        self.__grid[13:18:4, 56:58:1] = board.WORD

    def getgrid(self, posx, posy):
        """
        to get grid
        """
        return self.__grid[posx, posy].decode()

    def printboard(self):
        """
        to print
        """
        os.system('clear')
        print(str(self.__grid).replace(' ', '').replace('.', '').replace(
            '[', '').replace(']', '').replace('b', '').replace('\'\'', ""))

    def update(self, posx, posy, character):
        """
        to update
        """
        self.__grid[posx, posy] = character
