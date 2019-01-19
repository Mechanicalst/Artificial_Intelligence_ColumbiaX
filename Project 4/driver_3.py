#importing libraries
import argparse as argP
#importing copy & deepcopy from copy
from copy import deepcopy, copy
import sys


#Creating Rows and Columns and Options
options = [x + 1 for x in range(9)]
Rows = 'ABCDEFGHI'
Columns = [x for x in range(9)]


#setting placeholder variables
ALL_in = []
COL_set = []
BOX_set = []
ROW_set = []


#creating temporary row col and box
for row, x in zip(Rows, range(len(Rows))):
    tmp_row = []
    for column in Columns:
        tmp_row.append("%s%s" % (row, column))
        ALL_in.append("%s%s" % (row, column))

    ROW_set.append(tmp_row)

for column, x in zip(Columns, range(len(Columns))):
    tmp_column = []
    for row in Rows:
        tmp_column.append("%s%s" % (row, column))

    COL_set.append(tmp_column)

for q in range(3):
    for x in range(3):
        tmp_box = []
        for y in range(3):
            row = Rows[y + q * 3]
            for z in range(3):
                column = Columns[z + 3 * x]
                tmp_box.append("%s%s" % (row, column))

        BOX_set.append(tmp_box)

#creating the Sudoku class
class Sudoku:

    def __init__(self, board):
        self.state = board
        self.unresolved = []
        self.domain = self.first_domain()
        self.next_guess = []

    def first_domain(self):
        domain = {}
        for location in ALL_in:
            if self.state[location] == 0:
                domain[location] = copy(options)
                #tuple with row, col, loc, & box
                self.unresolved.append(location) 

        return domain


    def NW_child(self):
        NW_inst = deepcopy(self)
        

        return NW_inst

    def IS_solved(self):
        for anything in ALL_in:
            if self.state[anything] == -1:
                return 2
        for row in ROW_set:
            Seen = set()
            for each in row:
                if self.state[each] == 0:
                    return 1
                if self.state[each] in Seen:
                    return 2
                else:
                    Seen.add(self.state[each])

        for column in COL_set:
            Seen = set()
            for each in column:
                if self.state[each] in Seen:
                    return 2
                else:
                    Seen.add(self.state[each])

        for box in BOX_set:
            Seen = set()
            for each in box:
                if self.state[each] in Seen:
                    return 2
                else:
                    Seen.add(self.state[each])

        return 0

    def SET_nxt(self):
        self.next_guess = []
        for key, value in self.domain.items():
            self.next_guess.append((len(value), key))

        self.next_guess.sort()

    #defining a legal move
    def Legal_mv(self, candidate, key):
        for row in ROW_set:
            if key in row:
                for spot in row:
                    if candidate == self.state[spot]:
                        return False

        for column in COL_set:
            if key in column:
                for spot in column:
                    if candidate == self.state[spot]:
                        return False

        for box in BOX_set:
            if key in box:
                for spot in box:
                    if candidate == self.state[spot]:
                        return False

        return True


    def Checker(self, Checks, position, Change_s):
        while True:
            Leav = 0
            for each in Checks:

                if self.state[each] != 0 and self.state[each] in self.domain[position]:
                    dq = self.domain[position].index(self.state[each])
                    del self.domain[position][dq]
                    Leav += 1
                    Change_s += 1
                    if len(self.domain[position]) == 1:
                        if self.Legal_mv(int(self.domain[position][0]), position):
                            self.state[position] = int(self.domain[position][0])
                            self.unresolved.remove(position)
                            del self.domain[position]
                        else:
                            self.state[position] = -1
                            self.unresolved.remove(position)
                            del self.domain[position]

                        return False



            if Leav == 0:
                return Change_s

#...................
    def acthree(self):
        while True:
            Change_s = 0
            for row in ROW_set:
                for position in row:
                    if position in self.unresolved:
                        Change_s = self.Checker(row, position, Change_s)

            for column in COL_set:
                for position in column:
                    if position in self.unresolved:
                        Change_s = self.Checker(column, position, Change_s)

            for box in BOX_set:
                for position in box:
                    if position in self.unresolved:
                        Change_s = self.Checker(box, position, Change_s)

            if Change_s == 0:
                return
            
            #defining the tree
    def BUILT_tree(self):
        self.SET_nxt()
        next = self.next_guess[0]
        del self.next_guess[0]
        key = next[1]
        takeAshot = self.domain[key]
        del self.domain[next[1]]
        self.unresolved.remove(key)
        for each in takeAshot:
            TestR = self.NW_child()
            TestR.state[key] = each
            TestR.acthree()
            TestR.SET_nxt()
            Result_f = TestR.IS_solved()
            if Result_f == 2:
                pass
            elif Result_f == 0:
                return TestR
            else:
                TestR = TestR.BUILT_tree()
                if TestR:
                    if TestR.IS_solved() == 0:
                        return TestR



    #defining Solve
    def Solve(self):
        self.acthree()
        Result_f = self.IS_solved()
        if Result_f == 0:
            return Result_f
        if Result_f == 2:
            return Result_f
        else:
            return self.BUILT_tree()

    #defining Print
    def PRNT_int(self):
        Var_val = 0
        for each, i  in zip(ALL_in, range(len(ALL_in))):
            Var_val += self.state[each]*pow(10, (80 - i))

        return Var_val

#.................#defining board allocation
        
def Alocate(board):
    Alocation = {}
    for each, i in zip(ALL_in, range(len(ALL_in))):
        Alocation[each] = int(float(board[i]))

    return Alocation

#final portion with file read and print
if __name__ == "__main__":
    parser = argP.ArgumentParser()
    parser.add_argument('start')
    board = Alocate(parser.parse_args().start)
    
    FIN = Sudoku(board)
    FIN = FIN.Solve()
    ANS = FIN.PRNT_int()
    Fil_opn = open('output.txt', 'w')
    Fil_opn.write("%i" % ANS)
    Fil_opn.close()




