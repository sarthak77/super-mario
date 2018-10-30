"""
main code of the game
"""

import sys
import tty
import select
import termios
import time
from start import *
from mainscene import *
from func import *

# GLABAL VARIABLES
QUITVAR = 1
i = 0  # index for maintaining screen
MARIOPRESENT = [33, 7]
MARIOPREV = ["-", "-", "-", "-", "-", "-", "-", "-"]  # 8 elements
LIFE = 3
SCORE = 0  # coins
BASETIME = time.time()
CJUMP = 10  # for surprise coin
BULLET = 0
BA = [51, 215, 216, 217, 218, 219]  # BULLET array
E1_ARR = []
E2_ARR = []
# to control enemy loop
LOOP = 0  # ENEMY1
LOOP2 = 0  # ENEMY2
# 9 enemies
ENEMY1 = np.chararray((5, 4))
ENEMY1[:] = "-"
ENEMY2 = np.chararray((4, 5))
ENEMY2[:] = "-"

#old settings
OLD = termios.tcgetattr(sys.stdin)


def is_data():
    """
    to take input
    """
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

# --------------take input without pressing enter-----------------------------


class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""

    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()


class _GetchUnix:
    def __call__(self):
        f_d = sys.stdin.fileno()
        old = termios.tcgetattr(f_d)
        try:
            tty.setraw(sys.stdin.fileno())
            c_h = sys.stdin.read(1)
        finally:
            termios.tcsetattr(f_d, termios.TCSADRAIN, old)
        return c_h


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.GETCH()


GETCH = _Getch()

# ------------------------------------------------------------------------------

# --------------------------start screen---------------------------------------


class START(object):
    """
    start screen
    """
    def __init__(self):
        """
        making object
        """
        self.__board = StartBoard()

    def run(self):
        """
        main function
        """
        self.__board.printboard()

        while 1:
            print()
            print(
                "                       --------------------------------------------------------")
            print(
                "                      |PRESS s TO GO DOWN---PRESS w TO GO UP---PRESS f TO ENTER|")
            print(
                "                       --------------------------------------------------------")
            print()
            inp = GETCH()

            if inp == "s":
                self.__board.update(23, 41, '-')
                self.__board.update(25, 41, '>')

            if inp == "f":
                if self.__board.getgrid(23, 41) == ">":
                    os.system('clear')
                    print(
                        "                                          STARTING GAME IN 3s")
                    os.system('aplay ./sounds/smb_world_clear.wav')
                    global QUITVAR
                    QUITVAR = 0
                break

            if inp == "w":
                self.__board.update(25, 41, '-')
                self.__board.update(23, 41, '>')

            self.__board.printboard()

# ---------------------------------------------------------------------------------

# ------------------------------game scene class-----------------------------------


