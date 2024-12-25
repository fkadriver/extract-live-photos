import os
import glob
import shutil
from moviepy import VideoFileClip

def extract_halfway_image(video_path, output_image_path):
    """
    Extracts the image at the halfway point in the video.

    Args:
    - video_path (str): Path to the video file.
    - output_image_path (str): Path to save the extracted image.
    """
    try:
        # Load the video file
        clip = VideoFileClip(video_path)
        
        # Get the duration of the video
        video_duration = clip.duration

        # If the video is less than 3 seconds, extract the image at the halfway point
        if video_duration <= 3:
            # Calculate the halfway point
            halfway_time = video_duration / 2
            # copy the source to the output
            video_output = video_path.replace('immich-library','output')
            os.makedirs(os.path.dirname(video_output), exist_ok=True)
            shutil.copy(video_path, video_output)

            # Get the frame at the halfway point
            frame = clip.get_frame(halfway_time)

            # Save the frame as an image
            from PIL import Image
            img = Image.fromarray(frame)
            img.save(output_image_path)
            print(f"Image saved at {output_image_path}")
        else:
            print(f"Video '{video_path}' is not less than 3 seconds.")
    except Exception as e:
        print(f"Error processing {video_path}: {e}")

def find_and_process_videos(directory):
    """
    Finds videos in the specified directory that are less than 3 seconds and extracts images.

    Args:
    - directory (str): Path to the directory containing videos.
    """
    # Use glob to find all video files (assuming common video formats)
    video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.flv', '*.wmv']
    video_files = []
    for ext in video_extensions:
        video_files.extend(glob.glob(os.path.join(directory, ext), recursive=True))

    # Process each video file
    for video_file in video_files:
        # Define output image path
        output_image_path = video_file.replace('immich-library','output').rsplit('.', 1)[0] + "_halfway.jpg"
        extract_halfway_image(video_file, output_image_path)

# Example usage
if __name__ == "__main__":
    # Specify the directory containing the videos
    video_dir = "/home/scott/git/live-photo-extract/immich-library/library/**"
    find_and_process_videos(video_dir)
