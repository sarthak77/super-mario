#main code of the game
from start import *
from mainscene import *
from func import *
import time
import sys
import select
import tty
import termios

#GLABAL VARIABLES
quit=1
mariopresent=[33,7]
marioprev=["-","-","-","-","-","-","-","-"]# 8 elements
life=3
score=0#coins
a=time.time()
cjump=10#for surprise coin
bullet=0
x=[]
y=[]
#to control enemy loop
loop=0
loop2=0
#9 enemies
enemy1=np.chararray((5,4))
enemy1[:]="-"
enemy2=np.chararray((4,5))
enemy2[:]="-"

old_settings = termios.tcgetattr(sys.stdin)

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [],[])

#--------------take input without pressing enter-----------------------------

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()

class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()

getch = _Getch()

#------------------------------------------------------------------------------

#--------------------------start screen---------------------------------------

class start(object):
    def __init__(self):
        #making object
        self.__board=start_board()

    #main function
    def run(self):
        self.__board.printboard()
        
        while(1):
            print()
            print("                       --------------------------------------------------------")
            print("                      |PRESS s TO GO DOWN---PRESS w TO GO UP---PRESS f TO ENTER|")
            print("                       --------------------------------------------------------")
            print()
            inp=getch()
            
            if inp=="s":
                self.__board.update(23,41,'-')
                self.__board.update(25,41,'>')
            
            if inp=="f":
                if self.__board.getgrid(23,41)==">":
                    os.system('clear')
                    print("                                          STARTING GAME IN 3s")
                    #time.sleep(3)
                    global quit
                    quit=0
                break
                
            if inp=="w":
                self.__board.update(25,41,'-')
                self.__board.update(23,41,'>')
                #self.__board.printboard()

            self.__board.printboard()

#---------------------------------------------------------------------------------

#------------------------------game scene class-----------------------------------

class screen(object):
    def __init__(self):
        #creating object
        self.__board=mainscene_board()

    #main function
    def run(self):
        #initial values
        self.__board.printboard(0,7,3,0,0)

        i=0#screen
        speed=2#do not change
        previnp="q"#for jumping

    
        try:
            tty.setcbreak(sys.stdin.fileno())
            while(1):

                global mariopresent
                global marioprev
                global life
                global score
                global a
                global cjump
                global bullet
                global x
                global y
                global loop
                global loop2

                #if won
                if mariopresent==[33,609]:
                    #spawn fireworks 
                    for f in range(580,650,10):
                        self.__board.addfireworks(10,f)
                        self.__board.printboard(i,mariopresent[1],life,score,bullet)
                        #print(f)
                        time.sleep(.5)

                    time.sleep(2)
                    os.system('clear')
                    print("SCORE->",score)
                    time.sleep(1)
                    print("LIFE_SCORE->",life*100)
                    time.sleep(1)
                    timescore=0
                    if (time.time()-a)<=100:
                        timescore=100
                    if (time.time()-a)<=150:
                        timescore=50
                    print("TIME_SCORE->",timescore)
                    time.sleep(1)
                    print("TOTAL SCORE->",score+life*100+timescore)
                    time.sleep(1)
                    print("YOU WON")
                    time.sleep(1)
                    break
                    #game ends

                #check on jump
                low=1

