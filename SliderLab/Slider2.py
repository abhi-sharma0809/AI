import sys; args=sys.argv[1:]
with open(args[0]) as f:
    allPuzzles = [line.strip() for line in f]

gWIDTH = 4
gHEIGHT = 4
indexDict = {(0,1):'R',(1,2):'R',(2,3):'R',(4,5):'R',(5,6):'R',(6,7):'R',(8,9):'R',(9,10):'R',
(10,11):'R',(12,13):'R',(13,14):'R',(14,15):'R',(1,0):'L',(2,1):'L',(3,2):'L',(5,4):'L',
(6,5):'L',(7,6):'L',(9,8):'L',(10,9):'L',(11,10):'L',(13,12):'L',(14,13):'L',(15,14):'L',
(0,4):'D',(1,5):'D',(2,6):'D',(3,7):'D',(4,8):'D',(5,9):'D',(6,10):'D',(7,11):'D',
(8,12):'D',(9,13):'D',(10,14):'D',(11,15):'D',(4,0):'U',(5,1):'U',(6,2):'U',(7,3):'U',
(8,4):'U',(9,5):'U',(10,6):'U',(11,7):'U', (12,8):'U',(13,9):'U',(14,10):'U',(15,11):'U'}

def makeHeapMin(arr,k):
    left = 2 * k + 1
    right = 2 * k + 2
    if left < len(arr) and arr[left] < arr[k]:
        smallest = left
    else:
        smallest = k
    if right < len(arr) and arr[right] < arr[smallest]:
        smallest = right
    if smallest != k:
        arr[k], arr[smallest] = arr[smallest], arr[k]
        makeHeapMin(arr, smallest)

def buildMin(arr):
    n = int((len(arr)//2)-1)
    for k in range(n, -1, -1):
        makeHeapMin(arr,k)

def removeMin(arr):
    arr[0], arr[len(arr)-1] = arr[len(arr)-1], arr[0]
    arr.pop()
    makeHeapMin(arr, 0)

def addMin(arr, i):
    if(arr):
        arr.append(i)
        n = len(arr) - 1
        while (n > 0 and arr[(n-1)//2] > arr[n]): arr[(n-1)//2], arr[n] = arr[n], arr[(n-1)//2]; n = (n-1)//2
    else:
        arr.append(i)

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

    return l%2<1 and ((pzcount+pzIndex)%2)==((gcount+gIndex)%2)

def swap(a, b, str):
    lst = list(str)
    fin = ''
    if 0<=a<len(lst) and 0<=b<len(lst):
        lst[a], lst[b], = lst[b], lst[a]
    return "".join(lst)

def neighbors(puzzle):
    #return a list of all the neighbors of pz
    id = puzzle.index('_')
    neighborSet = set()
    neighborSet.add(swap(id-gWIDTH, id, puzzle))
    neighborSet.add(swap(id+gWIDTH, id, puzzle))
    if id%gWIDTH == 0:
        neighborSet.add(swap(id+1, id, puzzle))
    elif id%gWIDTH == gWIDTH-1:
        neighborSet.add(swap(id-1, id, puzzle))
    else:
        neighborSet.add(swap(id-1, id, puzzle))
        neighborSet.add(swap(id+1, id, puzzle))
    return neighborSet - {puzzle}

def swapTup(a, b, str):
    lst = list(str)
    if 0<=a<len(lst) and 0<=b<len(lst):
        lst[a], lst[b], = lst[b], lst[a]
        return ("".join(lst), a, b)
    return str

def neighborsTup(puzzle):
    #return a list of all the neighbors of pz
    id = puzzle.index('_')
    neighborSet = set()
    neighborSet.add(swapTup(id-gWIDTH, id, puzzle))
    neighborSet.add(swapTup(id+gWIDTH, id, puzzle))
    if id%gWIDTH == 0:
        neighborSet.add(swapTup(id+1, id, puzzle))
    elif id%gWIDTH == gWIDTH-1:
        neighborSet.add(swapTup(id-1, id, puzzle))
    else:
        neighborSet.add(swapTup(id-1, id, puzzle))
        neighborSet.add(swapTup(id+1, id, puzzle))
    return neighborSet - {puzzle}


def compactifyPath(puzzle, sequence):
    comPath = ''
    if sequence:
        if len(sequence) == 1:
            comPath += 'G'
        else:
            for i in range(len(sequence)-1):
                comPath += indexDict.get((sequence[i].find('_'),sequence[i+1].find('_')))
    else:
        comPath += 'X'

    print(puzzle + ' Path ' + comPath)

def h(puzzle,goal):
    # for one manhatten distance: abs(x_value - x_goal) + abs(y-value - y_goal)
    return sum(abs(puzzle.index(ch)%4 - goal.index(ch)%4) + abs(puzzle.index(ch)//4 - goal.index(ch)//4) for ch in puzzle if ch != '_')

def astar(root, goal):
    if not isPossible(root, goal):
        return []
    openSet = [[] for i in range(56)]
    hCalc = h(root, goal)
    openSet[hCalc].append((root, hCalc))
    currF = hCalc
    closedSet = {}

    #editing solution
    while True:
        if not openSet[currF]:
            currF+=2
        poppedPuz = openSet[currF].pop()
        puzzle, manhatten = poppedPuz[0], poppedPuz[1]
        if puzzle in closedSet:
            continue
        closedSet[puzzle] = currF-manhatten
        if(puzzle == goal):
            return shortestastarpath(closedSet, root, goal)
        for n in neighborsTup(puzzle):
            id = n[2]
            ch = n[0][id]
            pzid=n[1]
            #abs switched number(n to goal) < abs switched number(puzzle to goal):
            inc = (abs(id%4 - goalDict.get(ch)%4) + abs(id//4 - goalDict.get(ch)//4)) - (abs(pzid%4 - goalDict.get(ch)%4) + abs(pzid//4 - goalDict.get(ch)//4))
            openSet[currF+inc+1].append((n[0], manhatten+inc))
    #working solution
    while True:
        manhatten = openSet[0][2]
        puzzle = openSet[0][1]
        fin = openSet[0][0] - manhatten
        removeMin(openSet)
        if puzzle in closedSet:
            continue
        closedSet[puzzle] = fin
        if(puzzle == goal):
            return shortestastarpath(closedSet, root, goal)
        for n in neighbors(puzzle):
            nManhatten = h(n, goal)
            addMin(openSet, (fin+1+nManhatten, n, nManhatten)) 

def shortestastarpath(path, root, goal):
    shortest = []
    current = goal
    while current!=root:
        shortest.append(current)
        possibleNext = neighbors(current).intersection(path.keys())
        for neigh in possibleNext:
            if path.get(neigh)==path.get(current)-1:
                current = neigh
                break
    shortest.append(root)
    return shortest[::-1]

def run():
    goal = allPuzzles[0]
    #print(astar(allPuzzles[8], goal))
    #return
    global goalDict
    goalDict = {val:i for i, val in enumerate(goal)}
    for puzzle in allPuzzles:
        path = astar(puzzle, goal)
        compactifyPath(puzzle, path)
run()
#Abhisheik Sharma 7 2024

