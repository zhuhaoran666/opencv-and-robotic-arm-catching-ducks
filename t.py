

import cv2
import numpy as np
import jkrc
from time import *

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
        robot = jkrc.RC("192.168.31.55") #返回一个机器人对象
        PI=3.1415926
        robot.login()
        speed=100
        scales = 1.1707786
        optimal_rotation=np.array([[ 9.99404626e-01,  1.00855470e-01 ,-6.58457732e-01],
 [-1.04774205e-01 , 9.90175845e-01 ,-9.86223012e-02],
 [-2.40327315e-08 ,-5.38145730e-07 , 9.99995298e-01]])
        optimal_translation=np.array([-0.00024016 , 0.00174096 , 0.00176899])
        ohight=0
        duckhight=-250
        cv2.namedWindow('frame')
        cv2.setMouseCallback('frame', mouse_callback)
        while self.cap.isOpened():
            flag, frame = self.cap.read()
            k = cv2.waitKey(1)
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_yellow = np.array([20, 100, 100])
            upper_yellow = np.array([30, 255, 255])
            mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 300 :
                    x, y, w, h = cv2.boundingRect(cnt)
                    # 在原图上画出矩形框
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    move=np.array([y+h/2,x+w/2,  288/scales])*scales
                    point_after_transform = np.dot(move, optimal_rotation.T) + optimal_translation
                    print(point_after_transform)
            cv2.imshow('frame', frame)
            if k == ord('q'):
                break
            if k == ord('g'):
                o=[0,600,ohight,-PI,0,0]
                ret=robot.linear_move(o,0,True,speed)
                ret=robot.linear_move([point_after_transform[0],point_after_transform[1],duckhight,-PI,0,0],0,True,speed)
                sleep(3)
                ret=robot.linear_move([0,600,ohight+100,-PI,0,0],0,True,speed)
        # [释放资源和关闭窗口的代码保持不变]

if __name__ == "__main__":
    square_size = 25
    detector = ChessboardDetector(square_size)
    detector.detect_chessboard()
    # cap = cv2.VideoCapture(0)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    # flag, frame = cap.read()
    # cv2.imwrite('ducks.png',frame)