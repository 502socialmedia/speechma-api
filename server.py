from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import asyncio
import edge_tts
import os
import uuid
import json

app = Flask(__name__)
CORS(app)

# Load voices from voices.json
with open('voices.json') as f:
    voices_data = json.load(f)
    voices_list = voices_data['voices']
    voices_dict = {v['name']: v for v in voices_list}

@app.route('/api/voices', methods=['GET'])
def get_voices():
    return jsonify(voices_data)

@app.route('/api/synthesize', methods=['POST'])
def synthesize():
    data = request.json
    text = data.get('text', '').strip()
    voice_name = data.get('voice', 'ar-EG-ShakirNeural')

    if not text:
        return jsonify({'error': 'Text is required'}), 400

    if voice_name not in voices_dict:
        return jsonify({'error': 'Invalid voice'}), 400

    # Generate unique filename
    filename = f"temp/{uuid.uuid4()}.mp3"

    # Split long text into sentences if needed (edge-tts handles long text, but split for safety)
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    if len(sentences) > 10:  # If more than 10 sentences, process in chunks
        chunks = []
        current_chunk = ""
        for sentence in sentences:
            if len(current_chunk + sentence) > 5000:  # Approximate char limit
                chunks.append(current_chunk)
                current_chunk = sentence + "."
            else:
                current_chunk += sentence + "."
        if current_chunk:
            chunks.append(current_chunk)
    else:
        chunks = [text]

    # Generate audio
    try:
        asyncio.run(generate_audio(chunks, voice_name, filename))
        return send_file(filename, as_attachment=True, download_name='speech.mp3', mimetype='audio/mpeg')
    except Exception as e:
        return jsonify({'error': str(e)}), 500

async def generate_audio(chunks, voice, output_file):
    if len(chunks) == 1:
        communicate = edge_tts.Communicate(chunks[0], voice)
        await communicate.save(output_file)
    else:
        # Combine multiple chunks
        combined = AudioSegment.empty()
        for chunk in chunks:
            temp_file = f"temp/temp_{uuid.uuid4()}.mp3"
            communicate = edge_tts.Communicate(chunk, voice)
            await communicate.save(temp_file)
            audio = AudioSegment.from_mp3(temp_file)
            combined += audio
            os.remove(temp_file)
        combined.export(output_file, format="mp3")

if __name__ == '__main__':
    app.run(debug=True)