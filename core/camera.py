import cv2
from typing import Union
import numpy as np


class OrbbecCamera:
    def __init__(self, camera_index=0):
        self.orbbec_cap: cv2.VideoCapture = cv2.VideoCapture(camera_index, cv2.CAP_OBSENSOR)
        self.orbbec_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.orbbec_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)

        if not self.orbbec_cap.isOpened():
            raise Exception(f"Open obbrec camera at index {camera_index} failed")

        self.__curr_bgr_frame: Union[np.ndarray, None] = None
        self.__curr_depth_frame: Union[np.ndarray, None] = None

    def release(self) -> bool:
        self.orbbec_cap.release()
        return True

    def update_frame(self) -> bool:
        cap = self.orbbec_cap
        if cap.grab():
            ret_bgr, bgr_frame = cap.retrieve(None, cv2.CAP_OBSENSOR_BGR_IMAGE)
            ret_depth, depth_frame = cap.retrieve(None, cv2.CAP_OBSENSOR_DEPTH_MAP)

            if ret_bgr and ret_depth:
                self.__curr_bgr_frame = bgr_frame
                self.__curr_depth_frame = depth_frame
                return True
            else:
                self.__curr_bgr_frame = None
                self.__curr_depth_frame = None
                return False
        return False

    def get_bgr_frame(self) -> Union[np.ndarray, None]:
        return self.__curr_bgr_frame

    def get_depth_frame(self) -> Union[np.ndarray, None]:
        return self.__curr_depth_frame


if __name__ == "__main__":
    import time

    cam = OrbbecCamera(0)

    while True:
        if cam.update_frame():
            bgr_frame = cam.get_bgr_frame()
            depth_frame = cam.get_depth_frame()
            cv2.imshow("BGR Frame", bgr_frame)
            cv2.imshow("Depth Frame", depth_frame)

        if cv2.waitKey(1) == ord("q"):
            break

        time.sleep(0.01)
