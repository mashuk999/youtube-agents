import torch
import soundfile as sf
import numpy as np
from kokoro import KPipeline

# Get device
device = "cuda" if torch.cuda.is_available() else "cpu"

def convertToSpeech(text, output_path='output.wav'):
    pipeline = KPipeline(lang_code='b')
    generator = pipeline(
        text, voice='am_michael',  # <= change voice here
        speed=1, split_pattern = r'[\n.!?]+'
    )

    sample_rate = 24000
    silence_duration_sec = 0  # half a second of silence
    silence = np.zeros(int(sample_rate * silence_duration_sec), dtype=np.float32)

    final_audio = []

    for i, (gs, ps, audio) in enumerate(generator):
        print(i)  # i => index
        print(gs) # gs => graphemes/text
        print(ps) # ps => phonemes
        final_audio.append(audio)
        final_audio.append(silence)  # add silence between chunks

    # Remove last silence if desired:
    if final_audio:
        final_audio = final_audio[:-1]

    # Concatenate all audio segments
    combined_audio = np.concatenate(final_audio)

    # Save the combined audio to a single .wav file
    sf.write(output_path, combined_audio, sample_rate)
    print(f"Saved combined audio to {output_path}")



def sendForAudioGeneration(response):
    finalMsg = ''
    for line in response['frames']:
        finalMsg = finalMsg + str(line['text'])
    print(finalMsg)
    convertToSpeech(finalMsg)
    return True