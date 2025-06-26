import assemblyai as aai
aai.settings.api_key = "aa6858980b8a4fda9103de2e70acc2cd"
transcriber = aai.Transcriber()
transcript = transcriber.transcribe("output.wav")
print(transcript.text)