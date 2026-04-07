
import random

class DeliveryEnv:

    def __init__(self):
        self.locations = ["A", "B", "C", "D", "E"]
        self.reset()

    def reset(self):
        self.current_location = random.choice(self.locations)
        self.pending_orders = random.randint(2,5)
        self.fuel = 100
        self.time = 0
        self.traffic = random.choice(["Low","Medium","High"])
        self.total_reward = 0

        return self.state()

    def state(self):
        return {
            "location": self.current_location,
            "orders": self.pending_orders,
            "fuel": self.fuel,
            "time": self.time,
            "traffic": self.traffic,
            "score": self.total_reward
        }

    def step(self, action):

        reward = 0

        if action == "deliver" and self.pending_orders > 0:
            self.pending_orders -= 1
            reward = 1

        elif action == "move":
            self.fuel -= 10
            self.time += 1

            if self.traffic == "High":
                reward = 0.2
            elif self.traffic == "Medium":
                reward = 0.4
            else:
                reward = 0.6

        elif action == "refuel":
            self.fuel = 100
            reward = 0.2

        else:
            reward = -0.5

        done = self.pending_orders == 0 or self.fuel <= 0

        self.total_reward += reward

        return self.state(), reward, done
