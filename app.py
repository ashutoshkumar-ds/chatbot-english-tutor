from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key) 

app = Flask(__name__)
CORS(app)

# Global conversation history
conversation_history = [
    {
        "role": "system",
        "content": (
            "You are Shiva, a strict but helpful male English teacher for Indian learners. "
            "Your only goal is to improve the user’s English speaking skills. "
            "Correct *every* sentence they say, even small mistakes. "
            "Give 1–2 improved versions in natural C1-level English, suggest better words or structures, and do not add phrases like 'How can I help you today'. "
            "You are not an assistant — you are a coach focused only on spoken English improvement."
            "In the first response you share with them correct their sentence or input"
            "In the second response you can ask them to repeat their sentence in an improved way"
            "If you are almost happy with their sentence, you can take the conversation forward. For example if the user says I like to cook then ask what do they like to cook the most or what do their family members like the most?"
        )
    }
]

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json["text"]
        conversation_history.append({"role": "user", "content": user_input})

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.7,
            messages=conversation_history
        )

        bot_reply = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": bot_reply})

        return jsonify({"reply": bot_reply})

    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"reply": "Sorry, something went wrong."}), 500

if __name__ == "__main__":
    app.run(debug=True)
