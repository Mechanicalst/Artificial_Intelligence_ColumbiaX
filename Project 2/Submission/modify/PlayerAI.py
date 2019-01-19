import math as Mt
import time as TT1
import numpy as np
from random import randint
from BaseAI import BaseAI



class PlayerAI(BaseAI):
	def __init__(self):
		self.prevTime = 0

	def getMove(self, grid):
		self.prevTime = TT1.clock()
		Depth = 3
		cur_node = Node(grid)
        
        #Defining Rem_child
		(Rem_child, _) = self.Max_zer(cur_node, float('-Inf'), float('Inf'), Depth)
		return(Rem_child.move)

#defining the Min_zer function
	def Min_zer(self, cur_node, phi, gamma, Depth):
		rem_Nodes = self.get_rem_Nodes(cur_node, max = True)
        #max = true
        
		if(self.Exceeds1(rem_Nodes) or Depth == 0):
			return((None, Eval(cur_node)))	
            # Time

		(minimumChild, minimumUtility) = (None, float('inf'))		
      
		for Rem_child in rem_Nodes:
			(_,utility) = self.Max_zer(Rem_child, phi, gamma, Depth - 1)
			if(utility < minimumUtility):
				(minimumChild, minimumUtility) = (Rem_child, utility)
            
			if(minimumUtility <= phi):
				break

			if(minimumUtility < gamma):
				gamma = minimumUtility

		return (minimumChild, minimumUtility)

#defining the Max_zer function
	def Max_zer(self, cur_node, phi, gamma, Depth):
		rem_Nodes = self.get_rem_Nodes(cur_node, max = True)
		
        #Creating conditions for Time.clock()- self.prevTime being > .2 ...or
		if(self.Exceeds1(rem_Nodes) or Depth == 0):  
			return((None, Eval(cur_node)))	

		(maximumChild, maximumUtility) = (None, float('-Inf'))

		for Rem_child in rem_Nodes:
			(_, utility) = self.Min_zer(Rem_child, phi, gamma, Depth - 1)
            
        #Condtion for utility > maximumUtility    
			if(utility > maximumUtility):
				(maximumChild, maximumUtility) = (Rem_child, utility)

			if(maximumUtility >= gamma):
				break

			if(maximumUtility > phi):
				phi = maximumUtility

		return (maximumChild, maximumUtility)
	
#defining the get_rem_Nodes function
	def get_rem_Nodes(self, cur_node, max):
		grid = cur_node.grid
		rem_Nodes = []

		if max:
			moveset = grid.getAvailableMoves()
			for moves in moveset:
				chosen_grid = grid.clone()
				chosen_grid.move(moves)
				nw_Node = Node(chosen_grid, moves)
				rem_Nodes.append(nw_Node)

		else:
			avlbl_cells = grid.getAvailableCells()
			if not (Board_filled(avlbl_cells)):
				for cell in avlbl_cells:
					for val in [2, 4]:
						chosen_grid = grid.clone()
						chosen_grid.setCellValue(cell, val)
						nw_Node = Node(chosen_grid, None)
						rem_Nodes.append(nw_Node)

		rem_Nodes.sort(key = Eval)			

		return(rem_Nodes)

	def Exceeds1(self, rem_Nodes):
		if(len(rem_Nodes)) == 0:
			Exceeds1 = True

	def Board_filled(self, avlbl_cells):
		return(len(avlbl_cells) == 0)

class Node():
	def __init__(self, grid, move = None):
		self.grid = grid
		self.move = move
    		#In this case, self.util is set equal to None

def maxTileCorn(cur_node):
	maximum_Tile = cur_node.grid.getMaxTile()
	istrue = cur_node.grid.map[3][3] == maximum_Tile
	return 1 if istrue else 0
 

def monotonic(grid):
    z = .5
    z1 = 0
    z2 = 0
    i = 0
    
    psu_matr = [3, 2, 1, 0]
    	
    
    for x in xrange(3,-1,-1):
        for y in xrange(0, 4):
            if(x ==2 or x == 0):
                y=psu_matr[y]
            z1+= grid.map[x][y]*pow(z, i)
            i += 1
    i = 0
     
    for y in xrange(0, 4, 1):
        for x in xrange(0, 4, 1):
            if(y == 2 or y == 0):
                x=psu_matr[x]
            z2+= grid.map[x][y]*pow(z, i)
            i += 1

    return(max(z1, z2))
     
            
            

#defining the Precision_ grid
def Precision_(grid):
    #in order to make this count minimized
	In_eQual = 0

	In_eQual += abs(grid.map[0][0]-grid.map[0][1]) + abs(grid.map[0][1]-grid.map[0][2]) + abs(grid.map[0][2]-grid.map[0][3])
	In_eQual += abs(grid.map[1][0]-grid.map[1][1]) + abs(grid.map[1][1]-grid.map[1][2]) + abs(grid.map[1][2]-grid.map[1][3])
	In_eQual += abs(grid.map[2][0]-grid.map[2][1]) + abs(grid.map[2][1]-grid.map[2][2]) + abs(grid.map[2][2]-grid.map[2][3])
	In_eQual += abs(grid.map[3][0]-grid.map[3][1]) + abs(grid.map[3][1]-grid.map[3][2]) + abs(grid.map[3][2]-grid.map[3][3])

	In_eQual += abs(grid.map[0][0]-grid.map[1][0]) + abs(grid.map[1][0]-grid.map[2][0]) + abs(grid.map[2][0]-grid.map[3][0])
	In_eQual += abs(grid.map[0][1]-grid.map[1][1]) + abs(grid.map[1][1]-grid.map[2][1]) + abs(grid.map[2][1]-grid.map[3][1])
	In_eQual += abs(grid.map[0][2]-grid.map[2][1]) + abs(grid.map[1][2]-grid.map[2][2]) + abs(grid.map[2][2]-grid.map[3][2])
	In_eQual += abs(grid.map[0][3]-grid.map[3][1]) + abs(grid.map[1][3]-grid.map[3][3]) + abs(grid.map[2][3]-grid.map[3][3])

	return(Mt.log(In_eQual, 2))

#defining the Count_merger grid
def Count_merger(grid):
	Summation = 0
	psu_matr = []
	for x in xrange(0, 3):
		for y in xrange(0, 3):
			if grid.map[x][y]!= 0:
				psu_matr.append(grid.map[x][y])
		if(len(psu_matr) > 0):
			for i in xrange(len(psu_matr) - 1):
				if psu_matr[i]==psu_matr[i + 1]:
					Summation+= 1

	for y in xrange(0, 3):
		for x in xrange(0, 3):
			if grid.map[x][y]!= 0:
				psu_matr.append(grid.map[x][y])

		if(len(psu_matr) > 0):
			for i in xrange(len(psu_matr)-1):
				if psu_matr[i]==psu_matr[i + 1]:
					Summation+= 1

	return Summation

#defining Eval
def Eval(cur_node):
    grid = cur_node.grid
    
    z_Max_zer = 2
    z_MRG = 2
    z_pn = 8
    z_sh = -4
    z_tic = 10
    z_edge = 5


    maximum_Tile = grid.getMaxTile()
    Tile_corner = maxTileCorn(cur_node)
    avlbl_cells = len(grid.getAvailableCells())
    func_smooth = Precision_(grid)
    func_monotonic = monotonic(grid)
    func_merger = Count_merger(grid)
    
    return z_tic*func_monotonic + z_pn*avlbl_cells+ z_Max_zer*Mt.log(maximum_Tile,2) +z_sh*func_smooth + z_edge*Tile_corner + z_MRG*func_merger 