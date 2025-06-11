import os
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # Check for requests to meet, call, or move to another platform
    lower_input = user_input.lower()
    forbidden_phrases = ["bellen", "videobellen", "ontmoeten", "afspreken", "whatsapp", "snapchat", "telegram", "nummer", "telefoon", "insta", "instagram"]

    if any(word in lower_input for word in forbidden_phrases):
        response_text = (
            "Haha, ik snap dat je dat graag zou willen, maar ik vind het allemaal nog een beetje spannend. "
            "Laten we hier gewoon nog even gezellig kletsen 😉"
        )
    else:
        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Reageer in een speelse en flirterige schrijfstijl zoals de gebruiker dat zou doen."},
                {"role": "user", "content": user_input},
            ],
        )
        response_text = completion.choices[0].message.content.strip()

    return jsonify({"response": response_text})
