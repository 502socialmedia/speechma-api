from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from pydub import AudioSegment
import os

app = Flask(__name__)
CORS(app)

# Load voices from voices.json
import json
with open('voices.json') as f:
    voices = json.load(f)

@app.route('/voices', methods=['GET'])
def get_voices():
    return jsonify(voices)

@app.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.json
    text = data.get('text')
    voice = data.get('voice', 'default')
    # Placeholder for synthesis logic
    # For example, use requests to call an API
    # response = requests.post('https://api.example.com/synthesize', json={'text': text, 'voice': voice})
    # audio = response.content
    # Save to temp
    # filename = f'temp/{voice}_{hash(text)}.mp3'
    # with open(filename, 'wb') as f:
    #     f.write(audio)
    # return jsonify({'audio_url': filename})
    return jsonify({'message': 'Synthesis not implemented yet'})

if __name__ == '__main__':
    app.run(debug=True)