from flask import Flask
from env import DeliveryEnv
import random

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>🚀 AI Smart Delivery Optimization</h1>
    <p>Status: Running Successfully</p>
    <hr>
    <a href="/run">
    <button style="padding:10px;font-size:16px;">
    ▶ Run Simulation
    </button>
    </a>
    <hr>
    <p>🤖 Powered by Varshini AI</p>
    """

@app.route("/run")
def run():

    env = DeliveryEnv()
    state = env.reset()

    done = False
    steps = 0

    while not done and steps < 10:
        action = random.choice(["deliver","move","refuel"])
        state, reward, done = env.step(action)
        steps += 1

    score = state["score"]

    return f"""
    <h1>🚚 AI Smart Delivery Optimization</h1>
    <h2>📊 Simulation Result</h2>
    <p>✅ Delivery Completed Successfully</p>
    <p>🏆 Final Score: {score}</p>
    <hr>
    <a href="/">
    <button style="padding:10px;font-size:16px;">
    ⬅ Back to Home
    </button>
    </a>
    <hr>
    <p>🤖 Powered by Varshini AI</p>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
