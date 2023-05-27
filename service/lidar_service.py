"""
激光雷达服务
lidar_service.py
使用 rdr 接收点云数据
created by 陈希峻 2023/4/9
"""

import time
from threading import Thread
from typing import Optional

import cv2 as cv
import numpy as np
from loguru import logger

from abstraction.provider import GenericProvider
from config import neo_camera_config
from config_type import RdrLiDARConfig
from pyrdr.client import LiDARClient, LiDARPCDMock
from service.abstract_service import StartStoppableTrait
from utils.fps_counter import FpsCounter


class RdrLiDARService(StartStoppableTrait):
    """
    使用 rdr_service 接收激光雷达点云数据的服务
    """

    @logger.catch()
    def __init__(self, config: RdrLiDARConfig, pcd: Optional[str] = None):
        logger.info("正在初始化 RdrLiDARService")
        self._client: Optional[LiDARClient] = None
        self._spinner: Optional[Thread] = None
        self._config = config
        self._lidar_provider: GenericProvider[np.ndarray] = GenericProvider()
        self._getter_increment = 0
        self._is_terminated = False
        self._fps_counter = FpsCounter()

        self._depth_image = np.full(config.resolution, np.nan, dtype=float)
        self._cam_config = neo_camera_config[config.camera_name]
        self._pcd = pcd

    def start(self):
        if self._pcd:
            self._client = LiDARPCDMock(self._pcd)
            logger.warning(
                f"正在读取 {self._pcd} 中的点云而不是连接到 Livox SDK 2 转发服务，请确认现在不是在比赛中")
        else:
            self._client = LiDARClient(self._config.endpoint)
            logger.info(f"正在启动连接到 {self._config.endpoint} 的线程")
        self._is_terminated = False
        self._spinner = Thread(target=self._spin, name=f"RdrThread-{self._config.endpoint}")
        self._spinner.daemon = True
        self._spinner.start()

    def stop(self):
        logger.info(f"正在停止连接到 {self._config.endpoint} 的线程")
        self._is_terminated = True
        self._spinner.join()
        # self._client.close()

    @logger.catch()
    def _spin(self):
        count = 0
        while not self._is_terminated:
            self._fps_counter.update()
            # logger.info(f"正在等待 {self._config.endpoint} 的消息")
            msg: list[tuple[int, int, int]] = self._client.recv()
            if msg is None:
                logger.warning(f"等待 {self._config.endpoint} 的消息超时")
                time.sleep(0.1)  # 防止主线程退出之后刷屏
            else:
                # msg 中的点以毫米为单位
                np_msg = np.array(msg, dtype=np.float32)
                if np_msg.shape[0] == 0:
                    logger.warning("出现空消息")
                    continue
                # 添加一列 1 以便于后续的矩阵运算
                np_msg = np.column_stack((np_msg, np.ones(np_msg.shape[0], dtype=np.float32)))
                # 乘以转换矩阵
                np_msg = (self._config.e_0 @ np_msg.T).T[:, :3]
                np.column_stack((np_msg, np.ones(np_msg.shape[0], dtype=np.float32)))
                # 此时已转换到相机坐标系下，再进行投影转换（不需要再传入相机-世界标定）
                point_in_image, _ = cv.projectPoints(
                    np_msg[:, :3].T,
                    np.zeros(3), np.zeros(3),
                    self._cam_config.k_0, self._cam_config.c_0)
                stacked_points = np.column_stack((point_in_image[:, 0], np_msg[:, 2]))  # (n, 3)
                stacked_points = np.array(stacked_points)
                is_inside = (stacked_points.T[0] > 0) & (stacked_points.T[0] < self._config.resolution[1]) & (
                        stacked_points.T[1] > 0) & (stacked_points.T[1] < self._config.resolution[0]) & (
                                    stacked_points.T[2] > 0)  # (n,)
                xs, ys = np.floor(stacked_points[is_inside][:, 0:2].T).astype(np.int32)
                self._depth_image[ys, xs] = stacked_points[is_inside][:, 2].T
                count += 1
                if count % 100 == 0:
                    count = 0
                    # 存一张参考用的深度图
                    dimg = cv.normalize(np.nan_to_num(self._depth_image), None, 255, 0, cv.NORM_MINMAX, cv.CV_8UC1)
                    # dimg = cv.cvtColor(dimg, cv.COLOR_GRAY2BGR)
                    # dimg = cv.dilate(dimg, None, iterations=3)
                    cv.imwrite("depth.bmp", dimg)
                #     cv.imshow("image", image)
                #     cv.pollKey()
                # logger.info(f"收到了 {self._config.endpoint} 的消息并推送了出去")

    def __del__(self):
        if not self._is_terminated:
            logger.warning(f"连接到 {self._config.endpoint} 的线程未被正常停止！")
            self.stop()

    def average_depth_of_roi(self, roi: tuple[int, int, int, int]):
        """
        计算 ROI 的平均深度
        :param roi: ROI，格式为 (x, y, w, h)
        :return: ROI 的平均深度，米
        """
        x, y, w, h = roi
        x = int(np.floor(x))
        y = int(np.floor(y))
        w = int(np.floor(w))
        h = int(np.floor(h))
        return np.nanmean(self._depth_image[y:y + h, x:x + w]) / 100  # TODO：改成除 1k

    def detect_depth(self, rects: list[tuple[float, float, float, float]]):
        """
        试图重现 DepthQueue::detect_depth
        :param rects: [(x0,y0,w,h)]
        :return:
        """
        # logger.info(f"rects: {rects}")
        stack = np.stack([self.average_depth_of_roi(rect) for rect in rects])
        # logger.info(f"stack: {stack}")
        return stack

    def read(self):
        # return cv.cvtColor((self._depth_image % 256).astype(np.uint8), cv.COLOR_GRAY2BGR)
        return self._depth_image

    # def world_location_of_roi(self, roi: tuple[int, int, int, int]):
    #     """
    #     计算 ROI 的世界坐标
    #     :param roi: ROI，格式为 (x, y, w, h)
    #     :return: ROI 按某种方式平均后的世界坐标
    #     """
    #     x, y, w, h = roi
    #     x_c = x + w // 2
    #     y_c = y + h // 2
    #     depth = self.average_depth_of_roi(roi)
    #     return np.mean(self._depth_image[y:y + h, x:x + w])


if __name__ == '__main__':
    rls = RdrLiDARService(RdrLiDARConfig(
        resolution=(2048, 3072),
        camera_name="cam_left",
        e_0=np.mat([
            [0.00462803, -0.999749, 0.0219115, 0.154876 * 1000],
            [0.0931124, -0.0213857, -0.995426, -0.0506296 * 1000],
            [0.995645, 0.0066471, 0.0929901, -0.137197 * 1000],
            [0, 0, 0, 1]
        ]),
        endpoint="tcp://127.0.0.1:8200",
    ))
    rls.start()
    cv.namedWindow("read", 16)
    cv.namedWindow("points", 16)
    bg = cv.imread("/home/shiroki/0.bmp")
    for i in range(100):
        read = rls.read()
        img = cv.normalize(np.nan_to_num(read), None, 255, 0, cv.NORM_MINMAX, cv.CV_8UC1)
        img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
        img = cv.dilate(img, None, iterations=3)
        mask = (img == img[0, 0])[:, :, 0]
        cv.imshow("points", img)
        img[mask, :] = bg[mask, :]
        cv.imshow("read", img)
        cv.waitKey(100)

    rls.stop()
