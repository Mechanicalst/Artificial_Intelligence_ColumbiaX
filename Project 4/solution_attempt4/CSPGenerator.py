from Sudoku import Sudoku


class CSPGenerator:

    def __init__(self):
        
        """
        .....................
        """

    def get_csp(self, csp_type, data):
        
        if csp_type == "sudoku":
            return Sudoku(data)
        else:
            raise ValueError("unknown csp type")
