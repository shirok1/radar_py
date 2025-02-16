"""
配置类
config.py
从外部文件读取配置
created by 李龙 2021/12
最终修改 by 李龙 2021/1/15
"""
import os
import numpy as np
from real_points import real_points
from config_type import HikCameraConfig, VideoConfig, CameraConfig, RdrConfig

mongo_url = "mongodb://localhost:27017/"

enemy_color = 1  # 0：对方是红色（我们是蓝色）；1：对方是蓝色（我们是红色）
# 需要设计来应对集成这种红蓝雷达在同一边的场地
my_color = TeamColor.RED
my_viewing_position = TeamColor.RED  # 雷达站在谁的雷达基座上，在集成产业园的测试场地上需要设置为 TeamColor.RED，比赛时设置为 my_color 即可

# 下面是复制用的样板
# match my_color:
#     case TeamColor.RED:
#         # 我是红方
#         pass
#     case TeamColor.BLUE:
#         # 我是蓝方
#         pass


serial_usable = False  # 串口可用状态
# lidar_usable = True  # 激光雷达可用状态
# locate_mode = 0  # 定位模式 0：激光雷达（深度图）, 1: 德劳内, 2: kd_tree, 3: 禁用

USEABLE = {
    "serial": False,
    "Lidar": False,
    "locate_state": [1, 1],
}
BO = 0  # 未知串口相关配置，需要清理

# use_mock_lidar = False  # str 路径表示从 pcd 读存下来的点云，False 表示从驱动读
use_mock_lidar = "/home/shiroki/code/Livox2Rdr/小组赛1.pcd"

DEBUG = False
resource_prefix = os.path.dirname(os.path.abspath(__file__)) + "/resources/"
cam_config = {
    "cam_left": {
        "name": "cam_left",
        "enable": True,
        "id": "J87631625",
        "size": (3072, 2048),
        "roi": (0, 0, 3072, 2048),
        "using_video": True,
        "using_net": True,
        "using_net_record": False,
        "video_path": resource_prefix + "two_cam/1.avi",
        "K_0": np.mat([[2599.59101996968, 0.0, 1528.51343714847],
                       [0.0, 2599.32628783837, 1005.63370496221],
                       [0.0, 0.0, 1.0]]),
        "C_0": np.mat([[-0.0827470703754226], [0.173839479717410], [-0.000408515186013770],
                       [0.000440205348940563], [-0.0805391333761662]]),
        "exposure": 15000,
        "gain": 21,
        "rvec": np.mat([[1.69750257], [0.69091169], [-0.54474128]]),
        "tvec": np.mat([[-11381.85466339], [-479.01247871], [9449.30328641]]),
        "E_0": np.mat([
            [0.0265686, -0.999625, -0.00665175, -0.131281 * 1000],
            [0.0841975, 0.0088682, -0.99641, 0.106948 * 1000],
            [0.996095, 0.0259131, 0.0844015, -0.213647 * 1000],
            [0, 0, 0, 1]
        ])},

    "cam_right": {
        "name": "cam_right",
        "enable": False,
        "id": "J37877236",
        "size": (3072, 2048),
        "roi": (0, 0, 3072, 1648),
        "using_video": True,
        "using_net": False,
        "using_net_record": False,
        "video_path": resource_prefix + "two_cam/1.avi",
        "K_0": np.mat([[2505.2629026927225, 0.0, 1529.4286325395244],
                       [0.0, 2505.5722700649067, 1026.1378217662113],
                       [0.0, 0.0, 1.0]]),
        "C_0": np.mat([-0.06856710471358254, 0.1269396451339073,
                       -0.0003599605406165552, -0.0004173270419984247,
                       -0.141056084229664]),
        "exposure": 7000,
        "gain": 18,
        "rvec": np.mat([[1.69750257], [0.69091169], [-0.54474128]]),
        "tvec": np.mat([[-11381.85466339], [-584.01247871], [9359.30328641]]),
        "E_0": np.mat([
            [0.00462803, -0.999749, 0.0219115, 0.154876],
            [0.0931124, -0.0213857, -0.995426, -0.0506296],
            [0.995645, 0.0066471, 0.0929901, -0.137197],
            [0, 0, 0, 1]
        ])},

}

