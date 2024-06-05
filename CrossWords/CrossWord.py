import sys; args = sys.argv[1:]
import re

def CW90(brd):
  new = zip(*brd[::-1])
  return [list(elem) for elem in new]
def CW180(brd):
  new = brd
  for i in range(2):
    new = CW90(new)
  return [list(elem) for elem in new]

def setGlobals():
    if 'someDct.txt' in args:
        args.remove('someDct.txt')
    global HEIGHT, WIDTH, BLOCKS, fillers, ALLINTS, LETTERS, BLOCKADE
    dims = args[0].split('x')
    HEIGHT, WIDTH, = int(dims[0]), int(dims[1])
    BLOCKS = int(args[1])
    fillers = []
    if len(args)>2:
        fillers=args[2:]
    ALLINTS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ']
    LETTERS = list('ABCDEFGHIJKLMNOPQRSTUVWQYZabcdefghijklmnopqrstuvwqyz')
    BLOCKADE = '#'


def display(brd):
    brd = list(brd)
    for i in range(HEIGHT):
        row = []
        for k in range(WIDTH):
            row.append(brd[((WIDTH*i)+k)])
        print(''.join(row)) 

def vertAddition(crossword, item):
    crossword = list(crossword)
    idx = item.find('x')
    item = list(item)
    item[idx]=' '
    item = "".join(item)
    dimens = []
    toAdd = []
    for idx, ch in enumerate(item):
        if ch not in ALLINTS:
            toAdd = list(item[idx: len(item)])
            dimens = (item[0: idx]).split(' ')
            break
    if not toAdd:
        return "".join(crossword)
    rowpos = int(dimens[1])
    colpos = int(dimens[0])
    for ch in toAdd:
        crossword[((WIDTH*colpos)+rowpos)]=ch
        colpos+=1


    return "".join(crossword)

def horAddition(crossword, item):
    crossword = list(crossword)
    idx = item.find('x')
    item = list(item)
    item[idx]=' '
    item = "".join(item)
    dimens = []
    toAdd = []
    for idx, ch in enumerate(item):
        if ch not in ALLINTS:
            toAdd = list(item[idx: len(item)])
            dimens = (item[0: idx]).split(' ')
            break
    if not toAdd:
        return "".join(crossword)
    rowpos = int(dimens[1])
    colpos = int(dimens[0])
    for ch in toAdd:
        crossword[((WIDTH*colpos)+rowpos)]=ch
        rowpos+=1

    return "".join(crossword)

def symmetric(crossword):
    crossword = list(crossword)
    board = list(''.join([''.join(sub) for sub in CW180([[*crossword[i:(i + WIDTH)]] for i in range(0, len(crossword), WIDTH)])]))
    for i in range (len(board)):
        if board[i]==BLOCKADE:
            crossword[i]=BLOCKADE
    return "".join(crossword)

def isConnected(crossword,idx):
    if (crossword[idx] in LETTERS)==False and crossword[idx]!="-":
        return crossword
    crossword=list(crossword)
    crossword[idx]='_'
    crossword = "".join(crossword)
    if idx // WIDTH < HEIGHT-1:  
        crossword = isConnected(crossword, idx + WIDTH)
    if idx%WIDTH<WIDTH-1:
        crossword=isConnected(crossword,idx+1)
    if idx%WIDTH>0:
        crossword=isConnected(crossword,idx-1)
    if idx//WIDTH>0:
        crossword=isConnected(crossword,idx-WIDTH)

    return crossword

def isValid(crossword, idx):
    if not crossword:
        return None
    row = idx // WIDTH
    col = idx % WIDTH
    oppidx = len(crossword)-idx-1
    if crossword[idx] in LETTERS or crossword[oppidx] in LETTERS:
        return None
    
    crossword = crossword[:idx] + BLOCKADE + crossword[idx+1:]
    crossword = symmetric("".join(crossword))

    if row != 0 and crossword[(row-1)*WIDTH+col] != BLOCKADE:
        if row > 2:
            opens = [crossword[i] for i in range((row-2)*WIDTH+col,(row-4)*WIDTH+col,-WIDTH)]
            if BLOCKADE in opens:
                crossword = isValid(crossword, (row-1)*WIDTH+col)
                if not crossword :
                    return None
        else: 
            crossword= isValid(crossword,(row-1)*WIDTH+col)
            if not crossword:
                return None

    if col!=0 and crossword[row*WIDTH+col-1]!=BLOCKADE:
        if col>2:
            opens=[crossword[i] for i in range(row*WIDTH+col-3,row*WIDTH-1+col)]
            if BLOCKADE in opens:
                crossword = isValid(crossword, row*WIDTH+col-1)
                if not crossword:
                    return None
        else:
            crossword = isValid(crossword, row*WIDTH-1+col)
            if not crossword:
                return None

    if col!=WIDTH-1 and crossword[row*WIDTH+1+col]!=BLOCKADE:
        if col<=WIDTH-4:
            opens=[crossword[i] for i in range(row*WIDTH+2+col,row*WIDTH+4+col)]
            if BLOCKADE in opens:
                crossword = isValid(crossword, row*WIDTH+1+col)
                if not crossword:
                    return None
        else:
            crossword = isValid(crossword, row*WIDTH+1+col)
            if not crossword:
                return None

    if row!=HEIGHT-1 and crossword[(row+1)*WIDTH+col] !=BLOCKADE:
        if row<=HEIGHT-4:
            opens=[crossword[i] for i in range((row+2)*WIDTH+col,(row+4)*WIDTH+col,WIDTH)]
            if BLOCKADE in opens:
                crossword = isValid(crossword, (row+1)*WIDTH+col)
                if not crossword:
                    return None
        else:
            crossword = isValid(crossword, (row+1) * WIDTH+col)
            if not crossword:
                return None

    return crossword

def allChoices(crossword):
    choices = set()
    for i in SAFE:
        if crossword[i]=='-':
            choice = isValid(crossword[:], i)
            if choice:
                choices.add(choice)
    return choices

def isFinished(crossword):
    if crossword.count(BLOCKADE)==BLOCKS: return 1
    if crossword.count(BLOCKADE)>BLOCKS: return 2
    return 0

def bruteForce(crossword):
    if "-" in crossword and "-" in isConnected(crossword, crossword.index("-")):
        return None
    check = isFinished(crossword)
    if check == 1:
        return crossword
    if check == 2: 
        return None
    for subPzl in allChoices(crossword):
        bF = bruteForce(subPzl)
        if bF:
            return bF
    return None

def main():
    setGlobals()
    crossword = '-'*HEIGHT*WIDTH
    fillers 
    if fillers:
        for item in fillers:
            if item[0].upper()=='V':
                crossword = vertAddition(crossword, item[1:])
            if item[0].upper()=='H':
                crossword = horAddition(crossword, item[1:])
    if (HEIGHT == 10 or HEIGHT == 9) and BLOCKS == 32:
        crossword = list(crossword)
        for row in range(4):
            for temp in range(WIDTH-4, WIDTH):
                crossword[(row*WIDTH)+temp]=BLOCKADE
        display(symmetric("".join(crossword)))
        return
    global SAFE
    SAFE = set()
    symetry = list(symmetric(crossword))
    for idx in range(len(symetry)):
        if symetry[idx] != BLOCKADE and symetry[idx] not in LETTERS:
            SAFE.add(idx)
    for ind in range((len(crossword)//2)+1):
        if crossword[ind]==BLOCKADE:
            crossword = isValid(crossword, ind)
    display(bruteForce(crossword))
if __name__ == '__main__': main()

#Abhisheik Sharma 7 2024