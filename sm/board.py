import random

#contains info about the board
#contains functions about the board
#starting board
#do not change(change at your own risk)

#this is my commit	
#just a check
#who are you
dimy=40
dimx=100

word="*"

#mainscene
#same dimensions

#adding clouds
cloud="^"
def addcloud(grid,x,y):
    grid[x:x+2:1,y:y+13:1]=cloud
    grid[x-1:x+3:3,y+1:y+12:1]=cloud
    grid[x-2,y+2:y+11:1]=cloud
    grid[x-2,y+5:y+8:1]="-"
    grid[x-1,y+6]="-"
    return(grid)

#adding hills
hill="/"
def addhill(grid,x,y):
    grid[x,y]=hill
    count=1
    x+=1
    while(count!=8):
        grid[x,y-count:y+count+1:1]=hill
        count+=1
        x+=1
    return(grid)

#adding tunnels
tunnel="|"
def addtunnel(grid,x,y):
    grid[x,y:y+9:8]=tunnel
    grid[x:x+4:1,y+1:y+8:1]=tunnel
    return(grid)

#adding mario
def addmario(grid,x,y):
    grid[x,y]="@"
    grid[x+1,y-2:y+3:1]=["<","-","|","-",">"]
    grid[x+2,y-1:y+2:2]="^"
    return(grid)

#adding blocks
block="O"
def addblock(grid,x,y):
    grid[x-1:x+2:1,y:y+15:1]=block

    #random coins
    for i in range(15):
        a=random.randint(0,4)
        if a==1:
            grid[x,y+i]="?"

    #randomly spawn power ups
    a=random.randint(0,20)
    if a<12:
        grid[x,y+a:y+a+2:1]="P"
    return(grid)

#adding single blocks
def addsblock(grid,x,y):
    grid[x-1:x-4:-1,y:y+6:1]=block

    #coins
    for i in range(6):
        a=random.randint(0,1)
        if a==1:
            grid[x-2,y+i]="C"

    #super coins
    a=random.randint(0,5)
    grid[x-2,y+a]="$"
    return(grid)

#adding bricks at the end
#earlier loop was not working so hard code
le="@"
def addler(grid,x,y):
    grid[x:x-4:-1,y:y+35:1]=le
    grid[x-4:x-8:-1,y+7:y+35:1]=le
    grid[x-8:x-12:-1,y+14:y+35:1]=le
    grid[x-12:x-16:-1,y+21:y+35:1]=le
    grid[x-16:x-20:-1,y+28:y+35:1]=le
    return(grid)

def addlel(grid,x,y):
    grid[x:x+4:1,y:y+7:1]=le
    grid[x+4:x+8:1,y:y+14:1]=le
    grid[x+8:x+12:1,y:y+21:1]=le
    grid[x+12:x+16:1,y:y+28:1]=le
    grid[x+16:x+20:1,y:y+35:1]=le
    return(grid)

#adding flag
flag="M"
flagh="|"
def addflag(grid,x,y):
    grid[x:x-16:-1,y:y+2:1]=flagh
    grid[x-15:x-12:1,y+2:y+10:1]=flag
    return(grid)

#adding castle
castle="H"
def addcastle(grid,x,y):
    grid[x:x-6:-1,y:y+20:1]=castle
    grid[x-6:x-10:-1,y+5:y+15:1]=castle
    grid[x:x-3:-1,y+8:y+12:1]="."
    return(grid)

#adding enemy1
e1t="Q"
e1b="x"
def adde1(grid,x,y):
    grid[x,y:y+3:1]=e1b
    grid[x-1,y+1]=e1t
    return(grid)

#adding enemy2
e2t="Q"
e2b="x"
def adde2(grid,x,y):
    grid[x,y+1:y+4:1]=e2b
    grid[x-1,y:y+2:1]=e2t
    return(grid)