class SCREEN(object):
    """
    main class
    """
    def __init__(self):
        """
        creating object
        """
        self.__board = MainsceneBoard()

    def reset(self):
        """
        to reset when dead
        """
        global MARIOPRESENT, MARIOPREV, i, LIFE, SCORE, BULLET

        self.__board.clean(MARIOPRESENT, MARIOPREV)
        MARIOPREV = ["-", "-", "-", "-", "-", "-", "-", "-"]
        os.system('clear')
        print("START AGAIN")
        time.sleep(1)
        MARIOPRESENT = [33, 7]
        i = 0
        BULLET = 0
        os.system('clear')
        os.system('aplay ./sounds/background.wav&')
        printobj = [i, MARIOPRESENT[1], LIFE, SCORE, BULLET]
        self.__board.printboard(printobj)


    def rivercheck(self):
        """
        to check if fallen in river or not
        """
        global LIFE
        c_2 = checkrv(self.__board.getgrid(
            MARIOPRESENT[0]+3, MARIOPRESENT[1]-1), \
            self.__board.getgrid(MARIOPRESENT[0]+3, MARIOPRESENT[1]+1))

        LIFE += c_2
        self.__board.updatemario(MARIOPRESENT[0], MARIOPRESENT[1])
        os.system('clear')
        printobj = [i, MARIOPRESENT[1], LIFE, SCORE, BULLET]
        self.__board.printboard(printobj)

        # if falls in river
        if c_2 == -1:
            os.system('pkill -kill aplay')
            os.system('aplay ./sounds/smb_mariodie.wav')
            SCREEN.reset(self)

    def movef(self, speed):
        """
        to help mario move forward
        """
        global MARIOPRESENT, MARIOPREV
        self.__board.updateboardf(MARIOPRESENT, MARIOPREV)

        # updating prev array (writing forward bacause early depends on late)
        MARIOPREV[0] = self.__board.getgrid(MARIOPRESENT[0], MARIOPRESENT[1]+2)
        MARIOPREV[1] = MARIOPREV[3]
        MARIOPREV[2] = MARIOPREV[4]
        MARIOPREV[3] = MARIOPREV[5]
        MARIOPREV[4] = self.__board.getgrid(
            MARIOPRESENT[0]+1, MARIOPRESENT[1]+3)
        MARIOPREV[5] = self.__board.getgrid(
            MARIOPRESENT[0]+1, MARIOPRESENT[1]+4)
        MARIOPREV[6] = MARIOPREV[7]
        MARIOPREV[7] = self.__board.getgrid(
            MARIOPRESENT[0]+2, MARIOPRESENT[1]+3)

        # updating mario
        MARIOPRESENT = [MARIOPRESENT[0], MARIOPRESENT[1]+speed]

    def moveb(self, speed):
        """
        to help mario move backward
        """
        global MARIOPRESENT, MARIOPREV
        self.__board.updateboardb(MARIOPRESENT, MARIOPREV)

        # updating prev array (writing backward because later depends on early)
        MARIOPREV[7] = MARIOPREV[6]
        MARIOPREV[6] = self.__board.getgrid(
            MARIOPRESENT[0]+2, MARIOPRESENT[1]-3)
        MARIOPREV[5] = MARIOPREV[3]
        MARIOPREV[4] = MARIOPREV[2]
        MARIOPREV[3] = MARIOPREV[1]
        MARIOPREV[2] = self.__board.getgrid(
            MARIOPRESENT[0]+1, MARIOPRESENT[1]-3)
        MARIOPREV[1] = self.__board.getgrid(
            MARIOPRESENT[0]+1, MARIOPRESENT[1]-4)
        MARIOPREV[0] = self.__board.getgrid(MARIOPRESENT[0], MARIOPRESENT[1]-2)

        # updating mario
        MARIOPRESENT = [MARIOPRESENT[0], MARIOPRESENT[1]-speed]

    def updprevjmp(self, constant):
        """
        update MARIOPREV when jumping
        """
        MARIOPREV[0] = self.__board.getgrid(
            MARIOPRESENT[0]-2+constant, MARIOPRESENT[1])
        MARIOPREV[1] = self.__board.getgrid(
            MARIOPRESENT[0]-1+constant, MARIOPRESENT[1]-2)
        MARIOPREV[2] = self.__board.getgrid(
            MARIOPRESENT[0]-1+constant, MARIOPRESENT[1]-1)
        MARIOPREV[3] = self.__board.getgrid(
            MARIOPRESENT[0]-1+constant, MARIOPRESENT[1])
        MARIOPREV[4] = self.__board.getgrid(
            MARIOPRESENT[0]-1+constant, MARIOPRESENT[1]+1)
        MARIOPREV[5] = self.__board.getgrid(
            MARIOPRESENT[0]-1+constant, MARIOPRESENT[1]+2)
        MARIOPREV[6] = self.__board.getgrid(
            MARIOPRESENT[0]+constant, MARIOPRESENT[1]-1)
        MARIOPREV[7] = self.__board.getgrid(
            MARIOPRESENT[0]+constant, MARIOPRESENT[1]+1)


    def run(self):
        """
        main function
        """
        # initial values
        printobj = [0, 7, 3, 0, 0]
        self.__board.printboard(printobj)

        speed = 2  # do not change
        previnp = "s"  # for jumping

        try:
            tty.setcbreak(sys.stdin.fileno())
            while 1:

                global MARIOPRESENT, MARIOPREV, LIFE, SCORE, BASETIME,\
                 CJUMP, BULLET, E1_ARR, E2_ARR, i, LOOP, LOOP2, BA

                # if won
                if MARIOPRESENT == [33, 609]:
                    os.system('pkill -kill aplay')
                    os.system('aplay ./sounds/smb_stage_clear.wav')
                    # spawn fireworks
                    for f_i in range(580, 650, 10):
                        self.__board.addfireworks(10, f_i)
                        os.system('clear')
                        printobj = [i, MARIOPRESENT[1], LIFE, SCORE, BULLET]
                        self.__board.printboard(printobj)
                        os.system('aplay ./sounds/smb_fireworks.wav')

                    time.sleep(2)
                    os.system('clear')
                    print("SCORE->", SCORE)
                    time.sleep(1)
                    print("LIFE_SCORE->", LIFE*100)
                    time.sleep(1)
                    time_score = 0
                    if (time.time()-BASETIME) <= 100:
                        time_score = 100
                    if (time.time()-BASETIME) <= 150:
                        time_score = 50
                    print("time_score->", time_score)
                    time.sleep(1)
                    print("TOTAL SCORE->", SCORE+LIFE*100+time_score)
                    time.sleep(1)
                    print("YOU WON")
                    time.sleep(1)
                    break
                    # game ends

                # check on jump
                low = 1

