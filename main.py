from ultralytics import YOLO
import cv2
import os
import numpy as np
from trackers import Tracker

def main():
    # Input and output video paths
    video_path = '08fd33_4.mp4'
    output_path = 'output video/output_3.avi'

    # Load the trained YOLO model for player detection
    model = YOLO('training\\runs\\detect\\train\\weights\\best.pt')

    # Open input video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Cannot open video!")
        return

    # Get video properties for output
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Create output directory if it doesn't exist
    os.makedirs("output video", exist_ok=True)

    # Initialize video writer with XVID codec
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Initialize tracker and start processing
    tracker = Tracker(model, video_path, output_path)
    tracker.track(cap, out)

    

if __name__ == "__main__":
    main()
