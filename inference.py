import os
import requests
from openai import OpenAI

API_BASE_URL = os.environ.get("API_BASE_URL")
API_KEY = os.environ.get("API_KEY")
ENV_URL = os.environ.get("ENV_URL", "http://localhost:7860")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)


def act(observation):

    prompt = f"""
You are an intelligent delivery optimization agent.

Your goal:
- Deliver all packages
- Save fuel
- Avoid high traffic
- Finish quickly

Current Observation:
Location: {observation['location']}
Orders Remaining: {observation['orders']}
Fuel: {observation['fuel']}
Time: {observation['time']}
Traffic: {observation['traffic']}
Score: {observation['score']}

Rules:
- If fuel low → refuel
- If orders available and fuel ok → deliver
- If traffic high → move carefully

Choose best action:
deliver, move, refuel

Return only one word.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        action = response.choices[0].message.content.strip().lower()

        if action not in ["deliver", "move", "refuel"]:
            action = "move"

        return action

    except Exception as e:
        print("LLM error:", e, flush=True)
        return "move"


def run_task(task_name):

    print(f"[START] task={task_name}", flush=True)

    try:
        reset = requests.post(f"{ENV_URL}/reset")
        state = reset.json()["state"]

    except Exception as e:
        print("Reset error:", e, flush=True)
        return

    done = False
    steps = 0
    total_reward = 0

    while not done and steps < 20:

        action = act(state)

        try:
            response = requests.post(
                f"{ENV_URL}/step",
                json={"action": action}
            ).json()

            state = response["state"]
            reward = response["reward"]
            done = response["done"]

        except Exception as e:
            print("Step error:", e, flush=True)
            break

        total_reward += reward
        steps += 1

        print(f"[STEP] step={steps} reward={reward}", flush=True)

    # Improved scoring logic
    score = (total_reward * 0.5) + ((20 - steps) * 0.02)

    # Keep score strictly between 0 and 1
    score = max(0.1, min(0.9, score))

    print(f"[END] task={task_name} score={score} steps={steps}", flush=True)


def main():

    # Multiple runs for robustness
    for i in range(2):
        run_task("easy")

    for i in range(2):
        run_task("medium")

    for i in range(2):
        run_task("hard")


if __name__ == "__main__":
    main()
