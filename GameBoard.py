import collections
import sys
from enum import Enum
import queue
import random

"""
    Types of grid objects
"""


class Object(Enum):
    EMPTY = " "
    WALL = "#"
    BOX = "$"
    TERMINAL = "."
    PLAYER = "@"
    TERMINAL_WITH_BOX = "*"


"""
    Movement directions 
"""


class Move(Enum):
    U = (-1, 0)
    D = (1, 0)
    L = (0, -1)
    R = (0, 1)


"""
    grid object is basically a cell on the board, it has a pair of coordinate and type associated with it.
    Basic getters, setters and print_board function is defined for this class, also boolean checks to check type are 
    implemented.
"""


class GridObject:
    def __init__(self):
        self.Type = Object.EMPTY
        self.is_terminal_loc = False
        self.has_player = False

    def get_type(self) -> Object:
        return self.Type

    def set_type(self, new_type: Object) -> None:
        if (new_type == Object.TERMINAL):
            self.is_terminal_loc = True

        if (new_type == Object.TERMINAL and self.Type == Object.BOX) or (
                new_type == Object.BOX and self.Type == Object.TERMINAL):
            self.Type = Object.TERMINAL_WITH_BOX
            self.is_terminal_loc = True
            return

        if self.is_terminal_loc and new_type == Object.EMPTY:
            self.Type = Object.TERMINAL
            return

        self.Type = new_type

    def print_grid_object(self) -> None:
        print(self.Type.value, end="")

    def is_empty(self) -> bool:
        return Object.EMPTY == self.Type

    def is_box(self) -> bool:
        return Object.BOX == self.Type

    def is_player(self) -> bool:
        return Object.PLAYER == self.Type

    def is_wall(self) -> bool:
        return Object.WALL == self.Type

    def is_terminal(self) -> bool:
        return Object.TERMINAL == self.Type

    def is_terminal_with_box(self) -> bool:
        return Object.TERMINAL_WITH_BOX == self.Type

    def is_obstacle(self) -> bool:
        return self.is_wall() or self.is_box() or self.is_terminal_with_box()



"""
    State class to hold just player and box locations
"""


# TODO: Is this the best way in Python if we want to pass around the state?


class State:
    def __init__(self, player_location: tuple, boxes: set):
        self.player = player_location
        self.boxes = boxes

    def __hash__(self):
        return hash(tuple((self.player, tuple(list(self.boxes)))))

    def __eq__(self, other):
        return isinstance(other, State) and self.player == other.player and self.boxes == other.boxes

    def __repr__(self):
        return "Player at {} and boxes at {}".format(self.player, self.boxes)


"""
    Action class for details about an action being performed: moving a box
"""


# TODO: Is this the best way in Python if we want to pass around the action?


class Action:
    def __init__(self, box_location: tuple, move_direction: Move, action_cost: int, path: str):
        self.box = box_location
        self.direction = move_direction
        self.action_cost = action_cost
        self.path = path

    def __hash__(self):
        return hash(tuple((self.box, self.direction, self.action_cost, self.path)))

    def __eq__(self, other):
        return isinstance(other, Action) and self.__hash__() == other.__hash__()

    def __repr__(self):
        return "Player move {} to push box at {} {}, {} steps.".format(self.path, self.box, self.direction,
                                                                       self.action_cost)


"""
    main board object, takes in multiple arguments from the parser class and also basic getters and setters are 
    defined. Will definitely need new functions as we proceed with the project. 
"""


