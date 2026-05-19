''' simple object to track a position on a grid '''
class Position:
    '''
    Class to represent a position on a grid.
    Parameters:
        row (int): The row of the position.
        col (int): The column of the position.

    '''
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col