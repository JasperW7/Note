from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pydub import AudioSegment
import assemblyai as aai
import os
import traceback

aai.settings.api_key = "aa6858980b8a4fda9103de2e70acc2cd"

app = Flask(__name__)
CORS(app)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/transcribe/", methods=["POST"])
def transcribe():
    try:
        file = request.files["audio"]
        raw_path = "temp.webm"
        wav_path = "output.wav"

        file.save(raw_path)

        audio = AudioSegment.from_file(raw_path, format="webm")
        audio.export(wav_path, format="wav")

        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(wav_path)

        os.remove(raw_path)
        os.remove(wav_path)

        return jsonify({"text": transcript.text})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
