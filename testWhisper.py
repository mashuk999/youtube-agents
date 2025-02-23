import whisper

model = whisper.load_model("turbo")
result = model.transcribe("/workspaces/youtube-agents/0-audio.wav")
print(result)