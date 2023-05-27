import time
from typing import Optional

import cv2 as cv
import numpy as np
import open3d as o3d
import zmq
from loguru import logger

import config
from proto.rdr.detected_armor_pb2 import ImageAndArmor, CarInfo
from proto.rdr.encoded_img_pb2 import EncodedImg
from proto.rdr.lidar_pb2 import LiDARRawPoints
from record.data_recorder import DataRecorder
from record.cast_helper import data_cast, DataTypeEnum


class ImageClient:
    def __init__(self, endpoint: str, context=None):
        self.context = context or zmq.Context.instance()
        self.socket: zmq.Socket = self.context.socket(zmq.constants.SocketType.SUB)
        self.socket.connect(endpoint)
        self.socket.subscribe(b'')

    def recv(self, timeout=1000) -> Optional[np.ndarray]:
        ok = self.socket.poll(timeout)
        if not ok:
            return None
        data = self.socket.recv()
        # print(data)
        # data = data[0]
        result: EncodedImg = EncodedImg.FromString(data)

        logger.debug(f'Received armor @{result.timestamp}')
        img = cv.imdecode(np.frombuffer(result.data, np.uint8), cv.IMREAD_UNCHANGED)
        return img


class ImageAndArmorClient:
    def __init__(self, endpoint: str, context=None):
        self.context = context or zmq.Context.instance()
        self.socket = self.context.socket(zmq.constants.SocketType.SUB)
        self.socket.connect(endpoint)
        self.socket.subscribe(b'')

    def recv(self) -> (np.ndarray, list[CarInfo]):
        data = self.socket.recv()
        # print(len(data))
        result: ImageAndArmor = ImageAndArmor.FromString(data)
        # print(str(result))
        logger.debug(f'Received armor @{result.timestamp}')
        # print(result.armors)
        # print(result.timestamp)
        # np.ndarray
        img = cv.imdecode(np.frombuffer(result.data, np.uint8), cv.IMREAD_UNCHANGED)
        return img, list(result.armors)


class LiDARClient:
    """
    跟某个 ZeroMQ 发布者通信，获取 LiDARRawPoints
    旧代码中全部假设输入为毫米，与 LiDARRawPoints 中假设相同
    """
    def __init__(self, endpoint: str, context=None):
        self.context = context or zmq.Context.instance()
        self.socket: zmq.Socket = self.context.socket(zmq.constants.SUB)
        self.socket.connect(endpoint)
        self.socket.subscribe(b'')

    def recv(self) -> Optional[np.ndarray]:
        ok = not self.socket.closed and self.socket.poll(1000)
        if not ok:
            return None
        data = self.socket.recv()
        result: LiDARRawPoints = LiDARRawPoints.FromString(data)
        DataRecorder.push(data_cast[DataTypeEnum.LiDARRawDump](result, config.current_lidar_name))
        # logger.debug(f'Received lidar @{result.timestamp}')
        return np.ndarray([(p.x, p.y, p.z) for p in result.points])


class LiDARPCDMock:
    """
    接口模仿 LiDARClient，但是从 pcd 读取
    此处简单假设 pcd 中的量纲为米，因此在读出时要转换为毫米
    """
    def __init__(self, path: str, step=1000, delay=0.1):
        pcd = o3d.io.read_point_cloud(path)
        self.points = np.asarray(pcd.points)
        self.step = step
        self.delay = delay
        self.current = 0

    def recv(self) -> Optional[np.ndarray]:
        start = self.current * self.step
        end = start + self.step
        if end <= self.points.shape[0]:
            self.current += 1
            time.sleep(self.delay)
            return self.points[start:end] * 1000  # 从原始的米转换为毫米
        else:
            return None
