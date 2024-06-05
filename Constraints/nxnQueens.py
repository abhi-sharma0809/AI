import sys; args = sys.argv[1:]

PZ = 81
SL = 9
rChoices = [{r for r in range(i*SL,(i+1)*SL)} for i in range(SL)]
cChoices = [{c for c in range(i, PZ, SL)} for i in range(SL)]
gWIDTH, gHEIGHT = 3, 3
subBlocks = [{bR + bCO + r * SL + c for r in range(gHEIGHT) for c in range(gWIDTH)} for bR in range(0, PZ, gHEIGHT * SL) for bCO in range(0, SL, gWIDTH)]
subBlocks += rChoices
subBlocks += cChoices

setOfChoices = {'1', '2', '3', '4', '5', '6', '7', '8', '9'}

def isInvalid(pz):
    for i in range(1, 81):
        for k in range(i):
            if pz[i] != '.' and pz[i] == pz[k]:
                for blocks in subBlocks:
                    if i in blocks and k in blocks:
                        return True
    return False

def allChoices(pz):
    for i in range(len(pz)):
        if pz[i] == '.':
            choices = set()
            for choice in setOfChoices:
                subPz = list(pz[:]); subPz[i] = choice
                subPz = "".join(subPz)
                choices.add(subPz)
            return choices
    return set()

def isFinished(pz):
    return pz.find('.')==-1

def bruteForce(pz):
    if isInvalid(pz):
        return ''
    if isFinished(pz):
        return pz
    for subPzl in allChoices(pz):
        bF = bruteForce(subPzl)
        if bF:
            return bF
    return ''


if args:
    print(bruteForce(args[0]))
else:
    print(bruteForce('.'*24))
#.................................................