#------------------------------keystroke dependent----------------------------------

                if isData():
                    # read input keystroke from user
                    keyStroke = sys.stdin.read(1)

                    #for bullets
                    if keyStroke=="f" and bullet==1:

                        #checking directions
                        direction=1#if no previnp
                        if previnp=="d":
                            direction=1
                        elif previnp=="a":
                            direction=-1
                        
                        #range of bullet
                        for b in range(0,11*direction,direction):
                            g=self.__board.getgrid(mariopresent[0]+1,mariopresent[1]+3*direction+b)#storing next cell
                            self.__board.fire1(mariopresent[0]+1,mariopresent[1]+3*direction+b)
                            #os.system('clear')
                            self.__board.printboard(i,mariopresent[1],life,score,bullet)
                            self.__board.fire2(mariopresent[0]+1,mariopresent[1]+3*direction+b,g)
                            time.sleep(.03)
                            #os.system('clear')
                            self.__board.printboard(i,mariopresent[1],life,score,bullet)

                            #check if enemy dead or not
                            if self.__board.getgrid(mariopresent[0]+1,mariopresent[1]+3*direction+b+direction)=="Q":
                                if self.__board.getgrid(mariopresent[0]+1,mariopresent[1]+3*direction+b+2*direction)!="Q":#enemy2 cannot be killed
                                    self.__board.cleane1a(mariopresent[1]+3*direction+b+direction,enemy1[x.index(mariopresent[1]+3*direction+b+direction),:])#vanish
                                    x[x.index(mariopresent[1]+3*direction+b+direction)]=-1#send back
                                score+=20

                            #check if bullet can move forward
                            if checkj(self.__board.getgrid(mariopresent[0]+1,mariopresent[1]+3*direction+b+direction),self.__board.getgrid(mariopresent[0]+1,mariopresent[1]+3*direction+b+direction))==-1:
                                break
                       


                    #moving forward
                    if keyStroke=="d" and mariopresent[1]<(i+100-6):

                        #check obstacle
                        c1=checkmv(self.__board.getgrid(mariopresent[0]+1,mariopresent[1]+4))
                        if c1:
                            self.__board.updateboardf(mariopresent,marioprev)
                           
                            #updating prev array (writing forward bacause early depends on late)
                            marioprev[0]=self.__board.getgrid(mariopresent[0],mariopresent[1]+2)
                            marioprev[1]=marioprev[3]
                            marioprev[2]=marioprev[4]
                            marioprev[3]=marioprev[5]
                            marioprev[4]=self.__board.getgrid(mariopresent[0]+1,mariopresent[1]+3)
                            marioprev[5]=self.__board.getgrid(mariopresent[0]+1,mariopresent[1]+4)
                            marioprev[6]=marioprev[7]
                            marioprev[7]=self.__board.getgrid(mariopresent[0]+2,mariopresent[1]+3)

                            #updating mario
                            mariopresent=[mariopresent[0],mariopresent[1]+speed]

                            #check river
                            c2=checkrv(self.__board.getgrid(mariopresent[0]+3,mariopresent[1]-1),self.__board.getgrid(mariopresent[0]+3,mariopresent[1]+1))
                            
                            life+=c2
                            self.__board.updatemario(mariopresent[0],mariopresent[1])
                            previnp="d"
                            self.__board.printboard(i,mariopresent[1],life,score,bullet)

                            #if falls in river
                            if c2==-1:
                                self.__board.clean(mariopresent,marioprev)
                                marioprev=["-","-","-","-","-","-","-","-"]
                                os.system('clear')
                                print("START AGAIN")
                                time.sleep(1)
                                mariopresent=[33,7]
                                i=0
                                self.__board.printboard(i,mariopresent[1],life,score,bullet)



                    #moving backward
                    if keyStroke=="a" and mariopresent[1]>i+6:

                        #checking obstacles
                        c1=checkmv(self.__board.getgrid(mariopresent[0]+1,mariopresent[1]-4))
                        if c1:
                            self.__board.updateboardb(mariopresent,marioprev)

                            #updating prev array (writing backward because later depends on early)
                            marioprev[7]=marioprev[6]
                            marioprev[6]=self.__board.getgrid(mariopresent[0]+2,mariopresent[1]-3)
                            marioprev[5]=marioprev[3]
                            marioprev[4]=marioprev[2]
                            marioprev[3]=marioprev[1]
                            marioprev[2]=self.__board.getgrid(mariopresent[0]+1,mariopresent[1]-3)
                            marioprev[1]=self.__board.getgrid(mariopresent[0]+1,mariopresent[1]-4)
                            marioprev[0]=self.__board.getgrid(mariopresent[0],mariopresent[1]-2)

                            #updating mario
                            mariopresent=[mariopresent[0],mariopresent[1]-speed]
                            #river check
                            c2=checkrv(self.__board.getgrid(mariopresent[0]+3,mariopresent[1]-1),self.__board.getgrid(mariopresent[0]+3,mariopresent[1]+1))
                            
                            life+=c2
                            self.__board.updatemario(mariopresent[0],mariopresent[1])
                            previnp="a"
                            self.__board.printboard(i,mariopresent[1],life,score,bullet)

                            #if dead
                            if c2==-1:
                                self.__board.clean(mariopresent,marioprev)
                                marioprev=["-","-","-","-","-","-","-","-"]
                                os.system('clear')
                                print("START AGAIN")
                                time.sleep(1)
                                mariopresent=[33,7]
                                i=0
                                self.__board.printboard(i,mariopresent[1],life,score,bullet)



                    #jumps to height +10
                    if keyStroke=="w":

                        #moving up
                        timer=5
                        while(timer!=0):
                            time.sleep(.01)

                            #checks if can move up
                            c3=checkj(self.__board.getgrid(mariopresent[0]-2,mariopresent[1]+1),self.__board.getgrid(mariopresent[0]-2,mariopresent[1]-1))
                            if c3==-1:
                                djump=0
                                break
                            else:
                                djump=1

                            self.__board.updateboardbup(mariopresent,marioprev)

                            #updating prev array
                            marioprev[0]=self.__board.getgrid(mariopresent[0]-2,mariopresent[1])
                            marioprev[1]=self.__board.getgrid(mariopresent[0]-1,mariopresent[1]-2)
                            marioprev[2]=self.__board.getgrid(mariopresent[0]-1,mariopresent[1]-1)
                            marioprev[3]=self.__board.getgrid(mariopresent[0]-1,mariopresent[1])
                            marioprev[4]=self.__board.getgrid(mariopresent[0]-1,mariopresent[1]+1)
                            marioprev[5]=self.__board.getgrid(mariopresent[0]-1,mariopresent[1]+2)
                            marioprev[6]=self.__board.getgrid(mariopresent[0],mariopresent[1]-1)
                            marioprev[7]=self.__board.getgrid(mariopresent[0],mariopresent[1]+1)

                            mariopresent=[mariopresent[0]-speed,mariopresent[1]]
                            self.__board.updatemario(mariopresent[0],mariopresent[1])
                            timer-=1
                            self.__board.printboard(i,mariopresent[1],life,score,bullet)

                        #moving right
                        if previnp=="d" and (mariopresent[1]+14)<(i+100):

                            #4 units to right
                            timer=8
                            while(timer!=0):
                                time.sleep(.01)
                                self.__board.updateboardf(mariopresent,marioprev)

                                #updating prev array (writing forward bacause early depends on late)
                                marioprev[0]=self.__board.getgrid(mariopresent[0],mariopresent[1]+2)
                                marioprev[1]=marioprev[3]
                                marioprev[2]=marioprev[4]
                                marioprev[3]=marioprev[5]
                                marioprev[4]=self.__board.getgrid(mariopresent[0]+1,mariopresent[1]+3)
                                marioprev[5]=self.__board.getgrid(mariopresent[0]+1,mariopresent[1]+4)
                                marioprev[6]=marioprev[7]
                                marioprev[7]=self.__board.getgrid(mariopresent[0]+2,mariopresent[1]+3)

                                mariopresent=[mariopresent[0],mariopresent[1]+speed]
                                self.__board.updatemario(mariopresent[0],mariopresent[1])
                                timer-=1
                                self.__board.printboard(i,mariopresent[1],life,score,bullet)

                        #moving left
                        if previnp=="a" and (mariopresent[1]-14)>(i+6):

                            #4 units to left
                            timer=8
                            while(timer!=0):
                                time.sleep(.01)
                                self.__board.updateboardb(mariopresent,marioprev)

                                #updating prev array (writing backward because later depends on early)
                                marioprev[7]=marioprev[6]
                                marioprev[6]=self.__board.getgrid(mariopresent[0]+2,mariopresent[1]-3)
                                marioprev[5]=marioprev[3]
                                marioprev[4]=marioprev[2]
                                marioprev[3]=marioprev[1]
                                marioprev[2]=self.__board.getgrid(mariopresent[0]+1,mariopresent[1]-3)
                                marioprev[1]=self.__board.getgrid(mariopresent[0]+1,mariopresent[1]-4)
                                marioprev[0]=self.__board.getgrid(mariopresent[0],mariopresent[1]-2)

                                mariopresent=[mariopresent[0],mariopresent[1]-speed]
                                self.__board.updatemario(mariopresent[0],mariopresent[1])

                                timer-=1
                                self.__board.printboard(i,mariopresent[1],life,score,bullet)

                        #moving down
                        timer=5
                        while(timer!=0 and djump==1):

                            #check if it can move down
                            c3=checkj(self.__board.getgrid(mariopresent[0]+3,mariopresent[1]+1),self.__board.getgrid(mariopresent[0]+3,mariopresent[1]-1))
                            if c3==-1:
                                break 

                            #surprise coins
                            if mariopresent[1]==75 and mariopresent[0]==23 and cjump>0:
                                cjump-=1
                                self.__board.jumpupc(24,75)
                                os.system('clear')
                                self.__board.printboard(i,mariopresent[1],life,score,bullet)
                                time.sleep(.2)
                                self.__board.updatecell(21,75,"-")
                                self.__board.updatecell(22,75,"O")
                                score+=1

                            time.sleep(.06)
                            self.__board.updateboardbdown(mariopresent,marioprev)
                            #updating pre array
                            marioprev[0]=self.__board.getgrid(mariopresent[0]+2,mariopresent[1])
                            marioprev[1]=self.__board.getgrid(mariopresent[0]+3,mariopresent[1]-2)
                            marioprev[2]=self.__board.getgrid(mariopresent[0]+3,mariopresent[1]-1)
                            marioprev[3]=self.__board.getgrid(mariopresent[0]+3,mariopresent[1])
                            marioprev[4]=self.__board.getgrid(mariopresent[0]+3,mariopresent[1]+1)
                            marioprev[5]=self.__board.getgrid(mariopresent[0]+3,mariopresent[1]+2)
                            marioprev[6]=self.__board.getgrid(mariopresent[0]+4,mariopresent[1]-1)
                            marioprev[7]=self.__board.getgrid(mariopresent[0]+4,mariopresent[1]+1)
                        
                            mariopresent=[mariopresent[0]+speed,mariopresent[1]]
                            self.__board.updatemario(mariopresent[0],mariopresent[1])
                            timer-=1
                            self.__board.printboard(i,mariopresent[1],life,score,bullet)

                        previnp="w"

                    #for straight jump
                    if keyStroke not in ["a","w","d"]:
                        previnp="q"

