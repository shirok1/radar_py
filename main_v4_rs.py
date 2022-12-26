"""
UI类
created by 李龙 2022/8
last edited by 陈希峻 2022/11
"""
import queue
import sys
import time
import os
import cv2 as cv
import numpy as np
import threading
import logging
from PyQt5 import QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt, QRect

import config
from config import USEABLE, enemy_color, cam_config, using_video, enemy2color
from mapping.ui_v4 import Ui_MainWindow
from radar_detect.Linar_rs import Radar
from radar_detect.reproject import Reproject
from radar_detect.location_alarm import Alarm
from mul_manager.pro_manager import sub, process_detect, process_detect_rs
from Serial.HP_show import HP_scene
from Serial.port_operation import Port_operate
from radar_detect.solve_pnp import SolvePnp
from radar_detect.eco_forecast import eco_forecast
from radar_detect.decision import decision_tree
from mapping.drawing import drawing, draw_message


class Mywindow(QtWidgets.QMainWindow, Ui_MainWindow):  # 这个地方要注意Ui_MainWindow

    # _create_event = multiprocessing.get_context('spawn').Event
    # _create_queue = multiprocessing.get_context('spawn').Queue
    _create_event = threading.Event
    _create_queue = queue.Queue

    _right_record = _create_event()
    _left_record = _create_event()
    _que_left = _create_queue()
    _event_right = _create_event()
    _que_right = _create_queue()
    _event_left = _create_event()
    _event_close = _create_event()
    _event_speed = _create_event()

    def __init__(self):
        super(Mywindow, self).__init__()
        self.setupUi(self)
        self.hp_scene = HP_scene(enemy_color, lambda x: self.set_image(x, "blood"))
        self.board_api = lambda x, y, z: self.set_board_text(x, y, z)
        self.pnp_api = lambda x, y, z: self.set_pnp_text(x, y, z)
        self.show_map = lambda x: self.set_image(x, "map")

        self.epnp_image = QImage()
        self.item = None
        self.scene = QtWidgets.QGraphicsScene()  # 创建场景

        self.__res_right = False
        self.__res_left = False
        self.__pic_right = None
        self.__pic_left = None

        self._use_lidar = not USEABLE["locate_state"][0]
        self.__cam_left = USEABLE['cam_left']
        self.__cam_right = USEABLE['cam_right']
        self.__serial = USEABLE['serial']

        if self.__cam_left:
            self.PRE_left = threading.Thread(target=process_detect, args=(
                self._event_left, self._que_left, 'cam_left',
                {'close': self._event_close, 'record': self._left_record, 'speed': self._event_speed}))
            self.PRE_left.daemon = True

        if self.__cam_right:
            self.PRE_right = threading.Thread(target=process_detect, args=(
                self._event_right, self._que_right, 'cam_right',
                {'close': self._event_close, 'record': self._right_record, 'speed': self._event_speed}))
            self.PRE_right.daemon = True

        if self.__serial:
            # import threading
            import serial
            from Serial.UART import read, write
            ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)
            self.read_thr = threading.Thread(target=read, args=(ser,))
            self.write_thr = threading.Thread(target=write, args=(ser,))
            self.read_thr.daemon = True
            self.write_thr.daemon = True
            self.write_thr.start()
            self.read_thr.start()

        self.draw_module = drawing()  # 绘图及信息管理类
        self.text_api = lambda x: self.draw_module.update(x)
        self.lidar = Radar('cam_left', text_api=self.text_api, imgsz=cam_config['cam_left']["size"], queue_size=100)

        if USEABLE['Lidar']:
            self.lidar.start()
        else:
            # 读取预定的点云文件
            self.lidar.preload()

        self.sp = SolvePnp(self.pnp_api)  # pnp解算

        self.decision_tree = decision_tree(self.text_api)
        self.repo_left = Reproject('cam_left', self.text_api)  # 左相机反投影
        self.loc_alarm = Alarm(enemy=enemy_color, api=self.show_map, touch_api=self.text_api,
                               state_=USEABLE['locate_state'], _save_data=True, debug=False)  # 绘图及信息管理类
        self.decision_tree = decision_tree(self.text_api)  # 决策树
        self.supply_detector = eco_forecast(self.text_api)  # 经济预测(判断敌方哪个加弹了)

        try:
            self.sp.read(f'cam_left_{enemy2color[enemy_color]}')
            self.repo_left.push_T(self.sp.rvec, self.sp.tvec)
            self.loc_alarm.push_T(self.sp.rvec, self.sp.tvec, 0)
        except Exception as e:
            print(f"[ERROR] {e}")
            self.repo_left.push_T(cam_config["cam_left"]["rvec"], cam_config["cam_left"]["tvec"])
            self.loc_alarm.push_T(cam_config["cam_left"]["rvec"], cam_config["cam_left"]["tvec"], 0)
        try:
            self.sp.read(f'cam_right_{enemy2color[enemy_color]}')
            self.loc_alarm.push_T(self.sp.rvec, self.sp.tvec, 1)
        except Exception as e:
            print(f"[ERROR] {e}")
            self.loc_alarm.push_T(cam_config["cam_right"]["rvec"], cam_config["cam_right"]["tvec"], 1)

        self.draw_module.info_update_reproject(self.repo_left.get_scene_region())
        self.draw_module.info_update_dly(self.loc_alarm.get_draw(0))
        self.__ui_init()
        self.start()

    def __ui_init(self):
        frame = np.zeros((162, 716, 3)).astype(np.uint8)
        self.set_image(frame, "left_demo")
        self.set_image(frame, "right_demo")
        del frame
        self.board_textBrowser = {}
        self.pnp_textBrowser = {}
        # 状态反馈，初始化为全False
        self.view_change = 0  # 视角切换控制符
        self.terminate = False
        self.record_state = False  # 0:停止 1:开始
        self.epnp_mode = False  # 0:停止 1:开始
        self.show_pc_state = False
        self.set_board_text("INFO", "定位状态", self.loc_alarm.get_mode())
        self._Eco_point = [0, 0, 0, 0]
        self._Eco_cut = [700, 1300, 400, 600]
        self._num_kk = 0
        self.set_board_text("INFO", "框框状态", f"{self._num_kk + 1}框框")

    def condition_key_on_clicked(self, event) -> None:
        if event.key() == Qt.Key_Q:
            self.loc_alarm.change_mode(self.view_change)
            self._use_lidar = not self.loc_alarm.state[0]
            self.set_board_text("INFO", "定位状态", self.loc_alarm.get_mode())
        elif event.key() == Qt.Key_T:  # 将此刻设为start_time
            Port_operate.start_time = time.time()
        elif event.key() == Qt.Key_3:  # xiao能量机关激活
            Port_operate.set_state(3, time.time())
        elif event.key() == Qt.Key_4:  # da能量机关激活
            Port_operate.set_state(4, time.time())
        elif event.key() == Qt.Key_E:  # 添加工程预警
            self.text_api(draw_message("engineer", 0, "Engineer", "critical"))
        elif event.key() == Qt.Key_F:  # 添加飞坡预警
            self.text_api(draw_message("fly", 0, "Fly", "critical"))
        elif event.key() == Qt.Key_C:  # 添加清零
            self.draw_module.clear_message()
        else:
            pass

    def ChangeView_on_clicked(self) -> None:
        """
        切换视角
        """
        pass
        # if self.view_change:
        #     if self.__cam_left:
        #         self.view_change = 0
        #     else:
        #         return
        # else:
        #     if self.__cam_right:
        #         self.view_change = 1
        #     else:
        #         return

    def record_on_clicked(self) -> None:
        if not self.record_state:
            self.record.setText("录制 正在录制")
            self.record_state = True
            self._left_record.set()
            self._right_record.set()
        else:
            self.record.setText("录制")
            self.record_state = False
            self._left_record.set()
            self._right_record.set()

    def showpc_on_clicked(self) -> None:
        self.show_pc_state = not self.show_pc_state
        self.epnp_mode = False

    def CloseProgram_on_clicked(self) -> None:
        """
        关闭程序
        """
        self.terminate = True

    def SpeedUp_on_clicked(self) -> None:
        config.global_speed += 0.25
        self._event_speed.set()
        self.CurrentSpeed.setText(f"x{config.global_speed}")

    def SlowDown_on_clicked(self) -> None:
        if(config.global_speed <= 0.25):
            return
        config.global_speed -= 0.25
        self._event_speed.set()
        self.CurrentSpeed.setText(f"x{config.global_speed}")

    def Pause_on_clicked(self) -> None:
        config.global_pause = not config.global_pause
        if config.global_pause:
            self.Pause.setText("继续")
        else:
            self.Pause.setText("暂停")

    def epnp_on_clicked(self) -> None:
        if self.tabWidget.currentIndex() == 1:
            self.epnp_mode = True
            self.show_pc_state = False
            time.sleep(0.1)
            if not self.view_change:
                frame = self.__pic_left
            else:
                frame = self.__pic_right
            if frame.shape[2] == 3:
                rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            else:
                return

            self.epnp_image = QImage(rgb, rgb.shape[1], rgb.shape[0], QImage.Format_RGB888)
            width = self.pnp_demo.width()
            height = self.pnp_demo.height()
            pix = QPixmap.fromImage(self.epnp_image).scaled(width, height)
            self.item = QtWidgets.QGraphicsPixmapItem(pix)
            self.scene.clear()
            self.scene.addItem(self.item)
            self.pnp_demo.setScene(self.scene)

            self.sp.sel_cam(self.view_change)
        else:
            self.epnp_mode = False
        self.sp.clc()
        self.pnp_textBrowser.clear()

    def epnp_calculate(self) -> None:
        result = self.sp.locate_pick()
        if result:
            self.sp.save()
            self.sp.clc()
            self.pnp_textBrowser.clear()
            self._update_epnp(self.sp.translation, self.sp.rotation, self.view_change)
            self.draw_module.info_update_dly(self.loc_alarm.get_draw(0))
            self.draw_module.info_update_reproject(self.repo_left.get_scene_region())

    def epnp_mouseEvent(self, event) -> None:
        if self.epnp_mode:
            if event.button() == Qt.LeftButton:
                x = event.x()
                y = event.y()
                pointF = self.pnp_demo.mapToScene(QRect(0, 0, self.pnp_demo.viewport().width(),
                                                        self.pnp_demo.viewport().height()))[0]
                x_offset = pointF.x()
                y_offset = pointF.y()
                x = int((x + x_offset) / self.pnp_demo.width() * self.epnp_image.width())
                y = int((y + y_offset) / self.pnp_demo.height() * self.epnp_image.height())
                self.sp.add_point(x, y)

    def pc_mouseEvent(self, event) -> None:
        if self.show_pc_state:
            # TODO: 这里的3072是个常值，最好改了
            x = int(event.x() / self.main_demo.width() * 3072)
            y = int(event.y() / self.main_demo.height() * 2048) + cam_config['cam_left']['roi'][1]
            w = 10
            h = 5
            # 格式定义： [N, [bbox(xyxy), conf, cls, bbox(xyxy), conf, cls, col, N]
            self.repo_left.check(np.array([x, y, w, h, 1., 1, x, y, w, h, 1., 1., 1., 0]).reshape(1, -1))
            dph = self.lidar.detect_depth(
                rects=[[x - 5, y - 2.5, w, h]]).reshape(-1, 1)
            if not np.any(np.isnan(dph)):
                self.loc_alarm.pc_location(self.view_change, np.concatenate(
                    [np.array([[1., x, y]]), dph], axis=1))

    def eco_key_on_clicked(self, event) -> None:
        step = 20
        if event.key() == Qt.Key_P:  # 换框
            self.set_board_text("INFO", "框框状态", f"{self._num_kk + 1}框框")
            self._num_kk = abs(1 - self._num_kk)
        elif event.key() == Qt.Key_W and self._Eco_cut[2] > step:
            self._Eco_cut[2] -= step
            self._Eco_cut[3] -= step
        elif event.key() == Qt.Key_S and self._Eco_cut[3] < 2048 - step:
            self._Eco_cut[2] += step
            self._Eco_cut[3] += step
        elif event.key() == Qt.Key_A and self._Eco_cut[0] > step:
            self._Eco_cut[0] -= step
            self._Eco_cut[1] -= step
        elif event.key() == Qt.Key_D and self._Eco_cut[1] < 3072 - step:
            self._Eco_cut[0] += step
            self._Eco_cut[1] += step

    def eco_mouseEvent(self, event) -> None:
        if self.__pic_left is None:
            return
        x = event.x()
        y = event.y()
        x = int(x / self.far_demo.width() * (self._Eco_cut[1] - self._Eco_cut[0]) + self._Eco_cut[0])
        y = int(y / self.far_demo.height() * (self._Eco_cut[3] - self._Eco_cut[2]) + self._Eco_cut[2])
        if event.button() == Qt.LeftButton:
            self._Eco_point[0] = x
            self._Eco_point[1] = y
        if event.button() == Qt.RightButton:
            self._Eco_point[2] = x
            self._Eco_point[3] = y
        if self._Eco_point[2] > self._Eco_point[0] and self._Eco_point[3] > self._Eco_point[1]:
            self.supply_detector.update_ori(self.__pic_left, self._Eco_point, self._num_kk)
            self.text_api(
                draw_message("eco_board", 2,
                             (self._Eco_point[0], self._Eco_point[1],
                              self._Eco_point[2],
                              self._Eco_point[3]), "info"))

    def epnp_next_on_clicked(self) -> None:
        self.sp.step(1)

    def epnp_back_on_clicked(self) -> None:
        self.sp.step(-1)

    def epnp_del(self) -> None:
        self.sp.del_point()

    def epnp_clear_on_clicked(self) -> None:
        self.sp.clc()

    def set_image(self, frame, position="") -> bool:
        """
        Image Show Function

        :param frame: the image to show
        :param position: where to show
        :return: a flag to indicate whether the showing process have succeeded or not
        """
        if frame is None:
            return False
        if position not in ["main_demo", "map", "far_demo", "blood", "hero_demo", "left_demo", "right_demo"]:
            print("[ERROR] The position isn't a member of this UI_window")
            return False
        width = self.__dict__[position].width()
        height = self.__dict__[position].height()
        if frame.shape[2] == 3:
            rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        elif frame.shape[2] == 2:
            rgb = cv.cvtColor(frame, cv.COLOR_GRAY2RGB)
        else:
            return False

        # allocate the space of QPixmap
        temp_image = QImage(rgb, rgb.shape[1], rgb.shape[0], QImage.Format_RGB888)

        temp_pixmap = QPixmap(temp_image).scaled(width, height, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        # set the image to the QPixmap location to show the image on the UI
        self.__dict__[position].setPixmap(temp_pixmap)
        self.__dict__[position].setScaledContents(True)
        return True

    def set_board_text(self, _type: str, position: str, message: str) -> None:
        """
        to set text in the QtLabel
        :param message: message that will be put on the screen;
        :param _type: message level [ERROR,INFO,WARNING];
        :param position: message that will put on position [LOCATION,ALARM_POSITION]
        :return:
        a flag to indicate whether the showing process have succeeded or not
        """
        # Using "<br \>" to combine the contents of the message list to a single string message
        if message == "":
            if position in self.board_textBrowser.keys():
                self.board_textBrowser.pop(position)
        else:
            if _type == "ERROR":
                msg = f"<font color='#FF0000'><b>{message}</b></font>"
            elif _type == "INFO":
                msg = f"<font color='#404040'><b>{message}</b></font>"
            else:
                msg = f"<font color='#FF8033'><b>{message}</b></font>"
            self.board_textBrowser[position] = msg.replace('\n', "<br />")

    def set_pnp_text(self, _type: str, position: str, message: str) -> bool:
        """
        to set text in the QtLabel
        :param message: message that will be put on the screen;
        :param _type: message level [ERROR,INFO,WARNING];
        :param position: message that will put on position [LOCATION,ALARM_POSITION,TIMEING]
        :return:
        a flag to indicate whether the showing process have succeeded or not
        """
        # Using "<br \>" to combine the contents of the message list to a single string message
        if message == "":
            if position in self.pnp_textBrowser.keys():
                self.pnp_textBrowser.pop(position)
        else:
            if _type == "ERROR":
                msg = f"<font color='#FF0000'><b>{message}</b></font>"
            elif _type == "INFO":
                msg = f"<font color='#404040'><b>{message}</b></font>"
            else:
                msg = f"<font color='#FF8033'><b>{message}</b></font>"
            self.pnp_textBrowser[position] = msg.replace('\n', "<br />")
        text = "<br \>".join(list(self.pnp_textBrowser.values()))  # css format to replace \n
        self.pnp_condition.setText(text)
        return True

    def start(self) -> None:
        if self.__cam_left:
            self.PRE_left.start()
        if self.__cam_right:
            self.PRE_right.start()

    def _update_state(self) -> None:
        text = ("左相机寄了" if isinstance(self.__res_left, bool) \
            else "左相机正常工作") \
            + "\t" + ("右相机寄了" if isinstance(self.__res_right, bool) \
            else "右相机正常工作")
        self.set_board_text("INFO", "相机", text)
        text = "<br \>".join(list(self.board_textBrowser.values()))  # css format to replace \n
        self.condition.setText(text)

    # 更新图像
    def _update_image(self) -> None:
        if self.__pic_left is not None:
            self.draw_module.draw_message(self.__pic_left)
            self.set_image(self.__pic_left, "main_demo")
            self.set_image(self.__pic_left[self._Eco_cut[2]:self._Eco_cut[3], self._Eco_cut[0]:self._Eco_cut[1]],
                           "far_demo")
        if self.__pic_right is not None:
            self.set_image(self.__pic_right, "hero_demo")

    # 更新epnp 函数
    def _update_epnp(self, tvec: np.ndarray, rvec: np.ndarray, side: int) -> None:
        if not side:
            self.repo_left.push_T(rvec, tvec)
            self.loc_alarm.push_T(rvec, tvec, 0)
        else:
            self.loc_alarm.push_T(rvec, tvec, 1)

    # 更新反投影
    def _update_reproject(self) -> None:
        if self.__cam_left:
            self.repo_left.check(self.__res_left)
            self.repo_left.push_text()

    # 位置预警函数，更新各个预警区域的预警次数
    def _update_location_alarm(self) -> None:
        t_loc_left = None
        if isinstance(self.__res_left, np.ndarray):
            if self.__res_left.shape[0] != 0:
                if self._use_lidar:
                    armors = self.__res_left[:, [11, 6, 7, 8, 9]]
                    armors[:, 3] = armors[:, 3] - armors[:, 1]
                    armors[:, 4] = armors[:, 4] - armors[:, 2]
                    armors = armors[np.logical_not(np.isnan(armors[:, 0]))]
                    if armors.shape[0] != 0:
                        armors[:, 2] += cam_config['cam_left']['roi'][1]
                        dph = self.lidar.detect_depth(rects=armors[:, 1:].tolist()).reshape(-1, 1)
                        x0 = (armors[:, 1] + armors[:, 3] / 2).reshape(-1, 1)
                        y0 = (armors[:, 2] + armors[:, 4] / 2).reshape(-1, 1)
                        t_loc_left = np.concatenate([armors[:, 0].reshape(-1, 1), x0, y0, dph], axis=1)
                else:
                    armors = self.__res_left[:, [11, 6, 7, 8, 9]]
                    armors = armors[np.logical_not(np.isnan(armors[:, 0]))]
                    if armors.shape[0] != 0:
                        armors[:, 2] += cam_config['cam_left']['roi'][1]
                        x0 = (armors[:, 1] + (armors[:, 3] - armors[:, 1]) / 2).reshape(-1, 1)
                        y0 = (armors[:, 2] + (armors[:, 4] - armors[:, 2]) / 2).reshape(-1, 1)
                        t_loc_left = np.concatenate([armors[:, 0].reshape(-1, 1), x0, y0, np.zeros(x0.shape)], axis=1)
        t_loc_right = None
        self.loc_alarm.two_camera_merge_update(t_loc_left, t_loc_right, self.repo_left.get_rp_alarming())
        self.loc_alarm.check()
        self.loc_alarm.show()

    # 更新串口
    def _update_serial(self) -> None:

        if self.__serial:
            Port_operate.gain_positions(self.loc_alarm.get_last_loc())
            Port_operate.gain_decisions(self.decision_tree.get_decision())
            if Port_operate.change_view != -1:
                self.view_change = Port_operate.change_view
        Port_operate.get_message(self.hp_scene)
        self.hp_scene.show()

    # 更新决策类
    def _update_decision(self) -> None:
        self.supply_detector.eco_detect(self.__pic_left, self.loc_alarm.get_last_loc(),
                                        lambda x: self.set_image(x, "hero_demo"))
        self.decision_tree.update_serial(Port_operate.positions_us(),
                                         Port_operate.HP()[8 * (1 - enemy_color):8 * (1 - enemy_color) + 8],
                                         Port_operate.HP()[8 * enemy_color:8 * enemy_color + 8],
                                         Port_operate.get_state(),
                                         int(420 - time.time() + Port_operate.start_time),
                                         False)
        self.decision_tree.update_information(self.loc_alarm.get_last_loc(), self.repo_left.fly,
                                              self.repo_left.fly_result, self.repo_left.hero_r3,
                                              self.__res_left, self.repo_left.rp_alarming.copy())
        self.decision_tree.decision_alarm()

    # 主函数循环
    def spin(self) -> None:
        # get images
        if self.__cam_left:
            self.__res_left, self.__pic_left = sub(self._event_left, self._que_left)
        if self.__cam_right:
            self.__res_right, self.__pic_right = sub(self._event_right, self._que_right)

        # if in epnp_mode , just show the images
        if not self.epnp_mode:
            if self.show_pc_state:
                if self.view_change == 0 and isinstance(self.__pic_left, np.ndarray):
                    if self._use_lidar:
                        depth = self.lidar.read()
                        self.draw_module.draw_pc(self.__pic_left, depth, cam_config['cam_left']['roi'])
                    self.draw_module.draw_CamPoints(self.__pic_left, cam_config['cam_left']['roi'])
            else:
                self._update_reproject()
                self._update_location_alarm()
                self._update_serial()
                self._update_decision()
        self._update_image()
        self._update_state()

        # if close the program
        if self.terminate:
            self.loc_alarm.close_data()
            self._event_close.set()
            if self.__cam_left:
                # self.PRE_left.join(timeout=0.5)
                self.PRE_left.join()
            if self.__cam_right:
                # self.PRE_right.join(timeout=0.5)
                self.PRE_right.join()
            sys.exit()

    # def closeEvent(self, event) -> None:
    #     self.terminate = True
    #     event.ignore()

class LOGGER(object):
    """
    logger 类
    """

    def __init__(self):
        # 创建一个logger
        import time
        logger_name = time.strftime('%Y-%m-%d %H-%M-%S')
        self.terminal = sys.stdout
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        # 创建一个handler，用于写入日志文件
        log_path = os.path.abspath(os.getcwd()) + "/logs/"  # 指定文件输出路径
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        LogName = log_path + logger_name + '.log'  # 指定输出的日志文件名
        fh = logging.FileHandler(LogName, encoding='utf-8')  # 指定utf-8格式编码，避免输出的日志文本乱码
        fh.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(message)s')
        fh.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)

    def write(self, message):
        # self.terminal.write(message)
        _stdout.write(message)
        if message == '\n':
            return
        if "[ERROR]" in message:
            self.logger.error(message)
        elif "[WARNING]" in message:
            self.logger.warning(message)
        else:
            self.logger.info(message)

    def flush(self):
        _stdout.flush()
        pass

    def __del__(self):
        pass


if __name__ == "__main__":
    # multiprocessing.set_start_method('spawn')
    # ui
    app = QtWidgets.QApplication(sys.argv)
    _stdout = sys.stdout
    sys.stdout = LOGGER()
    MyShow = Mywindow()
    MyShow.show()

    timer_main = QTimer()  # 主循环使用的线程
    timer_main.timeout.connect(MyShow.spin)
    timer_main.start(0)

    sys.exit(app.exec_())
