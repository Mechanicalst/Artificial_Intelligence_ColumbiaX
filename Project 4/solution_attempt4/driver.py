#Importing libraries
from CSPGenerator import CSPGenerator
import sys


#creating main defintion
def main(argv = None, csp_type = "sudoku"):

    csp_gen = CSPGenerator()

#output file
    o_file = open("output.txt", "wb")
#if-else to catch exceptions
    if not argv:
        puzzles = open("sudokus_start.txt", "r")
        answers = open("sudokus_finish.txt", "r")

        x = 1
        for line in puzzles.readlines():
            line.strip("\n")
            answer = answers.readline().strip("\n")
            csp = csp_gen.get_csp(csp_type=csp_type, data=line)
            result = csp.backtrack_solve()
            result_string = csp.convert_result_to_proper_Format(result)
            o_file.write(result_string+"\n")
            if result_string != answer:
                print result_string
                print answer
                print "Failed puzzle %d" % x
            else:
                print "Solved puzzle %d" % x
            x += 1

        puzzles.close()
        answers.close()
        o_file.close()
    else:
        csp = csp_gen.get_csp(csp_type=csp_type, data=argv)
        result = csp.backtrack_solve()
        result_string = csp.convert_result_to_proper_Format(result)
        o_file.write(result_string + "\n")
        o_file.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(argv=sys.argv[1])
    else:
        main()
