# Sudoku_solver

from Sudoku import *
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python driver.py <input_string>'
        sys.exit(0)

    sudo = Sudoku(sys.argv[1])
    csp = SudokuCSP(sudo)
    AC3(csp)

# Assignment obtained from remaining
    x = BacktrackingSearch(csp)

    for var in x:
        csp.domain[var] = [x[var]]

    sol = ""
    for row in "ABCDEFGHI":
        for col in "123456789":
            sol += str(csp.domain[row + col][0])

    with open("output.txt", "w") as output:
        output.write(sol)

#end of project