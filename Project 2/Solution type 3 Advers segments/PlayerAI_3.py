#Importing libraries
import time as TtM

#from imports
from math import log2 as LG2
from itertools import product as ProD
from BaseAI_3 import BaseAI as BAI
from collections import Counter as CNT
import random as RND_

#defining heuristic class
class Heuristic:
    def __init__(self):
        self.weights = [1.033, 3.012, 0.261, 2.73, 0.76, 3.51]

    def __call__(self, grid):
        #Assigning placeholder vars 
        Var_1 = LG2(grid.getMaxTile())
        Var_2 = len(grid.getAvailableCells())
        Var_3 = len(grid.getAvailableMoves())
        Var_4, Var_5 = self.Prec1_2Gether(grid)
        Var_6 = self.Mono_tone(grid)
        #Vector of feats
        Vec_Feat = [Var_1, Var_2, Var_3, Var_4, Var_5, Var_6]
        Var_10 = 0
        
        #Creating Var10 fir future use
        for PL_1, PL_2 in zip(self.weights, Vec_Feat):
            Var_10 = Var_10 + (PL_1 * PL_2)
        return Var_10

#defining CNT with the help of Grid
    def CNT(self, grid):
        PL_3 = CNT

        for zz in range(grid.size):
            for qq in range(grid.size):
                PL_3[grid.map[zz][qq]] = 1 + PL_3[grid.map[zz][qq]]
        return sum(PL3 for PL3 in PL_3.values() if PL3 > 1)
    
    #defintion for Likelihood with Qt representing placeholder var
    def LikeliHood(self, grid):
        Mean_ = 0
        Qt = 0
        
        for zz in range(grid.size):
            for qq in range(grid.size):
                Qt = 1 + Qt
                VOR = LG2(grid.map[zz][qq]) if grid.map[zz][qq] > 0 else 0
                Mean_ = Mean_ + (VOR * Qt)
        return Mean_

    def Mono_tone(self, grid):
        # initializing rows and cols
        Col_count_sum = [[0,0],[0,0],[0,0],[0,0]]
        Row_count_sum = [[0,0],[0,0],[0,0],[0,0]]
        for zz in range(grid.size):
            for qq in range(grid.size-1):
                #PL
                PL_result = grid.map[zz][qq]
                PL_result = LG2(PL_result) if PL_result > 0 else 0
                #FOL
                FOL_result = grid.map[zz][qq+1]
                FOL_result = LG2(FOL_result) if FOL_result > 0 else 0

                if PL_result > FOL_result:
                    Row_count_sum[zz][0] = Row_count_sum[zz][0] + FOL_result - PL_result
                elif PL_result < FOL_result:
                    Row_count_sum[zz][1] = Row_count_sum[zz][1] + PL_result - FOL_result

        for qq in range(grid.size):
            for zz in range(grid.size-1):
                #Pl res
                PL_result = grid.map[zz][qq]
                PL_result = LG2(PL_result) if PL_result > 0 else 0
                #Fol res
                FOL_result = grid.map[zz+1][qq]
                FOL_result = LG2(FOL_result) if FOL_result > 0 else 0
                #assigning conditions
                if PL_result > FOL_result:
                    Col_count_sum[qq][0] = Col_count_sum[qq][0] + FOL_result - PL_result
                elif PL_result < FOL_result:
                    Col_count_sum[qq][1] = Col_count_sum[qq][1] + PL_result - FOL_result

        Temp_Res = 0
        for row, col in zip(Row_count_sum, Col_count_sum):
             Temp_Res = Temp_Res + max(row[0], row[1])
             Temp_Res = Temp_Res + max(col[0], col[1])
        return Temp_Res
    

#definining 
    def Mono_tone2(self, grid):
# initializing rows and cols
        Row_count_sum = [0,0,0,0]
        Col_count_sum = [0,0,0,0]
# arguments for Row
        for zz in range(grid.size):
            previous = 0
            for qq in range(grid.size-1):
                #PL res
                PL_result = grid.map[zz][qq]
                PL_result = LG2(PL_result) if PL_result > 0 else 0
                #Fol results
                FOL_result = grid.map[zz][qq+1]
                FOL_result = LG2(FOL_result) if FOL_result > 0 else 0

                Dfrnce = FOL_result - PL_result
                if Dfrnce * previous >= 0:
                    Row_count_sum[zz] = Row_count_sum[zz] + abs(Dfrnce)
                else:
                    Row_count_sum[zz] = 0
                    break


