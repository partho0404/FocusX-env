import random

class FocusEnv:
    def __init__(self):
        self.state = None
        self.step_count = 0
        self.max_steps = 10
        self.reset()

    def reset(self):
        self.step_count = 0
        self.state = {
            "energy": random.randint(40, 100),
            "focus": random.randint(40, 100),
            "distraction": random.randint(0, 50),
            "tasks_left": 5
        }
        return self.state

    def step(self, action):
        self.step_count += 1
        reward = 0.0

        if action == "study":
            self.state["focus"] = min(100, self.state["focus"] + 10)
            self.state["energy"] = max(0, self.state["energy"] - 10)
            self.state["tasks_left"] = max(0, self.state["tasks_left"] - 1)
            reward = 1.0
        elif action == "rest":
            self.state["energy"] = min(100, self.state["energy"] + 20)
            self.state["distraction"] = max(0, self.state["distraction"] - 10)
            reward = 0.5
        elif action == "scroll":
            self.state["distraction"] = min(100, self.state["distraction"] + 20)
            self.state["focus"] = max(0, self.state["focus"] - 10)
            reward = -0.5

        done = self.step_count >= self.max_steps or self.state["tasks_left"] == 0
        return self.state, reward, done, {}

    def get_state(self):
        return self.state
