import cv2

DEFAULT_FPS = 30


class Video:
    def __init__(self, path, custom_fps=DEFAULT_FPS, cust_size: tuple[int] = None, isduplicate=False):
        self.path = path
        if cust_size:
            self.frame_width, self.frame_height = cust_size[0], cust_size[1]
        self.fps = custom_fps
        if not isduplicate:
            cap = cv2.VideoCapture(path)
            if not cust_size:
                self.frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                self.frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.frames = self.crop_frames_init(cap)

    def crop_frames_init(self, cap):
        # box is (x, y, w, h)
        frame_list = []
        x, y, w, h = 0, 0, self.frame_width, self.frame_height
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            cropped_frame = frame[y:y + h, x:x + w]
            frame_list.append(cropped_frame)
        cap.release()

        return frame_list

    def duplicate(self):
        new_video = Video(self.path, self.fps, (self.frame_width, self.frame_height))
        new_video.frames = self.frames

    def crop_frames(self, box):
        # box is (x, y, w, h)
        frame_list = []
        x, y, w, h = box
        for frame in self.frames:
            cropped_frame = frame[y:y + h, x:x + w]
            frame_list.append(cropped_frame)


        return frame_list




    def save_video(self, frames, output_path, fps=0):
        if fps == 0:
            fps = self.fps
        height, width, _ = self.frame_height, self.frame_width
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        for frame in frames:
            # out.write(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            out.write(frame)





    def display_video(self):
        for frame in self.frames:
            # Display the frame
            cv2.imshow('Video (press q to quit)', frame)

            # Wait for the specified time based on the desired FPS
            delay = int(1000 / (self.fps + 4))  # Calculate the delay in milliseconds
            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()


if __name__ == "__main__":
    video_path = '../resources/fence_seq_1.mp4'
    vid = Video(video_path)
    print(DEFAULT_FPS)
    print(vid.frame_width, vid.frame_height)
    print("Frame Rate:", vid.fps)
    vid.display_video()
