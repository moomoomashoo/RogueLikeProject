import constants
from random import randrange
from random import seed

class CA_CaveFactory:
    def __init__(self, length, width, initial_open = 0.40):
        #seed(constants.SEED)
        self.__length = length
        self.__width = width
        self.__area = length * width
        self.__map = []
        self.__plat_map = []
        self.__up_loc = 0
        self.__center_pt = (int(self.__length/2), int(self.__width/2))
        self.__gen_initial_map(initial_open)
      
    def print_grid(self):
        for r in range(0, self.__length):
            for c in range(0, self.__width):
                if self.__map[r][c] in (constants.WALL, constants.PERM_WALL):
                    print('#', end = " ")
                elif self.__map[r][c] is "S":
                    print('S', end = " ")
                elif self.__map[r][c] is "E":
                    print('E', end = " ")
                elif self.__map[r][c] is 8:
                    print('f', end = " ")
                else:
                    print('.', end = " ")
            print("")
        print("")
    
    def gen_map(self):
        for r in range(1, self.__length-1):
            for c in range(1, self.__width-1):
                wall_count = self.__adj_wall_count(r,c)
                
                if self.__map[r][c] == constants.FLOOR:
                    if wall_count > 5 and self.__map[r][c]:
                        self.__map[r][c] = constants.WALL
                elif wall_count < 4 and self.__map[r][c] is not constants.SPAWN_POINT:
                    self.__map[r][c] = constants.FLOOR
                    
        return self.__map
        
    def __set_border(self):
        for j in range(0, self.__length):
            self.__map[j][0] = constants.PERM_WALL
            self.__map[j][self.__width-1] = constants.PERM_WALL
            
        for j in range(0, self.__width):
            self.__map[0][j] = constants.PERM_WALL
            self.__map[self.__length-1][j] = constants.PERM_WALL
    
    def __gen_initial_map(self, initial_open):
        for r in range(0, self.__length):
            row = []
            plat_row = []
            for c in range(0, self.__width):
                row.append(constants.WALL)
                plat_row.append(0)
            self.__map.append(row)
            self.__plat_map.append(plat_row)
            
        open_count = int(self.__area * initial_open)
        
        self.__set_border()
        
        while open_count > 0:
            rand_r = randrange(1, self.__length-1)
            rand_c = randrange(1, self.__width-1)
        
            if self.__map[rand_r][rand_c] == constants.WALL:
                self.__map[rand_r][rand_c] = constants.FLOOR
                open_count -= 1
        
        #self.__set_spawn()
    
    def __adj_wall_count(self, sr, sc):
        count = 0
        
        for r in (-1, 0, 1):
            for c in (-1, 0, 1):
                if self.__map[(sr + r)][sc + c] != constants.FLOOR and not(r == 0 and c == 0):
                    count += 1
                    
        return count
    
    def __adj_floor_count(self, sr, sc):
        count = False
        
        for r in (-1, 0):
            if self.__map[(sr + r)][(sc)] == constants.FLOOR:
                if self.__map[sr + 1][sc] == constants.WALL:
                    count = True
                    
        return count
        
    def __adj_floor_count_e(self, sr, sc):
        count = False
        
        for r in (-1, 0):
            if self.__map[(sr + r)][(sc)] == constants.PERM_FLOOR:
                if self.__map[sr + 1][sc] == constants.WALL:
                    count = True
                    
        return count
        
    def set_object_spawn(self, _object, max_num_object, spawn_on_floor):
        object_num = max_num_object
        while object_num > 0:
            rand_r = randrange(2, self.__length-2)
            rand_c = randrange(2, self.__width-2)
            if self.__map[rand_r][rand_c] == constants.PERM_FLOOR:
                if spawn_on_floor:
                    if self.__map[rand_r+1][rand_c] == constants.WALL:
                        self.__map[rand_r][rand_c] = _object
                        object_num -= 1
                    else:
                        ()
                else:
                    self.__map[rand_r][rand_c] = _object
                    object_num -= 1
        
    def set_spawn(self):
        spawn_count = 1
        while spawn_count > 0:
            rand_r = randrange(2, self.__length-2)
            rand_c = randrange(2, self.__width-2)
            floor_count = self.__adj_floor_count(rand_r, rand_c)
            if floor_count:
                for r in (-1, 0):
                    for c in (-1, 0, 1):
                        self.__map[rand_r + r][rand_c + c] = constants.FLOOR
                self.__map[rand_r][rand_c] = constants.SPAWN_POINT
                spawn_count -= 1
                
    def get_spawn(self):
        spawn = []
        for r in range(1, self.__length-1):
            for c in range(1, self.__width-1):
                if self.__map[r][c] == constants.SPAWN_POINT:
                    spawn.append(r)
                    spawn.append(c)
                    return spawn
                    
    
    def set_exit(self):
        exit_count = 1
        while exit_count > 0:
            rand_r = randrange(2, self.__length-2)
            rand_c = randrange(2, self.__width-2)
            floor_count = self.__adj_floor_count_e(rand_r, rand_c)
            if floor_count:
                for r in (-1, 0):
                    for c in (-1, 0, 1):
                        self.__map[rand_r + r][rand_c + c] = constants.PERM_FLOOR
                self.__map[rand_r][rand_c] = constants.EXIT_POINT
                exit_count -= 1
                
    def flood_fill(self, lev, x, y, oldChar, newChar):
        if lev[x][y] != oldChar:
            return
        
        lev[x][y] = newChar
        
        if x > 0:
            self.flood_fill(lev, x-1, y, oldChar, newChar)
        if y > 0:
            self.flood_fill(lev, x, y-1, oldChar, newChar)
        if x < self.__width-1:
            self.flood_fill(lev, x+1, y, oldChar, newChar)
        if y < self.__length-1:
            self.flood_fill(lev, x, y+1, oldChar, newChar)    
    
    def check_percent_fill(self, lev):
        count = 0
        for r in range(1, self.__length-1):
            for c in range(1, self.__width-1):
                if lev[r][c] == constants.PERM_FLOOR:
                    count += 1
                    
        if count/self.__area > 0.4:
            return True
        
        return False
    
    def what_dirt(self):
        """for r in (-1, 0, 1):
            for c in (-1, 0, 1):
                if self.__map[(sr + r)][sc + c] != constants.FLOOR and not(r == 0 and c == 0):
                    ()"""
        return self.__plat_map
    
                    
#caf = CA_CaveFactory(50, 50, 0.41)
#caf.gen_map()
#caf.print_grid()