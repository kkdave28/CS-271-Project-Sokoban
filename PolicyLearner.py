import collections
import random
import sys

from GameBoard import GameBoard, State, Action, Move

"""
    Constants
"""
STEPS_MIN = - sys.maxsize - 1
STEPS_MAX = sys.maxsize


class PolicyLearner:
    def __init__(self, game_board: GameBoard):
        self.initial_state = game_board
        self.state_board = game_board
        self.state = State(game_board.get_player_loc(), game_board.box_locations)
        self.total_steps = 0
        self.terminated = False
        self.learning_rate = 1.0
        self.discount = 1.0
        self.exploration_factor = 1.0
        self.best_steps = STEPS_MAX
        self.quality_values = collections.defaultdict(dict)

    def reset_state(self) -> None:
        self.state_board = self.initial_state
        self.total_steps = 0
        self.terminated = False

    def learn(self, learning_time: int, learning_threshold: float) -> None:
        current_time = 0
        total_steps = STEPS_MIN
        while current_time < learning_time and (self.total_steps - total_steps > learning_threshold):
            if total_steps == STEPS_MIN:
                total_steps = 0
            self.reset_state()
            while not self.terminated:
                action, reward, terminated = self.choose_action()
                next_state, move_steps = self.perform(action)
                self.total_steps += move_steps
                next_action = self.choose_best_action(next_state)
                next_action_quality = self.get_quality(next_action, next_state)
                action_quality = self.get_current_quality(action)
                new_quality = action_quality + self.learning_rate * (reward + self.discount * next_action_quality
                                                                     - action_quality)
                self.set_quality(action, new_quality)
                self.update_state(next_state)

            if self.state_board.goal_reached():
                self.best_steps = min(self.best_steps, self.total_steps)

    def choose_action(self) -> (Action, float, bool):
        # TODO: placeholder for choose action logic
        random.seed()
        e = random.random()
        if e < self.exploration_factor:
            pass  # TODO: choose a random permitted action
        else:
            self.choose_best_action(self.state)

        action = Action((0, 0), Move.DOWN)
        reward = -1
        terminated = False
        return action, reward, terminated

    def perform(self, action) -> (State, int):
        moved_player, moved_box, move_steps = self.state_board.tentative_move_box(action.box, action.direction)
        new_state = self.state
        new_state.player = moved_player
        new_state.boxes.remove(action.box)
        new_state.boxes.add(moved_box)
        return new_state, move_steps

    def choose_best_action(self, state) -> Action:
        # TODO: check the q-values dictionary for state to find the one with best q-value
        return Action((0, 0), Move.DOWN)

    def get_quality(self, action, state) -> float:
        if state in self.quality_values and action in self.quality_values[state]:
            return self.quality_values[state][action]
        return 1.0  # TODO: Correct the default q-value

    def get_current_quality(self, action) -> float:
        return self.get_quality(action, self.state)

    def set_quality(self, action, new_quality) -> None:
        if self.state not in self.quality_values:
            self.quality_values[self.state] = dict()
        self.quality_values[self.state][action] = new_quality

    def update_state(self, next_state) -> None:
        self.state_board.update_locations(next_state)
        self.state = next_state
