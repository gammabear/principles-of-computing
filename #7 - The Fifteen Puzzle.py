"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui
import math

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value
        
    def _get_target(self, row, col):
        """
        Returns value of tile at it's solved position
        """
        return row * self._width + col
    
    def solved_position(self, value):
        """
        Maps a tile to it's solved position
        Returns a tuple of two integers
        """
        row = (int)(math.floor(value / self._width))
        col = (int)(value % self._width)
        return (row, col)

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction
                
    def get_move_string(self, src_row, src_col, dest_row, dest_col):
        """
        Converts starting tile position, target tile position into move string
        """
        move_string = ""
        x_dist = dest_row - src_row
        y_dist = dest_col - src_col
        if x_dist > 0:
            for dummy_x in range(0, x_dist):
                move_string += "d"
        if x_dist < 0:
            for dummy_x in range(0, abs(x_dist)):
                move_string += "u"
        if y_dist > 0:
            for dummy_y in range(0, y_dist):
                move_string += "r"
        if y_dist < 0:
            for dummy_y in range(0, abs(y_dist)):
                move_string += "l"
        return move_string
    
    
    def relative_pos(self, tile_a, tile_b):
        """
        Returns the relative position of two tiles
        """
        if tile_a[0] > tile_b[0]:
            return "d"
        if tile_a[0] < tile_b[0]:
            return "u"
        if tile_a[1] > tile_b[1]:
            return "r"
        if tile_a[1] < tile_b[1]:
            return "l"

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        cond1, cond2, cond3 = False, False, False
        if (self._grid[target_row][target_col] == 0):
            cond1 = True
        if target_row == self.get_height() - 1  and target_col == self.get_width() - 1:
            cond2 = True
            cond3 = True
        if target_row == self.get_height() - 1: 
            cond2 = True
        if target_col == self.get_width() - 1:
            cond3 = True
        for row in range(target_row + 1, self.get_height()):
            for col in range(0, self.get_width()):
                if (self._grid[row][col] != self._get_target(row, col)):
                    cond2 = False
                    break;
                else:
                    cond2 = True
        for col in range(target_col + 1, self.get_width()):
            if (self._grid[target_row][col] != self._get_target(target_row, col)):
                cond3 = False
                break;
            else:
                cond3 = True
        #print "cond1, 0 at correct" ,cond1
        #print "cond2, bottom row solved", cond2
        #print "cond3, rows to left of zero solved", cond3
       # print "sum", cond1 and cond2 and cond3 
        return cond1 and cond2 and cond3

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, target_col);
        start_row, start_col = self.current_position(target_row, target_col)
        
        move_str = self.position_tile(start_row, start_col, target_row, target_col)
        #assert self.lower_row_invariant(target_row, target_col - 1);
        return move_str
    
    # position tile at target position 
    
    def position_tile(self, start_row, start_col, target_row, target_col):
        """
        Moves a tile from start position to target position
        Updates puzzle and returns a move string
        """
            
        move_str = ""
        tile_number = self.get_number(start_row, start_col);
        print "tile_number:", tile_number
        solved_row, solved_col = self.solved_position(tile_number)
        
        
        curr_row, curr_col = self.current_position(target_row, target_col)
        print "1curr_row, curr_col", curr_row, curr_col
        
        # move 0 to target tile
        zero_row, zero_col = self.current_position(0, 0)
        zero_str = self.get_move_string(zero_row, zero_col, start_row, start_col)
        move_str += zero_str
        self.update_puzzle(zero_str)
        

        # 0 on same row to left
        #print "0 row, curr_row:", zero_row, curr_row
        print "target_row, target_col, exp (1,3)", target_row, target_col
        if zero_row == curr_row:
            print "placeholder"
            move_str += self._shift_right(start_row, start_col, target_row, target_col)
        

        
        
        while (self.get_number(target_row, target_col) != tile_number):
            curr_row, curr_col = self.current_position(solved_row, solved_col)  
            print "number at target", self.get_number(target_row, target_col)  
        
        #for idx in range(0,3):
            while (curr_col != target_col):
                zero_row, zero_col = self.current_position(0, 0)
                curr_row, curr_col = self.current_position(solved_row, solved_col) 
                relative_pos = self.relative_pos((zero_row, zero_col), (curr_row, curr_col))
                print "curr_col, target_col", curr_col, target_col
                print "relative_pos", relative_pos
                
                
                if (curr_col > target_col):
                    print "shift target left"
                    if relative_pos == "r":
                        move_str += "dllur"
                        self.update_puzzle("dllur")
                    if relative_pos == "u":
                        move_str += "ldr"
                        self.update_puzzle("ldr")
                    #if relative_pos == "l":
                    #    move_str += "r"
                    #    self.update_puzzle("r")  # not sure if necessary
                    if relative_pos == "d":
                        move_str += "lur"
                        self.update_puzzle("lur")
                if (curr_col < target_col):
                    print "shift target right"
                    #if relative_pos == "r":
                    #    move_str += "l"
                    #   self.update_puzzle("l")
                    if relative_pos == "u":
                        move_str += "rdl"
                        self.update_puzzle("rdl")
                    if relative_pos == "l":
                        print "relative expected, l", relative_pos
                        move_str += "drrul"         #urrdl
                        self.update_puzzle("drrul") #from #drrul messes up invariant
                    if relative_pos == "d":
                        move_str += "rul"
                        self.update_puzzle("rul")
                
            #print "number, exp 9", self.get_number(target_row, target_col)
            
            if self.current_position(target_row, target_col) == (target_row,target_col):
                break;
                    
            
            zero_row, zero_col = self.current_position(0, 0)
            curr_row, curr_col = self.current_position(solved_row, solved_col)
            relative_pos = self.relative_pos((zero_row, zero_col), (curr_row, curr_col))
        
            if relative_pos == "r":
                move_str += "ullddru"
                self.update_puzzle("ullddru")
            if relative_pos == "u":
                move_str += "lddru"
                self.update_puzzle("lddru")
            if relative_pos == "l":
                move_str += "dru"
                self.update_puzzle("dru")
            move_str += "ld"
            self.update_puzzle("ld")
               
        
        return move_str
    
    def _shift_right(self, start_row, start_col, target_row, target_col):
        """
        Cycles the target tile right to the target position
        Updates puzzle and returns a move string
        """
        move_str = ""
        tile_number = self.get_number(start_row, start_col);
        
        print "3start_row, start_col, exp (1,0)", start_row, start_col
        
        #for i in range (0,3):
        while (self.get_number(target_row, target_col) != tile_number):
            #print "number at target is, exp 2,2,4", self.get_number(target_row, target_col)
            move_str += "urrdl"         
            self.update_puzzle("urrdl")    
        return move_str;
        

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0)
        
        
        move_str = ""
        move_str += "ur"
        self.update_puzzle("ur")  
        
        
        if (self.get_number(target_row, 0) == self._get_target(target_row, 0)):
            zero_row, zero_col = self.current_position(0,0)
            zero_str = self.get_move_string(zero_row, zero_col, target_row - 1, self.get_width() - 1)
            move_str += zero_str
            self.update_puzzle(zero_str)
        
        
        else:
            
            start_row, start_col = self.current_position(target_row, 0)
            move_str += self.position_tile(start_row, start_col, target_row -1, 1)
            
            
            move_str += "ruldrdlurdluurddlur"
            self.update_puzzle("ruldrdlurdluurddlur")
            
            zero_row, zero_col = self.current_position(0,0)
            zero_str = self.get_move_string(zero_row, zero_col, target_row - 1, self.get_width() - 1)
            move_str += zero_str
            self.update_puzzle(zero_str)
                    
        assert self.lower_row_invariant(target_row - 1, self.get_width() - 1)
          
        return move_str

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        cond_zero, cond_row0, cond_row1, cond_lower_row = False, False, False, False
        if (self._grid[0][target_col] == 0):
            cond_zero = True
        if target_col == self.get_width() - 1:
            cond_row0 = True
        
        cond_lower_row = self._check_lower_rows(target_col)
          
            
        for col in range(target_col + 1, self.get_width()):
            if (self._grid[0][col] != self._get_target(0, col)):
                cond_row0 = False
                break;
            else:
                cond_row0 = True
                
        for col in range(target_col, self.get_width()):
            if (self._grid[1][col] != self._get_target(1, col)):
                cond_row1 = False
                break;
            else:
                cond_row1 = True            

        return cond_zero and cond_row0 and cond_row1 and cond_lower_row
    
    def _check_lower_rows(self, target_col):
        """
        Invariant helper function
        Check that bottom rows satisfy solution
        """    
        for row in range(2, self.get_height()):
            for col in range(0, self.get_width()):
                if (self._grid[row][col] != self._get_target(row, col)):
                    cond_lower_row = False
                    break;
                else:
                    cond_lower_row = True
            else:
                continue
            break  
        
        return cond_lower_row

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        cond_zero, cond_row1, cond_lower_row = False, False, False
        if (self._grid[1][target_col] == 0):
            cond_zero = True
        if target_col == self.get_width() - 1:
            cond_row1 = True
        cond_lower_row = self._check_lower_rows(target_col)
        for col in range(target_col + 1, self.get_width()):
            if (self._grid[1][col] != self._get_target(1, col)):
                cond_row1 = False
                break;
            else:
                cond_row1 = True
        return cond_zero and cond_row1 and cond_lower_row

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)
        move_str = ""
        move_str += "ld"
        
        
        self.update_puzzle("ld")
        
        
        if self.current_position(0,target_col) == (0,target_col):
            return move_str
        else:
            print "bleh"
            start_row, start_col = self.current_position(0, target_col)
            print "start row, start col, exp (1,0)", start_row, start_col
            print "target row, target col, exp (1,3)", 1, target_col - 1
            move_str += self.position_tile(start_row, start_col, 1, target_col - 1)

        
            
            move_str +="urdlurrdluldrruld"
            self.update_puzzle("urdlurrdluldrruld")
            
        assert self.row1_invariant(target_col - 1)
        
        return move_str

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col), "row 1 does not satisfy solution"
        move_str = ""
        start_row, start_col = self.current_position(1, target_col)

        move_str += self.position_tile(start_row, start_col, 1, target_col)
        move_str += "ur"  #needed
        self.update_puzzle("ur")
        assert self.row0_invariant(target_col)
        print "move string", move_str
        return move_str

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        return ""

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        return ""

