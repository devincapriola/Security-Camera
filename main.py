# Security Camera with Face Detection
# Importing the Libraries
import cv2
import time
import datetime

# Creating a VideoCapture object and reading from input file
video_capture = cv2.VideoCapture(0)

# Loading the cascades
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Parameters
detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 2
frame_size = (int(video_capture.get(3)), int(video_capture.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")


# Creating a face detector
def detect(gray, frame):
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    return frame


print("Press q to quit")
while True:
    _, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    canvas = detect(gray, frame)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    cv2.imshow('Video', canvas)

    if len(faces) > 0:
        if detection:
            timer_started = False
        else:
            detection = True
            # d = day, m = month, Y = year, H = hour, M = minute, S = second
            current_time = datetime.datetime.now().strftime("%H-%M")
            out = cv2.VideoWriter(
                f"{current_time}.mp4", fourcc, 24.0, frame_size)
    elif detection:
        if timer_started:
            if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                detection = False
                timer_started = False
                out.release()
        else:
            timer_started = True
            detection_stopped_time = time.time()

    if detection:
        out.write(frame)

    if cv2.waitKey(1) == ord('q'):  # Press q to quit
        break

out.release()
video_capture.release()
cv2.destroyAllWindows()
