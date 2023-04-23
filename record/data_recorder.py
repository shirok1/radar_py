"""
用 MongoDB 记录数据
"""

import datetime
import pymongo


class DataRecorder:
    """
    数据记录类, 不应直接被调用, 应该是单例
    """
    _client: pymongo.MongoClient
    _init_timestamp: datetime.datetime

    def connect(self, url: str):
        DataRecorder._client = pymongo.MongoClient(url)
        DataRecorder._init_timestamp = datetime.datetime.utcnow()
    
    def push(self, collection: str, data: dict):
        if (not hasattr(DataRecorder, "_client")):
            raise RuntimeError("DataRecorder not connected")
        DataRecorder._client["radar"][collection].insert_one({
            "init_timestamp": self._init_timestamp,
            "timestamp": datetime.datetime.utcnow(),
            **data
        })