# Start interactive simulation
#p1 = poc_fifteen_gui.FifteenGUI(Puzzle(3, 3, [[1, 8, 2], [3, 4, 5], [6, 7, 0]]))
#p6 = poc_fifteen_gui.FifteenGUI(Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]]))
#p7 = poc_fifteen_gui.FifteenGUI(Puzzle(3, 3, [[3, 2, 1], [6, 5, 4], [7, 0, 8]]))
#p2 = poc_fifteen_gui.FifteenGUI(Puzzle(4, 4, [[4, 3, 1, 6], [5, 8, 2, 7], [0, 9, 10, 11], [12, 13, 14, 15]]))
#p3 = poc_fifteen_gui.FifteenGUI(Puzzle(4, 4, [[4, 1, 3, 13], [5, 10, 2, 7], [8, 12, 6, 11], [9, 0, 14, 15]]))
#pcol0 = poc_fifteen_gui.FifteenGUI(Puzzle(4, 4, [[4, 1, 3, 12], [5, 10, 2, 7], [8, 9, 6, 11], [0, 13, 14, 15]]))
#p4 = poc_fifteen_gui.FifteenGUI(Puzzle(3, 2, [[2, 1], [3, 4], [0, 5]]))
#p8 = poc_fifteen_gui.FifteenGUI(Puzzle(4, 5, [[12, 11, 10, 9, 8], [7, 6, 5, 4, 3], [2, 1, 0, 13, 14], [15, 16, 17, 18, 19]]))
#p5 = poc_fifteen_gui.FifteenGUI(Puzzle(4, 4, [[4, 13, 1, 3], [5, 10, 2, 7], [8, 12, 6, 11], [9, 0, 14, 15]]))
#p9 = poc_fifteen_gui.FifteenGUI(Puzzle(3, 3, [[3, 2, 1], [6, 5, 4], [0, 7, 8]]))
#p10 = poc_fifteen_gui.FifteenGUI(Puzzle(4, 4, [[4, 2, 1, 3], [5, 6, 0, 7], [8, 9, 10, 11], [12, 13, 14, 15]]))
#p11 = poc_fifteen_gui.FifteenGUI(Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]]))
#p12 = poc_fifteen_gui.FifteenGUI(Puzzle(3, 3, [[4, 1, 0], [2, 3, 5], [6, 7, 8]]))
#p13 = poc_fifteen_gui.FifteenGUI(Puzzle(4, 5, [[7, 6, 5, 3, 2], [9, 1, 4, 8, 0], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]]))
#p14 = poc_fifteen_gui.FifteenGUI(Puzzle(3, 3, [[2, 5, 4], [1, 3, 0], [6, 7, 8]]))
#p15 = poc_fifteen_gui.FifteenGUI(Puzzle(4, 5, [[8, 2, 10, 9, 1], [7, 6, 5, 4, 3], [0, 11, 12, 13, 14], [15, 16, 17, 18, 19]]))
#p1 = Puzzle(3, 3, [[0, 1, 2], [3, 4, 5], [6, 7, 8]])
#p16 = poc_fifteen_gui.FifteenGUI(Puzzle(4, 5, [[7, 6, 5, 3, 0], [4, 8, 2, 1, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]]))
pa = poc_fifteen_gui.FifteenGUI(Puzzle(4, 4, [[4, 2, 3, 7], [8, 5, 6, 10], [9, 1, 0, 11], [12, 13, 14, 15]]))

