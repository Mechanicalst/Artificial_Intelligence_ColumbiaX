#import libraries
from Sudoku import *
import time

with open('sudokus_start.txt') as temp_file:
    sudokus_start = [line.rstrip('\r\n') for line in temp_file]

with open('sudokus_finish.txt') as temp_file:
    sudokus_finish = [line.rstrip('\r\n') for line in temp_file]

N = len(sudokus_start)
for k in xrange(N):
    sudo = Sudoku(sudokus_start[k])
    csp = SudokuCSP(sudo)
    AC3(csp)
    x = BacktrackingSearch(csp)
    for var in x:
        csp.domain[var] = [x[var]]
    sol = ""
    for row in "ABCDEFGHI":
        for col in "123456789":
            sol += str(csp.domain[row + col][0])

    print (k + 1, sol == sudokus_finish[k])
    
    time.sleep(0.001)
    
