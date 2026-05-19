'''Handles backend operations for high score management.'''

import os
import json

from src.config.settings import *

class Backend:
    '''
    Backend class to handle high score management.
    This class is responsible for reading and writing the high score
    to a file in the local app data directory.

    The file is created if it does not exist.

    '''
    def __init__(self, filename: str = "highscore.txt", boardfilename: str = "board.json") -> None:
        # Get local app data path and ensure pytris folder exists
        self.folder_path = os.path.join(os.getenv("LOCALAPPDATA"), "pytris")
        os.makedirs(self.folder_path, exist_ok=True)

        # Set the full file path
        self.file_path = os.path.join(self.folder_path, filename)
        self.json_path = os.path.join(self.folder_path, boardfilename)
        print(self.file_path)
        print(self.json_path)

        '''dictionary'''
        self.BOARD:dict = self.load_json()

    def get_highscore(self) -> int:
        '''
        Attempts to read the high score from a file.
        If the file does not exist or is invalid, it creates the file
        and initializes the high score to 0.

        Returns the high score as an integer.

        >>> backend = Backend()
        >>> print(backend.get_highscore())
        0

        '''
        try:
            with open(self.file_path, "r") as file:
                return int(file.read().strip())  # Read and convert to int
        except (FileNotFoundError, ValueError):
            # Create the file if it doesn't exist and return 0
            with open(self.file_path, "w") as file:
                file.write("0")
            return 0

    def update(self, number: int) -> None:
        '''
        Updates the high score in the file.

        >>> backend = Backend()
        >>> backend.update(100)
        >>> print(backend.get_highscore())
        100

        '''
        with open(self.file_path, "w") as file:
            file.write(str(number))  # Write the new high score

    def load_json(self):
        with open(self.json_path, "r") as file:
            return json.load(file)
        
    def load_board(self):
        try:
            return self.BOARD.get("data")
        except:
            #with open(self.json_path, "w") as f: 
            return [[0 for j in range(cols)] for i in range(rows)]
        
    def save_board(self):
        ...
