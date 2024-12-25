import os
import glob

directory="/home/scott/git/live-photo-extract/immich-library/library/**"
video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.flv', '*.wmv']
video_files = []
for ext in video_extensions:
    video_files.extend(glob.glob(os.path.join(directory, ext), recursive=True))

print(f'{video_files=}')