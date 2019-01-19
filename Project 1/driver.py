#8-Piece Puzzle 
#Name : Syed Rabbi
#Course : Artificial Intelligence Micromaster

import resource
import heapq as hpq
import sys
import numpy as np
from collections import deque
import time as tt




#definition
goal = [0,1,2,3,4,5,6,7,8]



#Code that presents the board in a visual
def mat2(boards): 
    boards = np.array(boards)
    if(len(boards)!=9):
        for board in boards:
            print(np.reshape(board,(3,3)))
    else:
        print(np.reshape(boards,(3,3)))



#Defining nodes Up
def Up(node):
    child_board = node.state[:]
    i = child_board.index(0)
    child_board[i],child_board[i-3] = child_board[i-3],child_board[i]
    return(nwNode(child_board,node,'Up',node.depth+1))

#Defining nodes Down    
def Down(node):
    child_board = node.state[:]
    i = child_board.index(0)
    child_board[i],child_board[i+3] = child_board[i+3],child_board[i]
    return(nwNode(child_board,node,'Down',node.depth+1))

#Defining nodes Left
def Left(node):
    child_board = node.state[:]
    i = child_board.index(0)
    child_board[i],child_board[i-1] = child_board[i-1],child_board[i]
    return(nwNode(child_board,node,'Left',node.depth+1))

#Defining nodes Right
def Right(node):
    child_board = node.state[:]
    i = child_board.index(0)
    child_board[i],child_board[i+1] = child_board[i+1],child_board[i]
    return(nwNode(child_board, node, 'Right', node.depth+1))



#U-D-L-R (up & down & left & right)
def Gt2Children(node): 
    board = node.state[:]
    pos = board.index(0)
    output=[]
    
    #Creating a series of if statements
    #if pos = 0
    if(pos == 0):
        output = [Down(node), Right(node)]
    #if pos = 1  
    if(pos == 1):
        output = [Down(node), Left(node), Right(node)]
     #if pos = 2     
    if(pos == 2):
        output = [Down(node), Left(node)]
    #if pos = 3     
    if(pos == 3):
        output = [Up(node), Down(node), Right(node)]
    #if pos = 4        
    if(pos == 4):
        output = [Up(node), Down(node), Left(node), Right(node)]
    #if pos = 5         
    if(pos == 5):
        output = [Up(node), Down(node), Left(node)]
    #if pos = 6     
    if(pos == 6):
        output = [Up(node), Right(node)]
    #if pos = 7       
    if(pos == 7):
        output = [Up(node), Left(node), Right(node)]
    #if pos = 8     
    if(pos == 8):
        output = [Up(node), Left(node)]
        
    return(output)



#...................
     #prints both child and parent boards
def checkState(board):
    print( "Parent board is (current state):")
    mat2(board)
    print( "Children boards are:")
    mat2(Gt2Children(board))

 

# definition
def goalTest(state):
    return(state ==goal)

def getPath(node):
    path = []
    
    while(node.parent != None):
        path.append(node.move)
        node = node.parent
    
    path = path[::-1]
    return(path)



class Node:
    def __init__(self, state, parent, move,depth):
        self.state = state
        self.parent = parent
        self.move = move #direction
        self.depth = depth
        self.cost = 0
    
def nwNode( state, parent, move, depth):
    return Node( state, parent, move, depth )




class Frontier:
    def __init__(self):
        self.myqueue = deque()
        self.myset = set()
    
    def enq2(self, node):
        self.myqueue.append(node)
        self.myset.add(str(node.state))
    
    def deq2(self):
        node = self.myqueue.popleft()
        self.myset.discard(str(node.state))
        return(node)
    
    def search(self, node):
        return(str(node.state) in self.myset)
    
    def size(self):
        return(len(self.myset))

    def push(self,node):
        self.myqueue.append(node)
        self.myset.add(str(node.state))
    
    def pop(self):
        node = self.myqueue.pop()
        self.myset.discard(str(node.state))
        return(node)




class Explored:
    def __init__(self):
        self.myset = set() 
    
    def add(self,node):
        self.myset.add(str(node.state))
        
    def search(self, node):
        return(str(node.state) in self.myset)
    
    def size(self):
        return(len(self.myset))



def solverBFS(board):
    start = tt.time()
    nodesExpanded = -1
    FrontierBFS = Frontier()
    ExploredBFS = Explored()

    root = nwNode(board, None, None, 0)
    FrontierBFS.enq2(root)

    while(FrontierBFS.size() != 0):
        node = FrontierBFS.deq2()
        nodesExpanded += 1
        ExploredBFS.add(node)


        if(goalTest(node.state) == True):
            path = getPath(node)
            break

        else:
            children = Gt2Children(node)
            for child in children:
                if (ExploredBFS.search(child) == False and FrontierBFS.search(child) == False):
                    FrontierBFS.enq2(child)

    end = tt.time()
    diff = end - start
    ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    
    writeOutput(path, nodesExpanded, node, child.depth, diff, ram)



