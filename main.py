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
    main_board = parser.parse_input()
    main_board.debug()

    policyLearner = PolicyLearner(main_board)

    policyLearner.learn(10000,1)
    print("done")



if __name__ == "__main__":
    main()
