"""
用 MongoDB 记录数据
"""

import datetime
from typing import Tuple
import pymongo


class DataRecorder:
    """
    数据记录类, 不应直接被调用, 应该是单例
    """
    _client: pymongo.MongoClient
    _init_timestamp: datetime.datetime

    def connect(url: str):
        DataRecorder._client = pymongo.MongoClient(url)
        DataRecorder._init_timestamp = datetime.datetime.utcnow()
    
    def push(x: Tuple[str, dict]):
        if (not hasattr(DataRecorder, "_client")):
            raise RuntimeError("DataRecorder not connected")
        collection, data = x
        DataRecorder._client["radar"][collection].insert_one({
            "init_timestamp": DataRecorder._init_timestamp,
            "timestamp": datetime.datetime.utcnow(),
            **data
        })

