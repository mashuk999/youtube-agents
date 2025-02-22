import torch
# from TTS.api import TTS
from kokoro import KPipeline
import soundfile as sf
import torch

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"


# Init TTS
# tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

def convertToSpeech(text):
    # # Run TTS
    # # ❗ Since this model is multi-lingual voice cloning model, we must set the target speaker_wav and language
    # # Text to speech list of amplitude values as output
    # wav = tts.tts(text=text, speaker_wav="/workspaces/youtube-agents/videoplayback.mp3", language="en")
    # # Text to speech to a file
    # tts.tts_to_file(text=text, speaker_wav="/workspaces/youtube-agents/videoplayback.mp3", language="en", file_path="/workspaces/youtube-agents/output.wav")
    pipeline = KPipeline(lang_code='b')
    generator = pipeline(
        text, voice='am_michael', # <= change voice here
        speed=1, split_pattern=r'\n+'
    )
    for i, (gs, ps, audio) in enumerate(generator):
        print(i)  # i => index
        print(gs) # gs => graphemes/text
        print(ps) # ps => phonemes
        sf.write(f'{i}-audio.wav', audio, 24000) # save each audio file