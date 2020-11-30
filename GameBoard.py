import collections

"""
    Types of grid objects
"""
Empty = 0
Wall = 1
Box = 2
Terminal = 3
Player = 4

"""
    grid object is basically a cell on the board, it has a pair of coordinate and type associated with it.
    Basic getters, setters and print_board function is defined for this class, also boolean checks to check type are implemented.
"""
class grid_object:
    def __init__(self, x_coord, y_coord):
        self.Type = Empty
        self.x = x_coord
        self.y = y_coord
    def getType(self)->int:
        return self.Type
    def setType(self, newType)->None:
        if newType > 4 or newType < 0:
            print("Error: Invalid Type specified.")
        else:
            self.Type = newType
    def get_x_coord(self)->int:
        return self.x
    def get_y_coord(self)->int:
        return self.y
    def set_coords(self, x_coord, y_coord)->None:
        self.x = x_coord
        self.y = y_coord
    def print_grid_object(self)->None:
        if self.Type == Empty:
            print(" ", end="")
        elif self.Type == Wall:
            print("#", end="")
        elif self.Type == Box:
            print("$", end="")
        elif self.Type == Terminal:
            print(".", end="")
        elif self.Type == Player:
            print("@", end="")

    def isEmpty(self)->bool:
        return self.Type == Empty
    def isBox(self)->bool:
        return self.Type == Box
    def isPlayer(self)->bool:
        return self.Type == Player
    def isWall(self)->bool:
        return self.Type == Wall
    def isTerm(self)->bool:
        return self.Type==Terminal

"""
    main board object, takes in multiple arguments from the parser class and also basic getters and setters are defined. Will definitely need new functions as we proceed
    with the project.
"""

class GameBoard:
    def __init__(self, rows: int, columns:int, walls: int, boxes: int, terms: int, player_loc: list):
        self.board = collections.defaultdict(dict)
        self.row_count = rows
        self.col_count = columns
        self.wall_count = walls
        self.box_count = boxes
        self.term_count = terms
        self.location = player_loc
        for r in range(1, 1+rows,1):
            self.board[r] = dict()
            for c in range(1, 1+columns, 1):
                self.board[r][c] = grid_object(r,c)
    def init_objects(self, object_coords: list, newType: int)->None:
        for i in range(0, len(object_coords), 2):
            wall_x = int(object_coords[i])
            wall_y = int(object_coords[i+1])
            self.board[wall_x][wall_y].setType(newType)
    
    def debug(self)->None:
        for r in self.board.keys():
            for c in self.board[r].keys():
                self.board[r][c].print_grid_object()
            print("")
    def get_rows(self)->int:
        return self.row_count
    def get_cols(self)->int:
        return self.col_count
    def get_box_count(self)->int:
        return self.box_count
    def get_term_count(self)->int:
        return self.term_count
    def set_player_loc(self, x: int, y: int)->None:
        self.location = [x,y]
        self.board[x][y].setType(Player)
    def get_player_loc(self)->list:
        return self.location
