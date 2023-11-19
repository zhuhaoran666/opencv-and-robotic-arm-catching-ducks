import time
from pymycobot import MyCobot
import platform
from core.config import *
from core.utils import get_logger

__logger = get_logger(__name__)

# For raspberry pi
if platform.system() == "Linux":
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)


def init_arm(arm: MyCobot):
    arm.send_angles(arm_idle_angle, 50)
    __logger.info("Move arm to idle position.")
    time.sleep(3)
    arm.set_fresh_mode(0)
    time.sleep(0.5)
    arm.set_tool_reference(tool_frame)
    time.sleep(0.5)
    arm.set_end_type(1)
    time.sleep(0.5)
    pump_off(arm)
    time.sleep(3)


def grab(arm: MyCobot, x, y, z):
    # hover to avoid collision
    arm.send_angles(arm_pick_hover_angle, 50)
    __logger.info(f"Step 1 : Move to hover angle; angle : {arm_pick_hover_angle}")
    time.sleep(3)

    coord = [x, y, z]

    # make arm perpendicular to the plane
    coord.extend(perpendicular_angle)

    # move x-y first, set z fixed
    target_xy_pos3d = coord.copy()[:3]
    target_xy_pos3d[2] = 80

    __logger.info(f"Step 2 : Move on top of target; coords : {target_xy_pos3d}")
    position_move(arm, *target_xy_pos3d)
    time.sleep(5)

    # send target angle
    __logger.info(f"Step 3 : Send full coords; coords : {coord}")
    arm.send_coords(coord, 50)
    time.sleep(5)

    pump_on(arm)
    __logger.info(f"Step 4 : Open pump")
    time.sleep(1)

    # elevate first
    arm.send_coord(3, 100, 50)
    __logger.info(f"Step 5 : Elevate first.")
    time.sleep(3)

    arm.send_angles(arm_drop_angle, 50)
    __logger.info(f"Step 6 : Move to drop point.")
    time.sleep(3)

    pump_off(arm)
    __logger.info(f"Step 7 : Close pump.")
    time.sleep(1)

    arm.send_angles(arm_idle_angle, 50)
    __logger.info(f"Step 8 : Return to idle position.")
    time.sleep(3)


def pump_on(arm: MyCobot):
    if platform.system() == "Windows":
        arm.set_basic_output(5, 0)
        time.sleep(0.05)
    elif platform.system() == "Linux":
        GPIO.output(20, 0)
        time.sleep(1)


def pump_off(arm: MyCobot):
    if platform.system() == "Windows":
        arm.set_basic_output(5, 1)
        time.sleep(0.05)
        # 泄气阀门开始工作
        arm.set_basic_output(2, 0)
        time.sleep(1)
        arm.set_basic_output(2, 1)
        time.sleep(0.05)
    elif platform.system() == "Linux":
        GPIO.output(20, 1)
        time.sleep(0.05)
        GPIO.output(21, 0)
        time.sleep(1)
        GPIO.output(21, 1)
        time.sleep(0.05)


def position_move(arm: MyCobot, x, y, z):
    curr_rotation = arm.get_coords()[-3:]
    curr_rotation[0] = 175
    curr_rotation[1] = 0
    target_coord = [x, y, z]
    target_coord.extend(curr_rotation)
    arm.send_coords(target_coord, 50)
