'''Contains the Block class which is used to create the blocks in the game.'''

# import external modules
import pygame

# import local modules
from src.config.colours import Colours
from src.util.position import Position

# create the block object
class Block:
	'''
	Base class for all blocks in the game.

	Parameters:
		id (int): The ID of the block.

	'''
	# constructor
	def __init__(self, id:int) -> None:
		# block id
		self.id = id

		# cell logic
		self.cells = {}
		self.cell_size = 30

		# positioning logic
		self.row_offset = 0
		self.column_offset = 0
		self.rotation_state = 0

		# set the colour
		self.colors = Colours.get_cell_colours()

	# method to move block
	def move(self, rows:int, columns:int) -> None:
		'''
		Move the block by the specified number of rows and columns.
		
		Parameters:
		rows (int): The number of rows to move the block.
		columns (int): The number of columns to move the block.

		'''
		self.row_offset += rows
		self.column_offset += columns

	# return the positions of the cells
	def get_cell_positions(self) -> list:
		'''
		Get the positions of the cells in the block.
		Returns:
		list: A list of Position objects representing the cells in the block.

		>>> block = Block(1)
		>>> block.cells = {0: [Position(0, 0), Position(0, 1)]}
		>>> block.get_cell_positions()
		[Position(0, 0), Position(0, 1)]
		>>> block.move(1, 1)
		>>> block.get_cell_positions()
		[Position(1, 1), Position(1, 2)]

		'''
		# temp variables
		tiles = self.cells[self.rotation_state]
		moved_tiles = []

		# loop through tiles and add offset, add to list
		for position in tiles:
			position = Position(position.row + self.row_offset, position.col + self.column_offset)
			moved_tiles.append(position)

		# return the list
		return moved_tiles

	# method to rotate block clockwise
	def rotate(self) -> None:
		'''
		Rotate the block clockwise.

		>>> block = Block(1)
		>>> block.cells = {0: [Position(0, 0), Position(0, 1)]}
		>>> block.rotate()
		>>> block.rotation_state
		1

		'''
		self.rotation_state += 1
		if self.rotation_state == len(self.cells):
			self.rotation_state = 0

	# method to rotate block counter-clockwise
	def undo_rotation(self) -> None:
		'''
		Undo the last rotation of the block.

		>>> block = Block(1)
		>>> block.cells = {0: [Position(0, 0), Position(0, 1)]}
		>>> block.rotate()
		>>> block.undo_rotation()
		>>> block.rotation_state
		0
		
		'''
		self.rotation_state -= 1
		if self.rotation_state == -1:
			self.rotation_state = len(self.cells) - 1

	# draw the block
	def draw(self, screen:pygame.display, offsetx:int, offsety:int, bomb:bool = False) -> None:
		'''
		Draw the block on the screen.

		Parameters:
		  - screen (pygame.display): The screen to draw the block on.
		  - offsetx (int): The x offset to draw the block at.
		  - offsety (int): The y offset to draw the block at.
		  - bomb (bool): If True, draw the block as a bomb block. Defaults to False.
		
		'''
		# get cells of block
		tiles = self.get_cell_positions()

		# loop through cells 
		for tile in tiles:

			# create a rect for cell
			tile_rect = pygame.Rect(
				offsetx + tile.col * self.cell_size, 
				offsety + tile.row * self.cell_size, 
				self.cell_size-1, 
				self.cell_size-1)
			
			# set colour to black if bomb block
			#if bomb:
				#colour = (0, 0, 0) 
			#else:
			colour = self.colors[self.id]

			# draw rect
			pygame.draw.rect(screen, colour, tile_rect)