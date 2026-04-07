from flask import Flask, jsonify, request
from env import DeliveryEnv

app = Flask(__name__)

env = DeliveryEnv()

@app.route("/")
def home():
    return "AI Delivery Optimization Running"

@app.route("/reset", methods=["POST"])
def reset():
    state = env.reset()
    return jsonify(state)

@app.route("/step", methods=["POST"])
def step():
    action = request.json.get("action")
    state, reward, done = env.step(action)

    return jsonify({
        "state": state,
        "reward": reward,
        "done": done
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
