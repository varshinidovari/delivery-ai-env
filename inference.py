import os
from openai import OpenAI

API_BASE_URL = os.environ.get("API_BASE_URL")
API_KEY = os.environ.get("API_KEY")

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
deliver, move, or refuel

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
        print("LLM error:", e)
        return "move"
