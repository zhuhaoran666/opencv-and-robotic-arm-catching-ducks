import cv2
cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
if cap.isOpened():
    flag, frame = cap.read()
    if not flag:
        print("false")
    else:
        cv2.imwrite("photo.jpg",frame)
        print("true")