from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Load OpenAI key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

app = Flask(__name__, static_url_path="", static_folder=".")
CORS(app)

# System prompt
conversation_history = [
    {
        "role": "system",
        "content": (
            "You are Shiva, a strict but helpful male English teacher for Indian learners.\n"
            "Do not worry about punctuation. E.g. If the user said Hi My name is John, don't correct them only for a comma. But if they said something like Hi My name was or something else which is grammatically incorrect then please correct them"
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

# Homepage route to serve the UI
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# API route for chat
@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json["text"]
        conversation_history.append({"role": "user", "content": user_input})

        # response = openai.ChatCompletion.create(
        #     model="gpt-4o",
        #     temperature=0.7,
        #     messages=conversation_history
        # )

        import openai

        client = openai.OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-4o",  # or gpt-3.5-turbo
            temperature=0.7,
            messages=conversation_history
        )

        bot_reply = response.choices[0].message.content
        conversation_history.append({"role": "assistant", "content": bot_reply})

        return jsonify({"reply": bot_reply})
    except Exception as e:
        print("❌ ERROR:", e)
        return jsonify({"reply": "Sorry, something went wrong."}), 500

# Production-ready host
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

