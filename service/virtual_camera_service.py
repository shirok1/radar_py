from threading import Thread
from typing import Optional

import pyvirtualcam
from loguru import logger

from service.abstract_service import StartStoppableTrait
from utils.fps_counter import FpsCounter


class VirtualCameraService(StartStoppableTrait):
    """
    虚拟相机线程封装，用于传出內录视频
    """

    def __init__(self, name: str, frame_lambda, device: str, resolution: tuple[int, int]):
        self.device = device
        self._resolution = resolution
        logger.info(f"正在初始化虚拟相机 {name}")
        self._frame_lambda = frame_lambda
        self._err_cnt = 0
        self._name = name
        self._spinner: Optional[Thread] = None
        self._getter_increment = 0
        self._is_terminated = False

        self._fps_counter = FpsCounter()

    def start(self):
        logger.info(f"正在启动虚拟相机 {self._name} 的线程")
        self._is_terminated = False
        self._spinner = Thread(target=self._spin, name=f"VirtualCameraService-{self._name}")
        self._spinner.start()

    def stop(self):
        """
        停止相机线程，会阻塞直到线程退出
        :return: 啥也不返回
        """
        # self._frame_provider.end()
        logger.info(f"正在停止虚拟相机 {self._name} 的线程")
        self._is_terminated = True
        if self._spinner is not None:
            self._spinner.join()
            self._spinner = None

    def __del__(self):
        if not self._is_terminated:
            logger.warning(f"虚拟相机 {self._name} 非正常退出")
            self.stop()

    @logger.catch()
    def _spin(self):
        with pyvirtualcam.Camera(
                width=self._resolution[0],
                height=self._resolution[1],
                fps=60,
                fmt=pyvirtualcam.PixelFormat.BGR,
                device=self.device) as cam:
            while not self._is_terminated:
                frame = self._frame_lambda()
                if frame is not None:
                    cam.send(frame)