# arguments for Col
        for qq in range(grid.size):
            previous = 0
            for zz in range(grid.size-1):
                #PL res
                PL_result = grid.map[zz][qq]
                PL_result = LG2(PL_result) if PL_result > 0 else 0
                                #Fol results

                FOL_result = grid.map[zz+1][qq]
                FOL_result = LG2(FOL_result) if FOL_result > 0 else 0

                Dfrnce = FOL_result - PL_result
                if Dfrnce * previous >= 0:
                    Col_count_sum[qq] = Col_count_sum[qq] + abs(Dfrnce)
                else:
                    Col_count_sum[qq] = 0
                    break
        return max(Row_count_sum) + max(Col_count_sum)


#defining 
    def TogetHER(self, grid):
        #creating placeholder for the function
        TogetHER_placeHolder = 0
        
        for zz in range(grid.size):
            for qq in range(grid.size):
                Y = 1 + qq
                if Y < grid.size:
                    Dfrnce_lr = abs(grid.map[zz][qq] - grid.map[zz][Y])
                    if Dfrnce_lr == 0:
                        TogetHER_placeHolder = 1 + TogetHER_placeHolder

                X = 1 + zz
                if X < grid.size:
                    diffUD = abs(grid.map[zz][qq] - grid.map[X][qq])
                    if diffUD == 0: 
                        TogetHER_placeHolder = 1 + TogetHER_placeHolder
        return TogetHER_placeHolder

#defining polar_val with arguments 
    def polar_Val(self, grid, pos, Vect1):
        zz, qq = pos
        Qt, j = Vect1
        Val_goal = 0
        while zz < grid.size and qq < grid.size and grid.map[zz][qq] != 0:
            Val_goal = grid.map[zz][qq]
            zz = zz + Qt
            qq = qq + j

        return Val_goal

#defining precision_1 and creating placeholders
    def precision_1(self, grid):
        precision_1 = 0
        for zz in range(grid.size):
            for qq in range(grid.size):
                if grid.map[zz][qq] != 0:
                    value = LG2(grid.map[zz][qq])
                    for Vect1 in [(1,0), (0,1)]:
                        Val_goal = self.polar_Val(grid, (zz, qq), Vect1)

                        if Val_goal != 0:
                            Val_goal = LG2(Val_goal)
                            precision_1 -= abs(value - Val_goal)
                            
        return precision_1

#defining Precision_together
    def Prec1_2Gether(self, grid):
        TogetHER_placeHolder = 0
        precision_1 = 0
        for zz in range(grid.size):
            for qq in range(grid.size):
                if grid.map[zz][qq] != 0:
                    value = LG2(grid.map[zz][qq])
                    for Vect1 in [(1,0), (0,1)]:
                        Val_goal = self.polar_Val(grid, (zz, qq), Vect1)

                        if Val_goal != 0:
                            Val_goal = LG2(Val_goal)
                            precision_1 -= abs(value - Val_goal)

                Y = 1 + qq
                if Y < grid.size:
                    Dfrnce_lr = abs(grid.map[zz][qq] - grid.map[zz][Y])
                    if Dfrnce_lr == 0: 
                        TogetHER_placeHolder = 1 + TogetHER_placeHolder

                X = zz + 1
                if X < grid.size:
                    diffUD = abs(grid.map[zz][qq] - grid.map[X][qq])
                    if diffUD == 0: 
                        TogetHER_placeHolder = 1 + TogetHER_placeHolder

        return TogetHER_placeHolder, precision_1
    


class Class_Min_max:

    def __init__(self, Heur_Alg, TtM_limit):
        self.Heur_Alg = Heur_Alg
        self.TtM_limit = TtM_limit
        self._stopped = None
        self.Restart()
        
        #Additional definitions
        
    @property #for hault
    def hault(self):
        #return
        return self._stopped

    @hault.setter
    def hault(self, value):
                #return

        self._stopped = value

    def Restart(self):
        self.hault = False
        self.Prec_2 = 0
        self.Prec_high = 1



    def Time_func(self):
        return TtM.clock() - self.start
    
    def __call__(self, grid):
        return self.MIN_MAX(grid)


    def LvL_eval(self, grid):
        flag = False
        if self.Time_func() >= self.TtM_limit:
            self.hault = True
            flag = True
        if self.Prec_2 >= self.Prec_high:
            flag = True
        moves = grid.getAvailableMoves()
        if not moves:
            flag = True
        return flag


    def MIN_MAX(self, grid):
        self.start = TtM.clock()
        self.Restart()
        
        PL3 = (float('-inf'), None)
        while not self.hault:
            self.Prec_2 = 0

            for move in grid.getAvailableMoves():
                BB = grid.clone()
                BB.move(move)
                PL3 = max(PL3 , (self.MIN_MAX2(BB, False), move))
            self.Prec_high = self.Prec_high + 1
        return PL3[1]

    def MIN_MAX2(self, grid, MAX):
        if self.LvL_eval(grid):
            return self.Heur_Alg(grid)

        if MAX:
            self.Prec_2 = self.Prec_2 + 1
            PL3 =  float('-inf')
            
            for move in grid.getAvailableMoves():
                BB = grid.clone()
                BB.move(move)
                PL3 = max(PL3, self.MIN_MAX2(BB, False))
                if self.hault:
                    break
        else:
            PL3 =  float('inf')
            Grid_Cc = grid.getAvailableCells()
            ITER = ProD(Grid_Cc, [2, 4])
            
            for Grid_C, T_eval in ITER:
                BB = grid.clone()
                BB.setCellValue(Grid_C, T_eval)
                PL3 = min(PL3, self.MIN_MAX2(BB, True))
                if self.hault:
                    break
        return PL3


