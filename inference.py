
import random
from env import DeliveryEnv

print("[START]")

env = DeliveryEnv()

tasks = ["easy", "medium", "hard"]

for task in tasks:

    print("[STEP] Task:", task)

    state = env.reset()
    done = False
    steps = 0

    while not done and steps < 20:

        action = random.choice(["deliver","move","refuel"])

        state, reward, done = env.step(action)

        print("[STEP]")
        print("action:", action)
        print("reward:", reward)
        print("score:", state["score"])

        steps += 1

    print("[END] Task:", task)
    print("Final Score:", state["score"])

print("[END]")
