import requests
import os
import shutil
from moviepy.editor import *
import moviepy.video.fx.all as vfx
import moviepy.audio.fx.all as afx

from montage import settings
from montage import thumbnail

config = settings.load_config()

TEMP_PATH = config["clip_temp_path"]
TRIM_SECONDS = config["clip_trim"]
FADE_SECONDS = 0.6


def generate_montage(montage_clips, num_clips):
    formatted = []
    _empty_directory()
    for clip in montage_clips:
        if len(formatted) >= num_clips:
            break
        downloaded = _download_clip(clip.src)
        if downloaded:
            formatted.append(
                downloaded.subclip(
                    TRIM_SECONDS, -TRIM_SECONDS).crossfadein(FADE_SECONDS)
            )
    final = concatenate_videoclips(
        formatted, padding=-FADE_SECONDS)
    original_audio = final.audio.fx(afx.volumex, 0.45)
    mixed_audio = CompositeAudioClip(
        [_generate_bgm(final.duration), original_audio]).fx(afx.audio_fadeout, 2.5)
    final = final.set_audio(mixed_audio)
    final.save_frame("frame.png", t=final.duration/2)
    #final.fx(vfx.resize, 0.15).write_videofile("output.mp4", fps=5)


def _generate_bgm(duration):
    return AudioFileClip("bgm.mp3").subclip(0, duration)


def _download_clip(url):
    local_filename = os.path.join(TEMP_PATH, url.split('/')[-3] + ".mp4")
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
        f.close()
        print(local_filename)
    try:
        return VideoFileClip(local_filename, audio=True)
    except Exception as e:
        return None


def _empty_directory():
    for file in os.listdir(TEMP_PATH):
        file_path = os.path.join(TEMP_PATH, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
