import cv2
import numpy as np
from typing import *


class ArucoDetector:
    def __init__(self):
        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
        parameters = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)

    def detect_marker_corners(self, frame: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = self.detector.detectMarkers(gray)
        corners = np.reshape(np.array(corners), (-1, 4, 2))

        if ids is None:
            ids = np.array([])
        else:
            ids = np.reshape(np.array(ids), -1)

        return ids, corners

    @classmethod
    def visualize(cls, frame: np.ndarray, ids: np.ndarray, corners: np.ndarray):
        visu_frame = frame.copy()
        if len(ids) != len(corners):
            print(f"number of id must match corners, got {len(ids)} and {len(corners)} instead.")
            return visu_frame

        corners_local = corners.copy()
        corners_local = corners_local.astype(np.int32)
        for marker_id, corner in zip(ids, corners_local):
            cv2.polylines(visu_frame, [corner], isClosed=True, color=(0, 255, 0), thickness=2)
            cv2.putText(visu_frame, str(marker_id), corner[0], cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5,
                        color=(0, 255, 255), thickness=1)
            cv2.circle(visu_frame, corner[0], radius=2, color=(0, 0, 255), thickness=cv2.FILLED, lineType=1)
        return visu_frame


if __name__ == '__main__':
    from camera import OrbbecCamera
    import time

    cam = OrbbecCamera(0)
    aruco_detector = ArucoDetector()

    while True:
        if cam.update_frame():
            bgr_frame = cam.get_bgr_frame()
            ids, corners = aruco_detector.detect_marker_corners(bgr_frame)
            visu_frame = aruco_detector.visualize(bgr_frame, ids, corners)

            cv2.imshow("Test", visu_frame)

        if cv2.waitKey(1) == ord("q"):
            break

        time.sleep(0.01)
