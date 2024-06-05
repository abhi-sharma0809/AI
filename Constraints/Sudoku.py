import sys; args = sys.argv[1:]
from time import perf_counter
with open(args[0]) as f:
    allPuzzles = [line.strip() for line in f]
def setGlobals(pz, symbolSet, puzLen, sideLen):
    global setOfChoices, subBlocks, dotIndex, original, csDict, lstSubBlocks, STATS, PZ, SL
    PZ = puzLen
    SL = int(sideLen)
    rChoices = [{r for r in range(i*SL,(i+1)*SL)} for i in range(SL)]
    cChoices = [{c for c in range(i, PZ, SL)} for i in range(SL)]
    setOfChoices = symbolSet
    dimLst = [[i, SL//i] for i in range(1, SL+1) if (SL%i==0)]
    dim = dimLst[len(dimLst)//2]
    gWIDTH, gHEIGHT = dim[0], dim[1]
    subBlocks = [{bR + bCO + r * SL + c for r in range(gHEIGHT) for c in range(gWIDTH)} for bR in range(0, PZ, gHEIGHT * SL) for bCO in range(0, SL, gWIDTH)]
    subBlocks += rChoices
    subBlocks += cChoices
    dotIndex = {}
    csDict = {i:[] for i in range(PZ)}
    for i in range(PZ):
        for k in range((SL*3)):
            if i in subBlocks[k]:
                csDict[i].append(k)
    original = pz
    lstSubBlocks = [list(subBlocks[i]) for i in range(SL*3)]
    STATS = set()

def updateStats(message):
    STATS.add(message)

def printFormat(pz):
    for i in range(0,81,9):
        print(pz[i:i+9])

def isInvalid(pz):
    check = dotIndex.get(pz)
    if pz == original:
        for i in range(1, 81):
            for k in range(i):
                if pz[i] != '.' and pz[i] == pz[k]:
                    for subset in subBlocks:
                        if i in subset and k in subset:
                            return True
        return False
    
    for j in csDict.get(check):
        for num in lstSubBlocks[j]:
            if num != check and pz[num]==pz[check]:
                return True
    return False

def forwardTrace(pz):
    traverseList = []
    traverseSet = set()
    for k in range(PZ):
        if len(pz.get(k))==1:
            traverseList.append(k)
            traverseSet.add(k)
    for i in traverseList:
        found = pz.get(i)
        for j in csDict.get(i):
            for num in lstSubBlocks[j]:
                if num != i:
                    pz[num]=pz.get(num).replace(found,'')
                    if len(pz.get(num))==1 and num not in traverseSet:
                        traverseList.append(num)
                        traverseSet.add(num)
                        pz[PZ]=pz.get(PZ)-1
                    if len(pz.get(num))==0:
                        return None
    return pz 

def constraintLook(pz):
    traverseSet = set()
    for k in range(PZ):
        if len(pz.get(k))==1:
            traverseSet.add(k)
    for cs in subBlocks:
        for val in setOfChoices:
            valInd = []
            for ind in cs:
                if val in pz.get(ind):
                    valInd.append(ind)
            if len(valInd) == 1:
                pz[valInd[0]]=val 
                if valInd[0] not in traverseSet:
                    pz[PZ]=pz.get(PZ)-1
                    traverseSet.add(valInd[0])
    return pz
       
def isFinished(pz):
    #return sum(len(pz.get(i)) for i in range(PZ))==PZ
    return pz.get(PZ)==0 or pz.get(PZ)==-1

def mostConstrained(pz):
    min = SL
    minInd = 0
    for i in range(PZ):
        if len(pz.get(i))==2:
            return i
        if 1<len(pz.get(i))<min:
            min = len(pz.get(i))
            minInd = i
    return minInd
    #choices = [(len(pz.get(i)),i) for i in range(81) if len(pz.get(i))>1]
    #return 0 if len(choices)==0 else min(choices)[1]

    
def bruteForce(pz):
    if isFinished(pz):
        return pz
    pz = constraintLook(pz)
    i = mostConstrained(pz)
    choices = pz.get(i)
    pz[PZ]=pz.get(PZ)-1  
    for ch in choices:
        subPz = pz.copy()
        subPz[i]=subPz.get(i).replace(choices, ch)
        bF = forwardTrace(subPz)
        if bF:
            result = bruteForce(bF)
            if result:
                return result
                    
    return None

def checkSum(pz):
    min = ord(pz[0])
    for ch in pz:
        asci = ord(ch)
        if asci < min:
            min = asci
    return sum((ord(char)-min) for char in pz)

def main():
    ovrTime = perf_counter()
    for i in range(len(allPuzzles)):
        og = allPuzzles[i]
        puzLen = len(og)
        sideLen = puzLen**(1/2)
        setOfChoices = {*"ABCDEFGHIJKLMNOPQRSTUVWQYZ"}
        symbolSet = set()
        pzl = {}
        dotCount = 0
        for k in range(puzLen):
            if og[k] == '.':
                pzl[k]='123456789'
                dotCount += 1
            else:
                pzl[k] = og[k]
                symbolSet.add(og[k])
        while(len(symbolSet) != sideLen): symbolSet.add(setOfChoices.pop())
        allChoicesStr = "".join(list(symbolSet))
        for key in pzl.keys():
            if len(pzl.get(key))>1:
                pzl[key]=allChoicesStr
        pzl[puzLen]=dotCount
        time = perf_counter()
        num = str(i+1)
        setGlobals(pzl, symbolSet, puzLen, sideLen)
        print(f"{i+1}: {allPuzzles[i]}")
        sol = bruteForce(pzl)
        solString = "".join([sol.get(key) for key in range(puzLen)])
        print(f" {' '*len(num)} {solString} {checkSum(solString)} {float('%.3g' % (perf_counter()-time))}s")
    print(f"{float('%.3g' % (perf_counter()-ovrTime))}s")

main()
#Abhisheik Sharma 7 2024