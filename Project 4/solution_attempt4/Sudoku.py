#importing libraries
from ConstraintSatProblem import ConstraintSatProblem

#definitng Generate
def generate_vars():

    #rows and cols and vars
    rows = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    cols = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    variables = {}
    for row in rows:
        for col in cols:
            variables[row + col] = None
    return variables

#domain generator
def generate_domains(variables):

    domains = {}
    for var in variables:
        domains[var] = {1: True, 2: True, 3: True, 4: True, 5: True, 6: True, 7: True, 8: True, 9: True}
    return domains

#constraint gen.
def generate_constraints(variables):

    constraints = {}
    for var in variables:
        row = var[0]
        col = var[1]
        cannot_equal = {}
        for var_two in variables:
            if var_two == var:
                continue
            if (row == var_two[0] or
                col == var_two[1] or
                same_subboard(var, var_two)):
                cannot_equal[var_two] = True

        constraints[var] = {"arcs": cannot_equal}
    return constraints

#defining rows and cols of subboards
def same_subboard(var_one, var_two):

    var_one_row_group = (ord(var_one[0]) - 65) / 3
    var_one_col_group = (int(var_one[1]) - 1) / 3
    var_two_row_group = (ord(var_two[0]) - 65) / 3
    var_two_col_group = (int(var_two[1]) - 1) / 3
    return (var_one_row_group == var_two_row_group and
            var_one_col_group == var_two_col_group)

#creating sudoku class for constraint problem
class Sudoku(ConstraintSatProblem):


    def __init__(self, data):

        super(Sudoku, self).__init__(csp_type="sudoku",
                                     generator={"variables": generate_vars,
                                                "domains": generate_domains,
                                                "constraints":generate_constraints})
        self.board = self.create_board(data)
        self.update_start_domains()

    def create_board(self, data=None):

        board_dict = {}
        x = 0
        for space in self.variables:
            board_dict[space] = int(data[((ord(space[0])-65)*9)+int(space[1])-1])
            x += 1
        return board_dict

    def Asignd_value(self, cell, value): 

        self.board[cell] = value

    def update_start_domains(self):

        for var_one in self.variables:
            if self.board[var_one] == 0:
                continue
            self.domains[var_one] = {self.board[var_one]: True}
            self.assignments[var_one] = self.board[var_one]
            del self.unassigned[var_one]

        for var_one in self.variables:
            for var_two in self.constraints[var_one]["arcs"]:
                if self.board[var_one] in self.domains[var_two]:
                    del self.domains[var_two][self.board[var_one]]
                    if len(self.domains[var_two]) == 1:
                        for key in self.domains[var_two]:
                            self.board[var_two] = key
                        self.assignments[var_two] = self.board[var_two]
                        del self.unassigned[var_two]

    def convert_result_to_proper_Format(self, result):

        var_list = result.keys()
        var_list.sort()
        result_string = ""
        for var in var_list:
            result_string += str(result[var])

        return result_string

