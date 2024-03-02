import sys; args = sys.argv[1:]
import random, re

BLOCKCHAR='#'
OPENCHAR='-'
PROTECTEDCHAR='~'

def main():
    if len(args)<1:
        exit()
    inTest=[r"^(\d+)x(\d+)$", r"^\d+$", r"^(H|V)(\d+)x(\d+)(.*)$"]
    xheight, xwidth, blockCt, dictSeen= 4,4,0,False
    fixedWords=[]
    dictLines=open(args[0]).read().splitlines()
    dictSeen = True
    for arg in args:
        for testNum, retest in enumerate(inTest):
            match= re.search(retest, arg, re.I)
            if not match: continue
            if testNum==0:
                xheight, xwidth = int(match.group(1)), int(match.group(2))
            elif testNum==1:
                    blockCt=int(match.group(0))
            else:
                direction,vpos, hpos, word= match.group(1).upper(), int(match.group(2)), int(match.group(3)), match.group(4).upper()
                if word == "":
                    word = "#"
                fixedWords.append((direction,vpos,hpos,word))
    xw=BLOCKCHAR*(xwidth+2)
    for r in range(xheight):
        xw=xw+BLOCKCHAR+OPENCHAR*xwidth+BLOCKCHAR
    xw=OPENCHAR*(xheight*xwidth)
    xw=fill(xw,int(blockCt),xheight,xwidth,fixedWords)
    display(xw,xheight,xwidth,fixedWords)

def display(xw,height,width,words):
    xwlist=list(removeborders(xw,height,width))
    for arg in words:
        x=arg[1]*width+arg[2]
        if arg[0]=='H':
            for a in range(x,x+len(arg[3])):
                xwlist[a]= arg[3][a-x]
        if arg[0]=='V':
            for a in range(x,x+len(arg[3])*width,width):
                xwlist[a]= arg[3][(a-x)//width]
    for r in range(len(xwlist)):
        if xwlist[r]==PROTECTEDCHAR:
            xwlist[r]=OPENCHAR
    xw=''.join(xwlist)
    for r in range(height):
        print(xw[r*width:r*width+width])

def removeborders(xw,height,width):
    newxw=""
    xw=''.join(xw)
    xw=xw[width+2:(height+1)*(width+2)]
    for i in range(height):
        newxw=newxw+xw[i*(width+2)+1:(i)*(width+2)+width+1]
    return newxw

def checkxw(xw, width):
    xw=''.join(xw)
    illegalRegex = '[{}](.?[{}]|[{}].?)[{}]'.format(BLOCKCHAR, PROTECTEDCHAR,PROTECTEDCHAR, BLOCKCHAR)
    substituteRegex = '[{}]{}(?=[{}])'.format(BLOCKCHAR, OPENCHAR, BLOCKCHAR)
    subRE2 = '[{}]{}{}(?=[{}])'.format(BLOCKCHAR, OPENCHAR, OPENCHAR, BLOCKCHAR)
    newH = width
    for counter in range(2):
        if re.search(illegalRegex, xw):
            return False
        xw = re.sub(substituteRegex, BLOCKCHAR*2, xw)
        xw = re.sub(subRE2, BLOCKCHAR*3, xw)
        xw = transpose(xw,newH)
        newH = len(xw)//newH
    return list(xw)

def addborder(xw,height,width):
    newxw=(width+2)*BLOCKCHAR
    for i in range(height):
        newxw=newxw+BLOCKCHAR+xw[i*width:i*width+width]+BLOCKCHAR
    newxw=newxw+BLOCKCHAR*(width+2)
    return newxw

def transpose(xw, newH):
    return ''.join([xw[col::newH] for col in range(newH)])

def fill(xw,block_count, height, width, fixedWords):
    if block_count == height * width:
        board = BLOCKCHAR * ((height+2) * (width+2))
        return board
    xwlist=list(xw)
    for arg in fixedWords:
        x=arg[1]*width+arg[2]
        if arg[0]=='H':
            for a in range(x,x+len(arg[3])):
                if arg[3][a-x]==BLOCKCHAR:
                    xwlist[a]=BLOCKCHAR
                    xwlist[len(xw)-a-1]=BLOCKCHAR
                else:
                    xwlist[len(xw)-a-1] = PROTECTEDCHAR
                    xwlist[a]= PROTECTEDCHAR
        if arg[0]=='V':
            for a in range(x,x+len(arg[3])*width,width):
                if arg[3][(a-x)//width]==BLOCKCHAR:
                    xwlist[a]=BLOCKCHAR
                    xwlist[len(xw)-a-1]=BLOCKCHAR
                else:
                    xwlist[len(xw)-a-1] = PROTECTEDCHAR
                    xwlist[a]= PROTECTEDCHAR
    if block_count%2==0 and height%2==1 and width%2==1:
        xwlist[len(xw)//2]=PROTECTEDCHAR
        xwlist[len(xw)//2-1]=PROTECTEDCHAR
        xwlist[len(xw)//2+1]=PROTECTEDCHAR
        xwlist[len(xw)//2-width]=PROTECTEDCHAR
        xwlist[len(xw)//2+width]=PROTECTEDCHAR
    if block_count%2==1:
        xwlist[len(xw)//2]==BLOCKCHAR
    xwlist=list(addborder(''.join(xwlist),height, width))
    return block(xwlist, height+2, width+2, block_count+2*(height+width+2))

def block(xw, height, width,block_count):
    goodxw=xw
    while (block_count-goodxw.count(BLOCKCHAR))!=0:
        goodxw=block_helper(xw,height,width,block_count)
    if connected(goodxw,height,width)==True:
        return goodxw
    else:
        goodxw=block(xw,height,width,block_count)
    return goodxw

def block_helper(xw,height,width,block_count):
    newxw=list(xw)
    testlist=list()
    openlist = []
    while (block_count-newxw.count(BLOCKCHAR))>0:
        for x in range(len(newxw)):
            if newxw[x] == OPENCHAR:
                openlist.append(x)
        r = random.choice(openlist)
        if r not in testlist:
            testlist.append(r)
            newxw[r] = BLOCKCHAR
            newxw[len(newxw)-r-1] = BLOCKCHAR
        while newxw != checkxw(newxw,width):
            if checkxw(newxw,width)==False:
                return xw
            else:
                newxw=checkxw(newxw,width)
    return newxw

def connected(xw,height, width):
    r=random.randint(0,len(xw)-1)
    while xw[r]==BLOCKCHAR:
        r=random.randint(0,len(xw)-1)
    checkxw=xw[:]
    connectedhelper(checkxw,r,height,width)
    for char in range(len(checkxw)):
        if checkxw[char]!=BLOCKCHAR:
            return False
    return True

def connectedhelper(xw,index, height, width):
    if index>0 and index<len(xw) and xw[index]!=BLOCKCHAR:
        xw[index]=BLOCKCHAR
        if index%width!=0:
            connectedhelper(xw,index-1, height, width)
        if index%width!=width-1:
            connectedhelper(xw,index+1, height, width)
        connectedhelper(xw,index-width, height, width)
        connectedhelper(xw,index+width, height, width)


if __name__=='__main__':
    main()

#Medha Pappula, 6, 2026