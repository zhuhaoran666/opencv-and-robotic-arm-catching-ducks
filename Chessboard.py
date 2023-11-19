

import cv2
import numpy as np

def euclidean_distance(point1, point2):
    return np.sqrt(np.sum(np.square(point1 - point2)))

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Clicked coordinates: ({x}, {y})")

class ChessboardDetector():
    def __init__(self, square_size):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.chessboard_size = (10, 6)
        self.square_size = square_size

    def detect_chessboard(self):
        scales = []
        cv2.namedWindow('frame')
        cv2.setMouseCallback('frame', mouse_callback)
        while self.cap.isOpened():
            flag, frame = self.cap.read()

            k = cv2.waitKey(1)
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(frame_gray, self.chessboard_size, None)

            if ret:
                frame = cv2.drawChessboardCorners(frame, self.chessboard_size, corners, ret)
                
                distances = []
                for i in range(self.chessboard_size[1]):
                    for j in range(self.chessboard_size[0] - 1):
                        idx = i * self.chessboard_size[0] + j
                        distances.append(euclidean_distance(corners[idx][0], corners[idx + 1][0]))

                for i in range(self.chessboard_size[1] - 1):
                    for j in range(self.chessboard_size[0]):
                        idx = i * self.chessboard_size[0] + j
                        distances.append(euclidean_distance(corners[idx][0], corners[idx + self.chessboard_size[0]][0]))

                avg_pixel_distance = np.mean(distances)
                scale = self.square_size / avg_pixel_distance
                scales.append(scale)


            cv2.imshow('frame', frame)

            if k == ord('q'):
                print(corners)
                break
            
        # [释放资源和关闭窗口的代码保持不变]

if __name__ == "__main__":
    # square_size = 25
    # detector = ChessboardDetector(square_size)
    # detector.detect_chessboard()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    flag, frame = cap.read()
    cv2.imwrite('ducks.png',frame)