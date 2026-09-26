import cv2
import math
import cvzone
from ultralytics import YOLO

# ==============================
# SETTINGS
# ==============================

video_path = "Media/helmet.mp4"
model_path = "Weights/best (1).pt"

classNames = ["With Helmet", "Without Helmet"]

# ==============================
# LOAD VIDEO
# ==============================

cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# ==============================
# LOAD YOLO MODEL
# ==============================

model = YOLO(model_path)

# ==============================
# PROCESS VIDEO
# ==============================

while True:

    # Read frame
    success, img = cap.read()

    # Stop when video finishes
    if not success:
        print("Video finished.")
        break

    # YOLO prediction
    results = model(img, stream=True)

    # Process detections
    for r in results:

        boxes = r.boxes

        for box in boxes:

            # Bounding box coordinates
            x1, y1, x2, y2 = box.xyxy[0]

            x1 = int(x1)
            y1 = int(y1)
            x2 = int(x2)
            y2 = int(y2)

            # Width and height
            w = x2 - x1
            h = y2 - y1

            # Confidence
            conf = float(box.conf[0])

            # Class
            cls = int(box.cls[0])

            # Make sure class exists
            if cls < len(classNames):

                # Draw bounding box
                cvzone.cornerRect(
                    img,
                    (x1, y1, w, h)
                )

                # Display confidence
                confidence = math.ceil(conf * 100) / 100

                # Display class + confidence
                cvzone.putTextRect(
                    img,
                    f"{classNames[cls]} {confidence}",
                    (max(0, x1), max(35, y1)),
                    scale=1,
                    thickness=1
                )

    # ==============================
    # SHOW VIDEO
    # ==============================

    cv2.imshow("Helmet Detection", img)

    # ==============================
    # CHECK KEYBOARD
    # ==============================

    key = cv2.waitKey(1) & 0xFF

    # Press Q to quit
    if key == ord("q"):
        print("Stopped by user.")
        break

    # ==============================
    # CHECK IF WINDOW WAS CLOSED
    # ==============================

    try:
        window_status = cv2.getWindowProperty(
            "Helmet Detection",
            cv2.WND_PROP_VISIBLE
        )

        if window_status < 1:
            print("Window closed.")
            break

    except cv2.error:
        break


# ==============================
# CLEANUP
# ==============================

cap.release()

cv2.destroyAllWindows()

print("Program closed.")



















































































# import cv2
# import math
# import cvzone
# from ultralytics import YOLO

# # Initialize video capture
# video_path = "Media/vid.mp4"
# cap = cv2.VideoCapture(video_path)

# # Load YOLO model with custom weights
# model = YOLO("Weights/best (1).pt")

# # Define class names
# classNames = ['With Helmet', 'Without Helmet']

# # For the use of Webcam
# # Open the webcam (use 0 for the default camera, or 1, 2, etc. for additional cameras)
# # cap = cv2.VideoCapture(0)

# while True:
#     success, img = cap.read()
#     results = model(img, stream=True)
#     for r in results:
#         boxes = r.boxes
#         for box in boxes:
#             x1, y1, x2, y2 = box.xyxy[0]
#             x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

#             w, h = x2 - x1, y2 - y1
#             cvzone.cornerRect(img, (x1, y1, w, h))
#             conf = math.ceil((box.conf[0] * 100)) / 100
#             cls = int(box.cls[0])

#             cvzone.putTextRect(img, f'{classNames[cls]} {conf}', (max(0, x1), max(35, y1)), scale=1, thickness=1)

#     cv2.imshow("Image", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break