class GameBoard:
    def __init__(self, rows: int, columns: int, walls: int, boxes: int, terms: int, player_loc: tuple):
        self.board = collections.defaultdict(dict)
        self.box_locations = set()
        self.terminal_locations = set()
        self.row_count = rows
        self.col_count = columns
        self.wall_count = walls
        self.box_count = boxes
        self.term_count = terms
        self.location = player_loc
        for r in range(1, 1 + rows, 1):
            self.board[r] = dict()
            for c in range(1, 1 + columns, 1):
                self.board[r][c] = GridObject()
        self.has_stuck_box = False

    def init_objects(self, object_coords: list, new_type: Object) -> None:
        for i in range(0, len(object_coords), 2):
            row = int(object_coords[i])
            column = int(object_coords[i + 1])
            self.board[row][column].set_type(new_type)
            if Object.BOX == new_type:
                self.box_locations.add((row, column))
            if Object.TERMINAL == new_type:
                self.terminal_locations.add((row, column))

    def debug(self) -> None:
        for r in self.board.keys():
            for c in self.board[r].keys():
                self.board[r][c].print_grid_object()
            print("")

    def get_rows(self) -> int:
        return self.row_count

    def get_cols(self) -> int:
        return self.col_count

    def get_box_count(self) -> int:
        return self.box_count

    def get_term_count(self) -> int:
        return self.term_count

    def move_player(self, destination: tuple) -> None:
        self.set_player_loc(destination[0], destination[1])

    def set_player_loc(self, x: int, y: int) -> None:
        current_location = self.get_player_loc()
        self.board[current_location[0]][current_location[1]].set_type(Object.EMPTY)
        self.location = (x, y)
        self.board[x][y].set_type(Object.PLAYER)

    def get_player_loc(self) -> tuple:
        return self.location

    def is_corner_location(self, x, y):
        obstacle_counts = [0,0,0,0]
        if self.board[x - 1][y - 1].is_obstacle():
            obstacle_counts[0] += 1

        if self.board[x - 1][y + 0].is_obstacle():
            obstacle_counts[0] += 1
            obstacle_counts[1] += 1

        if self.board[x - 1][y + 1].is_obstacle():
            obstacle_counts[1] += 1

        if self.board[x + 0][y + 1].is_obstacle():
            obstacle_counts[1] += 1
            obstacle_counts[2] += 1
            if max(obstacle_counts) == 3:
                return True

        if self.board[x + 1][y + 1].is_obstacle():
            obstacle_counts[2] += 1

        if self.board[x + 1][y + 0].is_obstacle():
            obstacle_counts[2] += 1
            obstacle_counts[3] += 1
            if max(obstacle_counts) == 3:
                return True

        if self.board[x + 1][y - 1].is_obstacle():
            obstacle_counts[3] += 1

        if self.board[x + 0][y - 1].is_obstacle():
            obstacle_counts[0] += 1
            obstacle_counts[3] += 1
            if max(obstacle_counts) == 3:
                return True

        if not self.board[x + 1][y].is_wall() and not self.board[x - 1][y].is_wall():
            return False
        if not self.board[x][y + 1].is_wall() and not self.board[x][y - 1].is_wall():
            return False
        return True

    def update_locations(self, new_state: State) -> None:
        self.move_player(new_state.player)
        unchanged_boxes = self.box_locations.intersection(new_state.boxes)

        for (x, y) in new_state.boxes - unchanged_boxes:
            # ISSUE: if (x,y) used to be Object.TERMINAL, it will be changed to BOX
            if not self.board[x][y].is_terminal() and self.is_corner_location(x, y):
                # the box is stuck at a non-terminal corner, which means game over
                self.has_stuck_box = True
            self.board[x][y].set_type(Object.BOX)

        self.box_locations = new_state.boxes

    def get_current_state(self) -> State:
        # output the current state of the board as a State object
        return State(self.get_player_loc(), self.box_locations)

    def get_valid_actions(self) -> [Action]:
        # if there is a box stuck at corner, there is no valid (meaningful) actions becuase the game is over
        if self.has_stuck_box:
            return []

        # output a list of actions that are valid given current state
        # an action => box location (x,y) + direction
        # an action is valid if following three conditions are met
        #   1. the destination grid is empty
        #   2. the grid opposite to the destination is reachable by the player WITHOUT pushing any box
        reachable_locations = self._get_reachable_locations()
        valid_actions = []

        def _get_path(location: tuple) -> str:
            # find the path from the player location in reachable_locations to the given origin
            # output the path as a string
            path = ""
            while reachable_locations[location][1] is not None:
                # backtrack to the player location
                parent_location = reachable_locations[location][1]
                move = (location[0] - parent_location[0], location[1] - parent_location[1])
                path += ' ' + Move(move).name
                location = parent_location
            return path[::-1]

        for (x, y) in self.box_locations:
            for move in Move:
                (i, j) = move.value
                if self.board[x + i][y + j].is_empty() or self.board[x + i][y + j].is_terminal() or self.board[x + i][y + j].is_player():
                    if (x - i, y - j) in reachable_locations.keys():
                        path = _get_path((x - i, y - j)) + Move(move).name
                        valid_actions.append(Action((x, y), move, reachable_locations[(x - i, y - j)][0] + 1, path))
        return valid_actions

    def _get_reachable_locations(self):
        # output a dictionary of location
        # key is (x,y) tuple, value is (cost, parent (x,y))
        # the parent location is used to backtrack any point to player location along shortest path
        reachable_locations = dict()
        frontier = queue.Queue()

        reachable_locations[self.get_player_loc()] = (0, None)  # player location does not have a parent location
        frontier.put((self.get_player_loc(), 0))

        while not frontier.empty():
            ((x, y), d) = frontier.get()
            for move in Move:
                (i, j) = move.value
                if (x + i, y + j) not in reachable_locations.keys():
                    if self.board[x + i][y + j].is_empty() or self.board[x + i][y + j].is_terminal():
                        reachable_locations[(x + i, y + j)] = (d + 1, (x, y))
                        frontier.put(((x + i, y + j), d + 1))
        return reachable_locations

    def goal_reached(self) -> bool:
        if len(self.box_locations.intersection(self.terminal_locations)) == len(self.terminal_locations):
            return True
        return False

    def find_incentive(self, next_state):
        # find the incentive to be given for the next state as compare to the current state
        curr_total_dist = self._find_distance_to_terminal(self.get_current_state().boxes, self.terminal_locations.copy())
        new_total_dist = self._find_distance_to_terminal(next_state.boxes, self.terminal_locations.copy())
        return curr_total_dist - new_total_dist

    def _find_distance_to_terminal(self, boxes: set, terminals: set) -> int:
        total_distance = 0
        for box in boxes:
            min_dist = sys.maxsize
            nearest_terminal = ""
            for terminal in terminals:
                distance_from_terminal = self._find_distance(box[0], box[1], terminal[0], terminal[1])
                if distance_from_terminal < min_dist:
                    min_dist = distance_from_terminal
                    nearest_terminal = terminal
            terminals.remove(nearest_terminal)
            total_distance += min_dist
        return total_distance

    def _find_distance(self, x1, y1, x2, y2):
        return abs(y2 - y1) + abs(x2 - x1)