# ------------------------------key_stroke dependent----------------------------------

                if is_data():
                    # read input key_stroke from user
                    key_stroke = sys.stdin.read(1)

                    # for bullets
                    if key_stroke == "f" and BULLET == 1:
                        os.system('aplay ./sounds/smb_fireball.wav&')

                        # checking directions
                        direction = 1  # if no previnp
                        if previnp == "d":
                            direction = 1
                        elif previnp == "a":
                            direction = -1

                        # range of BULLET
                        for b_i in range(0, 11*direction, direction):
                            g_i = self.__board.getgrid(
                                MARIOPRESENT[0]+1, \
                                MARIOPRESENT[1]+3*direction+b_i)  # storing next cell
                            self.__board.updatecell(
                                MARIOPRESENT[0]+1, MARIOPRESENT[1]+3*direction+b_i, "+")
                            os.system('clear')
                            printobj = [i, MARIOPRESENT[1],
                                        LIFE, SCORE, BULLET]
                            self.__board.printboard(printobj)
                            self.__board.updatecell(
                                MARIOPRESENT[0]+1, MARIOPRESENT[1]+3*direction+b_i, g_i)
                            time.sleep(.03)
                            os.system('clear')
                            printobj = [i, MARIOPRESENT[1],
                                        LIFE, SCORE, BULLET]
                            self.__board.printboard(printobj)

                            # check if enemy dead or not
                            if self.__board.getgrid(MARIOPRESENT[0]+1, \
                            MARIOPRESENT[1]+3*direction+b_i+direction) == "Q":
                                # ENEMY2 cannot be killed
                                if self.__board.getgrid(MARIOPRESENT[0]+1, \
                                MARIOPRESENT[1]+3*direction+b_i+2*direction) != "Q":
                                    self.__board.cleane1a(
                                        MARIOPRESENT[1]+3*direction+b_i+direction,\
                                     ENEMY1[E1_ARR.index(
                                         MARIOPRESENT[1]+3*direction+b_i+direction), :])  # vanish
                                    os.system('aplay ./sounds/smb_kick.wav&')
                                    # send back
                                    E1_ARR.remove(
                                        MARIOPRESENT[1]+3*direction+b_i+direction)
                                SCORE += 10

                            # check if BULLET can move forward
                            if checkj(self.__board.getgrid(MARIOPRESENT[0]+1, \
                            MARIOPRESENT[1]+3*direction+b_i+direction), \
                            self.__board.getgrid(MARIOPRESENT[0]+1, \
                            MARIOPRESENT[1]+3*direction+b_i+direction)) == -1:
                                break

                    # moving forward
                    if key_stroke == "d" and MARIOPRESENT[1] < (i+100-6):

                        # check obstacle
                        c_1 = checkmv(self.__board.getgrid(
                            MARIOPRESENT[0]+1, MARIOPRESENT[1]+4))
                        if c_1:
                            SCREEN.movef(self, speed)
                            # check river
                            SCREEN.rivercheck(self)
                            previnp = "d"

                    # moving backward
                    if key_stroke == "a" and MARIOPRESENT[1] > i+6:

                        # checking obstacles
                        c_1 = checkmv(self.__board.getgrid(
                            MARIOPRESENT[0]+1, MARIOPRESENT[1]-4))
                        if c_1:
                            SCREEN.moveb(self, speed)
                            # river check
                            SCREEN.rivercheck(self)
                            previnp = "a"

                    # jumps to height +10
                    if key_stroke == "w":
                        os.system('aplay ./sounds/smb_jump-super.wav&')

                        # moving up
                        timer = 5
                        while timer != 0:
                            time.sleep(.01)

                            # checks if can move up
                            c_3 = checkj(self.__board.getgrid(
                                MARIOPRESENT[0]-2, MARIOPRESENT[1]+1), \
                                self.__board.getgrid(MARIOPRESENT[0]-2, MARIOPRESENT[1]-1))
                            if c_3 == -1:
                                djump = 0
                                break
                            else:
                                djump = 1

                            self.__board.updateboardbjump(
                                MARIOPRESENT, MARIOPREV)

                            # updating prev array
                            SCREEN.updprevjmp(self, 0)  # constant=0 for upjump

                            MARIOPRESENT = [
                                MARIOPRESENT[0]-speed, MARIOPRESENT[1]]
                            self.__board.updatemario(
                                MARIOPRESENT[0], MARIOPRESENT[1])
                            timer -= 1
                            os.system('clear')
                            printobj = [i, MARIOPRESENT[1],
                                        LIFE, SCORE, BULLET]
                            self.__board.printboard(printobj)

                        # moving right
                        if previnp == "d" and (MARIOPRESENT[1]+14) < (i+100):

                            # 16 units to right
                            timer = 8
                            while timer != 0:
                                time.sleep(.01)
                                c_1 = checkmv(self.__board.getgrid(
                                    MARIOPRESENT[0]+1, MARIOPRESENT[1]+4))
                                if c_1:
                                    SCREEN.movef(self, speed)
                                    self.__board.updatemario(
                                        MARIOPRESENT[0], MARIOPRESENT[1])
                                    timer -= 1
                                    os.system('clear')
                                    printobj = [i, MARIOPRESENT[1],
                                                LIFE, SCORE, BULLET]
                                    self.__board.printboard(printobj)
                                else:
                                    break

                        # moving left
                        if previnp == "a" and (MARIOPRESENT[1]-14) > (i+6):

                            # 16 units to left
                            timer = 8
                            while timer != 0:
                                time.sleep(.01)
                                c_1 = checkmv(self.__board.getgrid(
                                    MARIOPRESENT[0]+1, MARIOPRESENT[1]-4))
                                if c_1:
                                    SCREEN.moveb(self, speed)
                                    self.__board.updatemario(
                                        MARIOPRESENT[0], MARIOPRESENT[1])

                                    timer -= 1
                                    os.system('clear')
                                    printobj = [i, MARIOPRESENT[1],
                                                LIFE, SCORE, BULLET]
                                    self.__board.printboard(printobj)
                                else:
                                    break

                        # moving down
                        timer = 5
                        while(timer != 0 and djump == 1):

                            # check if it can move down
                            c_3 = checkj(self.__board.getgrid(
                                MARIOPRESENT[0]+3, MARIOPRESENT[1]+1), \
                                self.__board.getgrid(MARIOPRESENT[0]+3, \
                                MARIOPRESENT[1]-1))
                            if c_3 == -1:
                                break

                            # surprise coins
                            if MARIOPRESENT[1] == 75 and MARIOPRESENT[0] == 23 and CJUMP > 0:
                                CJUMP -= 1
                                self.__board.jumpupc(24, 75)
                                os.system('clear')
                                printobj = [i, MARIOPRESENT[1],
                                            LIFE, SCORE, BULLET]
                                self.__board.printboard(printobj)
                                time.sleep(.2)
                                self.__board.updatecell(21, 75, "-")
                                self.__board.updatecell(22, 75, "O")
                                SCORE += 1

                            time.sleep(.06)
                            self.__board.updateboardbjump(
                                MARIOPRESENT, MARIOPREV)
                            # updating pre array
                            # constant=4 for downjump
                            SCREEN.updprevjmp(self, 4)

                            MARIOPRESENT = [
                                MARIOPRESENT[0]+speed, MARIOPRESENT[1]]
                            self.__board.updatemario(
                                MARIOPRESENT[0], MARIOPRESENT[1])
                            timer -= 1
                            os.system('clear')
                            printobj = [i, MARIOPRESENT[1],
                                        LIFE, SCORE, BULLET]
                            self.__board.printboard(printobj)

                        previnp = "w"

                    if key_stroke == "q":
                        os.system('pkill -kill aplay')
                        break
                    # for straight jump
                    if key_stroke not in ["a", "w", "d", "q", "f"]:
                        previnp = "s"

