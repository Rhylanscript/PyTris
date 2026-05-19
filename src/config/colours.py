'''
This file contains the colour constants used in the Tetris game.
The colours are represented as RGB tuples.

'''

# class for colours
class Colours:
    '''Class to hold colour constants for the game.'''
    # colour consts
    DARK_GREY = (26, 31, 40)
    GREEN = (110, 250, 50)
    MAGENTA = (230, 18, 120)
    ORANGE = (226, 116, 17)
    YELLOW = (255, 255, 0)
    PURPLE = (200, 20, 255)
    CYAN = (21, 204, 209)
    BLUE = (80, 110, 255)

    # return a list; used with block ids
    @classmethod
    def get_cell_colours(cls) -> list:
        '''
        Return a list of colours for the blocks.
        
        Returns:
        list: A list of RGB tuples representing the colours for the blocks.

        >>> Colours.get_cell_colours()
        [(26, 31, 40), (200, 20, 255), (226, 116, 17), (110, 250, 50), (21, 204, 209), (255, 255, 0), (230, 18, 120), (80, 110, 255)]
        
        '''
        # _, L, J, I, O, S, T, Z
        return [cls.DARK_GREY, cls.PURPLE, cls.ORANGE, cls.GREEN, cls.CYAN, cls.YELLOW, cls.MAGENTA, cls.BLUE]