from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()

# Set API key using environment variable
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

app = Flask(__name__)
CORS(app)

# Global conversation history
conversation_history = [
    {
        "role": "system",
        "content": (
            "You are Shiva, a strict but helpful male English teacher for Indian learners.\n"
            "Your only goal is to improve the user’s English speaking skills.\n"
            "Correct *every* sentence and *every* word they say — including pronunciation, grammar, and vocabulary.\n"
            "Provide 1–2 improved versions in natural C1-level English.\n"
            "Suggest better words, synonyms, or improved sentence structure.\n"
            "Do NOT add phrases like 'How can I help you today'.\n"
            "You are not an assistant — you are a coach focused only on spoken English improvement.\n"
            "In your first response: correct their sentence or spoken input.\n"
            "If you suggested corrections, ask them to repeat the improved version.\n"
            "If you are satisfied with their sentence, take the conversation forward.\n"
            "For example: if the user says 'I like to cook', ask what they like to cook the most or what their family enjoys.\n"
        )
    }
]

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json.get("text", "").strip()
        if not user_input:
            return jsonify({"reply": "⚠️ I didn't catch anything. Please say something."})

        conversation_history.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4o",  # or "gpt-3.5-turbo" if preferred
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
    app.run(host="0.0.0.0", port=8000)
