import collections
import operator
import random
import sys
import math
import time

from GameBoard import GameBoard, State, Action, Object

"""
    Constants
"""
STEPS_MIN = - sys.maxsize - 1
STEPS_MAX = sys.maxsize
MIN_QUALITY = - sys.maxsize - 1
MAX_QUALITY = 100
DEFAULT_QUALITY = 0.0  # TODO: Find a good value for this


class PolicyLearner:
    def __init__(self, game_board: GameBoard, original_player_loc, original_walls_loc, original_boxes_loc, original_terminal_loc):
        self.game_board = game_board
        self.state = game_board.get_current_state()
        self.terminated = False
        self.learning_rate = 1.0
        self.discount = 1.0
        self.exploration_factor = 1.0
        self.quality_values = collections.defaultdict(dict)

        self.original_player_loc = original_player_loc
        self.original_walls_loc = original_walls_loc
        self.original_boxes_loc = original_boxes_loc
        self.original_terminal_loc = original_terminal_loc

    def reset_state(self) -> None:
        self.game_board = GameBoard(self.game_board.row_count, self.game_board.col_count,
                                    self.game_board.wall_count, self.game_board.box_count,
                                    self.game_board.term_count, self.original_player_loc)
        self.game_board.init_objects(self.original_walls_loc, Object.WALL)
        self.game_board.init_objects(self.original_boxes_loc, Object.BOX)
        self.game_board.init_objects(self.original_terminal_loc, Object.TERMINAL)
        self.game_board.init_objects([c for c in self.original_player_loc], Object.PLAYER)
        self.terminated = False

    def learn(self, learning_time: int) -> None:
        start = time.time()
        current_time = 0
        while current_time < learning_time:
            if current_time % 1000 == 0:
                print("----------------------------time " + str(current_time) + "------------------------------")

            self.reset_state()
            # self.exploration_factor = math.cos((current_time / learning_time) * math.pi / 2)
            self.exploration_factor = (learning_time - current_time) / learning_time
            # self.exploration_factor = math.sqrt(1 - (current_time / learning_time) ** 2.5)
            # self.exploration_factor = math.sqrt(1 - (current_time / learning_time) ** 2)
            # self.discount = current_time / learning_time
            # self.discount = (math.e + 1) / math.e - 1 / (math.exp(current_time / learning_time))
            # self.learning_rate = math.sqrt(1 - (current_time / learning_time) ** 3)
            # self.learning_rate = (learning_time - current_time) / learning_time
            # self.learning_rate = math.cos((current_time / learning_time) * math.pi / 2)
            # self.learning_rate = 1 / math.exp(current_time / learning_time)
            while not self.terminated:
                action = self.choose_action()
                if action is None:
                    self.terminated = True
                    # print("No actions in this iteration")
                    break
                next_state = self.get_next_state(action)
                # reward = self.calculate_reward(next_state, action)
                reward = -action.action_cost
                old_state = self.game_board.get_current_state()
                action_quality = self.get_current_quality(action)   # old action quality

                self.update_state(next_state)

                # print("old state: ", old_state)
                # print("take action: ", action)
                # print("reward: ", reward)
                # print("action_quality: ", action_quality)
                # print("new state: ", next_state)

                # print("---------------------------------------------------------")
                # self.game_board.debug()
                # print("---------------------------------------------------------")

                # print(self.quality_values)

                if self.terminated:
                    # goal state reached
                    self.set_quality(old_state, action, MAX_QUALITY - action.action_cost)
                    # print("----------------------------time " + str(current_time) + "------------------------------")
                    # print("Goal state reached!")
                    break

                new_action = self.choose_best_action()
                if new_action is None:
                    # if no valid_actions: # and goal is not reached
                    #     # if no valid actions left for next state, it is a terminal state
                    #     # so, set q-value for current state and chosen action as -infinity
                    self.terminated = True
                    self.set_quality(old_state, action, MIN_QUALITY)
                    # print("No more actions")
                    break
                new_action_quality = self.get_quality(new_action, self.game_board.get_current_state())

                new_quality = action_quality + self.learning_rate * (reward + self.discount * new_action_quality
                                                                     - action_quality)
                self.set_quality(old_state, action, new_quality)
                # print(self.quality_values)

            current_time += 1
        print("Time is up. done learning")
        # print("final q table: ", self.quality_values)

        final_total_steps = 0
        self.reset_state()
        best_action = None
        visited_states = set()
        while not self.terminated:
            current_state = self.game_board.get_current_state()
            if current_state in self.quality_values:
                if current_state in visited_states:
                    print("states start to loop, no solution found")
                    break
                visited_states.add(current_state)
                self.game_board.debug()
                # print("Looking for actions")
                # for current_action in self.quality_values[current_state]:
                #     print(current_action)
                #     print(self.quality_values[current_state][current_action])
                best_action = max(self.quality_values[current_state].items(), key=operator.itemgetter(1))[0]

                final_total_steps += best_action.action_cost
                print("Chosen action:")
                print(best_action)
                next_state = self.get_next_state(best_action)
                self.update_state(next_state)
            else:
                print(current_state)
                print("not in q table")
                self.terminated = True
        self.game_board.debug()
        print(final_total_steps)
        print("Solution is found")

        end = time.time()
        print("learn function took ", end - start)

    def choose_action(self) -> (Action, float, bool):
        random.seed()
        e = random.random()

        if e < self.exploration_factor or self.game_board.get_current_state() not in self.quality_values:
            valid_actions = self.game_board.get_valid_actions()
            if len(valid_actions) == 0:
                return None
            index = random.randrange(0, len(valid_actions))
            return valid_actions[index]
        return self.choose_best_action()

    def get_next_state(self, action: Action) -> State:
        moved_player_loc = action.box  # after a push action, the player will remain in the original box location

        # after a push action, the box will be at location original + direction
        moved_box_loc = (action.box[0] + action.direction.value[0], action.box[1] + action.direction.value[1])

        box_loc = self.game_board.get_current_state().boxes.copy()
        box_loc.remove(moved_player_loc)
        box_loc.add(moved_box_loc)
        new_state = State(moved_player_loc, box_loc)

        return new_state

    def choose_best_action(self):
        # check the q-values dictionary for state to find the one with best q-value
        # key: dict(state: action), value: q-value (number)
        current_state = self.game_board.get_current_state()
        if current_state in self.quality_values:
            return max(self.quality_values[current_state].items(), key=operator.itemgetter(1))[0]

        valid_actions = self.game_board.get_valid_actions()
        if len(valid_actions) == 0:
            return None
        index = random.randrange(0, len(valid_actions))
        return valid_actions[index]

    def get_quality(self, action, state) -> float:
        if state in self.quality_values and action in self.quality_values[state]:
            return self.quality_values[state][action]
        return DEFAULT_QUALITY

    def get_current_quality(self, action) -> float:
        return self.get_quality(action, self.game_board.get_current_state())

    def set_quality(self, state, action, new_quality) -> None:
        if state not in self.quality_values:
            self.quality_values[state] = dict()
        self.quality_values[state][action] = new_quality

    def update_state(self, next_state) -> None:
        self.game_board.update_locations(next_state)
        self.terminated = self.game_board.goal_reached()

    def calculate_reward(self, next_state, action) -> float:
        reward = -action.action_cost
        incentive = self.game_board.find_incentive(next_state)
        # incentive = self.game_board.get_placed_boxes(next_state)
        return reward + incentive
