import cv2
import os
import time
import subprocess

def convert_to_ascii(frame):
    height, width, _ = frame.shape
    aspect_ratio = width / height
    new_width = 120
    new_height = int(new_width / aspect_ratio * 0.55)
    resized_frame = cv2.resize(frame, (new_width, new_height))
    return resized_frame

def frame_to_ascii(frame, threshold=127):
    chars = '@%#*+=-:. '
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ascii_frame = ''
    for row in gray_frame:
        for pixel in row:
            ascii_frame += chars[min(int(pixel / threshold * len(chars)), len(chars) - 1)]
        ascii_frame += '\n'
    return ascii_frame

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def play_video_with_audio(video_path, target_fps):
    print("Starting play_video_with_audio")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    print("Video file opened successfully")
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Video FPS: {video_fps}")

    delay = 1 / target_fps
    frame_count = 0
    while cap.isOpened():
        start_time = time.time()
        ret, frame = cap.read()
        if not ret:
            print("End of video or error reading frame")
            break

        print(f"Processing frame {frame_count}")
        print("Original frame shape:", frame.shape)
        
        frame = convert_to_ascii(frame)
        print("Converted frame shape:", frame.shape)
        ascii_frame = frame_to_ascii(frame)
        print("ASCII frame generated")
        
        #ASCII frame
        clear_screen()
        print(ascii_frame, end='', flush=True)

        #ffmpeg
        if frame_count == 0:
            subprocess.Popen(['ffplay', '-nodisp', '-autoexit', video_path])

        #next frame
        elapsed_time = time.time() - start_time
        if elapsed_time < delay:
            time.sleep(delay - elapsed_time)

        frame_count += 1

    print("Releasing video capture")
    cap.release()
    print("Exiting play_video_with_audio")

if __name__ == "__main__":
    video_path = "video.mp4"#ここに動画のパスを入力
    target_fps = 30#ここにFPSを入力
    
    play_video_with_audio(video_path, target_fps)