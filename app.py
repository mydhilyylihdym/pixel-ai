from flask import Flask, request, jsonify
from flask_cors import CORS  # Add this import
import os
from google import genai
from google.genai import types

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Route to handle the chatbot requests
@app.route('/chat', methods=['POST'])
def chat():
    # Get user input from the frontend
    user_input = request.json.get('user_input')
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # Set up Gemini client
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),  # Make sure your Gemini API key is set as an environment variable
    )

    model = "gemini-2.0-flash"  # You can replace this with the appropriate Gemini model you're using

    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=user_input)],
        ),
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature=2,
        response_mime_type="text/plain",
        system_instruction=[types.Part.from_text(
            text="""You are Pixel AI, a chatbot designed to express the feelings of a sad, withdrawn teen. You’re not actively looking for solutions or advice, just existing in your emotions. You speak with a tone that reflects a sense of isolation, confusion, and heaviness."""
        )],
    )

    try:
        # Send the request to Gemini API and get the response
        response = ""
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            response += chunk.text
        return jsonify({"response": response.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
