# -*- coding: utf-8 -*-
"""
Created on Sun Oct 14 03:24:35 2018

@author: st
"""

import math
import time
import numpy as np
from random import randint
from BaseAI import BaseAI



class PlayerAI(BaseAI):
	def __init__(self):
		self.prevTime = 0

	def getMove(self, grid):
		self.prevTime = time.clock()
		Depth = 3
		cur_node = Node(grid)
        
        #Defining child
		(child, _) = self.maximize(cur_node, float('-Inf'), float('Inf'), Depth)
		return(child.move)

#defining the minimize function
	def minimize(self, cur_node, phi, gamma, Depth):
		children = self.getChildren(cur_node, max = True)
        #max = true
        
		if(self.isOver(children) or Depth == 0):
			return((None, Eval(cur_node)))	
            # Time

		(minimumChild, minimumUtility) = (None, float('inf'))		
      
		for child in children:
			(_,utility) = self.maximize(child, phi, gamma, Depth - 1)
			if(utility < minimumUtility):
				(minimumChild, minimumUtility) = (child, utility)
            
			if(minimumUtility <= phi):
				break

			if(minimumUtility < gamma):
				gamma = minimumUtility

		return (minimumChild, minimumUtility)

#defining the maximize function
	def maximize(self, cur_node, phi, gamma, Depth):
		children = self.getChildren(cur_node, max = True)
		
        #Creating conditions for time.clock()- self.prevTime being > .2 ...or
		if(self.isOver(children) or Depth == 0):  
			return((None, Eval(cur_node)))	

		(maximumChild, maximumUtility) = (None, float('-Inf'))

		for child in children:
			(_, utility) = self.minimize(child, phi, gamma, Depth - 1)
            
        #Condtion for utility > maximumUtility    
			if(utility > maximumUtility):
				(maximumChild, maximumUtility) = (child, utility)

			if(maximumUtility >= gamma):
				break

			if(maximumUtility > phi):
				phi = maximumUtility

		return (maximumChild, maximumUtility)
	
#defining the getChildren function
	def getChildren(self, cur_node, max):
		grid = cur_node.grid
		children = []

		if max:
			moveset = grid.getAvailableMoves()
			for moves in moveset:
				chosen_grid = grid.clone()
				chosen_grid.move(moves)
				nw_Node = Node(chosen_grid, moves)
				children.append(nw_Node)

		else:
			avlbl_cells = grid.getAvailableCells()
			if not (isBoardfull(avlbl_cells)):
				for cell in avlbl_cells:
					for val in [2, 4]:
						chosen_grid = grid.clone()
						chosen_grid.setCellValue(cell, val)
						nw_Node = Node(chosen_grid, None)
						children.append(nw_Node)

		children.sort(key = Eval)			

		return(children)

	def isOver(self, children):
		if(len(children)) == 0:
			isOver = True

	def isBoardfull(self, avlbl_cells):
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
	
	l = [3, 2, 1, 0]
	
	for x in xrange(3,-1,-1):
	    for y in xrange(0, 4):
	        if(x ==2 or x == 0):
	            y=l[y]
	        z1+= grid.map[x][y]*pow(z, i)
	        i += 1


	i = 0 
	for y in xrange(0, 4, 1):
	    for x in xrange(0, 4, 1):
	    #for any x in the predefined range(3,-1,-1):
	    	if(y == 2 or y == 0):
	        	x=l[x]
	        z2+= grid.map[x][y]*pow(z, i)
	        i += 1

	return(max(z1, z2))

#defining the Smoothness grid
def Smoothness(grid):
    #in order to make this count minimized
	dfrnce = 0

	dfrnce += abs(grid.map[0][0]-grid.map[0][1]) + abs(grid.map[0][1]-grid.map[0][2]) + abs(grid.map[0][2]-grid.map[0][3])
	dfrnce += abs(grid.map[1][0]-grid.map[1][1]) + abs(grid.map[1][1]-grid.map[1][2]) + abs(grid.map[1][2]-grid.map[1][3])
	dfrnce += abs(grid.map[2][0]-grid.map[2][1]) + abs(grid.map[2][1]-grid.map[2][2]) + abs(grid.map[2][2]-grid.map[2][3])
	dfrnce += abs(grid.map[3][0]-grid.map[3][1]) + abs(grid.map[3][1]-grid.map[3][2]) + abs(grid.map[3][2]-grid.map[3][3])

	dfrnce += abs(grid.map[0][0]-grid.map[1][0]) + abs(grid.map[1][0]-grid.map[2][0]) + abs(grid.map[2][0]-grid.map[3][0])
	dfrnce += abs(grid.map[0][1]-grid.map[1][1]) + abs(grid.map[1][1]-grid.map[2][1]) + abs(grid.map[2][1]-grid.map[3][1])
	dfrnce += abs(grid.map[0][2]-grid.map[2][1]) + abs(grid.map[1][2]-grid.map[2][2]) + abs(grid.map[2][2]-grid.map[3][2])
	dfrnce += abs(grid.map[0][3]-grid.map[3][1]) + abs(grid.map[1][3]-grid.map[3][3]) + abs(grid.map[2][3]-grid.map[3][3])

	return(math.log(dfrnce, 2))

#defining the Count_merger grid
def Count_merger(grid):
	total = 0
	l = []
	for x in xrange(0, 3):
		for y in xrange(0, 3):
			if grid.map[x][y]!= 0:
				l.append(grid.map[x][y])
		if(len(l) > 0):
			for i in xrange(len(l) - 1):
				if l[i]==l[i + 1]:
					total+= 1

	for y in xrange(0, 3):
		for x in xrange(0, 3):
			if grid.map[x][y]!= 0:
				l.append(grid.map[x][y])

		if(len(l) > 0):
			for i in xrange(len(l)-1):
				if l[i]==l[i + 1]:
					total+= 1

	return total

#defining Eval
def Eval(cur_node):
    grid = cur_node.grid
    
    z_open = 8
    z_smooth = -4
    z_monotonic = 10
    z_corner = 5
    z_max = 2
    z_merger = 2

    maximum_Tile = grid.getMaxTile()
    Tile_corner = maxTileCorn(cur_node)
    avlbl_cells = len(grid.getAvailableCells())
    func_smooth = Smoothness(grid)
    func_monotonic = monotonic(grid)
    func_merger = Count_merger(grid)
    
    return z_monotonic*func_monotonic + z_open*avlbl_cells+ z_max*math.log(maximum_Tile,2) +z_smooth*func_smooth + z_corner*Tile_corner + z_merger*func_merger 