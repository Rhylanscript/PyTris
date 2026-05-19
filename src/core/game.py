'''
This file has the Game class for the Tetris game.
It handles the game logic, including block movement, rotation, scoring, and game over conditions.
It also handles the drawing of the game grid and blocks.

'''

# import external modules
import pygame
import random

# import local modules
from src.ui.grid import Grid
from src.core.backend import Backend

from src.util.blocks import *
from src.config.settings import *

# game object
class Game:
    '''
    Game class represents the Tetris game.
    It handles the game logic, including block movement, rotation, scoring, and game over conditions.

    '''
    # constructor
    def __init__(self, backend: Backend) -> None:

        self.backend = backend

        # create grid object
        self.grid = Grid(backend)

        # block handling
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.block_ids = [LBlock(), JBlock(), IBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]

        # game blocks
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()

        # game variables
        self.game_over = False
        self.score = 0
        self.is_bomb = False

        # sound effects
        self.rotate_sound = pygame.mixer.Sound("../assets/sounds/rotate.ogg")
        self.clear_sound = pygame.mixer.Sound("../assets/sounds/clear.ogg")

        # play background music
        pygame.mixer.music.load("../assets/sounds/music.ogg")
        pygame.mixer.music.play(-1)
    
    # method to update score taking 2 params
    def update_score(self, lines_cleared:int, move_down_points:int) -> None:
        '''
        Update the score based on the number of lines cleared and points for moving down.
        Parameters:
          - lines_cleared (int): The number of lines cleared.
          - move_down_points (int): The points for moving the block down.
        
        >>> game = Game()
        >>> game.update_score(2, 5)
        >>> game.score
        255
        
        '''
        
        # line clear calc
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 250
        elif lines_cleared == 3:
            self.score += 500
        elif lines_cleared == 4:
            self.score += 1000

        # add the points for moving tetronimo down
        self.score += move_down_points

    # method that returns a random block
    def get_random_block(self) -> Block:

        '''
        Get a random block from the list of blocks.
        If all blocks have been used, reset the list and return a random block.

        Returns:
          - Block: A random block from the list of blocks.

        >>> game = Game()
        >>> block = game.get_random_block()
        >>> isinstance(block, LBlock)
        False
        >>> isinstance(block, JBlock)
        True
        
        '''

        # if list is empty (all tetronimos used) reset it
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        
        # select and return a block
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block
    
    # game controls
    def move_left(self) -> None:
        '''
        Move the current block to the left.
        If the block collides with another block or goes outside the grid, undo the move.
        
        '''
        # move in direction
        self.current_block.move(0, -1)
        # check for collisions, if so, undo move
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)
    def move_right(self) -> None:
        '''
        Move the current block to the right.
        If the block collides with another block or goes outside the grid, undo the move.
        
        '''
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)
    def move_down(self) -> None:
        '''
        Move the current block down.
        If the block collides with another block or goes outside the grid, undo the move and lock the block in place.
        
        '''
        self.current_block.move(1, 0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
            # lock block if collision and moving down
            self.lock_block()

    # called when space pressed
    def drop_block(self) -> None:
        '''
        Drop the current block to the bottom of the grid.
        If the block collides with another block or goes outside the grid, undo the move and lock the block in place.
        
        '''
        # temp variable for scoring
        temp_score = 0

        # move block down until collision
        while True:
            self.current_block.move(1, 0)
            temp_score += 1
            if self.block_inside() == False or self.block_fits() == False:
                self.current_block.move(-1, 0)
                self.lock_block()

                # multiply score by 1.5 and break
                if temp_score % 2 == 1:
                    temp_score += 1
                
                temp_score *= 1.5
                self.score += temp_score
                break

    # lock block in place after collision
    def lock_block(self) -> None:
        '''
        Lock the current block in place on the grid.
        This method stores the block's cell positions in the grid and checks for full rows to clear.
        
        '''
        # store the tetronimo cells
        tiles = self.current_block.get_cell_positions()
        
        # set tetronimo cells ids to tetronimo id (set colour)
        for position in tiles:
            self.grid.grid[position.row][position.col] = self.current_block.id
        
        # set new blocks and clear rows if needed
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        
        # play sound and add score if rows are cleared
        if rows_cleared > 0:
            self.clear_sound.play()
            self.update_score(rows_cleared, 0)

        # if block doesnt fit when spawned, game over
        if self.block_fits() == False:
            self.game_over = True

        # update scores
        self.update_score(0, 5)

        # rng for bomb blocks
        if random.randint(0, 4) == 4:
            self.is_bomb = True
        else:
            self.is_bomb = False
    
    # reset the game
    def reset(self) -> None:
        '''
        Reset the game to its initial state.
        
        '''
        # reset grid
        self.grid.reset()

        # reset block logic
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()

        # reset score
        self.score = 0

    # check if block fits in new position
    def block_fits(self) -> bool:
        '''
        This method checks if the current block fits in the grid.
        It checks if the block's cell positions are empty in the grid.

        Returns:
          - bool: True if the block fits, False otherwise.

        >>> game = Game()
        >>> game.current_block = IBlock()
        >>> game.current_block.move(0, 1)
        >>> game.block_fits()
        True
        
        '''
        # store cell positions
        tiles = self.current_block.get_cell_positions()

        # loop through tiles to check for collisions
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.col) == False:
                return False
        return True

    # rotate method
    def rotate(self) -> None:
        '''
        Rotate the current block.
        If the block collides with another block or goes outside the grid, undo the rotation.
        
        '''
        self.current_block.rotate()

        # check collisions
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()
        else:
            # play sound if no collisions
            self.rotate_sound.play()

    # check if block is outside grid
    def block_inside(self) -> bool:
        '''
        Check if the current block is inside the grid.

        Returns:
          - bool: True if the block is inside, False otherwise.
        
        >>> game = Game()
        >>> game.current_block = IBlock()
        >>> game.current_block.move(-1, 0)
        >>> game.block_inside()
        False
        >>> game.current_block.move(1, 0)
        >>> game.block_inside()
        True
        
        '''
        tiles = self.current_block.get_cell_positions()

        # check collisions
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.col) == False:
                return False
        return True
    
    def copy_block(self, copy_block:Block) -> Block:
        '''
        Create a copy of the current block.
        This method is used to create a shadow block that shows where the current block will land.

        Parameters:
          - copy_block (Block): The block to copy.

        Returns:
          - Block: A copy of the block with the same position and rotation state.

        >>> game = Game()
        >>> block = game.copy_block(IBlock())
        >>> isinstance(block, IBlock)
        True
        
        '''
        temp_block = copy_block
        temp_block_copy = self.block_ids[copy_block.id - 1]
        temp_block_copy.row_offset = temp_block.row_offset
        temp_block_copy.column_offset = temp_block.column_offset
        temp_block_copy.rotation_state = copy_block.rotation_state
        return temp_block_copy
    
    # method to get the shadow tile position
    def get_shadow_position(self) -> list:
        '''
        Get the shadow position of the current block.
        This method creates a copy of the current block and moves it down until it collides with another block or goes outside the grid.

        Returns:
          - list: A list of Position objects representing the shadow block's cell positions.

        >>> game = Game()
        >>> shadow_positions = game.get_shadow_position()
        >>> isinstance(shadow_positions[0], Position)
        True
        >>> shadow_positions[0].row
        0
        
        '''
        # temp variable
        moves = 0

        # move block until collision
        while self.block_inside() and self.block_fits():
            self.current_block.move(1, 0)
            moves += 1

        # after collision, move block back
        self.current_block.move(-1, 0)
        moves -= 1

        # create the shadow block as temp obj
        """temp_block = self.current_block
        temp_block_copy = self.block_ids[self.current_block.id - 1]
        temp_block_copy.row_offset = temp_block.row_offset
        temp_block_copy.column_offset = temp_block.column_offset
        temp_block_copy.rotation_state = self.current_block.rotation_state"""

        temp_block_copy = self.copy_block(self.current_block)

        # move current block back into place
        self.current_block.move(-moves, 0)

        # return shadow block positions
        return temp_block_copy.get_cell_positions()
    
    # swap blocks with the next block
    def swap_blocks(self):
        '''
        Swap the current block with the next block.
        This method checks if the swapped block fits in the grid and adjusts its position accordingly.

        If the swapped block doesn't fit, it swaps back to the original position.
        
        '''

        # Swap the blocks
        self.current_block, self.next_block = self.next_block, self.current_block
        
        # Adjust position to ensure the swapped block appears correctly
        self.current_block.row_offset = 0
        self.current_block.column_offset = cols // 2 - 1

        # If the swapped block doesn't fit, swap back
        if not self.block_fits() or not self.block_inside():
            self.current_block, self.next_block = self.next_block, self.current_block
    
    # draw game
    def draw(self, screen: pygame.display) -> None:
        '''
        Draw the game on the screen.
        This method draws the grid, the current block, and the next block.

        Parameters:
          - screen (pygame.display): The screen to draw the game on.
        
        >>> game = Game()
        >>> game.draw(screen)
        >>> isinstance(game.grid, Grid)
        True
        
        '''
        # draw grid
        self.grid.draw(screen)
        if not self.game_over:
            # loop through shadow block positions
            shadow_positions = self.get_shadow_position()
            for tile in shadow_positions:
                shadow_rect = pygame.Rect(
                    13 + tile.col * self.current_block.cell_size,
                    13 + tile.row * self.current_block.cell_size,
                    self.current_block.cell_size - 5,
                    self.current_block.cell_size - 5
                )
                pygame.draw.rect(screen, (80, 80, 80), shadow_rect, 3, 3)

        # if block is a bomb, colour is black
        if self.is_bomb:
            self.current_block.draw(screen, 11, 11, True)
        else:
            self.current_block.draw(screen, 11, 11)

        # draw the next block. note that as the oblock and
        # the iblock have different dimensions to the others
        # (1x4 and 2x2 as opposed to 3x2), different draw
        # positions are required
        if self.next_block.id == 3:
            self.next_block.draw(screen, 255, 425)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 255, 415)
        else:
            self.next_block.draw(screen, 270, 405)