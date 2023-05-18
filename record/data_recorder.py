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

    @classmethod
    def connect(cls, url: str):
        cls._client = pymongo.MongoClient(url)
        cls._init_timestamp = datetime.datetime.utcnow()

    @classmethod
    def push(cls, x: Tuple[str, dict]):
        if not hasattr(cls, "_client"):
            raise RuntimeError("DataRecorder not connected")
        collection_enum, data = x
        collection = str(collection_enum)
        cls._client["radar"][collection].insert_one({
            "init_timestamp": cls._init_timestamp,
            "timestamp": datetime.datetime.utcnow(),
            **data
        })
