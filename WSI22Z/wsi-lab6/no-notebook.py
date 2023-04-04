import numpy as np
import gymnasium as gym
import matplotlib.pyplot as plt
from time import sleep
env = gym.make('Taxi-v3', render_mode="ansi")

# Interfejs


class QLearningSolver:
    """Class containing the Q-learning algorithm
     that might be used for different discrete environments."""

    def __init__(self,
                 observation_space: int,
                 action_space: int,
                 learning_rate: float = 0.1,
                 gamma: float = 0.9,
                 epsilon: float = 1,
                 epsilon_mult=0.99,
                 epsilon_min=0.01
                 ):
        self.observation_space = observation_space
        self.action_space = action_space
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon

        self.epsilon_mult = epsilon_mult
        self.epsilon_min = epsilon_min

        self.Q = np.zeros((observation_space.n, action_space.n))

    def __call__(self, state: int, action: int) -> np.ndarray:
        """Return Q-value of given state and action."""
        return self.Q[state, action]

    def update(self, state: int, action: int, reward: float, nextState: int) -> None:
        """Update Q-value of given state and action."""
        current = self.Q[state, action]
        next_best = np.max(self.Q[nextState])
        new = current + self.learning_rate * \
            (reward+self.gamma*next_best - current)
        self.Q[state, action] = new

    def get_best_action(self, state: int) -> np.ndarray:
        """Return action that maximizes Q-value for a given state."""
        return np.argmax(self.Q[state])

    def __repr__(self):
        """Elegant representation of Q-learning solver."""
        pass

    def __str__(self):
        return self.__repr__()

    def update_epsilon(self):
        self.epsilon = max(self.epsilon*self.epsilon_mult, self.epsilon_min)


# ---- 3

penalty_data = []

max_steps = 10000

episode_count = 10000

# s = env.action_space.sample()

qsolver = QLearningSolver(env.observation_space, env.action_space)
for e in range(episode_count):
    qsolver.update_epsilon()
    state, stuff = env.reset()
    counter = 0
    penalty_sum = 0
    while counter < max_steps or True:
        # select random sometimes
        if np.random.rand() < qsolver.epsilon:
            selectedAction = env.action_space.sample()
        else:
            selectedAction = qsolver.get_best_action(state)

        # selectedAction = s
        nextState, r, finished, truncated, stuff = env.step(selectedAction)
        qsolver.update(state, selectedAction, r, nextState)

        state = nextState
        counter += 1
        penalty_sum += r
        # if not counter % 1000:
        #    print("e...", e, counter)

        if finished:  # terminalny
            print("finished", e, counter)
            print("penalty:", penalty_sum)
            penalty_data.append(penalty_sum)
            print(env.render())
            break
