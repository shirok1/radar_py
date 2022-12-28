# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : decision.py
# Time       ：2022/7/1 下午10:28
# Author     ：author name
# version    ：python 3.8
# Description：
"""
import time

import numpy as np
from mapping.drawing import draw_message
from config import enemy_color


class decision_tree(object):

    def __init__(self, text_api):
        self.init_flag = False

        self._enemy_position = np.zeros((5, 2))  # 敌方位置
        self._our_position = np.zeros((5, 2))  # 我方位置
        self._enemy_blood = np.zeros((8, 1))  # 敌方血量
        self._our_blood = np.zeros((8, 1))  # 我方血量
        self._last_blood = np.zeros((8, 1))  # 我方血量
        self._our_blood_max = np.ones((8, 1))  # 我方血量上限
        self._position_2d = None    #
        self._rp_alarming = {}  # 反投影预警信息
        self._state = 0  # 第几次能量机关
        self.text_api = text_api    # 文字api（待）
        # _car_decision第一维：0~4：对应装甲板1~5号（1:英雄 2:工程 3~5:步兵） 6：哨兵（旧版）
        # _car_decision第二维：0-预警类型（0:normal 1:attack 2:run 3:fly(tou?) 4:fly?） 1-攻击目标 2-云台 3-方位
        self._car_decision = np.zeros((6, 4)).astype(np.uint8)
        self._decision_time = np.zeros((6, 1))
        if enemy_color:
            self.start_x = 0
        else:
            self.start_x = 28.
        self._start_time = time.time()
        self._energy_time = time.time()
        self._guard_time = time.time()
        self._fly_numbers = np.array([])
        self._engineer_flag = False
        self._fly_flag = False
        self._tou_flag = False
        self._tou_qsz = False
        self._remain_time = 0

    # 入口
    def decision_alarm(self):
        # abandon
        # 判断是否已获取场上信息
        if self.init_flag:
            self.tt = time.time()
            self._tou_flag = False
            self._engineer_alarm()
            self._tou_alarm()
            self._blood_alarm()
            self._car_alarm()
        else:
            # 还原判断标记
            self.clear_state()
        self.generate_information()

    # 工程机器人预警
    def _engineer_alarm(self):
        flag = False
        # 获取工程机器人位置
        eng_pos = self._enemy_position[1]
        if eng_pos.all():
            x_abs = abs(eng_pos[0] - self.start_x)
            if x_abs < 8 and eng_pos[3] < 0.1:
                flag = True
        for r in self._rp_alarming.keys():
            # 格式解析
            _, _, location, _ = r.split('_')
            if location in ["我方3号高地", "前哨站我方盲道", "3号高地下我方盲道及公路区", "tou"]:
                # 在该区域里的敌方小车数量
                sz = self._rp_alarming[r].shape[0]
                # 工程机器人对基地无直接威胁
                if 2 in self._rp_alarming[r]:
                    flag = True
                    sz -= 1
                # 几处区域有其他车，认为有偷家情况
                if sz > 0:
                    self._tou_flag = True
        # 检测到工程机器人
        self._engineer_flag = flag

    def _run_alarm(self, valid: np.ndarray):
        # state 为 4
        if self._state == 4:
            # 大能量机关，车血量剩余40%以下时危险
            decision = (self._our_blood / self._our_blood_max <= 0.4).reshape(-1)[:6]
            decision = np.bitwise_and(decision, valid)
            # 赶紧润
            self._car_decision[decision, 0] = 2
        elif self._state != 1 and self._state != 2:
            # 第三次争夺能量机关，车血量剩余25%以下
            decision = (self._our_blood / self._our_blood_max <= 0.25).reshape(-1)[:6]
            decision = np.bitwise_and(decision, valid)
            # 润
            self._car_decision[decision, 0] = 2

    def _tou_alarm(self):
        """

        """
        # car_flag = False
        # for i in range(5):
        #     if self._our_position[i][0] != 0:
        #         distance = abs(self._enemy_position[i][0] - self.start_x)
        #         if distance <= 8:
        #              car_flag = True
        #             break
        # if not car_flag:
        # 距离基地太近，可以认为在偷家
        result = np.bitwise_and(self._enemy_position[:, 0] != 0,
                                abs(self._enemy_position[:, 0] - self.start_x) <= 8.5)
        # 只有敌方工程进基地不算偷
        result[1] = False
        if result.any():
            self._tou_flag = True

    # 待补充
    def _target_attack(self, valid: np.ndarray):
        # 敌方机器人在己方半场，且血量较低
        choose = np.bitwise_and(self._enemy_blood[:5, 0] <= 100,
                                np.bitwise_and(self._enemy_position[:, 0] != 0,
                                               abs(self._enemy_position - self.start_x)[:, 0] <= 14))
        choose[1] = False
        if choose.any():
            valid_c = np.argwhere(choose == True).reshape(-1).tolist()
            # 优先攻击最低血量
            best_c = np.argmin(self._enemy_blood[valid_c, 0])
            best_c = valid_c[best_c]
            self._car_decision[:, 1] = best_c + 1
            self._car_decision[valid, 0] = 1

    # 待补充
    def _guard_decision(self):
        # 哨兵决策
        self._car_decision[5][2:4] = [0, 0]
        for r in self._rp_alarming.keys():
            # 格式解析
            _, _, location, _ = r.split('_')
            if location in ["我方3号高地", "3号高地下我方盲道及公路区", "前哨站我方盲道", "环形高地1"]:
                if self._rp_alarming[r].shape[0] != 0:
                    if location == "我方3号高地":
                        self._car_decision[5][2:4] = [1, 1]
                    elif location == "前哨站我方盲道":
                        self._car_decision[5][2:4] = [2, 1]
                    else:
                        self._car_decision[5][2:4] = [2, 2]

    def _blood_alarm(self):
        # 基地掉血警告
        blood_minus = self._last_blood - self._our_blood
        # 哨兵掉血，或者基地掉血在1000以内，认定为偷家
        # 大于1000可能是飞镖等特殊情况
        if blood_minus[5] > 0 or 1000 > blood_minus[7] > 0:
            self._tou_flag = True
        # 前哨站迅速掉血，认定为前哨站被偷袭
        # 一次伤害大于600，认为是飞镖伤害
        if 600 > blood_minus[6] > 100:
            self._tou_qsz = True

    def _car_alarm(self):
        # 进行哨兵预警
        self._guard_decision()
        # 如果发生偷家或飞坡，及时更新决策信息
        if self._fly_flag:
            self._car_decision[:5, 0] = 4
            self._decision_time[:, 0] = self.tt
        elif self._tou_flag:
            self._car_decision[:5, 0] = 3
            self._decision_time[:, 0] = self.tt
        else:
            # 短时间内下达了决策的机器人，不再下达决策
            valid = (self.tt - self._decision_time[:, 0] > 4).reshape(-1)
            valid[5] = False
            self._car_decision[valid, 0] = 0
            self._target_attack(valid)
            self._run_alarm(valid)
            self._decision_time[:, 0] = self.tt

    def _show_energy(self):
        self.text_api(draw_message("remain_time", 1,
                                   ("{0}:{1}".format(self._remain_time // 60, self._remain_time % 60), (1400, 120)),
                                   "critical"))
        remain_time = int(time.time() - self._energy_time)
        if self._state == 0:
            return
        elif self._state == 2:
            text = "BIG"
            remain_time = 45 - remain_time
            level = "critical"
        elif self._state == 1:
            text = "SMALL"
            remain_time = 45 - remain_time
            level = "critical"
        elif self._state == 4:
            text = "BIG"
            remain_time = 45 - remain_time
            level = "critical"
        elif self._state == 3:
            text = "SMALL"
            remain_time = 45 - remain_time
            level = "critical"
        else:
            text = "UNABLE"
            remain_time = 30 - remain_time
            level = "info"
            self.text_api(draw_message("energy_time", 1,
                                       ("", (1600, 120)),
                                       "critical"))
        self.text_api(draw_message("energy_time", 1,
                                   ("{0}  {1}".format(text, remain_time), (1600, 120)),
                                   level))

    def get_flag(self):
        return self._tou_flag or self._engineer_flag

    def clear_state(self):
        self._enemy_position = np.zeros((5, 2))  # 敌方位置
        self._our_position = np.zeros((5, 2))  # 我方位置
        self._enemy_blood = np.zeros((8, 1))  # 敌方血量
        self._our_blood = np.zeros((8, 1))  # 我方血量
        self._last_blood = np.zeros((8, 1))  # 我方血量
        self._our_blood_max = np.ones((8, 1))  # 我方血量上限
        self._position_2d = None
        self._rp_alarming = {}
        self._state = 0  # 增益
        self._car_decision = np.zeros((6, 4)).astype(np.uint8)
        self._decision_time = np.zeros((6, 1))
        self._engineer_flag = False
        self._fly_flag = False
        self._fly_numbers = np.array([])

    def update_serial(self, our_position: np.ndarray, our_blood: np.ndarray,
                      enemy_blood: np.ndarray, state: list, remain_time: float, high_light: bool):

        self._our_position = our_position
        self._last_blood = self._our_blood
        self._our_blood = our_blood.reshape((8, 1))
        self._enemy_blood = enemy_blood.reshape((8, 1))
        self._stage, self._state, self._energy_time = state
        self._remain_time = remain_time
        self._high_light = high_light

    def generate_information(self):
        self._show_energy()
        if self._fly_flag:
            self.text_api(draw_message("fly", 0, f"FLY_{self._fly_numbers}", "critical"))
            if isinstance(self._position_2d, np.ndarray):
                count = self._position_2d[:, 11]
                arg = np.argwhere(count == self._fly_numbers)[0][0]
                self.text_api(
                    draw_message("fly_alarm", 2, self._position_2d[arg][0:4].astype(int).tolist(), "critical"))
        if self._engineer_flag:
            self.text_api(draw_message("engineer", 0, "Engineer", "critical"))
        if self._tou_qsz:
            self.text_api(draw_message("tou_qsz", 0, "HERO Outpost!!!", "warning"))
        if self._tou_flag:
            self.text_api(draw_message("tou", 0, "DEFEND!!!", "critical"))
        self._guard_decision()
        if isinstance(self._position_2d, np.ndarray):
            if (self._remain_time < 600 or self._high_light) and self._position_2d.size > 0:
                arg = np.argwhere(self._position_2d[:, 11] == 1).reshape(-1, 1)
                if arg.size > 0:
                    self.text_api(
                        draw_message("hero", 2, self._position_2d[arg[0][0]][0:4].astype(int).tolist(), "critical"))
                # else:
                #     if self._high_light:
                #         self.text_api(draw_message(f"{i[11]}", 2, i[0:4].astype(int).tolist(), "warning"))

    def update_information(self, enemy_position: np.ndarray, fly_flag: bool, fly_numbers: np.ndarray, hero_r3: bool,
                           position_2d, rp_alarming: dict):
        self._enemy_position = enemy_position
        self._hero_r3 = hero_r3
        self._fly_flag = fly_flag
        self._rp_alarming = rp_alarming
        self._fly_numbers = fly_numbers
        self._position_2d = position_2d
        self.init_flag = True

    def get_decision(self) -> np.ndarray:
        # print(self._car_decision)
        return self._car_decision
