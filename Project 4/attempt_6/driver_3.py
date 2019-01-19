# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 15:03:40 2018

@author: st
"""

#tree search

function Tree-Search(initialState, goalTest)
    returns Success or Failure:
        
        inialize frontier with initialState
        
        while not frontier.isEmpty():
            state = frontier.remove()
            
            if goalTest(state):
                return Success(state)
            
            for neighbor in state.neighbors():
                frontier.add(neighbor)
                
        return Failure
    
#Graph search
        
    function Graph-Search(intialState, goalTest):
        returns Success or Failure:
            
            initialize frontier with initialState
            explored = Set.new()
            
            while not frontier.isEmpty():
                state = frontier.remove()
                explored.add(state)
                
                if goalTest(state):
                    return Success(state)
                
                for neighbor in state.neighbors():
                    if neighbor not in frontier Union explored:
                        frontier.add(neighbor)
                        
            return Failure

#Breadth First Search
    function Breadth-First-Search(intialState, goalTest):
        returns Success or Failure:
            
            frontier = Queie.new(initialState)
            explored = Set.new()
            
            while not frontier.isEmpty():
                state = frontier.dequeue()
                explored.add(state)
                
                if goalTest(state):
                    return Success(state)
                
                for neighbor in state.neighbors():
                    if neighbor not in frontier Union explored:
                        frontier.enqueue(neighbor)
                        
            return Failure

#