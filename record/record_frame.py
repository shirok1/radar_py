import numpy as np
import cv2
from config import resource_prefix, cam_config, record_fps
import time
from record.protobuf.record_pb2 import Record, NpArray

class RecordWriteManager:
    """
    录制写入管理器
    """
    def __init__(self, cam_name):
        print("开始录制")
        basic_path = resource_prefix + 'record/' + cam_name + '-' + RecordWriteManager.gen_timestamp()
        print(basic_path)
        self._record_file = open(basic_path + '.pb', 'ab')
        self._video_file = cv2.VideoWriter(basic_path + '.avi', cv2.VideoWriter_fourcc(*'MP42'),
                                           record_fps, cam_config[cam_name]['size'])
        self.frame_count = 0

    def __del__(self):
        self._record_file.close()
        self._video_file.release()
        print("录制结束")

    def write(self, video_data, net_data):
        # print("执行写入")
        self._video_file.write(video_data)
        # cv2.imwrite(resource_prefix + 'record/' + str(self.frame_count) + '.jpg', video_data)
        record_str = Record(frame_num=self.frame_count, net_data=RecordWriteManager.serialize_ndarray(net_data))\
            .SerializeToString()
        self.frame_count += 1
        self._record_file.write(record_str)

    @staticmethod
    def gen_timestamp():
        return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())

    @staticmethod
    def serialize_ndarray(ndarr: np.ndarray) -> NpArray:
        if ndarr is None:
            return NpArray()
        else:
            return NpArray(dtype=str(ndarr.dtype), shape=ndarr.shape, data=ndarr.tobytes())

    @staticmethod
    def deserialize_ndarray(nparr: NpArray) -> np.ndarray:
        return np.frombuffer(nparr.data, dtype=np.dtype(nparr.dtype)).reshape(nparr.shape)
