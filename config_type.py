"""
配置文件的类型定义
"""

from dataclasses import dataclass
from enum import Enum

import numpy as np


class TeamColor(Enum):
    """队伍颜色"""
    RED = 0
    BLUE = 1

    def as_lower(self) -> str:
        """返回小写的字符串"""
        return self.name.lower()

    @classmethod
    def from_lower(cls, name: str):
        """从小写的字符串返回枚举"""
        return cls[name.upper()]

    @property
    def enemy(self) -> "TeamColor":
        """返回敌方颜色"""
        match self:
            case TeamColor.RED:
                return TeamColor.BLUE
            case TeamColor.BLUE:
                return TeamColor.RED


class RdrReceive:
    """表示从 pyrdr 接收网络数据"""
    pass


@dataclass
class CameraConfig:
    """相机的通用设置"""
    enable: bool
    """是否启用"""
    net_process: bool | str | RdrReceive
    """是否启用网络处理，如果是字符串则直接回放预先推理的模型输出"""
    k_0: np.matrix
    """内参"""
    c_0: np.matrix
    """畸变系数"""
    rotate_vec: np.matrix
    """旋转向量"""
    transform_vec: np.matrix
    """平移向量"""
    e_0: np.matrix
    """外参"""


@dataclass
class HikCameraDriverConfigExt:
    """海康相机驱动的设置，用作 :py:class:`CameraConfig` 的扩展"""
    roi: tuple[int, int, int, int]
    """ROI 设置 (x, y, w, h)，注意偏移需要是 8 的整倍数而长宽需要是 16 的整倍数，建议在 MVS 中测试可用后再填入"""
    camera_id: str
    """序列号"""
    exposure: int
    """曝光时间"""
    gain: int
    """增益"""


@dataclass
class HikCameraConfig(CameraConfig, HikCameraDriverConfigExt):
    """海康相机的设置"""
    pass


@dataclass
class VideoConfig(CameraConfig):
    """视频假相机的设置"""
    path: str
    """视频路径"""


@dataclass
class RdrConfig(CameraConfig):
    """pyrdr传入相机"""
    endpoint: str
