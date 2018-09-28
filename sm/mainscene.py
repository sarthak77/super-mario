#contains game board and functions which effect the board
#and involve any change to the board

import numpy as np
import board
import os,time,sys
import color

#for maintaining timer
from main import a

#to print in a good way
np.set_printoptions(linewidth=1000,threshold=np.nan)

#global variables
a1=[]
a2=[]

class mainscene_board:

    def __init__(self):

        #basic structure
        self.__grid=np.chararray((40,100*10))
        self.__grid[:]="-"
        self.__grid[36:40:1,:]="#"

        #gaps
        #also in moveflag func
        self.__grid[36:40:1,180:190:1]="~"
        self.__grid[36:40:1,485:490:1]="~"

        #clouds
        for i in range(7,600,100):
            self.__grid=board.addcloud(self.__grid,5,i)
        for i in range(60,600,100):
            self.__grid=board.addcloud(self.__grid,7,i)

        #hills
        for i in range(40,600,100):
            self.__grid=board.addhill(self.__grid,28,i)

        #tunnels
        for i in range(100,540,150):
            self.__grid=board.addtunnel(self.__grid,32,i)

        #mario
        self.__grid=board.addmario(self.__grid,33,6)

        #blocks
        for i in range(40,400,57):
            self.__grid=board.addblock(self.__grid,27,i)

        #random blocks

        #type1
        self.__grid=board.addblock(self.__grid,23,230)
        self.__grid=board.addblock(self.__grid,23,240)
        self.__grid=board.addblock(self.__grid,23,290)
        self.__grid=board.addblock(self.__grid,23,300)
        self.__grid=board.addblock(self.__grid,19,520)
        self.__grid=board.addblock(self.__grid,19,530)

        #type2
        self.__grid=board.addsblock(self.__grid,15,233)
        self.__grid=board.addsblock(self.__grid,15,239)
        self.__grid=board.addsblock(self.__grid,15,245)
        self.__grid=board.addsblock(self.__grid,19,159)

        #enemies

        #enemy1 y=even

        self.__grid=board.adde1(self.__grid,35,80)
        self.__grid=board.adde1(self.__grid,35,160)
        self.__grid=board.adde1(self.__grid,35,166)
        self.__grid=board.adde1(self.__grid,35,300)
        self.__grid=board.adde1(self.__grid,35,310)
        self.__grid=board.adde1(self.__grid,35,424)

        #enemy2
        self.__grid=board.adde2(self.__grid,35,220)
        self.__grid=board.adde2(self.__grid,35,390)
        #self.__grid=board.adde2(self.__grid,35,425)
        self.__grid=board.adde2(self.__grid,35,529)


        #random tunnels
        self.__grid=board.addtunnel(self.__grid,32,350)

        #level ender
        self.__grid=board.addler(self.__grid,35,450)
        self.__grid=board.addlel(self.__grid,16,490)

        #flag
        self.__grid=board.addflag(self.__grid,35,550)

        #castle
        self.__grid=board.addcastle(self.__grid,35,600)

        #bullets
        self.__grid[27,215:220:1]="?"
        self.__grid[27,51]="?"


    #for printing the game scene
    def printboard(self,index,coor,life,score,bullet):
        os.system('clear')

        sys.stdout.flush()
        #print(str(self.__grid[:,0+index:100+index:1]).replace(' ','').replace('.','').replace('[','').replace(']','').replace('b','').replace('\'\'',""))
        for row in range(40):
            for column in range(0+index,100+index,1):
                sys.stdout.write(color.getcolor(self.__grid[row,column].decode()))
            sys.stdout.write("\n")

        print()
        global a
        print("TIME->",int(time.time()-a))
        print("LIFE->",life,"BULLET->",bullet)#bullet 1 means yes
        print("COINS:",score,"MARIO:",coor)
        print()

        
        #making easy to avoid enemies
        if life<3:
            print("ENEMY1->",a1,"ENEMY2->",a2)
        #printing controls
        print("d->right\na->left\nf->bullet\n\nsw->jump\ndw->rjump\naw->ljump\n\nq->quit")
       