left_specs = dict(
    k_0=np.mat([[2599.59101996968, 0.0, 1528.51343714847],
                [0.0, 2599.32628783837, 1005.63370496221],
                [0.0, 0.0, 1.0]]),
    c_0=np.mat([[-0.0827470703754226], [0.173839479717410], [-0.000408515186013770],
                [0.000440205348940563], [-0.0805391333761662]]),
    rotate_vec=np.mat([[1.69750257], [0.69091169], [-0.54474128]]),
    transform_vec=np.mat([[-11381.85466339], [-479.01247871], [9449.30328641]]),
    e_0=np.mat([
        [0.0265686, -0.999625, -0.00665175, -0.131281 * 1000],
        [0.0841975, 0.0088682, -0.99641, 0.106948 * 1000],
        [0.996095, 0.0259131, 0.0844015, -0.213647 * 1000],
        [0, 0, 0, 1]
    ]))

right_specs = dict(
    k_0=np.mat([[2505.2629026927225, 0.0, 1529.4286325395244],
                [0.0, 2505.5722700649067, 1026.1378217662113],
                [0.0, 0.0, 1.0]]),
    c_0=np.mat([-0.06856710471358254, 0.1269396451339073,
                -0.0003599605406165552, -0.0004173270419984247,
                -0.141056084229664]),
    rotate_vec=np.mat([[1.69750257], [0.69091169], [-0.54474128]]),
    transform_vec=np.mat([[-11381.85466339], [-584.01247871], [9359.30328641]]),
    e_0=np.mat([
        [0.00462803, -0.999749, 0.0219115, 0.154876],
        [0.0931124, -0.0213857, -0.995426, -0.0506296],
        [0.995645, 0.0066471, 0.0929901, -0.137197],
        [0, 0, 0, 1]
    ]))

neo_camera_config = {
    "cam_left": VideoConfig(
        enable=True,
        net_process=True,
        path="/home/shiroki/radar_data/16_4_33_left.avi",
        **left_specs
    ),
    # "cam_left": RdrConfig(
    #     enable=True,
    #     net_process=False,
    #     endpoint="tcp://127.0.0.1:5555",
    #     **left_specs
    # ),
    "cam_right": VideoConfig(
        enable=False,
        net_process=False,
        path="/home/shiroki/radar_data/16_4_33_right.avi",
        **right_specs
    ),
}

net1_engine = resource_prefix + "net_onnx/net1.engine"
net2_engine = resource_prefix + "net_onnx/net2.engine"

net1_cls = ['car', 'watcher', 'base']
net2_cls_names = ["0", "1", "2", "3", "4",
                  "5", "O", "Bs", "Bb"]
net2_col_names = ["B", "R", "N", "P"]
color2enemy = {"red": 0, "blue": 1}
enemy2color = ['red', 'blue']
num2cam = ['左', '右']

armor_list = ['R1', 'R2', 'R3', 'R4', 'R5', 'B1', 'B2', 'B3', 'B4', 'B5']  # 雷达站实际考虑的各个装甲板类
unit_list = ['R1', 'R2', 'R3', 'R4', 'R5', 'RG', 'RO', 'RB', 'B1', 'B2', 'B3', 'B4', 'B5', 'BG', 'BO',
             'BB']  # 赛场上各个目标，主要用于HP显示

# 小地图图片路径
MAP_PATH = resource_prefix + "map.png"
BAG_FIRE = resource_prefix + "2022_06_15_10_11_01.dat"

# 小地图设定大小
map_size = (716, 384)  # 按像素尺寸
real_size = (28., 15.)  # 现实尺寸（m）

# 参加反投影预警区域
# 被反投影后的画布坐标的点可以通过 Reproject::get_scene_region 获取
region = \
    {
        'a_red_环形高地1_a': [real_points[27], real_points[28], real_points[25], real_points[26]],
        'a_red_环形高地2_a': [real_points[31], real_points[27], real_points[26], real_points[32]],
        'a_red_我方前哨站_d': [real_points[15], real_points[29], real_points[30], real_points[19],
                                   real_points[18], real_points[17], real_points[51]],
        'a_red_敌方前哨站_d': [real_points[33], real_points[8], real_points[43], real_points[2],
                                   real_points[1], real_points[0], real_points[71]],
        'a_red_飞坡_d': [real_points[0], real_points[66], real_points[67], real_points[75]],
        # 'a_red_我方3号高地_a': [real_points[59], real_points[60], real_points[35], real_points[64], real_points[63]],
        # 'a_red_敌方3号高地_a': [real_points[44], real_points[70], real_points[12], real_points[54], real_points[68]],
        'a_red_前哨站我方盲道_d': [real_points[30], real_points[25], real_points[58],
                                   real_points[21], real_points[79], real_points[19]],
        # 'a_red_3号高地下我方盲道及公路区_a': [real_points[26], real_points[60], real_points[35], real_points[65]],

        'a_blue_环形高地1_a': [real_points[9], real_points[10], real_points[11], real_points[7]],
        'a_blue_环形高地2_a': [real_points[10], real_points[11], real_points[13], real_points[14]],
        'a_blue_我方前哨站_d': [real_points[33], real_points[8], real_points[43], real_points[2],
                                real_points[1], real_points[0], real_points[71]],
        'a_blue_敌方前哨站_d': [real_points[15], real_points[29], real_points[30], real_points[19],
                                real_points[18], real_points[17], real_points[51]],
        'a_blue_飞坡_d': [real_points[55], real_points[17], real_points[78], real_points[56]],
        # 'a_blue_我方3号高地_a': [real_points[44], real_points[70], real_points[12], real_points[54], real_points[68]],
        # 'a_blue_敌方3号高地_a': [real_points[59], real_points[60], real_points[35], real_points[64], real_points[63]],
        'a_blue_前哨站我方盲道_d': [real_points[43], real_points[7], real_points[47],
                                    real_points[4], real_points[76], real_points[2]],
        # 'a_blue_3号高地下我方盲道及公路区_a': [real_points[11], real_points[53], real_points[12], real_points[45]],
    }

