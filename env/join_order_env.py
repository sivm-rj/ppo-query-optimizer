import gymnasium as gym
from gymnasium import spaces
import numpy as np

def mock_cost(plan):
    cost = 0
    for i in range(1, len(plan)):
        if abs(plan[i] - plan[i - 1]) > 1:
            cost += 5
        else:
            cost += 1
    return cost

class JoinOrderEnv(gym.Env):
    def __init__(self, num_tables=20):
        self.num_tables = num_tables
        self.tables = list(range(num_tables))
        self.action_space = spaces.Discrete(num_tables)
        self.observation_space = spaces.MultiBinary(num_tables)
        self.reset()

    def reset(self, seed=None, options=None):
        self.remaining = self.tables.copy()
        self.plan = []
        return self._get_obs(), {}

    def _get_obs(self):
        obs = np.zeros(self.num_tables, dtype=int)
        for t in self.remaining:
            obs[t] = 1
        return obs

    def step(self, action):
        if action not in self.remaining:
            return self._get_obs(), -10, False, False, {}

        self.plan.append(action)
        self.remaining.remove(action)

        done = len(self.plan) == self.num_tables
        reward = -mock_cost(self.plan) if done else 0
        return self._get_obs(), reward, done, False, {}