class Class_ALF_BET_FIND:

    def __init__(self, TtM_limit, Heur_Alg):
        self.Heur_Alg = Heur_Alg if Heur_Alg else Heuristic()
        #grid and tile eval
        self.grid_cache = {}
        self.eval_cache = {}
                #set self.hault to False

        self._stopped = None
        self.TtM_limit = TtM_limit
        self.Restart()

    @property #for hault
    def hault(self):
        return self._stopped

    @hault.setter
    def hault(self, value):
        self._stopped = value

    def Restart(self):
        self.grid_cache = {}
        self.eval_cache = {}
        #set self.hault to False
        self.hault = False
        self.Prec_2 = 0
        self.Prec_high = 3

    def Time_func(self):
        return TtM.clock() - self.start
    
    def __call__(self, grid):
        return self.ALF_BET_PRUN(grid)

    

    def LvL_eval(self, grid):
        flag = False
        if self.Time_func() >= self.TtM_limit:
                    #set self.hault to True
            self.hault = True
            flag = True
        if self.Prec_2 >= self.Prec_high:
            flag = True
        moves = grid.getAvailableMoves()
        if not moves:
            flag = True

        return flag
    



    def ALF_BET_PRUN(self, grid):
        self.start = TtM.clock()
        self.Restart()
        High_Val = (float('-inf'), None)
        while not self.hault:
            self.Prec_2 = 0
            ALF = float('-inf')
            BET = float('inf')

            High_Val = max(High_Val, self.ALF_BET_PRUN_2(grid, ALF, BET))

            self.Prec_high = self.Prec_high + 1
        return High_Val[1]


    def ALF_BET_PRUN_2(self, grid, ALF, BET):
        self.Prec_2 = self.Prec_2 + 1
        High_Val = (float('-inf'), None)

        if not self.grid_cache.get(grid):
            self.grid_cache[grid] = []
            for move in grid.getAvailableMoves():
                BB = grid.clone()
                BB.move(move)
                self.grid_cache[grid].append((move, BB))

        for move, BB in self.grid_cache[grid]:
            BB = grid.clone()
            BB.move(move)
            High_Val = max(High_Val, (self.Var_Min(BB, ALF, BET), move))
            if High_Val[0] >= BET:
                return High_Val
            ALF = max(High_Val[0], ALF)
            if self.hault:
                break

        return High_Val
    
    #define maximum
    def Var_Mx(self, grid, ALF, BET):
        if self.LvL_eval(grid):
            #conditionals
            if not self.eval_cache.get(grid):
                self.eval_cache[grid] = self.Heur_Alg(grid)
            return self.eval_cache[grid]



        self.Prec_2 += 1
        PL3 = float('-inf')

        if not self.grid_cache.get(grid):
            self.grid_cache[grid] = []
            for move in grid.getAvailableMoves():
                BB = grid.clone()
                BB.move(move)
                self.grid_cache[grid].append((move, BB))

        for move, BB in self.grid_cache[grid]:
            BB = grid.clone()
            BB.move(move)
            PL3 = max(PL3, self.Var_Min2(BB, ALF, BET))

            ALF = max(PL3, ALF)
            if BET <= ALF:
                break

            if self.hault:
                break

        return PL3
    


