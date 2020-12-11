import collections
import operator
import random
import sys

from GameBoard import GameBoard, State, Action

"""
    Constants
"""
STEPS_MIN = - sys.maxsize - 1
STEPS_MAX = sys.maxsize
MIN_QUALITY = - sys.maxsize - 1
DEFAULT_QUALITY = 1.0  # TODO: Find a good value for this


class PolicyLearner:
    def __init__(self, game_board: GameBoard):
        self.initial_state = game_board
        self.game_board = game_board
        self.state = game_board.get_current_state()
        self.total_steps = 0
        self.terminated = False
        self.learning_rate = 1.0
        self.discount = 1.0
        self.exploration_factor = 1.0
        self.best_steps = STEPS_MAX
        self.quality_values = collections.defaultdict(dict)

    def reset_state(self) -> None:
        self.game_board = self.initial_state
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
                action = self.choose_action()
                next_state = self.get_next_state(action)
                reward = self.calculate_reward(next_state, action)
                self.total_steps += action.action_cost
                next_action = self.choose_best_action(next_state)
                next_action_quality = self.get_quality(next_action, next_state)
                action_quality = self.get_current_quality(action)
                new_quality = action_quality + self.learning_rate * (reward + self.discount * next_action_quality
                                                                     - action_quality)
                self.set_quality(action, new_quality)
                self.update_state(next_state, action)

            if self.game_board.goal_reached():
                self.best_steps = min(self.best_steps, self.total_steps)

    def choose_action(self) -> (Action, float, bool):
        random.seed()
        e = random.random()

        if e < self.exploration_factor or self.state not in self.quality_values:
            valid_actions = self.game_board.get_valid_actions()
            index = random.randrange(0, len(valid_actions))
            return valid_actions[index]

        return self.choose_best_action(self.state)

    def get_next_state(self, action: Action) -> State:
        moved_player_loc = action.box  # after a push action, the player will remain in the original box location

        # after a push action, the box will be at location original + direction
        moved_box_loc = (action.box[0] + action.direction.value[0], action.box[1] + action.direction.value[1])

        box_loc = self.state.boxes.copy()
        box_loc.remove(moved_player_loc)
        box_loc.add(moved_box_loc)
        new_state = State(moved_player_loc, box_loc)

        return new_state

    def choose_best_action(self, state) -> Action:
        # check the q-values dictionary for state to find the one with best q-value
        # key: dict(state: action), value: q-value (number)
        return max(self.quality_values[state].items(), key=operator.itemgetter(1))[0]

    def get_quality(self, action, state) -> float:
        if state in self.quality_values and action in self.quality_values[state]:
            return self.quality_values[state][action]
        return DEFAULT_QUALITY  # TODO: Change to heuristic/computed value

    def get_current_quality(self, action) -> float:
        return self.get_quality(action, self.state)

    def set_quality(self, action, new_quality) -> None:
        if self.state not in self.quality_values:
            self.quality_values[self.state] = dict()
        self.quality_values[self.state][action] = new_quality

    def update_state(self, next_state, action) -> None:
        self.game_board.update_locations(next_state)
        valid_actions = self.game_board.get_valid_actions()
        self.terminated = self.game_board.goal_reached() or not valid_actions
        if not valid_actions:
            # if no valid actions left for next state, it is a terminal state
            # so, set q-value for current state and chosen action as -infinity
            self.set_quality(action, MIN_QUALITY)
        self.state = next_state

    def calculate_reward(self, next_state, action) -> float:
        reward = action.action_cost
        incentive = self.game_board.find_incentive(next_state)
        return reward + incentive