#---------------mario-------------------------------------
    #help make mario move forward
    def updateboardf(self,present,prev):
        self.__grid[present[0],present[1]]=prev[0]
        self.__grid[present[0]+1,present[1]-2]=prev[1]
        self.__grid[present[0]+1,present[1]-1]=prev[2]
        self.__grid[present[0]+2,present[1]-1]=prev[6]


        #to update start position of mario
        if present[1]<30:
            self.__grid[33:36:1,2:15:1]="-"
         

        return()

    #help make mario move backward
    def updateboardb(self,present,prev):
        self.__grid[present[0],present[1]]=prev[0]
        self.__grid[present[0]+1,present[1]+1]=prev[4]
        self.__grid[present[0]+1,present[1]+2]=prev[5]
        self.__grid[present[0]+2,present[1]+1]=prev[7]


        #to update start position of mario
        if present[1]<10:
            self.__grid[33:36:1,2:15:1]="-"
         

        return()

    #help make mario move up
    def updateboardbup(self,present,prev):
        self.__grid[present[0],present[1]]=prev[0]
        self.__grid[present[0]+1,present[1]-2]=prev[1]
        self.__grid[present[0]+1,present[1]-1]=prev[2]
        self.__grid[present[0]+1,present[1]]=prev[3]
        self.__grid[present[0]+1,present[1]+1]=prev[4]
        self.__grid[present[0]+1,present[1]+2]=prev[5]
        self.__grid[present[0]+2,present[1]-1]=prev[6]
        self.__grid[present[0]+2,present[1]+1]=prev[7]

        #to update start position of mario
        if present[0]>20:
            self.__grid[20:36:1,2:15:1]="-"
        
        return()

    #help make mario move down
    def updateboardbdown(self,present,prev):
        self.__grid[present[0],present[1]]=prev[0]
        self.__grid[present[0]+1,present[1]-2]=prev[1]
        self.__grid[present[0]+1,present[1]-1]=prev[2]
        self.__grid[present[0]+1,present[1]]=prev[3]
        self.__grid[present[0]+1,present[1]+1]=prev[4]
        self.__grid[present[0]+1,present[1]+2]=prev[5]
        self.__grid[present[0]+2,present[1]-1]=prev[6]
        self.__grid[present[0]+2,present[1]+1]=prev[7]

        return()

    #to print mario
    def updatemario(self,x,y):
        self.__grid=board.addmario(self.__grid,x,y)
        
    #to remove mario from screen
    def clean(self,present,prev):
        self.__grid[present[0],present[1]]=prev[0]
        self.__grid[present[0]+1,present[1]-2]=prev[1]
        self.__grid[present[0]+1,present[1]-1]=prev[2]
        self.__grid[present[0]+1,present[1]]=prev[3]
        self.__grid[present[0]+1,present[1]+1]=prev[4]
        self.__grid[present[0]+1,present[1]+2]=prev[5]
        self.__grid[present[0]+2,present[1]-1]=prev[6]
        self.__grid[present[0]+2,present[1]+1]=prev[7]
#--------------------------------------------------------------

#----------------------enemies-------------------------------
   
    #finds enemies on the board
    def searchenemy(self,i):
        for j in range(80+i,100+i,1):#max=100+i and difference = increment in i
            if self.__grid[34,j]==b'Q':
                if self.__grid[34,j+1]==b'Q':
                    global a2
                    try:
                        a2.index(j)
                    except:
                        a2.append(j)
                elif self.__grid[34,j-1]!=b'Q':
                    global a1
                    try:
                        a1.index(j)
                    except:
                        a1.append(j)

        return(a1,a2)

    #helps move enemy1 back
    def updateenemy1b(self,a,b):
        self.__grid[34,a]=b[0]
        self.__grid[35,a]=b[2]
        self.__grid[35,a+1]=b[3]

    #helps move enemy1 forward
    def updateenemy1f(self,a,b):
        self.__grid[34,a]=b[0]
        self.__grid[35,a-1]=b[1]
        self.__grid[35,a]=b[2]

    #to add enemy1
    def updateenemy1(self,x,y):
        self.__grid=board.adde1(self.__grid,x+1,y-1)

    #helps move enemy2 back
    def updateenemy2b(self,a,b):
        self.__grid[34,a]=b[0]
        self.__grid[34,a+1]=b[1]
        self.__grid[35,a+2]=b[3]
        self.__grid[35,a+3]=b[4]

    #to add enemy2
    def updateenemy2(self,x,y):
        self.__grid=board.adde2(self.__grid,x+1,y)


    #to remove enemy1 from screen if dead
    def cleane1a(self,y,prev):
        self.__grid[34,y]=prev[0]
        self.__grid[35,y-1]=prev[1]
        self.__grid[35,y]=prev[2]
        self.__grid[35,y+1]=prev[3]

#------------------------------------------------


#------------coins-----------------------------
   
    #when jumping up on blocks
    def jumpupc(self,x,y):
        self.__grid[x,y]="-"
        self.__grid[x-3,y]="O"
        if self.__grid[x-1,y].decode()=="?":
            return(1)
        elif self.__grid[x-1,y].decode()=="C":
            return(10)
        elif self.__grid[x-1,y].decode()=="$":
            return(50)
        elif self.__grid[x-1,y].decode()=="P":
            return(11)
        else:
            return(0)

    #for "coin coming out" effect
    def jumpdownc(self,x,y):
        self.__grid[x,y]="O"
        self.__grid[x-1,y]="O"
        self.__grid[x-3,y]="-"

    #to make the powerup come out of the blocks
    def powerup(self,x,y):
        self.__grid[x-3,y]="P"
        
#---------------------------------------------------

    # to update the value at any cell
    def updatecell(self,x,y,value):
        self.__grid[x,y]=value

    #make flower come out of the brick
    def addflower(self,x,y):
        self.__grid[x-1,y]="I"
        self.__grid[x-2,y]="*"
        self.__grid[x-2,y-1]="*"
        self.__grid[x-2,y+1]="*"

    #to make bullet move ahead
    def fire1(self,x,y):
        self.__grid[x,y]="+"

    #to update the previous cells of the bullet
    def fire2(self,x,y,value):
        self.__grid[x,y]=value
    
    #to add fireworks at the end of game
    def addfireworks(self,x,y):
        self.__grid[x,y-1:y+2:1]="*"
        self.__grid[x-1,y]="*"
        self.__grid[x+1,y]="*"

    #to get character at any point
    def getgrid(self,x,y):
        return self.__grid[x,y].decode()

    #moves flag down at the end
    def moveflag(self,i):
        self.__grid[i,552:560:1]="-"
        self.__grid[i+3,552:560:1]=board.flag






