from moviepy.editor import *
import whisper
import os
import random

def create_outlined_text(text, fontsize=100, font="/workspaces/youtube-agents/Impact.ttf", color="white", outline_color="black"):
    """Creates text with a simulated outline effect."""

    # Create the black outline text clip
    outline_clip = TextClip(text, fontsize=fontsize + 4,  # Slightly larger
                            font=font, color=outline_color,
                            method="caption", size=(1000, None), align="center")

    # Create the white fill text clip
    fill_clip = TextClip(text, fontsize=fontsize, font=font,
                            color=color, method="caption",
                            size=(1000, None), align="center")

    # Composite the clips (fill over outline)
    text_clip = CompositeVideoClip([outline_clip, fill_clip.set_position("center")])
    return text_clip

def create_captioned_video_with_background(audio_file, output_video, video_folder, model_size="base"):
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
        final_clip = final_clip.set_audio(audio_clip)

        final_clip.write_videofile(output_video, fps=5)

        print(f"Video with captions and background saved to {output_video}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    audio_file_path = "/workspaces/youtube-agents/output.wav"
    output_video_path = "/workspaces/youtube-agents/output_video.mp4"
    video_folder_path = "/workspaces/youtube-agents/background_videos" #Path to video folder

    if not os.path.exists(audio_file_path):
        print(f"Error: Audio file not found at {audio_file_path}")
    elif not os.path.exists(video_folder_path) or not os.path.isdir(video_folder_path):
        print(f"Error: Video folder not found at {video_folder_path}")
    else:
        create_captioned_video_with_background(audio_file_path, output_video_path, video_folder_path)