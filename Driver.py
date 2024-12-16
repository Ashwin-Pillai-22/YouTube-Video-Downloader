from pytubefix import YouTube
import os
from pathlib import Path


def check_conflict(title, extension):
    """Check for filename conflicts and generate a unique name."""
    base_name = f"{title}.{extension}"
    new_name = base_name
    counter = 1
    while os.path.exists(os.path.join(Path.home(), 'Downloads', new_name)):
        new_name = f"{title} ({counter}).{extension}"
        counter += 1
    return new_name


def download_audio(link):
    """Download audio-only stream."""
    audio_stream = link.streams.get_audio_only()
    if audio_stream:
        file_name = check_conflict(link.title, "m4a")
        audio_stream.download(output_path=os.path.join(Path.home(), 'Downloads'), filename=file_name)
        print(f"Downloaded audio as: {file_name}")
    else:
        print("Audio stream not available.")


def download_video(link, quality):
    """Download video stream based on quality preference."""
    resolution_map = {
        1: link.streams.get_highest_resolution(),
        2: link.streams.get_lowest_resolution(),
        3: link.streams.get_by_resolution("720p"),
        4: link.streams.get_by_resolution("480p"),
        5: link.streams.get_by_resolution("360p"),
        6: link.streams.get_by_resolution("240p"),
        7: link.streams.get_by_resolution("144p")
    }
    
    stream = resolution_map.get(quality)
    if stream:
        file_name = check_conflict(link.title, "mp4")
        stream.download(output_path=os.path.join(Path.home(), 'Downloads'), filename=file_name)
        print(f"Downloaded video as: {file_name}")
    else:
        print("Selected resolution not available.")


def main():
    try:
        link = YouTube(input("Enter the YouTube link: "))
        print("\nEnter your preferences:")
        print("1. Audio only")
        print("2. Video")
        choice = int(input("Your choice: "))
        
        if choice == 1:
            download_audio(link)
        elif choice == 2:
            print("\nPreferred quality:")
            print("1. Highest quality")
            print("2. Lowest quality")
            print("3. 720p")
            print("4. 480p")
            print("5. 360p")
            print("6. 240p")
            print("7. 144p")
            quality = int(input("Your choice: "))
            download_video(link, quality)
        else:
            print("Invalid choice.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
