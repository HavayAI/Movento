import cv2
import os

DEFAULT_FPS = 30

def play_video_frames(frames, frame_rate=DEFAULT_FPS):
    for frame in frames:
        cv2.imshow('Image', frame)
        if cv2.waitKey(int(1000 / frame_rate)) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

def save_video(frames, output_path, fps=DEFAULT_FPS):
    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for frame in frames:
        # out.write(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        out.write(frame)

def crop_frames(cap, box):
    # box is (x, y, w, h)
    frame_list = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Crop the frame using the bounding box coordinates
        x, y, w, h = box
        cropped_frame = frame[y:y + h, x:x + w]

        # Append the cropped frame to the list
        frame_list.append(cropped_frame)

    # Release the video capture
    cap.release()

    return frame_list


if __name__ == "__main__":
    video_path = '../resources/fence_seq_1.mp4'
    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(frame_width, frame_height)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print("Frame Rate:", fps)
    frames = crop_frames(cap, (0, 0, frame_width, frame_height))
    save_video(frames, "../resources/blablabla.mp4")
    cap.release()






