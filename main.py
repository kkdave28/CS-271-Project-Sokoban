#!/usr/bin/env python3
# Project Sokoban AI for the class of CS 271
# Contributers for this project are Kush Dave, Sriram Rao and Yinan Zhou
import sys
import GameBoard
from Parser import Parser
from PolicyLearner import PolicyLearner

"""
    Main function that creates a parser, a new board and returns it to the main.
"""


def main():
    parser = Parser(sys.argv[1])
    main_board, original_player_loc, original_walls_loc, original_boxes_loc, original_terminal_loc = parser.parse_input()
    print("Solving sokoban game:")
    main_board.debug()

    policyLearner = PolicyLearner(main_board, original_player_loc, original_walls_loc, original_boxes_loc, original_terminal_loc)
    policyLearner.learn(float(sys.argv[2]))

if __name__ == "__main__":
    main()
