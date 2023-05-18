"""
用于将数据转化为给 MongoDB 储存的字典
"""

from enum import Enum

import numpy as np

import proto.rdr.lidar_pb2


class DataTypeEnum(Enum):
    """
    数据类型到数据库名的枚举
    """
    NetworkOutputNp = "network_output_np"
    NetworkOutputTyped = "network_output_typed"
    LiDARRawDump = "lidar_raw_dump"
    PositionUpdate = "position_update"


def numpy_to_bson(data: np.ndarray):
    return {
        "shape": data.shape,
        "dtype": str(data.dtype),
        "data": data.tobytes()
    }


def _cast_network_output_np(data: np.ndarray):
    return numpy_to_bson(data)


def _cast_network_output_typed(data: np.ndarray):
    return {
        "bboxes": [{
            "lt": (bbox[0], bbox[1]),
            "rb": (bbox[2], bbox[3]),
            "conf": bbox[4], "type": int(bbox[5])
        } for bbox in data]
    }


def _cast_lidar_raw_dump(data: proto.rdr.lidar_pb2.LiDARRawPoints, device: str):
    return {
        "rdr_timestamp": data.timestamp.ToDatetime(tzinfo=None),
        "device": device,
        "points": [(point.x, point.y, point.z) for point in data.points]
    }


def _cast_position_update(data: dict):
    return {
        "armors": data
    }


data_cast = {
    DataTypeEnum.NetworkOutputNp: lambda data: (DataTypeEnum.NetworkOutputNp, _cast_network_output_np(data)),
    DataTypeEnum.NetworkOutputTyped: lambda data: (DataTypeEnum.NetworkOutputTyped, _cast_network_output_typed(data)),
    DataTypeEnum.LiDARRawDump: lambda data, device: (DataTypeEnum.LiDARRawDump, _cast_lidar_raw_dump(data, device)),
    DataTypeEnum.PositionUpdate: lambda data: (DataTypeEnum.PositionUpdate, _cast_position_update(data))
}
