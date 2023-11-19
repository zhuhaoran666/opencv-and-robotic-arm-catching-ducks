from typing import Tuple


class CoordCalc:
    def __init__(
            self, target_base_pos3d, plane_center_pos2d, plane_frame_size_ratio
    ) -> None:
        # cobot坐标系下，抓取中心点的世界坐标
        self.target_base_pos3d = target_base_pos3d

        # 屏幕坐标的中心点
        self.plane_center_pos2d = plane_center_pos2d

        # 抓取平面在真实世界的大小和屏幕像素大小的比值
        self.ratio = plane_frame_size_ratio

    def frame2real(self, x, y) -> Tuple[int, int, int]:
        real_x, real_y, real_z = self.target_base_pos3d
        plane_center_x, plane_center_y = self.plane_center_pos2d
        real_x = (y - plane_center_y) * self.ratio + real_x
        real_y = (x - plane_center_x) * self.ratio + real_y
        return real_x, real_y, real_z