# --------------------------------------------------------------------------------------

# ---------------------------key_stroke independent process------------------------------

                # if already climbed an object check to move it down
                # whenever normal jump not there this code will be executed
                while low:

                    # check for end flag
                    if self.__board.getgrid(MARIOPRESENT[0]+3, MARIOPRESENT[1]-1) == "M" and \
                    self.__board.getgrid(MARIOPRESENT[0]+3, MARIOPRESENT[1]+1) == "M" \
                    and MARIOPRESENT[0] < 25:
                        os.system('aplay ./sounds/smb_flagpole.wav&')
                        flag_index = 20
                        while flag_index != 33:
                            self.__board.moveflag(flag_index)
                            flag_index += 1
                            time.sleep(.03)
                            os.system('clear')
                            printobj = [i, MARIOPRESENT[1],
                                        LIFE, SCORE, BULLET]
                            self.__board.printboard(printobj)

                    # to move down
                    temp = ["-", "/"]
                    if self.__board.getgrid(MARIOPRESENT[0]+3, MARIOPRESENT[1]-1) in temp and \
                    self.__board.getgrid(MARIOPRESENT[0]+3, \
                    MARIOPRESENT[1]+1) in temp and \
                    self.__board.getgrid(MARIOPRESENT[0]+3, MARIOPRESENT[1]) in temp:

                        # check for BULLET power up
                        if MARIOPRESENT[0] == 29 and MARIOPRESENT[1] in BA:
                            os.system('aplay ./sounds/smb_vine.wav&')
                            self.__board.addflower(25, MARIOPRESENT[1])
                            BA.remove(MARIOPRESENT[1])

                        # coins
                        if self.__board.getgrid(MARIOPRESENT[0]-1, MARIOPRESENT[1]) == "O":
                            temp_score = SCORE
                            SCORE += self.__board.jumpupc(
                                MARIOPRESENT[0]-1, MARIOPRESENT[1])
                            # powerup check
                            p_u = 0
                            if SCORE-temp_score == 11:
                                p_u = 1
                            # time.sleep(0.1)
                            os.system('clear')
                            printobj = [i, MARIOPRESENT[1],
                                        LIFE, SCORE, BULLET]
                            self.__board.printboard(printobj)
                            time.sleep(0.1)
                            self.__board.jumpdownc(
                                MARIOPRESENT[0]-1, MARIOPRESENT[1])
                            if p_u == 1:
                                self.__board.updatecell(
                                    MARIOPRESENT[0]-1-3, MARIOPRESENT[1], "P")
                            # time.sleep(0.1)
                            os.system('clear')
                            printobj = [i, MARIOPRESENT[1],
                                        LIFE, SCORE, BULLET]
                            self.__board.printboard(printobj)


                        low = 1
                        time.sleep(.06)
                        self.__board.updateboardbjump(MARIOPRESENT, MARIOPREV)
                        # updating pre array
                        SCREEN.updprevjmp(self, 4)

                        MARIOPRESENT = [MARIOPRESENT[0]+speed, MARIOPRESENT[1]]
                        self.__board.updatemario(
                            MARIOPRESENT[0], MARIOPRESENT[1])
                        printobj = [i, MARIOPRESENT[1], LIFE, SCORE, BULLET]
                        self.__board.printboard(printobj)

                    # kill enemy by jumping
                    elif self.__board.getgrid(MARIOPRESENT[0]+3, MARIOPRESENT[1]-1) == "Q" or \
                    self.__board.getgrid(MARIOPRESENT[0]+3, MARIOPRESENT[1]+1) == "Q" or \
                    self.__board.getgrid(MARIOPRESENT[0]+3, MARIOPRESENT[1]) == "Q":
                        low = 1
                        # print("EFEFEF")
                        SCORE += 20
                        if self.__board.getgrid(MARIOPRESENT[0]+3, MARIOPRESENT[1]-1) == "Q":
                            # ENEMY2 check
                            if self.__board.getgrid(MARIOPRESENT[0]+3,\
                             MARIOPRESENT[1]-2) != "Q" and \
                            self.__board.getgrid(MARIOPRESENT[0]+3, MARIOPRESENT[1]) != "Q":
                                os.system('aplay ./sounds/smb_stomp.wav&')
                                self.__board.cleane1a(
                                    MARIOPRESENT[1]-1, ENEMY1[E1_ARR.index(MARIOPRESENT[1]-1), :])
                                # E1_ARR[E1_ARR.index(MARIOPRESENT[1]-1)]=-1#send back
                                E1_ARR.remove(MARIOPRESENT[1]-1)  # send back
                            # if ENEMY2 then dead
                            else:
                                LIFE -= 1
                                os.system('pkill -kill aplay')
                                os.system('aplay ./sounds/smb_mariodie.wav')
                                SCREEN.reset(self)

                        elif self.__board.getgrid(MARIOPRESENT[0]+3, MARIOPRESENT[1]+1) == "Q":
                            if self.__board.getgrid(MARIOPRESENT[0]+3, \
                            MARIOPRESENT[1]+2) != "Q" and \
                            self.__board.getgrid(MARIOPRESENT[0]+3, MARIOPRESENT[1]) != "Q":
                                os.system('aplay ./sounds/smb_stomp.wav&')
                                self.__board.cleane1a(
                                    MARIOPRESENT[1]+1, ENEMY1[E1_ARR.index(MARIOPRESENT[1]+1), :])
                                # E1_ARR[E1_ARR.index(MARIOPRESENT[1]+1)]=-1#send back
                                E1_ARR.remove(MARIOPRESENT[1]+1)  # send back
                            # if ENEMY2 then dead
                            else:
                                LIFE -= 1
                                os.system('pkill -kill aplay')
                                os.system('aplay ./sounds/smb_mariodie.wav')
                                SCREEN.reset(self)

                        else:
                            if self.__board.getgrid(MARIOPRESENT[0]+3, MARIOPRESENT[1]+1) != "Q" \
                            and self.__board.getgrid(MARIOPRESENT[0]+3, MARIOPRESENT[1]-1) != "Q":
                                os.system('aplay ./sounds/smb_stomp.wav&')
                                self.__board.cleane1a(
                                    MARIOPRESENT[1], ENEMY1[E1_ARR.index(MARIOPRESENT[1]), :])
                                # E1_ARR[E1_ARR.index(MARIOPRESENT[1])]=-1#send back
                                E1_ARR.remove(MARIOPRESENT[1])  # send back
                            # if ENEMY2 then dead
                            else:
                                LIFE -= 1
                                os.system('pkill -kill aplay')
                                os.system('aplay ./sounds/smb_mariodie.wav')
                                SCREEN.reset(self)

                    else:
                        low = 0
                        c_2 = checkrv(self.__board.getgrid(
                            MARIOPRESENT[0]+3, MARIOPRESENT[1]-1), \
                            self.__board.getgrid(MARIOPRESENT[0]+3, MARIOPRESENT[1]+1))
                        LIFE += c_2
                        if c_2 == -1:
                            os.system('pkill -kill aplay')
                            os.system('aplay ./sounds/smb_mariodie.wav')
                            SCREEN.reset(self)

                if 1:

                    # FOR SCREEN
                    # position of mario at which screen moves
                    if MARIOPRESENT[1] > (i+50):
                        i += 20
                        # time.sleep(0.03)
                        os.system('clear')
                        printobj = [i, MARIOPRESENT[1], LIFE, SCORE, BULLET]
                        self.__board.printboard(printobj)

                    # array of enemies
                    # enemies completely governed by these arrays
                    E1_ARR, E2_ARR = self.__board.searchenemy(i)

                    # check for powerups
                    if self.__board.getgrid(MARIOPRESENT[0]+2, MARIOPRESENT[1]) == "P":
                        os.system('aplay ./sounds/smb_1-up.wav&')
                        LIFE += 1
                        self.__board.updatecell(
                            MARIOPRESENT[0]+2, MARIOPRESENT[1], "-")

                    # check for flower
                    if MARIOPREV[3] == 'I':
                        os.system('aplay ./sounds/smb_powerup.wav&')
                        MARIOPREV[3] = "-"
                        BULLET = 1

                    # speed increase as mario progresses
                    if MARIOPRESENT[1] > 350:
                        check = .7
                    else:
                        check = 1

                    if time.time()-LOOP > check:
                        LOOP = time.time()
                        # FOR ENEMY1
                        if E1_ARR and i+100 > E1_ARR[len(E1_ARR)-1] > i:
                            for count in range(len(E1_ARR)):
                                if MARIOPRESENT[1] < E1_ARR[count]:
                                    c_1 = checkmv(self.__board.getgrid(
                                        35, E1_ARR[count]-3))
                                    if c_1:
                                        self.__board.updateenemy1b(
                                            E1_ARR[count], ENEMY1[count, :].decode())
                                        # updating prev array
                                        ENEMY1[count, 3] = ENEMY1[count, 1]
                                        ENEMY1[count, 2] = self.__board.getgrid(
                                            35, E1_ARR[count]-2)
                                        ENEMY1[count, 1] = self.__board.getgrid(
                                            35, E1_ARR[count]-3)
                                        ENEMY1[count, 0] = self.__board.getgrid(
                                            34, E1_ARR[count]-2)
                                        E1_ARR[count] -= 2
                                        self.__board.updateenemy1(
                                            34, E1_ARR[count])
                                else:
                                    c_1 = checkmv(self.__board.getgrid(
                                        35, E1_ARR[count]+3))
                                    if c_1:
                                        self.__board.updateenemy1f(
                                            E1_ARR[count], ENEMY1[count, :].decode())
                                        # updating prev array
                                        ENEMY1[count, 0] = self.__board.getgrid(
                                            34, E1_ARR[count]+2)
                                        ENEMY1[count, 1] = ENEMY1[count, 3]
                                        ENEMY1[count, 2] = self.__board.getgrid(
                                            35, E1_ARR[count]+2)
                                        ENEMY1[count, 3] = self.__board.getgrid(
                                            35, E1_ARR[count]+3)
                                        E1_ARR[count] += 2
                                        self.__board.updateenemy1(
                                            34, E1_ARR[count])
                            time.sleep(0.03)
                            os.system('clear')
                            printobj = [i, MARIOPRESENT[1],
                                        LIFE, SCORE, BULLET]
                            self.__board.printboard(printobj)

                    if time.time()-LOOP2 > check-0.5:
                        LOOP2 = time.time()
                        # FOR ENEMY2
                        if E2_ARR and i+100 > E2_ARR[len(E2_ARR)-1] > i:
                            for count in range(len(E2_ARR)):
                                c_1 = checkmv(self.__board.getgrid(
                                    35, E2_ARR[count]-2))
                                if c_1:
                                    self.__board.updateenemy2b(
                                        E2_ARR[count], ENEMY2[count, :].decode())

                                    # updating prev array
                                    ENEMY2[count, 4] = ENEMY2[count, 2]
                                    ENEMY2[count, 3] = self.__board.getgrid(
                                        35, E2_ARR[count])
                                    ENEMY2[count, 2] = self.__board.getgrid(
                                        35, E2_ARR[count]-1)
                                    ENEMY2[count, 1] = self.__board.getgrid(
                                        34, E2_ARR[count]-1)
                                    ENEMY2[count, 0] = self.__board.getgrid(
                                        34, E2_ARR[count]-2)
                                    E2_ARR[count] -= 2
                                    self.__board.updateenemy2(34, E2_ARR[count])
                            # faster
                            time.sleep(0.01)
                            os.system('clear')
                            printobj = [i, MARIOPRESENT[1],
                                        LIFE, SCORE, BULLET]
                            self.__board.printboard(printobj)

                    # dead if in contact with enemy
                    if MARIOPREV[6] == "x" or MARIOPREV[7] == "x" or \
                    self.__board.getgrid(MARIOPRESENT[0]+1, MARIOPRESENT[1]) == "Q":
                        # not updating enemy prev so it shows dead location
                        LIFE -= 1
                        os.system('pkill -kill aplay')
                        os.system('aplay ./sounds/smb_mariodie.wav')
                        SCREEN.reset(self)

                    # if all lives used up
                    if LIFE <= 0:
                        os.system('clear')
                        os.system('pkill -kill aplay')
                        print("GAME OVER   ALL LIVES USED")
                        os.system('aplay ./sounds/smb_gameover.wav')
                        break

# ----------------------------------------------------------------------------------------

        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, OLD)


# running program
if __name__ == "__main__":

    X = START()
    X.run()
    if QUITVAR == 0:
        os.system('aplay ./sounds/background.wav&')
        X = SCREEN()
        X.run()
