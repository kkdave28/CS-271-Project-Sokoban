from GameBoard import GameBoard, Object


class Parser:
    def __init__(self, path: str) -> None:
        self.filename = path

    def parse_input(self) -> GameBoard:
        input_file = open(self.filename, "r")  # open the file
        input_lines = input_file.read().split("\n")  # get each line as individual list object

        """
            first line specifies the dimensions of the board eg 3 (rows) x 5 (columns)
            second line specifies the location of walls with the first integer specifying number of walls
            third line specifies the number of boxes and their coordinates
            fourth line specifies the number of terminal locations and their coordinates
            fifth line specifies the player location
        """

        """
            Parsing input
        """
        board_dimensions = input_lines[0].split()
        walls = input_lines[1].split()
        boxes = input_lines[2].split()
        terminals = input_lines[3].split()
        player_loc_str = input_lines[4].split()
        player_loc = (int(player_loc_str[0]), int(player_loc_str[1]))

        wall_count = int(walls[0])
        walls.pop(0)
        boxes_count = int(boxes[0][0])
        boxes.pop(0)
        term_count = int(terminals[0][0])
        terminals.pop(0)
        cols = int(board_dimensions[0])
        rows = int(board_dimensions[1])

        if len(board_dimensions) != 2:
            print("Error: Board dimensions are not specified correctly")
            return None
        """
            Create a new GameBoard object and initialize all walls/boxes/terminals and player
        """
        x = GameBoard(rows, cols, wall_count, boxes_count, term_count, player_loc)
        """
            Generic function can be called repeatedly with different args
        """
        x.init_objects(walls, Object.WALL)
        x.init_objects(boxes, Object.BOX)
        x.init_objects(terminals, Object.TERMINAL)
        x.init_objects(player_loc, Object.PLAYER)
        """
            return the newly created object to the caller.
        """
        return x
