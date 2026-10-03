import cv2 as cv
from MediaSearch_project.scanners import image as image_engine
import math
from rich import print

def scan(path: str,
               ocr: str,
               seconds: int,):
    
    cap = cv.VideoCapture(path)
    total_frames = cap.get(cv.CAP_PROP_FRAME_COUNT)
    frame_count = 0

    fps = cap.get(cv.CAP_PROP_FPS)
    time = math.floor(fps * seconds)   # Converts seconds to frames

    frames_scanned = []

    # Cannot open video
    if not cap.isOpened():
        print(f'Unable to open video path: {path}.')
        return ''
    
    # Iterate frames

    while frame_count <= total_frames:
        # Skip Frames
        frame_count += 1

        if frame_count % time != 0 and frame_count != 0:
            continue
        else:
            cap.set(cv.CAP_PROP_POS_FRAMES, frame_count)

        ret, frame = cap.read()
        print(f'[[blue]-[/blue]] [yellow]{path}[/yellow] [blue]Frame {frame_count} out of {int(total_frames)}[/blue]')

        # Frame reading Error
        if not ret and frame_count != total_frames:
            error_input = ''

            while error_input not in ['y','yes','n','no']:
                error_input = input('There was an error while trying to read a frame. Continue? (Y/N)')

                if error_input.lower() in ['y','yes']:
                    continue
                elif error_input.lower() in ['n','no']:
                    return ''
                else:
                    print('Please enter a valid input.')

        frames_scanned.append((frame_count, image_engine.scan(frame, ocr)))


    return frames_scanned