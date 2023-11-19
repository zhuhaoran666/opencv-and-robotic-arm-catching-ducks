import cv2
import dlib
import numpy as np


class face_emtion():
    def __init__(self):
        # 加载dlib 人脸检测器
        self.detector = dlib.get_frontal_face_detector()
        # 加载dlib 人脸关键点
        self.predictor = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')

        # 获取摄像头对象
        self.cap = cv2.VideoCapture(0)
        # 设置摄像头参数
        self.cap.set(3,480)
        # 截图creenshoot的计数器
        self.cnt = 0

    def learning_face(self):

        while(self.cap.isOpened()):
            # 读取摄像头帧
            flag, frame = self.cap.read()
            k = cv2.waitKey(1)
            # 转换为灰度图
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 检测人脸
            faces = self.detector(frame_gray, 0)
            # 如果检测到人脸了
            if len(faces) != 0:
                for i in range(len(faces)):
                    for face_count, face in enumerate(faces):
                        print(face.left(),face.top(),face.right(),face.bottom())
                        # 用矩形框出人脸
                        frame_face = cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), (0,255,0), 2)

                        # 获取脸宽，并打印出来
                        self.face_width = face.right() - face.left()
                        print("FACE_Width: %d \n" %(self.face_width))

                        # 帧数比CV的人脸分类器要高一些
                        # cv2.imshow('frame', frame)

                        # 检测出68个人脸关键点
                        # 检测每一张人脸的关键点
                        face_points = self.predictor(frame_gray, face)

                        # 标出所有的68个点位
                        for point in face_points.parts():
                            pos = (point.x, point.y)
                            frame_points = cv2.circle(frame, pos, 2, (0,255,0), 2)

                        # 计算嘴巴张开的程度
                        # 利用嘴的关键点计算嘴张开的大小与人脸宽度进行比较得到张开的程度
                        mouth_width = (face_points.part(54).x - face_points.part(48).x) / self.face_width
                        mouth_higth = (face_points.part(66).y - face_points.part(62).y) / self.face_width
                        print("MOUTH_Width: %f, MOUTH_Hight: %f\n" %(mouth_width, mouth_higth))

                        # 通过眉毛的关键点计算挑眉和皱眉的程度
                        brow_sum = 0
                        frown_sum = 0
                        line_brow_x = []
                        line_brow_y = []
                        for j in range(17,21):
                            # 挑眉
                            brow_sum += (face_points.part(j).y - face.top()) + (face_points.part(j + 5).y - face.top())
                            # 皱眉
                            frown_sum += face_points.part(j + 5).x - face_points.part(j).x
                            line_brow_x.append(face_points.part(j).x)
                            line_brow_y.append(face_points.part(j).y)

                        # 算出眉宽和眉高占比
                        brow_width = (brow_sum / 10) / self.face_width
                        brow_hight = (frown_sum / 5) / self.face_width
                        print("BROW_Width: %f, BROW_Hight: %f" %(brow_width, brow_hight))

                        tempx = np.array(line_brow_x)
                        tempy = np.array(line_brow_y)
                        z1 = np.polyfit(tempx, tempy ,1)
                        self.brow_k = -round(z1[0], 3)
                        print("BROW_K: %f\n" %(self.brow_k))

                        # 获取眼睛的距离
                        eye_sum = (face_points.part(41).y - face_points.part(37).y + face_points.part(40).y - face_points.part(38).y
                                + face_points.part(47).y - face_points.part(43).y + face_points.part(46).y - face_points.part(44).y)
                        # 眼睛的占比
                        eye_hight = (eye_sum / 4) / self.face_width
                        print("EYE_Hight: %f\n" %(eye_hight))

                        # 接下来判断表情
                        # 根据眼睛，嘴巴，眉毛来判断
                        if round(mouth_higth >= 0.03):
                            if eye_hight >= 0.046:
                                cv2.putText(frame, "amazing", (0,30), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0,0,255), 2, bottomLeftOrigin= False)
                            else:
                                cv2.putText(frame, "happy", (0,30), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0,0,255), 2, bottomLeftOrigin= False)
                        else:
                            if self.brow_k <= 0.295:
                                cv2.putText(frame, "angry", (0,30), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0,0,255), 2, bottomLeftOrigin= False)
                            else:
                                cv2.putText(frame, "nature", (0,30), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0,0,255), 2, bottomLeftOrigin= False)


                        cv2.imshow('frame',frame)

            if k == ord('q'):
                break
        # 释放摄像头
        self.cap.release()

        # 删除建立的窗口
        cv2.destroyAllWindows()


if __name__ == "__main__":
    my_face = face_emtion()
    my_face.learning_face()