#minimum_var1
    def Var_Min(self, grid, ALF, BET):
        if self.LvL_eval(grid):
            if not self.eval_cache.get(grid):
                self.eval_cache[grid] = self.Heur_Alg(grid)
            return self.eval_cache[grid]


        self.Prec_2 = self.Prec_2 + 1
        PL3 = float('inf')
        if not self.grid_cache.get(grid):
            self.grid_cache[grid] = []
            Grid_Cc = grid.getAvailableCells()
            ITER = ProD(Grid_Cc, [2, 4])
            for Grid_C, T_eval in ITER:
                BB = grid.clone()
                BB.setCellValue(Grid_C, T_eval)
                self.grid_cache[grid].append(BB)

        for BB in self.grid_cache[grid]:
            PL3 = min(PL3, self.Var_Mx(BB, ALF, BET))
            BET = min(PL3, BET)
            if BET <= ALF:
                break
            if self.hault:
                break

        return PL3

#minimum_var2
    def Var_Min2(self, grid, ALF, BET):
        if self.LvL_eval(grid):
            if not self.eval_cache.get(grid):
                self.eval_cache[grid] = self.Heur_Alg(grid)
            return self.eval_cache[grid]

        PL3 = float('inf')
        if not self.grid_cache.get(grid):
            self.grid_cache[grid] = []
            Grid_Cc = grid.getAvailableCells()
            ITER = ProD(Grid_Cc, [2, 4])
            for Grid_C, T_eval in ITER:
                BB = grid.clone()
                BB.setCellValue(Grid_C, T_eval)
                self.grid_cache[grid].append(BB)

        Lowest_BB = None
        Lowest_Val = float('inf')
        for BB in self.grid_cache[grid]:
            if not self.eval_cache.get(BB):
                self.eval_cache[BB] = self.Heur_Alg(BB)
            if Lowest_Val > self.eval_cache[BB]:
                Lowest_Val = self.eval_cache[BB]
                Lowest_BB = BB

        PL3 = min(PL3, self.Var_Mx(Lowest_BB, ALF, BET))
        BET = min(PL3, BET)
        return PL3

        ################################################################################
    ################################################################################
    ################################################################################
    ################################################################################



    def ALF_BET_PRUN_3(self, grid):
        self.start = TtM.clock()
        self.Restart()
        PL3 = (float('-inf'), None)
        while not self.hault:
            self.Prec_2 = 0
            ALF = float('-inf')
            BET = float('inf')
            if not self.grid_cache.get(grid):
                self.grid_cache[grid] = []
                for move in grid.getAvailableMoves():
                    BB = grid.clone()
                    BB.move(move)
                    self.grid_cache[grid].append((move, BB))

            for move, BB in self.grid_cache[grid]:
                PL3 = max(PL3 ,
                        (self.ALF_BET_PRUN_4(BB, False, ALF, BET), move)
                )

            self.Prec_high = self.Prec_high + 1
        return PL3[1]

    def ALF_BET_PRUN_4(self, grid, MAX, ALF, BET):
        if self.LvL_eval(grid):
            if not self.eval_cache.get(grid):
                self.eval_cache[grid] = self.Heur_Alg(grid)

            return self.eval_cache[grid]

#max Conditions
        if MAX:
            self.Prec_2 = self.Prec_2 + 1 
            PL3 =  float('-inf')
            if not self.grid_cache.get(grid):
                self.grid_cache[grid] = []
                for move in grid.getAvailableMoves():
                    BB = grid.clone()
                    BB.move(move)
                    self.grid_cache[grid].append((move, BB))

            for move, BB in self.grid_cache[grid]:
                PL3 = max(PL3, self.ALF_BET_PRUN_4(BB, False, ALF, BET))
                ALF = max(PL3, ALF)
                if  BET <= ALF:
                    return PL3

                if self.hault:
                    break
        else:
            PL3 =  float('inf')
            if not self.grid_cache.get(grid):
                self.grid_cache[grid] = []
                Grid_Cc = grid.getAvailableCells()
                ITER = ProD(Grid_Cc, [2, 4])
                for Grid_C, T_eval in ITER:
                    BB = grid.clone()
                    BB.setCellValue(Grid_C, T_eval)
                    self.grid_cache[grid].append(BB)

            for BB in self.grid_cache[grid]:
                PL3 = min(PL3, self.ALF_BET_PRUN_4(BB, True, ALF, BET))
                BET = min(PL3, BET)
                if BET <= ALF:
                    return PL3

                if self.hault:
                    break
        return PL3

#Player AI class
class PlayerAI(BAI):

    def __init__(self, TtM_limit = 0.099, Heur_Alg = None):
        self.search = Class_ALF_BET_FIND(TtM_limit, Heur_Alg = None)

    def getMove(self, grid):
        return self.search(grid)

#main func
if __name__ == "__main__":
    #using GameManager_3 to import main()
    
    from GameManager_3 import main
    main()
    
    print(Heuristic().weights)
    
    #end of project