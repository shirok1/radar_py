import datetime

import numpy as np
import pymongo
from loguru import logger

import proto.rdr.lidar_pb2


def numpy_to_bson(data: np.ndarray):
    return {
        "shape": data.shape,
        "dtype": str(data.dtype),
        "data": data.tobytes()
    }


class TempMongoWriter:
    CONNECTION_STRING = "mongodb://localhost:27017/"

    def __init__(self):
        self._client = pymongo.MongoClient(self.CONNECTION_STRING)
        self._db = self._client["radar"]
        self._network_output_np = self._db["network_output_np"]
        self._network_output_typed = self._db["network_output_typed"]
        self._lidar_raw_dump = self._db["lidar_raw_dump"]
        self._position_update = self._db["position_update"]
        self._init_timestamp = datetime.datetime.utcnow()
        logger.info(f"TempMongoWriter init at {self._init_timestamp}: {self._client.server_info()}")

    def push_network_output_np(self, data: np.ndarray):
        self._network_output_np.insert_one({
            "init_timestamp": self._init_timestamp,
            "timestamp": datetime.datetime.utcnow(),
            **numpy_to_bson(data)
        })

    def push_network_output_typed(self, data: np.ndarray):
        self._network_output_typed.insert_one({
            "init_timestamp": self._init_timestamp,
            "timestamp": datetime.datetime.utcnow(),
            "bboxes": [{
                "lt": (bbox[0], bbox[1]),
                "rb": (bbox[2], bbox[3]),
                "conf": bbox[4], "type": int(bbox[5])
            } for bbox in data]
        })

    def push_lidar_raw_dump(self, data: proto.rdr.lidar_pb2.LiDARRawPoints, device: str):
        self._lidar_raw_dump.insert_one({
            "init_timestamp": self._init_timestamp,
            "rdr_timestamp": data.timestamp.ToDatetime(tzinfo=None),
            "device": device,
            "timestamp": datetime.datetime.utcnow(),
            "points": [(point.x, point.y, point.z) for point in data.points]
            # "points": data.points
        })

    def push_position_update(self, armors: dict):
        self._position_update.insert_one({
            "init_timestamp": self._init_timestamp,
            "timestamp": datetime.datetime.utcnow(),
            "armors": armors
        })


INSTANCE = TempMongoWriter()
