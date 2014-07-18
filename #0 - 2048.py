"""
Clone of 2048 game.
"""

import poc_2048_gui 
import random
#import poc_simpletest

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.    
OFFSETS = {UP: (1, 0), 
           DOWN: (-1, 0), 
           LEFT: (0, 1), 
           RIGHT: (0, -1)} 
   
def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    result = []
    #print len(line)
    for i in range (len(line)):
        result.append(0)
    
    j = 0
    for i in range (len(line)):
        if line[i] !=0:
            result[j] = line[i]
            j += 1
    
    last_tile = -1
    merged = False
    final = []
    for i in range (len(line)):
        curr_tile = result[i]
        if merged == False:
                       
            if curr_tile == last_tile:
                final.pop()
                last_tile += curr_tile 
                final.append(last_tile)
                merged = True        
            else:
                final.append(curr_tile)
                last_tile = curr_tile
        
        elif merged == True:
            final.append(curr_tile)
            last_tile = curr_tile
            merged = False
    
    for i in range(len(line)-len(final)):
        final.append(0)
        
    return final

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.cells = []
        self.reset()
        self.initial_tiles_dict = {}
        
        # generate dictionary of initial tiles
        # d = {1: 'a', 2: 'b', 3: 'c'}
        #initial_tiles = {UP: [(0, 0), (0, 1), (0, 2), (0, 3)], 
        #                 DOWN: [(3, 0), (3, 1), (3, 2), (3, 3)]}	
        #				  LEFT:	[(0, 0), (1, 0), (2, 0), (3, 0)]
        #				  RIGHT: [(0, 3), (1, 3), (2, 3), (3, 3)]	
        #			
        up_row = [0 for x in range(self.grid_width)]  # grid_width
        up_col = [x for x in range(self.grid_width)]
        down_row = [self.grid_height-1 for x in range(self.grid_width)]
        down_col = [x for x in range(self.grid_width)]
        left_row = [x for x in range(self.grid_height)]
        left_col = [0 for x in range(self.grid_height)]
        right_row = [x for x in range(self.grid_height)]
        right_col = [self.grid_width-1 for x in range(self.grid_height)]
        
        self.initial_tiles_dict = {UP: zip(up_row,up_col), 
                        DOWN: zip(down_row,down_col),
                        LEFT: zip(left_row, left_col),
                        RIGHT: zip(right_row, right_col)}
                       
    
    def reset(self):
        """
        Reset the game so the grid is empty.
        """
        self.cells = [ [0 for dummy_col in range(self.grid_width)] for dummy_row in range(self.grid_height)]

            
            
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        return str(self.cells)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.grid_height
    
    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.grid_width
                            
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        changed = False
        
        initial_tiles = self.initial_tiles_dict.get(direction)
        #print "initial tiles", initial_tiles
        offset = OFFSETS[direction]

        if direction == UP or direction == DOWN:
            size = self.grid_height
        elif direction == LEFT or direction == RIGHT:
            size = self.grid_width
         
        for tile_index in initial_tiles: 
            
            tile_indices = []
            # iterate through adding offset
            for dummy_i in range(size):
                tile_indices.append(tile_index)
           
                tile_index = [(sum(x)) for x in zip(tile_index,offset)]
                tile_index = tuple(tile_index)
      
            before_merge = []
            for tile_index in tile_indices:
                tile = self.get_tile(tile_index[0], tile_index[1])
                before_merge.append(tile)
            print tile_indices
            
            after_merge = merge(before_merge)

            
            for tile_index, tile_value in zip(tile_indices, after_merge):
                  if tile_value != self.get_tile(tile_index[0], tile_index[1]):
                    self.set_tile(tile_index[0], tile_index[1], tile_value)
                    changed = True
     
        if changed == True:
            self.new_tile()
                    
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty 
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        empty_square_list = [] 
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if self.cells[row][col] == 0:
                    empty_square_list.append((row, col))
 
        index = random.choice(empty_square_list)
        row = index[0]
        col = index[1]
        self.cells[row][col] = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """        
        self.cells[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """        
        return self.cells[row][col]
    
    def set_row(self, row, value):
        """
        Set row of tiles at position row, to have the given values.
        """ 
        for col in range(self.grid_width):
            self.cells[row][col] = value[col]
  
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))