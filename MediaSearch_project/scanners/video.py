import cv2 as cv
from MediaSearch_project.scanners import image as image_engine
import math

def scan(path: str,
               ocr: str,
               sr: str,
               sr_model: str,
               seconds: int,
               confidence_val: int = 90,
               search: list | None = None):
    
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
        if frame_count % time != 0 and frame_count != 0:
            frame_count += 1
            continue
        elif frame_count == 0:
            frame_count += 1
        else:
            cap.set(cv.CAP_PROP_POS_FRAMES, frame_count)

        ret, frame = cap.read()

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

        frames_scanned.append((time, image_engine.scan(ocr, frame)))
    
    return frames_scanned