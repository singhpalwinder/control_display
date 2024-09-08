#!/usr/bin/python3
import time
import numpy as np
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput
from time import sleep
import os 

MOTION_THRESHOLD=4
CHECK_INTERVAL=3

def detect_motion(picam2, prev_frame, lsize):
    w, h = lsize
    cur_frame = picam2.capture_buffer("lores")
    cur_frame = cur_frame[:w * h].reshape(h, w)

    if prev_frame is not None:
        # Measure pixel differences between current and previous frame
        mse = np.square(np.subtract(cur_frame, prev_frame)).mean()
        print(f"MSE: {mse}")  # Debugging: print the motion metric
        if mse > MOTION_THRESHOLD:
            return True, cur_frame  # Return True and update previous frame
        else:
            return False, cur_frame  # No motion, but still update previous frame

    return False, cur_frame  # If no previous frame, return False and store current frame
def control_display(motion_detected):
    if motion_detected:
            print("Motion Detected:", motion_detected)
            print("Display ON")
            os.system('wlr-randr --output DSI-1 --on')
    else:
            print("Motion Detected:", motion_detected)
            print("Display OFF")
            os.system('wlr-randr --output DSI-1 --off')
def main():
    lsize = (320, 240)
    picam2 = Picamera2()
    video_config = picam2.create_video_configuration(main={"size": (1280, 720), "format": "RGB888"},
                                                    lores={"size": lsize, "format": "YUV420"})
    picam2.configure(video_config)
    picam2.start()
    prev_frame = None

    while True:
        motion, prev_frame = detect_motion(picam2, prev_frame, lsize)
        control_display(motion)
        sleep(CHECK_INTERVAL)
if __name__ == "__main__":
     main()
    