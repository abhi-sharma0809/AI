import sys; args = sys.argv[1:]
import re
import random
import time

class Strategy:
    # implement all the required methods on your own
    logging = True # turns on logging
    def best_strategy(self, board, player, best_move, running):
        setGlobals(12)
        print(board)
        best_move.value = quickMove(board, player)
            # Note: It is not required for your Strategy class to have a "legal_moves" method,
            # but you must determine legal moves yourself. The server will NOT accept invalid moves.
          
def allFlips(board):
  global width, length
  dimLst = [[i, len(board)//i] for i in range(1, len(board)+1) if (len(board)%i==0)]; dim = dimLst[len(dimLst)//2]
  width = 8
  length = len(board) // width
  board = [[*board[i:(i + width)]] for i in range(0, len(board), width)]
  result = {''.join([''.join(sub) for sub in board]), ''.join([''.join(sub) for sub in xFlip(board)]),
              ''.join([''.join(sub) for sub in yFlip(board)]), ''.join([''.join(sub) for sub in CW90(board)]),
                ''.join([''.join(sub) for sub in CW180(board)]), ''.join([''.join(sub) for sub in CW270(board)])}
  result.add(''.join([''.join(sub) for sub in diag1(board)]))
  result.add(''.join([''.join(sub) for sub in diag2(board)]))
  return result


def xFlip(brd):
  temp1 = []
  for i in range(width):
    temp2 = []
    for j in brd:
      temp2 += [j[i]]
    temp1 += [temp2]
  temp1 = yFlip(temp1)
  new = []
  for i in range(length):
    temp2 = []
    for j in temp1:
      temp2 += [j[i]]
    new += [temp2]
  return new
def yFlip(brd):
  new = [sub[::-1] for sub in brd]
  return new
def diag1(brd):
  for i in range(3):
    brd = yFlip(CW90(brd))
  return brd
def diag2(brd):
  for i in range(3):
    brd = yFlip(CW90(brd))
  return CW180(brd)
def CW90(brd):
  new = zip(*brd[::-1])
  return [list(elem) for elem in new]
def CW180(brd):
  new = brd
  for i in range(2):
    new = CW90(new)
  return [list(elem) for elem in new]
def CW270(brd):
  new = brd
  for i in range(3):
    new = CW90(new)
  return [list(elem) for elem in new]

def setGlobals(lim):
    global excelList, topEdge, bottomEdge, leftEdge, rightEdge, edges, LIMIT, opening, openingBook
    excelList = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    topEdge = {0,1,2,3,4,5,6,7}
    bottomEdge = {56,57,58,59,60,61,62,63}
    leftEdge = {0,8,16,24,32,40,48,56}
    rightEdge = {7,15,23,31,39,47,55,63}
    edges = {1,2,3,4,5,6,57,58,59,60,61,62,8,16,24,32,40,48,15,23,31,39,47,55}
    LIMIT = lim
    opening = {'...........................OX......XO...........................': 19, 
                  '...................X.......XX......XO...........................': 18,
                  '..................OX.......OX......XO...........................': 17,
                  '.................XXX.......OX......XO...........................': 11,
                  '..........XO.....XXX.......OX......XO...........................': 20,
                  '...........O.....XXO.......OX......XO...........................': 10,
                  '..........XO.....XXXO......OO......XO...........................': 12}
    openingBook = {}
    for board in opening:
        brd = list(board)
        brd[opening.get(board)]='*'
        allRotations = allFlips("".join(brd))
        for rotated in allRotations:
            newRotated = list(rotated)
            pos = newRotated.index('*')
            newRotated[pos]='.'
            openingBook["".join(newRotated)]=pos
  
def display(brd):
    for i in range(8):
        row = []
        for k in range(8):
            row.append(brd.get((8*i)+k))
        print(''.join(row)) 

def findMoves(brd, turn):
    if type(brd) == str:
        brd = {i:brd[i].upper() for i in range(len(brd))}
    opp = 'X' if turn == 'O' else 'O'
    moves = {i:[] for i in range(64)}
    for key in brd:
        if brd.get(key)==turn:
            if key not in rightEdge and brd.get(key+1) == opp:
                #right case
                path = []
                ind = key+1
                while (ind not in rightEdge and brd.get(ind)!= turn):
                    path.append(ind)
                    if brd.get(ind)=='.':
                        moves[ind]=moves.get(ind)+path
                        break
                    ind+=1
                path.append(ind)
                if brd.get(ind)=='.':
                        moves[ind]=moves.get(ind)+path

            if key not in leftEdge and brd.get(key-1) == opp:
                #left case
                path = []
                ind = key-1
                while (ind not in leftEdge and brd.get(ind)!= turn):
                    path.append(ind)
                    if brd.get(ind)=='.':
                        moves[ind]=moves.get(ind)+path
                        break
                    ind-=1
                path.append(ind)
                if brd.get(ind)=='.':
                        moves[ind]=moves.get(ind)+path
            if key not in topEdge and brd.get(key-8) == opp:
                #top case
                path = []
                ind = key-8
                while (ind not in topEdge and brd.get(ind)!= turn):
                    path.append(ind)
                    if brd.get(ind)=='.':
                        moves[ind]=moves.get(ind)+path
                        break
                    ind-=8
                path.append(ind)
                if brd.get(ind)=='.':
                        moves[ind]=moves.get(ind)+path
            if key not in bottomEdge and brd.get(key+8) == opp:
                #bottom case
                path = []
                ind = key+8
                while (ind not in bottomEdge and brd.get(ind)!= turn):
                    path.append(ind)
                    if brd.get(ind)=='.':
                        moves[ind]=moves.get(ind)+path
                        break
                    ind+=8
                path.append(ind)
                if brd.get(ind)=='.':
                        moves[ind]=moves.get(ind)+path
            if key not in rightEdge and key not in bottomEdge and brd.get(key+9) == opp:
                #downRighttDiag case
                path = []
                ind = key+9
                while (ind not in rightEdge and ind not in bottomEdge and brd.get(ind)!= turn):
                    path.append(ind)
                    if brd.get(ind)=='.':
                        moves[ind]=moves.get(ind)+path
                        break
                    ind+=9
                path.append(ind)
                if brd.get(ind)=='.':
                        moves[ind]=moves.get(ind)+path
            if key not in leftEdge and key not in bottomEdge and brd.get(key+7) == opp:
                #downLeftDiag case
                path = []
                ind = key+7
                while (ind not in leftEdge and ind not in bottomEdge and brd.get(ind)!= turn):
                    path.append(ind)
                    if brd.get(ind)=='.':
                        moves[ind]=moves.get(ind)+path
                        break
                    ind+=7
                path.append(ind)
                if brd.get(ind)=='.':
                        moves[ind]=moves.get(ind)+path
            if key not in topEdge and key not in rightEdge and brd.get(key-7) == opp:
                #upRightDiag case
                path = []
                ind = key-7
                while (ind not in rightEdge and ind not in topEdge and brd.get(ind)!= turn):
                    path.append(ind)
                    if brd.get(ind)=='.':
                        moves[ind]=moves.get(ind)+path
                        break
                    ind-=7
                path.append(ind)
                if brd.get(ind)=='.':
                        moves[ind]=moves.get(ind)+path
            if key not in topEdge and key not in leftEdge and brd.get(key-9) == opp:
                #upLeftDiag case
                path = []
                ind = key-9
                while (ind not in leftEdge and ind not in topEdge and brd.get(ind)!= turn):
                    path.append(ind)
                    if brd.get(ind)=='.':
                        moves[ind]=moves.get(ind)+path
                        break
                    ind-=9
                path.append(ind)
                if brd.get(ind)=='.':
                        moves[ind]=moves.get(ind)+path
    return {i:moves.get(i) for i in moves.keys() if moves.get(i)}

def moveFormat(pos):
    if(pos[0]=='_'):
        return int(pos[1])
    if len(pos)==1:
        return int(pos)
    if pos[0] in excelList:
        return ((excelList.index(pos[0])%8)+(8*(int(pos[1])-1)))
    return int(pos)

def makeMove(brd, trace, tkn):
    brd = {i:brd[i].upper() for i in range(len(brd))}
    for i in trace:
        brd[i]=tkn
    return brd

def score(brd):
    xScore = 0
    oScore = 0
    for ch in brd.values():
        if ch == 'X':
            xScore +=1
        if ch == 'O':
            oScore +=1
    return f'{xScore}/{oScore}'

def projection2(brd, moves, move, turn):
    for i in moves.keys():
        brd[i] = '*'
    brd[move]=turn.lower()
    display(brd)

def projection(brd, moves):
    for i in moves.keys():
        brd[i] = '*'
    display(brd)

def possibleEdge(brd, tkn, edge):
    opp = 'X' if tkn == 'O' else 'O'
    neighbor = 8 if edge in leftEdge or edge in rightEdge else 1
    if brd.get(edge+neighbor)==opp and brd.get(edge-neighbor)=='.' or brd.get(edge-neighbor)==opp and brd.get(edge+neighbor)=='.':
        return False
    if brd.get(edge+neighbor)==opp and brd.get(edge-neighbor)==tkn or brd.get(edge-neighbor)==opp and brd.get(edge+neighbor)==tkn:
        return False
    return True

def isWedge(board, tkn, move):
    opp = 'X' if tkn == 'O' else 'O'
    if (move in leftEdge or move in rightEdge) and (board.get(move-8)==opp and board.get(move+8)==opp):
        return True
    if (move in topEdge or move in bottomEdge) and (board.get(move+1)==opp and board.get(move-1)==opp):
        return True
    return (board.get(move-8)==opp and board.get(move+8)==opp) or (board.get(move+1)==opp and board.get(move-1)==opp) or (board.get(move+9)==opp and board.get(move-9)==opp) or (board.get(move+7)==opp and board.get(move-7)==opp)

def findBadSpots(brd):                          
    badSpots = set()
    if brd[0]=='.':
        badSpots.update([1,8,9])
    if brd[7]=='.':
        badSpots.update([14,15,6])
    if brd[56]=='.':
        badSpots.update([48,49,57])
    if brd[63]=='.':
        badSpots.update([54,55,62])
    return badSpots

def forwardLook(brd, moveSet, turn):
    brd = makeMove(brd, moveSet, turn)
    turn = 'X' if turn == 'O' else 'O'
    posOppMoves = {key for key in findMoves(brd, turn).keys()}
    if len(posOppMoves)==0:
        return 1000000
    if len(posOppMoves.intersection({0,56,7,63}))>0:
        return -1000000
    return 0

def safeEdge(brd, move):
    tkns = ['X', 'O']
    if move in leftEdge:
        for i in leftEdge.difference({move}):
            if brd[i] not in tkns: return False
    if move in rightEdge:
        for i in rightEdge.difference({move}):
            if brd[i] not in tkns: return False
    if move in topEdge:
        for i in topEdge.difference({move}):
            if brd[i] not in tkns: return False
    if move in bottomEdge:
        for i in bottomEdge.difference({move}):
            if brd[i] not in tkns: return False
    return True

def quickMove(brd, turn):
    #print(brd)
    global LIMIT
    if not brd:
        LIMIT = turn
        return
    turn = turn.upper()
    board = {i:brd[i].upper() for i in range(len(brd))}
    dots = brd.count(".")
    if brd.upper() in openingBook:
        return openingBook.get(brd.upper())
    if dots < LIMIT:
        optimal = alphabeta(board, turn, -69, 69, True)
        #print(f'Min score: {optimal[0]}; move sequence: {optimal[1:]}')
        return optimal[-1]
    #if dots < 26:
    #    optimal = midGame(board, turn, -69, 69, True, 7, 0)
    #    return optimal[-1]
    if dots < 32:
        optimal = midGame(board, turn, -69, 69, True, 6, 0)
        #print(f'Min score: {optimal[0]}; move sequence: {optimal[1:]}')
        return optimal[-1]
    allMoves = findMoves(board, turn.upper())
    moves = {*[i for i in allMoves.keys()]}
    badSpots = findBadSpots(board)
    moveSpecs = {tup[0] : {*tup[1]} for tup in allMoves.items()}
    movePoints = {i:0 for i in moves}
    for move in moves:
        if move in {0, 7, 56, 63}:
            movePoints[move]=movePoints.get(move)+100000
    for move in moves:
        if move in badSpots:
            movePoints[move]=movePoints.get(move)-100000
    for move in moves:
        if move in edges and possibleEdge(board, turn, move):
            movePoints[move]=movePoints.get(move)+10000
    for move in moves:
        if isWedge(board, turn, move):
            movePoints[move]=movePoints.get(move)+100
    for move in moves:
        if move in edges and safeEdge(board, move):
            movePoints[move]=movePoints.get(move)+50000
    for move in moves:
        if move in edges:
            movePoints[move]=movePoints.get(move)+10
    for move in moveSpecs.keys():
        movePoints[move]=movePoints.get(move)+forwardLook(board.copy(), moveSpecs.get(move), turn)
    return max([(movePoints.get(key), key) for key in movePoints.keys()])[1]  
global NMCACHE
NMCACHE = {}

def negamax(brd, turn, topLevel):
    board = "".join(ch for ch in brd.values())
    key = (board, turn)
    if key in NMCACHE:
        return NMCACHE.get(key)
    eTkn = 'X' if turn == 'O' else 'O'
    if board.count('.')==0:
        return [board.count(turn) - board.count(eTkn)]
    possMoves = findMoves(brd, turn)
    if not possMoves:
        if findMoves(board, eTkn):
            nmOpp = negamax(brd, eTkn, False)
            bestSoFar = [-nmOpp[0]] + nmOpp[1:] + [-1]
        else:
            return [board.count(turn) - board.count(eTkn)]               
    else:
        bestSoFar = [-65]
        for mv in possMoves:
            newBrd = makeMove(brd.copy(),possMoves.get(mv),turn)
            nm = negamax(newBrd, eTkn, False)
            if -nm[0] > bestSoFar[0]:
                bestSoFar = [-nm[0]] + nm[1:] + [mv]
                if topLevel:
                    print(f'My preffered move is {bestSoFar[-1]}')
                    print(f'Min score: {bestSoFar[0]}; move sequence: {bestSoFar[1:]}')
    NMCACHE[key]=bestSoFar
    return bestSoFar
global ABCACHE
ABCACHE = {}

def alphabeta(brd, turn, minBound, maxBound, topLevel): 
    board = "".join(ch for ch in brd.values())
    key = (board, turn, minBound, maxBound)
    if key in ABCACHE:
        best = ABCACHE.get(key)
        #if topLevel:
        #    print(f'Min score: {best[0]}; move sequence: {best[1:]}')
        return best
    eTkn = 'X' if turn == 'O' else 'O'
    allMoves = findMoves(brd, turn)
    if not allMoves:
        if not findMoves(brd, eTkn):
            return [board.count(turn) - board.count(eTkn)]
        abOpp = alphabeta(brd, eTkn, -maxBound, -minBound, False)
        return [-abOpp[0]] + abOpp[1:] + [-1]
    best = [minBound-1]
    for mv in allMoves:
        ab = alphabeta(makeMove(brd.copy(), allMoves.get(mv), turn), eTkn, -maxBound, -minBound, False)
        score = -ab[0]
        if score <= minBound: continue
        if score > maxBound: return [score]
        best = [-ab[0]] + ab[1:] + [mv]
        minBound = score+1
    #if topLevel:
    #    print(f'Min score: {best[0]}; move sequence: {best[1:]}')
    ABCACHE[key] = best
    return best

global MGCACHE
MGCACHE = {}

def midGame(brd, turn, minBound, maxBound, topLevel, depth, curr): 
    board = "".join(ch for ch in brd.values())
    key = (board, turn, minBound, maxBound)
    if key in MGCACHE:
        best = MGCACHE.get(key)
        #if topLevel:
        #    print(f'Min score: {best[0]}; move sequence: {best[1:]}')
        return best
    eTkn = 'X' if turn == 'O' else 'O'
    if curr == depth:
            return [board.count(turn) - board.count(eTkn)]
    allMoves = findMoves(brd, turn)
    if not allMoves:
        if not findMoves(brd, eTkn):
            return [board.count(turn) - board.count(eTkn)]
        abOpp = midGame(brd, eTkn, -maxBound, -minBound, False, depth, curr+1)
        return [-abOpp[0]] + abOpp[1:] + [-1]
    best = [minBound-1]
    for mv in allMoves:
        ab = midGame(makeMove(brd.copy(), allMoves.get(mv), turn), eTkn, -maxBound, -minBound, False, depth, curr+1)
        score = -ab[0]
        if score <= minBound: continue
        if score > maxBound: return [score]
        best = [-ab[0]] + ab[1:] + [mv]
        minBound = score+1
    #if topLevel:
    #    print(f'Min score: {best[0]}; move sequence: {best[1:]}')
    MGCACHE[key] = best
    return best


def run(brd, moves, turn):
    for move in moves:
        if move<0: continue
        allMoves = findMoves(brd, turn)
        if not allMoves:
            turn = 'X' if turn == 'O' else 'O'
        brd = makeMove(brd, findMoves(brd, turn).get(move), turn)
        turn = 'X' if turn == 'O' else 'O'
    turn = 'X' if turn == 'O' else 'O'
    print(f'{turn} plays to {moves[-1]}')
    turn = 'X' if turn == 'O' else 'O'
    allMoves = findMoves(brd, turn)
    if len(allMoves)==0:
        turn = 'X' if turn == 'O' else 'O'
        allMoves = findMoves(brd, turn)
    projection2(brd.copy(), allMoves, move, 'X' if turn == 'O' else 'O')
    print(''.join(v for v in brd.values()))
    print(score(brd))
    if allMoves:
        print(f'Possible moves for {turn}: {"".join((str(ch) +", ") for ch in list(allMoves.keys()))[:-2]}')
        print(f'My preffered move is {quickMove("".join(ch for ch in brd.values()), turn)}')
def main():
    board, moves, turn, HL, Terse = {}, [], '', 8, True
    for info in args:
        if info == 'v' or info == 'V':
            Terse = False
        if len(info)==64 and '.' in info:
            for i in range(len(info)):
                board[i]=info[i].upper()
        elif info in 'xXoO':
            turn = info.upper()
        elif info[0] != '-' and len(info)<3 and info != 'z' and info != 'v' and info != 'V':
            moves.append(moveFormat(info))
        elif len(info)==3 or len(info)==4:
            HL = int(info[2:])
            setGlobals(HL) 
        else:
            condensedPath = re.findall(r'..', info)
            for move in condensedPath:
                moves.append(moveFormat(move))

    if not board:
        for i in range(27):
            board[i] = '.'
        board[27], board[28] = 'O', 'X'
        for i in range(29, 35):
            board[i] = '.'
        board[35], board[36] = 'X', 'O'
        for i in range(37, 64):
            board[i] = '.'
    if not turn:
        tokenCount = sum(1 for i in board.values() if i=='X' or i=='O')
        turn = 'X' if tokenCount%2 == 0 else 'O'
    
    if Terse and moves:
        board = run(board, moves, turn)
    else:
        allMoves = findMoves(board, turn)
        if not allMoves:
            turn = 'X' if turn == 'O' else 'O'
            allMoves = findMoves(board, turn)
        projection(board.copy(), allMoves)
        print(''.join(v for v in board.values()))
        print(score(board))
        if allMoves:
            print(f'Possible moves for {turn}: {"".join((str(ch) +", ") for ch in list(allMoves.keys()))[:-2]}')
            print(f'My preffered move is {quickMove("".join(ch for ch in board.values()), turn)}')
        print('\n')
        if moves:
            allMoves = findMoves(board, turn)
            for move in moves:
                if move<0:
                    continue
                turn2 = turn
                print(f'{turn} plays to {move}')
                board = makeMove(board, allMoves.get(move), turn)
                turn = 'X' if turn == 'O' else 'O'
                allMoves = findMoves(board, turn)
                if len(allMoves)==0:
                    turn = 'X' if turn == 'O' else 'O'
                    allMoves = findMoves(board, turn)
                projection2(board.copy(), allMoves, move, turn2)
                print(''.join(v for v in board.values()))
                print(score(board))
                if allMoves:
                    print(f'Possible moves for {turn}: {"".join((str(ch) +", ") for ch in list(allMoves.keys()))[:-2]}')
                    print(f'My preffered move is {quickMove("".join(ch for ch in board.values()), turn)}')
                    #if findMoves(board, 'X' if turn == 'O' else 'O'):
                     #   print(quickMove("".join(ch for ch in board.values()),'X' if turn == 'O' else 'O'))
                print('\n')

    #tokenCount = sum(1 for i in board.values() if i=='X' or i=='O')
    #turn = 'X' if tokenCount%2 == 0 else 'O' 
    #dots = sum(1 for val in board.values() if val == '.')
    #brd = "".join(ch for ch in board.values())
    #if findMoves(board, turn):
     #   print(f'My preffered move is {quickMove(brd, turn)}')

setGlobals(8)
if __name__ == '__main__': main()

#Abhisheik Sharma 7 2024