#--------------------------------------------------------------------------------------

#---------------------------keystroke independent process------------------------------

                #if already climbed an object check to move it down
                #whenever normal jump not there this code will be executed
                while low:

                    #check for end flag
                    if self.__board.getgrid(mariopresent[0]+3,mariopresent[1]-1)=="M" and self.__board.getgrid(mariopresent[0]+3,mariopresent[1]+1)=="M" and mariopresent[0]<25:
                        fi=20
                        while(fi!=33):
                            self.__board.moveflag(fi)
                            fi+=1
                            time.sleep(.03)
                            os.system('clear')
                            self.__board.printboard(i,mariopresent[1],life,score,bullet)
                    
                    #to move down
                    temp=["-","/"]
                    if self.__board.getgrid(mariopresent[0]+3,mariopresent[1]-1) in temp and self.__board.getgrid(mariopresent[0]+3,mariopresent[1]+1) in temp:

                        #check for bullet power up
                        if mariopresent[0]==29 and mariopresent[1] in [51,215,216,217,218,219]:
                            self.__board.addflower(25,mariopresent[1])
                       
                        #coins
                        if self.__board.getgrid(mariopresent[0]-1,mariopresent[1])=="O":
                            score+=self.__board.jumpupc(mariopresent[0]-1,mariopresent[1])
                            #powerup check
                            p=0
                            if self.__board.jumpupc(mariopresent[0]-1,mariopresent[1])==11:
                                p=1
                            #time.sleep(0.1)
                            #os.system('clear')
                            self.__board.printboard(i,mariopresent[1],life,score,bullet)
                            time.sleep(0.1)
                            self.__board.jumpdownc(mariopresent[0]-1,mariopresent[1])
                            if p==1:
                                self.__board.powerup(mariopresent[0]-1,mariopresent[1])
                            #time.sleep(0.1)
                            #os.system('clear')
                            self.__board.printboard(i,mariopresent[1],life,score,bullet)
                       
                        """
                        c3=checkj(self.__board.getgrid(mariopresent[0]+3,mariopresent[1]+1),self.__board.getgrid(mariopresent[0]+3,mariopresent[1]-1))
                        if c3==-1:
                            break 
                        """

                        low=1
                        time.sleep(.06)
                        self.__board.updateboardbdown(mariopresent,marioprev)
                        #updating pre array
                        marioprev[0]=self.__board.getgrid(mariopresent[0]+2,mariopresent[1])
                        marioprev[1]=self.__board.getgrid(mariopresent[0]+3,mariopresent[1]-2)
                        marioprev[2]=self.__board.getgrid(mariopresent[0]+3,mariopresent[1]-1)
                        marioprev[3]=self.__board.getgrid(mariopresent[0]+3,mariopresent[1])
                        marioprev[4]=self.__board.getgrid(mariopresent[0]+3,mariopresent[1]+1)
                        marioprev[5]=self.__board.getgrid(mariopresent[0]+3,mariopresent[1]+2)
                        marioprev[6]=self.__board.getgrid(mariopresent[0]+4,mariopresent[1]-1)
                        marioprev[7]=self.__board.getgrid(mariopresent[0]+4,mariopresent[1]+1)
                                
                        mariopresent=[mariopresent[0]+speed,mariopresent[1]]
                        self.__board.updatemario(mariopresent[0],mariopresent[1])
                        self.__board.printboard(i,mariopresent[1],life,score,bullet)

                    else:
                        low=0
                        c2=checkrv(self.__board.getgrid(mariopresent[0]+3,mariopresent[1]-1),self.__board.getgrid(mariopresent[0]+3,mariopresent[1]+1))
                        life+=c2
                        if c2==-1:
                            self.__board.clean(mariopresent,marioprev)
                            marioprev=["-","-","-","-","-","-","-","-"]
                            os.system('clear')
                            print("START AGAIN")
                            time.sleep(1)
                            mariopresent=[33,7]
                            i=0
                            self.__board.printboard(i,mariopresent[1],life,score,bullet)

                        

                if 1:
                    
                    #FOR SCREEN 
                    if mariopresent[1]>(i+50):#position of mario at which screen moves
                        i+=20
                        #time.sleep(0.03)
                        os.system('clear')
                        self.__board.printboard(i,mariopresent[1],life,score,bullet)
                       
                    #array of enemies 
                    #enemies completely governed by these arrays                   
                    x,y=self.__board.searchenemy(i)


                    #check for powerups
                    if self.__board.getgrid(mariopresent[0]+2,mariopresent[1])=="P":
                        life+=1
                        self.__board.updatecell(mariopresent[0]+2,mariopresent[1],"-")

                    #check for flower
                    if marioprev[3]=='I':
                        bullet=1

                    if time.time()-loop>1:
                        loop=time.time()
                        #FOR ENEMY1                    
                        if len(x)!=0 and i+100>x[len(x)-1]>i:
                            for count in range(len(x)):
                                if mariopresent[1]<x[count]:
                                    c1=checkmv(self.__board.getgrid(35,x[count]-3))
                                    if c1:
                                        self.__board.updateenemy1b(x[count],enemy1[count,:].decode())
                                        #updating prev array
                                        enemy1[count,3]=enemy1[count,1]
                                        enemy1[count,2]=self.__board.getgrid(35,x[count]-2)
                                        enemy1[count,1]=self.__board.getgrid(35,x[count]-3)
                                        enemy1[count,0]=self.__board.getgrid(34,x[count]-2)
                                        x[count]-=2
                                        self.__board.updateenemy1(34,x[count])
                                else:
                                    c1=checkmv(self.__board.getgrid(35,x[count]+3))
                                    if c1:
                                        self.__board.updateenemy1f(x[count],enemy1[count,:].decode())
                                        #updating prev array
                                        enemy1[count,0]=self.__board.getgrid(34,x[count]+2)
                                        enemy1[count,1]=enemy1[count,3]
                                        enemy1[count,2]=self.__board.getgrid(35,x[count]+2)
                                        enemy1[count,3]=self.__board.getgrid(35,x[count]+3)
                                        x[count]+=2
                                        self.__board.updateenemy1(34,x[count])
                            time.sleep(0.03)
                            os.system('clear')
                            self.__board.printboard(i,mariopresent[1],life,score,bullet)
                    
                    if time.time()-loop2>.5:
                        loop2=time.time()
                        #FOR ENEMY2                    
                        if len(y)!=0 and i+100>y[len(y)-1]>i:
                            for count in range(len(y)):
                                c1=checkmv(self.__board.getgrid(35,y[count]-2))
                                if c1:
                                    self.__board.updateenemy2b(y[count],enemy2[count,:].decode())

                                    #updating prev array
                                    enemy2[count,4]=enemy2[count,2]
                                    enemy2[count,3]=self.__board.getgrid(35,y[count])
                                    enemy2[count,2]=self.__board.getgrid(35,y[count]-1)
                                    enemy2[count,1]=self.__board.getgrid(34,y[count]-1)
                                    enemy2[count,0]=self.__board.getgrid(34,y[count]-2)
                                    y[count]-=2
                                    self.__board.updateenemy2(34,y[count])
                            #faster
                            time.sleep(0.01)
                            os.system('clear')
                            self.__board.printboard(i,mariopresent[1],life,score,bullet)

                    #if all lives used up
                    if life<=0:
                        os.system('clear')
                        print("GAME OVER   ALL LIVES USED")
                        break

                    #kill enemy by jumping
                    if self.__board.getgrid(mariopresent[0]+3,mariopresent[1]-1)=="Q" or self.__board.getgrid(mariopresent[0]+3,mariopresent[1]+1)=="Q":
                        score+=10
                        if self.__board.getgrid(mariopresent[0]+3,mariopresent[1]-1)=="Q":
                            if self.__board.getgrid(mariopresent[0]+3,mariopresent[1]-2)!="Q" and self.__board.getgrid(mariopresent[0]+3,mariopresent[1])!="Q":#enemy2 check
                                self.__board.cleane1a(mariopresent[1]-1,enemy1[x.index(mariopresent[1]-1),:])
                            #if enemy2 then dead
                            else:
                                life-=1
                                self.__board.clean(mariopresent,marioprev)
                                clean=[mariopresent,marioprev]
                                marioprev=["-","-","-","-","-","-","-","-"]
                                os.system('clear')
                                print("START AGAIN")
                                time.sleep(1)
                                mariopresent=[33,7]
                                i=0
                                self.__board.printboard(i,mariopresent[1],life,score,bullet)
                                self.__board.clean(clean[0],clean[1])

                        if self.__board.getgrid(mariopresent[0]+3,mariopresent[1]+1)=="Q":
                            if self.__board.getgrid(mariopresent[0]+3,mariopresent[1]+2)!="Q" and self.__board.getgrid(mariopresent[0]+3,mariopresent[1])!="Q":
                                self.__board.cleane1a(mariopresent[1]+1,enemy1[x.index(mariopresent[1]+1),:])
                            #if enemy2 then dead
                            else:
                                life-=1
                                self.__board.clean(mariopresent,marioprev)
                                clean=[mariopresent,marioprev]
                                marioprev=["-","-","-","-","-","-","-","-"]
                                os.system('clear')
                                print("START AGAIN")
                                time.sleep(1)
                                mariopresent=[33,7]
                                i=0
                                self.__board.printboard(i,mariopresent[1],life,score,bullet)
                                self.__board.clean(clean[0],clean[1])

                    #dead if in contact with enemy
                    if marioprev[6]=="x" or marioprev[7]=="x" or self.__board.getgrid(mariopresent[0]+1,mariopresent[1])=="Q" : 
                        life-=1
                        self.__board.clean(mariopresent,marioprev)
                        clean=[mariopresent,marioprev]
                        marioprev=["-","-","-","-","-","-","-","-"]
                        os.system('clear')
                        print("START AGAIN")
                        time.sleep(1)
                        mariopresent=[33,7]
                        i=0
                        self.__board.printboard(i,mariopresent[1],life,score,bullet)
                        self.__board.clean(clean[0],clean[1])

#----------------------------------------------------------------------------------------

        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

#running program
if __name__=="__main__":

    x=start()
    x.run()
    if quit==0:
        x=screen()
        x.run()
