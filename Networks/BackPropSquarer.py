import sys; args = sys.argv[1:]
import math

def setGlobals():
    global WEIGHTS, LAYERS, OLDLAYERS, INEQ, RADIUS
    filename = open(args[0])
    #for line in filename: print(line)
    WEIGHTS = [[float(i) for i in wLine.strip().split(',')] for wLine in filename if '# Weights file' not in wLine]
    LAYERS = [2]
    for weightlayer in WEIGHTS:
        LAYERS.append(len(weightlayer)//LAYERS[-1])
    OLDLAYERS = LAYERS
    print(OLDLAYERS)
    LAYERS = [i*2 for i in LAYERS]
    LAYERS[0], LAYERS[-1] = 3, 1
    LAYERS.append(1)
    eqn = args[1].strip()
    INEQ = ['>','<']['<' in eqn]
    RADIUS = 0
    if '=' in eqn:
       RADIUS = (float(eqn[:][9:])**.5)
    else:
        RADIUS = (float(eqn[:][8:])**.5)
    WEIGHTS[0]=[weight/RADIUS for weight in WEIGHTS[0]]


def makeNewWeights():
    newWeights = []
    for i in range(len(WEIGHTS)-1):
        layer = []
        for k in range(2):
            if i == 0:
                for j in range(OLDLAYERS[1]):
                    if k == 0:
                        layer = layer + [WEIGHTS[0][j*2], 0, WEIGHTS[0][(j*2)+1]]
                    if k == 1:
                        layer = layer + [0, WEIGHTS[0][j*2], WEIGHTS[0][(j*2)+1]]
            else:
                curr = OLDLAYERS[i]
                for j in range(OLDLAYERS[i+1]):
                    if k == 0:
                        layer = layer + WEIGHTS[i][j*curr:(j*curr)+curr] + [0]*curr
                    if k == 1:
                        layer = layer + [0]*curr + WEIGHTS[i][j*curr:(j*curr)+curr] 
        newWeights.append(layer)
    if INEQ =='>': newWeights.append(WEIGHTS[-1]*2)
    else: newWeights.append([WEIGHTS[-1][0]*-1]*2)
    if INEQ == '>': newWeights.append([(1+math.e)/(2*math.e)])
    else: newWeights.append([1.85914])
    return newWeights





def main():
    setGlobals()
    newWeights = makeNewWeights()
    print(f'Layer counts:', ' '.join([str(x) for x in LAYERS]))
    for layer in newWeights:
        string = ''
        for k in layer:
            string = string + str(k) + " "
        print(string)
main()

#Abhisheik Sharma 7 2024 