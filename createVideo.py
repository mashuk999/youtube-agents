from moviepy.editor import *
import whisper
import os
import random
from PIL import ImageFont
from moviepy.editor import TextClip, CompositeVideoClip
from PIL import ImageFont
import globalConfigs

def split_text_to_fit(text, font_path, fontsize, max_width):
    """Splits text so the first line fits max_width. Returns (first_line, rest)."""
    font = ImageFont.truetype(font_path, fontsize)
    words = text.split()
    line = ""
    for i, word in enumerate(words):
        test_line = line + (" " if line else "") + word
        w, _ = font.getsize(test_line)
        if w > max_width:
            break
        line = test_line
    rest = " ".join(words[i:])
    return line, rest

def create_outlined_text(text, fontsize=100, font= str(globalConfigs.BASE_DIRECTORY) + "/Impact.ttf",
                         color="white", outline_color="black", video_width=1080,
                         use_outline=False):

    # Split text into first line (yellow) and rest (white)
    first_line, remaining_text = split_text_to_fit(text, font, fontsize, video_width - 40)

    def outlined_clip(txt, txt_color):
        if use_outline:
            outline = TextClip(txt, fontsize=fontsize + 4, font=font,
                               color=outline_color, method="caption",
                               size=(video_width, None), align="center")
            fill = TextClip(txt, fontsize=fontsize, font=font,
                            color=txt_color, method="caption",
                            size=(video_width, None), align="center")
            return CompositeVideoClip([outline, fill.set_position("center")])
        else:
            return TextClip(txt, fontsize=fontsize, font=font,
                            color=txt_color, method="caption",
                            size=(video_width, None), align="center")

    clips = []
    if first_line:
        clips.append(outlined_clip(first_line, "yellow"))
    if remaining_text:
        clips.append(outlined_clip(remaining_text, "white").set_position(("center", clips[0].size[1])))

    # Combine vertically
    total_height = sum([clip.size[1] for clip in clips])
    final = CompositeVideoClip(clips, size=(video_width, total_height))
    return final

def create_captioned_video_with_background(audio_file, output_video, video_folder, bgm_folder, model_size="base"):
    try:
        model = whisper.load_model(model_size)
        result = model.transcribe(audio_file)
        segments = result["segments"]

        audio_clip = AudioFileClip(audio_file)
        duration = audio_clip.duration

        # Load background video clips
        video_files = [os.path.join(video_folder, f) for f in os.listdir(video_folder) if f.lower().endswith(('.mp4', '.avi', '.mov'))]
        if not video_files:
            raise ValueError(f"No video files found in {video_folder}")
        background_clips = [VideoFileClip(f).resize((1080, 1920)) for f in video_files]

        # Create background video loop
        background_duration = 0
        looped_background_clips = []
        while background_duration < duration:
            clip = random.choice(background_clips)
            looped_background_clips.append(clip)
            background_duration += clip.duration

        background_clip = concatenate_videoclips(looped_background_clips, method="compose").subclip(0, duration)

        # Apply black tint to background
        black_tint = ColorClip(size=(1080, 1920), color=(0, 0, 0), duration=duration, ismask=False).set_opacity(0.6)
        background_clip = CompositeVideoClip([background_clip, black_tint])

        text_clips = []
        for segment in segments:
            start = segment["start"]
            end = segment["end"]
            text = segment["text"]

            text_clip = create_outlined_text(text)  # Use the new function
            text_clip = text_clip.set_position("center").set_start(start).set_end(end)
            text_clips.append(text_clip)

        final_clip = CompositeVideoClip([background_clip] + text_clips)


        bgm_files = [os.path.join(bgm_folder, f) for f in os.listdir(bgm_folder) if f.lower().endswith(('.mp3', '.wav'))]

        if not video_files:
            raise ValueError(f"No bgm files found in {bgm_folder}")

        bgm_music = random.choice(bgm_files)

        background_music = AudioFileClip(bgm_music).volumex(0.09)
        background_music = background_music.subclip(7, duration+7)
        final_audio = CompositeAudioClip([audio_clip, background_music])

        final_clip = final_clip.set_audio(final_audio)

        final_clip.write_videofile(output_video, fps=5)

        print(f"Video with captions and background saved to {output_video}")

    except Exception as e:
        print(f"An error occurred: {e}")

def createVideo():
    audio_file_path =  str(globalConfigs.BASE_DIRECTORY) + "/output.wav"
    output_video_path =  str(globalConfigs.BASE_DIRECTORY) + "/output_video.mp4"
    video_folder_path =  str(globalConfigs.BASE_DIRECTORY) + "/background_videos" #Path to video folder
    background_music_path =  str(globalConfigs.BASE_DIRECTORY) + "/background_music/motivation"

    if not os.path.exists(audio_file_path):
        print(f"Error: Audio file not found at {audio_file_path}")
    elif not os.path.exists(video_folder_path) or not os.path.isdir(video_folder_path):
        print(f"Error: Video folder not found at {video_folder_path}")
    else:
        create_captioned_video_with_background(audio_file_path, output_video_path, video_folder_path, background_music_path)   

if __name__ == "__main__":
    createVideo()