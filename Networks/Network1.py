import sys; args = sys.argv[1:]
import random



def classical(nodes, edges):
    return

def incremental(nodes, edges):
    return 

def main():
    global NETWORK
    NETWORK = {}
    if args[1].upper() == 'C':
        classical(args[2], args[0]*args[2])
    else: incremental(args[2], args[0]*args[2])  

#Abhisheik Sharma 7 2024