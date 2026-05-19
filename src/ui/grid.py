# import external modules
import pygame

# import local modules
from src.config.colours import Colours
from src.core.backend import Backend
from src.config.settings import *

# grid object
class Grid:
    # constructor
    def __init__(self, backend: Backend) -> None:
        # col and row config
        self.num_rows = rows
        self.num_cols = cols

        self.backend = backend

        # setup cells
        self.cell_size = size
        self.grid = backend.load_board()
        self.colours = Colours.get_cell_colours()

    # method to print grid in terminal (debug)
    def print_grid(self) -> None: # debug
        for row in range(self.num_rows):
            for column in range(self.num_cols):
                print(self.grid[row][column], end = " ")
            print()

    # checks if param coords are inside grid, returns bool
    def is_inside(self, row:int, col:int) -> bool:
        if row >= 0 and row < self.num_rows and col >= 0 and col < self.num_cols:
            return True
        return False
    
    # checks if grid space has id of 0 (empty)
    def is_empty(self, row:int, col:int) -> bool:
        if self.grid[row][col] == 0:
            return True
        return False
    
    # check if row is full (will be cleared)
    def is_row_full(self, row:int) -> bool:
        # loop through columns
        for col in range(self.num_cols):
            if self.grid[row][col] == 0:
                return False
        return True

    # clear a row
    def clear_row(self, row:int) -> None:
        for col in range(self.num_cols):
            self.grid[row][col] = 0

    # move the above row down after clear
    def move_row_down(self, row:int, num_rows:int) -> None:
        for col in range(self.num_cols):
            self.grid[row+num_rows][col] = self.grid[row][col]
            self.grid[row][col] = 0

    # clear all rows
    def clear_full_rows(self) -> int:
        completed = 0
        # loop through rows
        for row in range(self.num_rows-1, 0, -1):
            if self.is_row_full(row):
                # clear row if completed
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                # move row down
                self.move_row_down(row, completed)
        return completed
    
    # reset grid
    def reset(self) -> None:
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                self.grid[row][col] = 0
    
    # draw the grid
    def draw(self, screen: pygame.display) -> None:
        # loop rows
        for row in range(self.num_rows):
            
            # loop cols
            for col in range(self.num_cols):
                # draw a rect for each cell
                cell_value = self.grid[row][col]
                cell_rect = pygame.Rect(col*self.cell_size+grid_offset+1, row*self.cell_size+grid_offset+1, self.cell_size-1, self.cell_size-1)
                pygame.draw.rect(screen, self.colours[cell_value], cell_rect)