def solverDFS(board):
    start = tt.time()
    nodesExpanded = -1
    maxDepth = 0
    FrontierDFS = Frontier()
    ExploredDFS = Explored()

    root = nwNode(board, None, None, 0)
    FrontierDFS.push(root)

    while(FrontierDFS.size() !=0):
        node = FrontierDFS.pop()
        nodesExpanded +=1
        ExploredDFS.add(node)


        if(goalTest(node.state) == True):
            path = getPath(node)
            break

        else:
            children = Gt2Children(node)[::-1]
            for child in children:
                if (ExploredDFS.search(child) == False and FrontierDFS.search(child) == False):
                    if(maxDepth < child.depth):
                        maxDepth += 1
                    FrontierDFS.push(child)
    end = tt.time()
    diff = end - start
    ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    writeOutput(path, nodesExpanded, node, maxDepth, diff,ram)


#heuristic distance
def sp(node): 
    board = node.state
    dist = 0
    for i in range(len(board)):
        xGoal = int(i/3)
        yGoal = i % 3
        pos = board.index(i)
        xBoard = int(pos/3)
        yBoard = pos%3
        dist += abs(xGoal - xBoard) + abs(yGoal - yBoard)
        
    return dist

def gx(node):
    return(len(getPath(node)))

class Front:
    def __init__(self):
        self.myheap = []
        self.myset = set()
    
    def __getitem__(self):
        return self.myheap
    
    def insert(self, node):
        hpq.heappush(self.myheap, (node.cost, node))
        self.myset.add(str(node.state))
    
    def deleteMin(self):
        _,node = hpq.heappop(self.myheap)
        self.myset.discard(str(node.state))
        return(node)
    
    def size(self):
        return(len(self.myheap))
    
    def search(self, node):
        return(str(node.state) in self.myset)
    
    def getIndex(self,node):
        return(h)



def solution(board):
    start = tt.time()
    nodesExpanded = -1
    maxDepth = 0
    lenF = []
    FrontierA = Front()
    ExploredA = Explored()

    root = nwNode(board, None, None, 0)
    FrontierA.insert(root)

    while(FrontierA.size() != 0):
        node = FrontierA.deleteMin()
        nodesExpanded += 1
        ExploredA.add(node)


        if(goalTest(node.state) == True):
            path = getPath(node)
            break

        else:
            children = Gt2Children(node)[::-1]
            for child in children:
                child.cost = sp(child) + gx(child)
                if (ExploredA.search(child) == False and FrontierA.search(child) == False):
                    if(maxDepth < child.depth):
                        maxDepth += 1
                    FrontierA.insert(child)
                else:
                    for i in range(len(FrontierA.myheap)):
                        curNode = FrontierA.myheap[i]
                        if(curNode[1] == child and curNode[0] > child.cost):
                            FrontierA.myheap[i] = (child.cost,child)
                            hpq.heapify(FrontierA.myheap)

    end = tt.time()
    diff = end - start
    ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    writeOutput(path, nodesExpanded, node, maxDepth, diff, ram)

#defining output
def writeOutput(path, nodesExpanded, node, maxDepth, diff, ram):
    myfile = open("output.txt", "w")
    
    myfile.write("path_to_goal: " + str(path) + "\n")
    myfile.write("cost_of_path: " + str(len(path)) + "\n")
    myfile.write("nodes_expanded: " + str(nodesExpanded) + "\n")
    myfile.write("search_depth: " + str(node.depth) + "\n")
    myfile.write("max_search_depth: " + str(maxDepth) +"\n")
    myfile.write("running_time: " + str(diff) + "\n")
    myfile.write("max_ram_usage:" + str(ram/(1024 * 1024)) + "\n")
    
    myfile.close()



def main():
    input_u = sys.argv
    algo = input_u[1]
    board = input_u[2].split(',')
    board = [int(i) for i in board]
    
    if (algo == 'bfs'):
        print("Solving puzzle BFS method: ... ")
        solverBFS(board)
        
    if(algo == 'dfs'):
        print("Solving puzzle DFS method: ... ")
        solverDFS(board)
    
    if(algo == 'ast'):
        print( "Solving puzzle AStar method: ... " )
        solution(board)

    print( "Puzzle Solved - Check output.txt for result")

main()

