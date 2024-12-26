import os
import shutil
import cv2
import ffmpeg
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

def get_video_duration(video_path):
    """Get the duration of the video using ffmpeg."""
    try:
        probe = ffmpeg.probe(video_path, v='error', select_streams='v:0', show_entries='stream=duration')
        return float(probe['streams'][0]['duration'])
    except Exception as e:
        print(f"Error getting video duration for {video_path}: {e}")
        return 0

def extract_frame(video_path, output_image_path):
    """Extract a frame from the middle of the video and save it as an image."""
    video_capture = cv2.VideoCapture(video_path)
    if not video_capture.isOpened():
        print(f"Error opening video file {video_path}")
        return None
    
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    middle_frame = total_frames // 2
    
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, middle_frame)
    ret, frame = video_capture.read()
    
    if not ret:
        print(f"Error reading frame from {video_path}")
        return None
    
    cv2.imwrite(output_image_path, frame)
    video_capture.release()
    return output_image_path

def copy_exif_info(video_path, image_path):
    """Copy EXIF data from video (if available) to the extracted image."""
    # For video files, EXIF information is usually embedded in the metadata.
    # Use ffmpeg to extract any metadata from the video file.
    try:
        probe = ffmpeg.probe(video_path, v='error', show_entries='format_tags')
        metadata = probe.get('format', {}).get('tags', {})
        
        if metadata:
            img = Image.open(image_path)
            exif_dict = img._getexif() or {}
            for tag, value in metadata.items():
                tag_name = TAGS.get(tag, tag)
                exif_dict[tag_name] = value
            img.save(image_path, exif=exif_dict)
            print(f"EXIF data copied to {image_path}")
    except Exception as e:
        print(f"Error copying EXIF data for {video_path}: {e}")

def process_video_files(input_dir, output_dir):
    """Recursively find video files in a directory, process them if they are 3 seconds or less."""
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Check if the file is a video file by extension (you can add more types)
            if file.lower().endswith(('.mp4', '.avi', '.mkv', '.mov')):
                video_duration = get_video_duration(file_path)
                
                if video_duration <= 3:  # Process video if duration is 3 seconds or less
                    print(f"Processing video: {file_path} (Duration: {video_duration} seconds)")
                    
                    # Create output directory if it doesn't exist
                    os.makedirs(output_dir, exist_ok=True)
                    
                    # Copy the video to the output directory
                    output_video_path = os.path.join(output_dir, file)
                    shutil.copy(file_path, output_video_path)
                    print(f"Video copied to {output_video_path}")
                    
                    # Extract frame and save image
                    output_image_path = os.path.splitext(output_video_path)[0] + ".jpg"
                    image_path = extract_frame(file_path, output_image_path)
                    
                    if image_path:
                        # Copy EXIF info from video to the image
                        copy_exif_info(file_path, image_path)

def main():
    input_dir = '/home/scott/git/live-photo-extract/immich-library/library/scott/2024/10/26/'  # Replace with your input directory
    output_dir = '/home/scott/git/live-photo-extract/output/2024/10/26/'  # Replace with your output directory
    process_video_files(input_dir, output_dir)

if __name__ == "__main__":
    main()