test_region = \
    {
        'a_fp_red_环形高地_a': [8.90, 6.69, 8.90, 9.36, 10.37, 9.00, 10.37, 7.00, 0.60],
        'a_fp_blue_环形高地_a': [8.90, 6.69, 8.90, 9.36, 10.37, 9.00, 10.37, 7.00, 0.60],
    }

PC_STORE_DIR = ""
LIDAR_TOPIC_NAME = "/livox/lidar"

# 0 为正式场上使用的 points 1 为 debug 用
# 用于 EPNP 标定，提示用，从 realpoints 中取点
objNames = [
    {
        "cam_left_red": ['飞坡点(右)', '风车狙击点角(左)', 'R3右后', 'R2右', '环形高地银矿左角（敌方）',
                         '敌方环形高地围栏点', '我方银矿左上', '我方银矿左下', 'B3B1', '我方长挡板高点'],
        "cam_right_red": ['我方风车狙击点角(左)', 'R3右后', 'R2右', '环形高地银矿左角(敌方)', '敌方环形高地围栏点',
                          '我方银矿左上', '我方银矿左下', 'R4右口', '我方长挡板高点'],
        "cam_left_blue": ['飞坡点(右)', '风车狙击点角(左)', 'B3右后', 'B2右', '环形高地银矿左角(敌方)',
                          '敌方环形高地围栏点', '我方银矿左上', '我方银矿左下', 'R3R1', '我方长挡板高点'],
        "cam_right_blue": ['我方风车狙击点角(左)', 'B3右后', 'B2右', '环形高地银矿左角(敌方)', '敌方环形高地围栏点',
                           '我方银矿左上', '我方银矿左下', 'B4右口', '我方长挡板高点'],
    },
    {
        "cam_left_red": ['风车狙击点角', '烧饼轨道左', '烧饼轨道右', '环形高低银矿处角',
                         '环形高低坡下角(右)', '环形高地坡右下角(左)', " "],
        "cam_right_red": ['风车狙击点角', '烧饼轨道左', '烧饼轨道右', '环形高低银矿处角',
                          '环形高低坡下角(右)', '环形高地坡右下角(左)', " "],
        "cam_left_blue": ['风车狙击点角', '烧饼轨道左', '烧饼轨道右', '环形高低银矿处角',
                          '环形高低坡下角(右)', '环形高地坡右下角(左)', " "],
        "cam_right_blue": ['风车狙击点角', '烧饼轨道左', '烧饼轨道右', '环形高低银矿处角',
                           '环形高低坡下角(右)', '环形高地坡右下角(左)', " "]
    }
]

# 德劳内三角定位选取定位点，是 realpoints 中的索引
choose = {"cam_left_red": [37, 65, 33, 66, 73, 72, 32, 28,
                           27, 29, 26, 30, 31, 15, 14, 41,
                           42, 40, 39, 9, 10, 11, 8, 12,
                           13, 1, 2, 3, 67, 38, 76, 77,
                           16, 17, 71],
          "cam_right_red": [33, 32, 28, 27, 29, 26, 31, 30,
                            80, 79, 20, 16, 17, 54, 2, 3,
                            76, 77, 9, 10, 11, 8, 15, 14,
                            13, 38, 71, 41, 42, 39, 40],
          "cam_left_blue": [38, 55, 14, 54, 53, 52, 15, 66,
                            11, 12, 10, 8, 9, 44, 32, 33,
                            39, 40, 42, 41, 30, 29, 28, 26,
                            61, 27, 36, 18, 19, 20, 56, 37,
                            79, 80, 34, 35],
          "cam_right_blue": [14, 15, 11, 12, 10, 8, 44, 9,
                             77, 76, 2, 34, 35, 66, 19, 20,
                             79, 80, 30, 29, 28, 26, 32, 33,
                             36, 37, 61, 39, 40, 41, 42]
          }

