import requests
import os
import shutil
from moviepy.editor import VideoFileClip, concatenate_videoclips

config = {
  "clip_temp_path": "./temp",
  "clip_trim": 1
}

TEMP_PATH = config["clip_temp_path"]
TRIM_SECONDS = config["clip_trim"]
FADE_SECONDS = 0.6

def generate_montage(montage_clips):
  formatted = []
  _empty_directory()
  for clip in montage_clips:
    downloaded = _download_clip(clip.src)
    if downloaded:
      formatted.append(
        downloaded.subclip(TRIM_SECONDS, -TRIM_SECONDS).crossfadein(FADE_SECONDS)
      )
  final = concatenate_videoclips(formatted, padding=-FADE_SECONDS, method="compose")
  final.write_videofile("output.mp4")
  
def _download_clip(url):
  local_filename = os.path.join(TEMP_PATH, url.split('/')[-3] + ".mp4")
  r = requests.get(url, stream=True)
  print(r)
  with open(local_filename, 'wb') as f:
    for chunk in r.iter_content(chunk_size=1024): 
      if chunk:
        f.write(chunk)
  try:
    return VideoFileClip(local_filename)
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