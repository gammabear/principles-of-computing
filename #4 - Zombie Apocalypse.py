"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        self._grid_height = grid_height
        self._grid_width = grid_width
        
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._human_list = []
        self._zombie_list = []
        
        
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row,col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)
      
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        num = 0
        while num < self.num_zombies():
            yield self._zombie_list[num]
            num = num + 1
        

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row,col))
        
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
   
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        num = 0
        while num < self.num_humans():
            yield self._human_list[num]
            num = num + 1
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        
        self._visited = poc_grid.Grid(self._grid_height, self._grid_width)
        self._distance_field = []
        self._distance_field = [ [self._grid_height * self._grid_width for dummy_col in range(self._grid_width)] for dummy_row in range(self._grid_height)]
         
        self._boundary = poc_queue.Queue()
        
        if entity_type == ZOMBIE:
            for cell in self._zombie_list:
                self._boundary.enqueue(cell)
        elif entity_type == HUMAN:
            for cell in self._human_list:
                self._boundary.enqueue(cell)
            
        for cell in self._boundary:
            self._visited.set_full(cell[0], cell[1])
            self._distance_field[cell[0]][cell[1]] = 0
            
        for row in range(self._grid_height):
            for col in range(self._grid_width):
                if self._cells[row][col] == FULL:
                    self._visited.set_full(row, col)

        while len(self._boundary) > 0:
            current_cell = self._boundary.dequeue()

            neighbors = self._visited.four_neighbors(current_cell[0], current_cell[1])
            for neighbor in neighbors:
                if self._visited.is_empty(neighbor[0], neighbor[1]):
                    self._visited.set_full(neighbor[0], neighbor[1])
                    self._distance_field[neighbor[0]][neighbor[1]] = self._distance_field[current_cell[0]][current_cell[1]] + 1
                    self._boundary.enqueue(neighbor)
                    
                    
        return self._distance_field 
        
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        
        zombie_grid = poc_grid.Grid(self._grid_height, self._grid_width)
        
        best_moves = []
        
        for human in self._human_list:
            possible_moves = zombie_grid.eight_neighbors(human[0], human[1])
            possible_moves.append(human)
            #best_move = ()
            
            possible_best_move = []
            max_distance = 0
            for move in possible_moves:
                distance = zombie_distance[move[0]][move[1]]
                if distance >= max_distance and distance < self._grid_height * self._grid_width:
                    
                    if distance == max_distance:
                        possible_best_move.append(move)
                    else:
                        del possible_best_move[:]
                        possible_best_move.append(move)
                    max_distance = zombie_distance[move[0]][move[1]]
 
            random.shuffle(possible_best_move)
            best_moves.append(possible_best_move[0])
        self._human_list = best_moves
        
    
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        human_grid = poc_grid.Grid(self._grid_height, self._grid_width)
        best_moves = []
        for zombie in self._zombie_list:
            possible_moves = human_grid.four_neighbors(zombie[0],zombie[1])
            possible_moves.append(zombie)
            #best_move = ()
            min_distance = self._grid_height * self._grid_width
            
            possible_best_move = []
            for move in possible_moves:
                distance = human_distance[move[0]][move[1]]
                if distance <= min_distance:
                    if distance == min_distance:
                        possible_best_move.append(move)
                    else:
                        del possible_best_move[:]
                        possible_best_move.append(move)
                    min_distance = human_distance[move[0]][move[1]]
 
            random.shuffle(possible_best_move)
            best_moves.append(possible_best_move[0])
        self._zombie_list = best_moves

# start up gui for simulation
poc_zombie_gui.run_gui(Zombie(30, 40))

#zombie = Zombie(3,3)
#zombie.add_zombie(0,2)
#zombie.add_zombie(1,1)
#zombie.add_zombie(2,0)


#print zombie.compute_distance_field(ZOMBIE)

#zombie2 = Zombie(5,5)
#zombie2.add_zombie(0,0)
#zombie2.set_full(3,2)
#zombie2.set_full(2,2)
#zombie2.set_full(1,2)
#zombie2.set_full(0,2)
#zombie2.add_human(3,3)

#zombie3 =Zombie(3, 3, [], [(2, 2)], [(1, 0)])
#dist = [[4, 3, 2], [3, 2, 1], [2, 1, 0]]
#zombie3.move_humans(dist)

#print zombie2.compute_distance_field(ZOMBIE)

#print "zombies at: ", zombie2._zombie_list 
