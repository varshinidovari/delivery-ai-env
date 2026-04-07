import random
from env import DeliveryEnv

print("[START]")

env = DeliveryEnv()

state = env.reset()
done = False
steps = 0

while not done and steps < 20:

    action = random.choice(["deliver", "move", "refuel"])
    state, reward, done = env.step(action)

    print(f"[STEP] action={action} reward={reward} score={state['score']}")

    steps += 1

print(f"[END] Final Score={state['score']}")
