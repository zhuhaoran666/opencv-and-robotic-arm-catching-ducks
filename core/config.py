arm_serial_port = "COM5"

arm_idle_angle = [0, 0, 0, -90, 0, 0]
arm_pick_hover_angle = [21, 0, -85, -11, 0, 22]
arm_drop_angle = [100, 15, -90, 0, 0, 25]

# 垂直姿态角
perpendicular_angle = [180, 0, -90]

# 用于计算的捕获帧大小
frame_size = 512

# 用于计算的屏幕坐标中心点
plane_center_pos2d = (frame_size // 2, frame_size // 2)

# 目标平面的实际大小
target_plan_real_world_size = 150

# 平面像素大小与实际大小（毫米）的比例
plane_frame_size_ratio = target_plan_real_world_size / frame_size

# Calc的坐标平面中心参数
target_base_pos3d = (175, 0, -10)

# 最终坐标偏移量
final_coord_offset = [-20, -20, -5]

# camera distance to floor
floor_depth = 373

# 工具坐标系
tool_frame = [0, 0, 80, 0, 0, 0]

# 相机刷新率
FPS = 30

# 刷新率帧间隔时间
frame_interval = 1 / FPS
