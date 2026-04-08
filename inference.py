import os
from openai import OpenAI
import requests

API_BASE_URL = os.environ.get("API_BASE_URL")
API_KEY = os.environ.get("API_KEY")

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

ENV_URL = os.environ.get("ENV_URL", "http://localhost:7860")

def act(observation):

    prompt = f"""
You are a delivery optimization agent.

Observation:
{observation}

Choose one action:
deliver, move, refuel

Return only one word.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        action = response.choices[0].message.content.strip().lower()

        if action not in ["deliver", "move", "refuel"]:
            action = "move"

        return action

    except Exception as e:
        print("LLM error:", e, flush=True)
        return "move"


def main():

    print("[START] task=delivery", flush=True)

    reset = requests.post(f"{ENV_URL}/reset")
    state = reset.json()["state"]

    done = False
    step_count = 0
    total_reward = 0

    while not done and step_count < 20:

        action = act(state)

        response = requests.post(
            f"{ENV_URL}/step",
            json={"action": action}
        ).json()

        state = response["state"]
        reward = response["reward"]
        done = response["done"]

        total_reward += reward
        step_count += 1

        print(f"[STEP] step={step_count} reward={reward}", flush=True)

    print(f"[END] score={total_reward} steps={step_count}", flush=True)


if __name__ == "__main__":
    main()
