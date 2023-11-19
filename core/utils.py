from typing import Tuple, Union
import numpy as np
import cv2
from core.aruco_detector import ArucoDetector
import logging
from serial.tools import list_ports


def get_available_serial_port():
    return list(list_ports.comports())


def select_com() -> str:
    print("Select a COM port (Enter the number):")

    while True:
        com_ports = get_available_serial_port()
        for i, port in enumerate(com_ports):
            print(f"({i}) - {port}")

        reply = input("Enter number of your select :")
        if str.isdigit(reply) and 0 <= int(reply) <= len(com_ports) - 1:
            device = com_ports[int(reply)].device
            return device

        print("Wrong number, try again.\n")


def get_logger(name):
    logger = logging.getLogger(name)
    logger.propagate = False
    hdlr = logging.StreamHandler()
    fmt = logging.Formatter("[%(levelname)s] [%(asctime)s] %(filename)s:%(lineno)d %(message)s")
    hdlr.setFormatter(fmt)
    logger.addHandler(hdlr)
    return logger


def crop_frame(frame: np.ndarray, pt1: Tuple[int, int], pt2: Tuple[int, int]):
    x1, y1 = pt1
    x2, y2 = pt2
    if x1 > x2 and y1 > y2:
        x1, y1, x2, y2 = x2, y2, x1, y1
    frame_local = frame.copy()
    return frame_local[y1: y2, x1: x2]


def crop_poly(frame: np.ndarray, ploy_vertices: np.ndarray) -> np.ndarray:
    mask = np.zeros(frame.shape, dtype=np.uint8)
    ploy_vertices = ploy_vertices.reshape((-1, 1, 2))
    ploy_vertices = ploy_vertices.astype(np.int32)
    cv2.fillPoly(mask, [ploy_vertices], 255)
    polygon_region = cv2.bitwise_and(frame, frame, mask=mask)
    return polygon_region


def detect_anchor_aruco(frame) -> Union[Tuple[np.ndarray, np.ndarray], None]:
    aruco_detector = ArucoDetector()
    ids, corners = aruco_detector.detect_marker_corners(frame)
    if len(ids) == 0 and len(corners) == 0:
        return None

    corners = corners.astype(np.int32)
    marker_info = zip(ids, corners)
    marker_info = list(filter(lambda x: x[0] == 0, marker_info))
    if len(marker_info) != 2:
        return None
    (id1, corner1), (id2, corner2) = marker_info
    return corner1, corner2


def crop_frame_by_anchor(frame, corner0, corner1):
    pt1 = corner0[0]
    pt2 = corner1[0]
    return crop_frame(frame, pt1, pt2)


def visualize_aruco(frame):
    aruco_detector = ArucoDetector()
    ids, corners = aruco_detector.detect_marker_corners(frame)
    visu_frame = aruco_detector.visualize(frame, ids, corners)
    return visu_frame
