
from env import DeliveryEnv
import random

env = DeliveryEnv()

state = env.reset()

for i in range(10):

    action = random.choice(["deliver","move","refuel"])

    state, reward, done = env.step(action)

    print("Step:",i)
    print("Action:",action)
    print("State:",state)
    print("Reward:",reward)
    print("------------------")

    if done:
        print("Task Completed")
        print("Final Score:",state["score"])
        break
