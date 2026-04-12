import random

class DeliveryEnv:

    def __init__(self):
        self.reset()

    def reset(self):

        self.location = "warehouse"
        self.orders = 6
        self.fuel = 10
        self.time = 0

        if self.orders <= 2:
            self.traffic = "low"
        elif self.orders <= 4:
            self.traffic = "medium"
        else:
            self.traffic = "high"

        self.score = 0.0

        self.delivered = 0
        self.total_orders = 6

        return self.get_state()


    def get_state(self):
        return {
            "location": self.location,
            "orders": self.orders,
            "fuel": self.fuel,
            "time": self.time,
            "traffic": self.traffic,
            "score": self.score
        }


    def get_score(self):

        score = self.delivered / (self.total_orders + 1)

        if score <= 0:
            score = 0.1
        elif score >= 1:
            score = 0.9

        return score


    def step(self, action):

        reward = 0
        done = False

        if action == "move":

            self.fuel -= 1
            self.time += 1

            if self.traffic == "high":
                reward = 0.1
                reward -= 0.1
            else:
                reward = 0.3


        elif action == "deliver":

            if self.orders > 0:
                self.orders -= 1
                self.delivered += 1
                reward = 0.5
                reward += 0.2
            else:
                reward = 0.1


        elif action == "refuel":

            self.fuel += 3
            reward = 0.2


        if self.fuel > 5:
            reward += 0.05


        self.traffic = random.choice(["low", "medium", "high"])


        if self.orders == 0:
            done = True

        if self.fuel <= 0:
            done = True


        self.score = self.get_score()

        return self.get_state(), reward, done
