"""
通过 PNP 解算确定相机——世界位姿
created by 黄继凡 2021/1
最新修改 by 李龙 2022/5/3
"""
import cv2
import numpy as np
from loguru import logger

from config import objPoints, objNames, DEBUG, cam_config, my_viewing_position
from config_type import CameraConfig
from radar_detect.location import CameraLocation


class SolvePnp(CameraLocation):
    """PNP解算"""
    imgPoints = np.zeros((6, 2), dtype=np.float32)
    # rvec = np.zeros((3, 1), dtype=np.float64)
    # tvec = np.zeros((3, 1), dtype=np.float64)
    # 鼠标回调事件
    count = 0  # 计数，依次确定个点图像坐标

    def __init__(self, text_api):
        # 用全零向量初始化 rvec 和 tvec
        super(SolvePnp, self).__init__(
            np.zeros((3, 1), dtype=np.float64),
            np.zeros((3, 1), dtype=np.float64)
        )
        self.debug = DEBUG  # 当前是否是调试模式，影响使用的点集、标定结果文件名
        self._api = text_api  # 向主窗口输出信息的接口，参数分别为等级、（信息在主窗口里的）位置、内容
        self.sp_state = False  # 是否已经进行了所有点的标注，并至少进行了一次 PNP 解算
        self.side_text = ""  # 使用的是哪只相机，需要删除

    def load_from_config(self, cam_config: CameraConfig):
        self.rvec = cam_config.rotate_vec
        self.tvec = cam_config.transform_vec

    def add_point(self, x: int, y: int) -> None:
        """
        添加选取点
        :param x: int类型，点坐标
        :param y: int类型，点坐标
        """
        if self.count < self.count_max - 1:
            self.imgPoints[self.count, :] = np.array([float(x), float(y) + self.offset_y])
            self.count += 1
        elif self.count == self.count_max - 1:
            self.imgPoints[self.count, :] = np.array([float(x), float(y) + self.offset_y])
        self._update_info()

    def del_point(self) -> None:
        """
        删除最后一个加入的点
        """
        if 0 < self.count < self.count_max:
            self.imgPoints[self.count] = np.array([0, 0])
        self._update_info()

    def sel_cam(self, side) -> None:
        """
        根据相机类型（左/右）初始化类成员
        :param side: 0:left 1:right
        """
        if side == 0:
            side_text = f'cam_left_{my_viewing_position.enemy.as_lower()}'
        else:
            side_text = f'cam_right_{my_viewing_position.enemy.as_lower()}'
        self.side_text = side_text
        self.count_max = len(objNames[int(self.debug)][side_text])
        self.names = objNames[int(self.debug)][side_text]
        # 初始化imgPoints
        self.imgPoints = np.zeros((self.count_max, 2), dtype=np.float32)
        # 使用config中存储的objPoints
        self.objPoints = objPoints[int(self.debug)][side_text] * 1000  # 米转换成毫米

        if side == 0:
            side_text = f'cam_left'
        else:
            side_text = f'cam_right'
        self.size = cam_config[side_text]['size']
        self.distCoeffs = cam_config[side_text]['C_0']  # 相机畸变系数
        self.cameraMatrix = cam_config[side_text]['K_0']  # 相机内参矩阵
        self.offset_y = cam_config[side_text]['roi'][1]
        self.count = 0
        self._update_info()

    def save(self) -> None:
        if self.debug:
            text = "_debug"
        else:
            text = ""
        self.save_to(self.side_text + text)
        self._update_info()

    def read(self, name) -> None:
        if self.debug:
            text = "_debug"
        else:
            text = ""
        ca = self.from_checkpoint(f"{name}{text}")
        self.tvec = ca.tvec
        self.rvec = ca.rvec

    def clc(self) -> None:
        """
        清除所有选取点
        """
        self.imgPoints = np.zeros((self.count_max, 2), dtype=np.float32)
        self.count = 0
        self._update_info()

    def step(self, num) -> None:
        """
        改变self.count，增量为num
        """
        if self.count + num >= self.count_max or self.count + num < 0:
            pass
        else:
            self.count = self.count + num
        self._update_info()

    def _update_info(self):
        """
        更新UI文本
        """
        self._api("INFO", "side", f"当前相机位置：{self.side_text}")
        self._api("INFO", "sp+state", f"当前标注状态：{self.sp_state}")
        self._api("INFO", "count", f"当前点：{self.count + 1}")
        for i in range(1, self.count_max + 1):
            text = f"{self.names[i - 1]}\n" \
                   f"x : {self.imgPoints[i - 1][0]} y: {self.imgPoints[i - 1][1]}"
            if i - 1 != self.count:
                self._api("INFO", f"count{i}", text)
            else:
                self._api("ERROR", f"count{i}", text)  # 只是显示一种颜色

    # 四点标定函数
    def locate_pick(self) -> bool:
        if self.imgPoints.all():  # 粗暴的判断
            try:
                # 调用opencv库的PnP解算函数，解算相机位姿向量
                _, rvec, tvec, _ = cv2.solvePnPRansac(objectPoints=self.objPoints,
                                                      distCoeffs=self.distCoeffs,
                                                      cameraMatrix=self.cameraMatrix,
                                                      imagePoints=self.imgPoints,
                                                      iterationsCount=1000,
                                                      reprojectionError=3,
                                                      confidence=0.99,
                                                      flags=cv2.SOLVEPNP_EPNP)
                rvec: np.ndarray
                tvec: np.ndarray
            except Exception as e:
                logger.error(e)
                self.sp_state = False
                self._update_info()
                return False
            if np.isnan(rvec).any() or np.isnan(rvec).any():  # TODO: 添加一个开关
                logger.warning(f"PNP 解算结果包含 NaN, 已放弃本次解算结果, rvec: {rvec.T}, tvec: {tvec.T}")
                self.sp_state = False
                self._update_info()
                return False
            self.rvec = rvec
            self.tvec = tvec
            logger.info(f"PNP 解算成功, rvec: {rvec.T}, tvec: {tvec.T}")
            self.sp_state = True
            self._update_info()
            return True
        else:
            self.sp_state = False
            self._update_info()
            return False
