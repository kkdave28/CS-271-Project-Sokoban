#!/usr/bin/env python3
# Project Sokoban AI for the class of CS 271
# Contributers for this project are Kush Dave, Sriram Rao and Yinan Zhou
import sys

game_board = {}

Empty = 0
Wall = 1
Box = 2
Terminal = 3
Player = 4

global_rows = -1
global_cols = -1
global_walls = -1
global_boxes = -1
global_terms = -1

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
            print("debug", end="")
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
def parse_input(filename: str) -> None:
    input_file = open(filename, "r") # open the file
    input_lines = input_file.read().split("\n") # get each line as individual list object
    
    """ debug"""
    print(input_lines)

    """
        first line specifies the dimensions of the board eg 3 (rows) x 5 (columns)
        second line specifies the location of walls with the first integer specifying number of walls
        third line specifies the number of boxes and their coordinates
        fourth line specifies the number of terminal locations and their coordinates
        fifth line specifies the player location
    """
    
    board_dimensions = input_lines[0].split()
    walls = input_lines[1].split()
    boxes = input_lines[2].split()
    terminals = input_lines[3].split()
    player_loc = input_lines[4].split()
    
    global_walls = int(walls[0])
    walls.pop(0)
    global_boxes = int(boxes[0][0])
    boxes.pop(0)
    global_terms = int(terminals[0][0])
    terminals.pop(0)
    global_rows = int(board_dimensions[0])
    global_cols = int(board_dimensions[1])
    
    if(len(board_dimensions) != 2):
        print("Error: Board dimensions are not specified coorectly")
        return
    """
        Generate the board with empty grid object.
    """
    for r in range(1, 1+global_rows,1):
        game_board[r] = {}
        for c in range(1, 1+global_cols,1):
            game_board[r][c] = grid_object(r,c)
    """
        Assign walls
    """
    for x in game_board.keys():
        for y in game_board[x].keys():
            game_board[x][y].print_grid_object()
    for i in range(0, len(walls), 2):
        wall_x = walls[i]
        wall_y = walls[i+1]
        print(wall_y)
        game_board[wall_x][wall_y].setType(Wall)


def main():
    parse_input(sys.argv[1])

if __name__ == "__main__":
    main()