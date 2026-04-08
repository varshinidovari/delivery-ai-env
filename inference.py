import os
from openai import OpenAI

API_BASE_URL = os.environ["API_BASE_URL"]
API_KEY = os.environ["API_KEY"]

client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

def act(observation):
    prompt = f"""
You are a delivery optimization agent.

Observation:
{observation}

Choose best action from:
- deliver
- move
- refuel

Return only one action.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    action = response.choices[0].message.content.strip()

    return action
