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
You are a delivery optimization agent.

Observation:
{observation}

Choose best action:
deliver, move, refuel

Return only one word.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
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

    reset = requests.post(f"{ENV_URL}/reset")
    state = reset.json()["state"]

    done = False
    steps = 0
    total_reward = 0

    while not done and steps < 20:

        action = act(state)

        response = requests.post(
            f"{ENV_URL}/step",
            json={"action": action}
        ).json()

        state = response["state"]
        reward = response["reward"]
        done = response["done"]

        total_reward += reward
        steps += 1

        print(f"[STEP] step={steps} reward={reward}", flush=True)

    # Normalize score between 0 and 1
    score = total_reward / (steps + 1)

    if score <= 0:
        score = 0.1
    if score >= 1:
        score = 0.9

    print(f"[END] task={task_name} score={score} steps={steps}", flush=True)


def main():

    run_task("easy")
    run_task("medium")
    run_task("hard")


if __name__ == "__main__":
    main()
