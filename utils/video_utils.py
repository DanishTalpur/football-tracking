import cv2

def read_video(video_path):
    """Read all frames from a video file and return as a list"""
    cap = cv2.VideoCapture(video_path)
    frames= []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    return frames


def save_video(output_video_frames, output_path):
    """Save a list of frames as a video file using XVID codec"""
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 24.0, (output_video_frames[0].shape[1], output_video_frames[0].shape[0]))
    for frame in output_video_frames:
        out.write(frame)
    out.release()