# 0为正式场上使用的 points, 1 为 debug 用
# 用于 EPNP 标定，提示用，从 realpoints 中取点, 是 realpoints 中的索引
objPoints = [
    {
        "cam_left_red": np.array([real_points[0],
                                  real_points[1],
                                  real_points[5],
                                  real_points[13],
                                  real_points[7],
                                  real_points[8],
                                  real_points[27],
                                  real_points[26],
                                  real_points[35],
                                  real_points[29]], dtype=np.float32),
        "cam_right_red": np.array([real_points[19],
                                   real_points[5],
                                   real_points[13],
                                   real_points[7],
                                   real_points[8],
                                   real_points[27],
                                   real_points[26],
                                   real_points[48],
                                   real_points[29]], dtype=np.float32),
        "cam_left_blue": np.array([real_points[17],
                                   real_points[18],
                                   real_points[22],
                                   real_points[32],
                                   real_points[25],
                                   real_points[29],
                                   real_points[10],
                                   real_points[11],
                                   real_points[12],
                                   real_points[8]], dtype=np.float32),
        "cam_right_blue": np.array([real_points[2],
                                    real_points[22],
                                    real_points[32],
                                    real_points[25],
                                    real_points[29],
                                    real_points[10],
                                    real_points[11],
                                    real_points[48],
                                    real_points[8]], dtype=np.float32),
    },
    {
        "cam_left_red": np.array([[9.56, 2.91, .90],  # 风车狙击点角
                                  [5.59, 5.50, 1.376],  # 烧饼轨道左
                                  [5.59, 9.36, 1.376],  # 烧饼轨道右
                                  [9.09, 6.69, .600],  # 环形高低银矿处角
                                  [11.18, 5.91, 0.],  # 环形高低坡下角(右)
                                  [10.15, 5.26, 0.],  # 环形高地坡右下角(左)
                                  [9.09, 9.36, .600]], dtype=np.float32),
        "cam_right_red": np.array([[9.56, 2.91, .90],  # 风车狙击点角
                                   [5.59, 5.50, 1.376],  # 烧饼轨道左
                                   [5.59, 9.36, 1.376],  # 烧饼轨道右
                                   [9.09, 6.69, .600],  # 环形高低银矿处角
                                   [11.18, 5.91, 0.],  # 环形高低坡下角(右)
                                   [10.15, 5.26, 0.],  # 环形高地坡右下角(左)
                                   [9.09, 9.36, .600]], dtype=np.float32),
        "cam_left_blue": np.array([[9.56, 2.91, .90],  # 风车狙击点角
                                   [5.59, 5.50, 1.376],  # 烧饼轨道左
                                   [5.59, 9.36, 1.376],  # 烧饼轨道右
                                   [9.09, 6.69, .600],  # 环形高低银矿处角
                                   [11.18, 5.91, 0.],  # 环形高低坡下角(右)
                                   [10.15, 5.26, 0.],  # 环形高地坡右下角(左)
                                   [9.09, 9.36, .600]], dtype=np.float32),
        "cam_right_blue": np.array([[9.56, 2.91, .90],  # 风车狙击点角
                                    [5.59, 5.50, 1.376],  # 烧饼轨道左
                                    [5.59, 9.36, 1.376],  # 烧饼轨道右
                                    [9.09, 6.69, .600],  # 环形高低银矿处角
                                    [11.18, 5.91, 0.],  # 环形高低坡下角(右)
                                    [10.15, 5.26, 0.],  # 环形高地坡右下角(左)
                                    [9.09, 9.36, .600]], dtype=np.float32),
    }
]

# 0为正式场上使用的points 1为debug用
Delaunary_points = [
    {
        "cam_left": [
            (0, 0, 3072, 2048),
            real_points
        ],
        "cam_right": [
            (0, 0, 3072, 2048),
            real_points
        ]
    },

    {
        "cam_left": [
            (0, 1023, 3072, 1024),
            real_points

        ],
        "cam_right": [
            (0, 1023, 3072, 1024),
            real_points
        ]
    }
]

speed_map = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0]
