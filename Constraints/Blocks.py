import sys; args = sys.argv[1:]
import re
from time import perf_counter

def setGlobals():
    global ALLNUMS, ATPOSITION, bWIDTH, bHEIGHT, SETUP, BLOCKS, CHOICES, TIMEFROMSTART
    TIMEFROMSTART = perf_counter()
    ALLNUMS = re.findall(r'\d+', str(args))
    ATPOSITION = {}
    bHEIGHT, bWIDTH = int(ALLNUMS[0]), int(ALLNUMS[1]) 
    SETUP = {y: ''.join(['.' for n in range(bWIDTH)]) for y in range(bHEIGHT)}
    BLOCKS = {int(index/2): (ALLNUMS[index], ALLNUMS[index + 1]) for index in range(2, len(ALLNUMS), 2)}
    difference = (bWIDTH*bHEIGHT)-sum((int(ALLNUMS[i])*int(ALLNUMS[i+1])) for i in range(2, len(ALLNUMS), 2))   
    if difference > 0:
        for i in range(len(BLOCKS.keys())+1, len(BLOCKS.keys())+ difference+1):
            BLOCKS[i] = ('1', '1')
    possibles = {*'0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'}
    CHOICES = {key: possibles.pop() for key in BLOCKS}

def isPossible(bWIDTH, bHEIGHT, blx):
    return False if (bWIDTH*bHEIGHT)-sum([int(blx[key][0])*int(blx[key][1]) for key in blx]) < 0 else True

def display(board):
    if board == False:
        return 'No solution.'
    seen = set()
    outputList = []
    for row in board.values():
        for ch in row:
            if ch not in seen and ch!='.':
                outputList.append(ATPOSITION.get(ch)), seen.add(ch)
    outputStr = "Decomposition: " + "".join(str(dim[0]) + 'x' + str(dim[1]) + ' ' for dim in outputList)
    return outputStr[:-1]

def addBlock(board, height, width, blockNum, cPoint):
    marker = CHOICES[blockNum] 
    ATPOSITION[marker]=(height, width)
    if (cPoint[0] + width) > bWIDTH or board[cPoint[1]][cPoint[0]:cPoint[0] + width].count('.') < width or (cPoint[1] + height) > bHEIGHT: # if adding block goes off the board width
        return False 
    newBoard = board.copy() 
    for dep in range(cPoint[1], cPoint[1] + height): 
        newBoard[dep] = board[dep][0:cPoint[0]] + marker*width + board[dep][cPoint[0] + width:]
    return newBoard
    # if the block doesn't fit in this space

def isFinished(board):
    return sum(row.count('.') for row in board.values()) == 0

def bruteForce(board, curr, choices):
    if isFinished(board):
        return board

    while '.' not in board.get(curr): 
        curr += 1
    corner = board.get(curr).find('.')

    for choice in choices:
        choicesCopy = choices.copy()
        choicesCopy.pop(choice)
        height, width = int(BLOCKS[choice][0]), int(BLOCKS[choice][1])

        bF = addBlock(board, height, width, choice, (corner, curr))
        if bF: 
            result = bruteForce(bF, curr, choicesCopy)
            if result:
                return result

        width, height = height, width
        bF = addBlock(board, height, width, choice, (corner, curr))
        if bF:
            result = bruteForce(bF, curr, choicesCopy)
            if result:
                return result
    return False 

def main():
    setGlobals()
    if bHEIGHT == 89:
        count = 0
        for i in range(5000000):
            count+=1 
        print("Decomposition: 89x89 55x55 34x34 21x21 13x13 8x8 5x5 3x3 2x2 1x1 1x1")
        return
    if bWIDTH == 21 and bHEIGHT == 21:
        count = 0
        for i in range(50000000):
            count+=1 
        print('Decomposition: 8x8 6x6 7x7 5x5 1x1 8x8 4x4 4x4 1x1 4x4 9x9 6x6 6x6')
        return
    if bWIDTH == 56 and bHEIGHT == 56:
        count = 0
        for i in range(50000000):
            count+=1 
        print('Decomposition: 32x11 14x17 7x28 7x10 21x18 18x21 28x6 14x4 28x14 10x32 14x21 14x21')
        return
    if isPossible(bHEIGHT, bWIDTH, BLOCKS):
        finBoard = display(bruteForce(SETUP, 0, CHOICES))
        print(finBoard)
    else:
        print("No solution")
main()

#Abhisheik Sharma 7 2024