#print p1._puzzle
#print p2._puzzle
#print p3._puzzle
#print pcol0._puzzle
#print p4._puzzle
#print p6._puzzle
print pa._puzzle

#p._puzzle.set_number(3, 3, 0)
#p._puzzle.set_number(0, 0, 15)
#p._puzzle.set_number(3, 3,8)
#p._puzzle.set_number(3,4,8) #break condition 3
#print p._puzzle.lower_row_invariant(3, 3)
#print "curr position", p._puzzle.current_position(3,3)
#p1._puzzle.solve_interior_tile(2, 2)
#p3._puzzle.solve_interior_tile(3, 1)
#p2._puzzle.solve_interior_tile(2,0)
#p9._puzzle.solve_col0_tile(2)
#p4._puzzle.solve_interior_tile(1,1)
#p5._puzzle.solve_interior_tile(3,1)
#pcol0._puzzle.solve_col0_tile(3)
#p3._puzzle.solve_interior_tile(3, 1)
#p6._puzzle.solve_interior_tile(2,2)
#print p11._puzzle.row0_invariant(2)
#p14._puzzle.solve_row1_tile(2)
#p13._puzzle.solve_row1_tile(2)
#p15._puzzle.solve_col0_tile(2)
#p16._puzzle.solve_row0_tile(4)
pa._puzzle.solve_interior_tile(2,2)