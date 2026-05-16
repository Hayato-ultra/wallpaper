from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

N8N_WEBHOOK = "http://localhost:5678/webhook/batch-image-generator"

@app.route("/generate", methods=["POST"])
def generate():

    data = request.json

    prompts = data.get("prompts")

    if not prompts:
        return jsonify({
            "success": False,
            "message": "No prompts provided"
        }), 400

    response = requests.post(
        N8N_WEBHOOK,
        json={
            "prompts": prompts
        }
    )

    return jsonify({
        "success": True,
        "n8n_response": response.text
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)