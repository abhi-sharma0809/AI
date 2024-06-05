import sys; args=sys.argv[1:]
import time

def dimension(puzzle):
    #return a 2 long array of the puzzles dimension: width/height
    ln=len(puzzle)
    dimLst = [[i, ln//i] for i in range(1, ln+1) if (ln%i==0)]
    dim = dimLst[len(dimLst)//2]
    global gWIDTH 
    gWIDTH = dim[0] 
    global gHEIGHT 
    gHEIGHT = dim[1]

def isPossible(puzzle, goal):
    l = gWIDTH*gHEIGHT
    pzlst = list(puzzle)
    pzIndex = (pzlst.index('_')//gHEIGHT)+1
    pzlst.remove('_')
    pzcount = sum(1 for i in range(l) for j in range(i + 1, len(pzlst)) if pzlst[i] > pzlst[j])
    
    glst = list(goal)
    gIndex = (glst.index('_')//gHEIGHT)+1
    glst.remove('_')
    gcount = 0
    gcount = sum(1 for i in range(l) for j in range(i + 1, len(glst)) if glst[i] > glst[j])

    return (l%2>0 and pzcount%2 == gcount%2) or (l%2<1 and ((pzcount+pzIndex)%2)==((gcount+gIndex)%2)) 

def swap(a, b, str):
    lst = list(str)
    if 0<=a<len(lst) and 0<=b<len(lst):
        lst[a], lst[b], = lst[b], lst[a]
    return "".join(lst)

def neighbors(puzzle):
    #return a list of all the neighbors of pz
    id = puzzle.index('_')
    neighborSet = {'hi'}
    neighborSet.add(swap(id-gWIDTH, id, puzzle))
    neighborSet.add(swap(id+gWIDTH, id, puzzle))
    if id%gWIDTH == 0:
        neighborSet.add(swap(id+1, id, puzzle))
    elif id%gWIDTH == gWIDTH-1:
        neighborSet.add(swap(id-1, id, puzzle[:]))
    else:
        neighborSet.add(swap(id-1, id, puzzle))
        neighborSet.add(swap(id+1, id, puzzle))
    set = neighborSet - {'hi'} - {puzzle}
    return list(set)

def printFormat(sequence):
    finLst = []
    while len(sequence)%5 != 0:
        sequence.append(' '*gWIDTH*gHEIGHT)
    for i in range(0, len(sequence), 5):
        finSubLst = []
        for h in range(gHEIGHT):
            formatted = ''
            for str in sequence[i:i+5]:
                formatted = formatted + str[h*gWIDTH:(h+1)*gWIDTH] + '   '
            print(formatted)
        print("\n")


def solve(puzzle, goal):
    #get to the goal in the shortest amount of steps
    #return the number of steps
    if not isPossible(puzzle, goal):
        return []
    if puzzle == goal:  
        return [puzzle]
    parseMe = [puzzle]
    dctSeen = {puzzle: ''}
    for itm in parseMe:
        nextItm = itm
        for n in neighbors(nextItm):
            if n not in dctSeen:
                if(n==goal):
                    dctSeen[n] = nextItm
                    return shortestPath(dctSeen, puzzle, n)
                parseMe.append(n)
                dctSeen[n] = nextItm
    return []

def shortestPath(path, puzzle, goal):
    shortest = []
    current = goal

    while current != puzzle:
        shortest.append(current)
        current = path.get(current)
    shortest.append(puzzle)
    return shortest[::-1]

def run():
    startTime = time.process_time()
    lst = args[:]
    puzzle = lst[0]
    goal = "".join(sorted(puzzle[:])) if len(lst) == 1 else lst[1]
    dimension(puzzle)
    path = solve(puzzle, goal)
    steps = len(path)-1
    printFormat(path) if path else printFormat([puzzle])
    print(f"Steps: {steps}")
    print(f"Time: {float('%.3g' % (time.process_time()-startTime))}s")
run()
#Abhisheik Sharma 7 2024

