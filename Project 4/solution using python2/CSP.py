#import commands
from copy import deepcopy, copy
from CSP import *

#creating QUEUE
class QUEUE:
    
    #implementing
    
    def is_empt(self):
        return len(self.queue) == 0
    
    def deQ(self):
        return self.queue.pop(0)

    def __len__(self):
        return len(self.queue)
    
    def enQ(self, e):
        self.queue.append(e)

    def __init__(self):
        self.queue = []

#creating CSP
class CSP:
    
    def __init__(self, domain, bin_constrnt, unassigned_vars):
        
        self.domain = domain
        self.bin_constrnt = bin_constrnt
        self.unassigned_vars
        self.empty

    def getNeighbors(self):
        raise NotImplementedError

    def getUnassignedVariables(self):
        raise NotImplementedError

    def assignVariable(self, var, Value):
        raise NotImplementedError

    def checkConsistency(self):
        raise NotImplementedError

def AC3(csp):

    queue = QUEUE()
    queue.queue = list(csp.bin_constrnt)

    while not queue.is_empt():
        (Xi, Xj) = queue.deQ()
        if Revise(csp, Xi, Xj):
            if len(csp.domain[Xi]) == 0:
                return False
            for Xk in csp.getNeighbors(Xi, Xj):
                queue.enQ((Xk, Xi))
           
    return True

def Revise(csp, Xi, Xj):

    revised = False
    for x in csp.domain[Xi]:
        canSatisfy = False
        for y in csp.domain[Xj]:
            if x != y:
                canSatisfy = True
                break
        if not canSatisfy:
            csp.domain[Xi].remove(x)
            revised = True
    return revised

def forwCheck(csp, var, Value):

    Variables = list(csp.getUnassignedVariables())
    if var in Variables:
        Variables.remove(var)

    for v in Variables:
        for val in list(csp.domain[v]):
            csp.assignVariable(v, val)
            if not csp.checkConsistency():
                csp.domain[v].remove(val)
            if len(csp.domain[v]) == 0:
                return False
        if len(csp.domain[v]) == 1:
            csp.assignVariable(v, csp.domain[v][0])
        else:
            csp.assignVariable(v, csp.empty)

    return True

def BacktrackingSearch(csp):

    return back_trk({}, csp)


def back_trk(assignment, csp, inference = forwCheck):

    
    Variables = list(csp.getUnassignedVariables())
    for key in assignment.keys():
        if key in Variables:
            Variables.remove(key)


    # Completion of Assignment
    if len(Variables) == 0:
        return assignment

    # next variable to be Picked and assign making use of MRV heuristic
    maxD = float('Inf')
    var = None
    for v in Variables:
        if len(csp.domain[v]) < maxD:
            maxD = len(csp.domain[v])
            var = v

    
    for Value in csp.domain[var]:
        cspTemp = deepcopy(csp)
        cspTemp.assignVariable(var, Value)
        cspTemp.unassigned_vars.remove(var)
        if cspTemp.checkConsistency():
            assignment[var] = Value
            inferences = []
            if inference(cspTemp, var, Value):
                for v in list(cspTemp.getUnassignedVariables()):
                    if len(cspTemp.domain[v]) == 1:
                        assignment[v] = cspTemp.domain[v][0]
                        inferences.append(v)

                result = back_trk(assignment, cspTemp)
                if result != False:
                    return result

            
            assignment.pop(var, None)
            for v in inferences:
                assignment.pop(v, None)

    return False

