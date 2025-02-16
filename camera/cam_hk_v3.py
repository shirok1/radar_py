"""
相机类
用于打开相机并且输出图像
created by 李龙 2021/11
最终修改 by 陈希峻 2022/11
"""
import cv2 as cv
import numpy as np
from loguru import logger

from camera.MvImport.MvCameraControl_class import *
from config_type import HikCameraDriverConfigExt


class Camera_HK:
    """
    海康机器人相机类。
    通过加载 Hikrobot MVS 提供的动态库来实现，
    需要设置 `MVCAM_COMMON_RUNENV`
    和 `LD_LIBRARY_PATH` 环境变量。
    """

    def __init__(self, config: HikCameraDriverConfigExt):
        """
        @param config: 相机配置
        """
        self.__camera_config = config
        self.__id = self.__camera_config.camera_id
        self.__roi = self.__camera_config.roi
        self.__exposure = self.__camera_config.exposure
        self.__gain = self.__camera_config.gain
        self.__img = None

        # ch:创建相机实例 | en:Creat Camera Object
        self.cam = MvCamera()

        SDKVersion = MvCamera.MV_CC_GetSDKVersion()
        logger.info("SDKVersion[0x%x]" % SDKVersion)

        deviceList = MV_CC_DEVICE_INFO_LIST()
        tlayerType = MV_USB_DEVICE

        # ch:枚举设备 | en:Enum device
        ret = MvCamera.MV_CC_EnumDevices(tlayerType, deviceList)
        if ret != 0:
            logger.error("enum devices fail! ret[0x%x]" % ret)
            self.init_ok = False
            return

        if deviceList.nDeviceNum == 0:
            logger.error("find no device!")
            self.init_ok = False

        Find = False

        for i in range(0, deviceList.nDeviceNum):
            mvcc_dev_info = cast(deviceList.pDeviceInfo[i], POINTER(MV_CC_DEVICE_INFO)).contents
            if mvcc_dev_info.nTLayerType == MV_USB_DEVICE:
                strSerialNumber = ""
                for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chSerialNumber:
                    if per == 0:
                        break
                    strSerialNumber = strSerialNumber + chr(per)
                if self.__id == strSerialNumber:
                    nConnectionNum = i
                    Find = True
                logger.info("user serial number: %s" % strSerialNumber)
        if Find:
            # ch:选择设备并创建句柄 | en:Select device and create handle
            self.__stDeviceList = cast(deviceList.pDeviceInfo[int(nConnectionNum)],
                                       POINTER(MV_CC_DEVICE_INFO)).contents

            ret = self.cam.MV_CC_CreateHandle(self.__stDeviceList)
            if ret != 0:
                logger.error("create handle fail! ret[0x%x]" % ret)
                self.init_ok = False

            # ch:打开设备 | en:Open device
            ret = self.cam.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0)
            if ret != 0:
                logger.error("open device fail! ret[0x%x]" % ret)
                self.init_ok = False

            ret = self.cam.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF)
            if ret != 0:
                logger.error("set TriggerMode failed! ret [0x%x]" % ret)
                self.init_ok = False

            ret = self.cam.MV_CC_SetEnumValue("ExposureMode", MV_EXPOSURE_AUTO_MODE_OFF)
            if ret != 0:
                logger.error("set height failed! ret [0x%x]" % ret)
                self.init_ok = False

            ret = self.cam.MV_CC_SetEnumValue("GainAuto", MV_GAIN_MODE_OFF)
            if ret != 0:
                logger.error("set GainAuto failed! ret [0x%x]" % ret)
                self.init_ok = False
            ret = self.cam.MV_CC_SetEnumValue("PixelFormat", PixelType_Gvsp_BayerRG8)
            if ret != 0:
                logger.error("set PixelFormat failed! ret [0x%x]" % ret)
                self.init_ok = False
            ret = self.cam.MV_CC_SetBoolValue("BlackLevelEnable", False)
            if ret != 0:
                logger.error("set BlackLevelEnable failed! ret [0x%x]" % ret)
                self.init_ok = False

            ret = self.cam.MV_CC_SetEnumValue("BalanceWhiteAuto", MV_BALANCEWHITE_AUTO_CONTINUOUS)
            if ret != 0:
                logger.error("set BalanceWhiteAuto failed! ret [0x%x]" % ret)
                self.init_ok = False

            ret = self.cam.MV_CC_SetEnumValue("AcquisitionMode", MV_ACQ_MODE_CONTINUOUS)
            if ret != 0:
                logger.error("set AcquisitionMode failed! ret [0x%x]" % ret)
                self.init_ok = False

            ret = self.cam.MV_CC_SetBoolValue("AcquisitionFrameRateEnable", False)
            if ret != 0:
                logger.error("set AcquisitionFrameRateEnable failed! ret [0x%x]" % ret)
                self.init_ok = False

            ret = self.cam.MV_CC_SetIntValue("Height", int(self.__roi[3]))
            if ret != 0:
                logger.error("set height failed! ret [0x%x]" % ret)
                self.init_ok = False

            ret = self.cam.MV_CC_SetIntValue("Width", int(self.__roi[2]))
            if ret != 0:
                logger.error("set width failed! ret [0x%x]" % ret)
                self.init_ok = False
            ret = self.cam.MV_CC_SetIntValue("OffsetX", int(self.__roi[0]))
            if ret != 0:
                logger.error("set width failed! ret [0x%x]" % ret)
                self.init_ok = False
            ret = self.cam.MV_CC_SetIntValue("OffsetY", int(self.__roi[1]))
            if ret != 0:
                logger.error("set OffsetY failed! ret [0x%x]" % ret)
                self.init_ok = False
            ret = self.cam.MV_CC_SetFloatValue("ExposureTime", self.__exposure)
            if ret != 0:
                logger.error("start grabbing fail! ret[0x%x]" % ret)
                self.init_ok = False

            ret = self.cam.MV_CC_SetFloatValue("Gain", float(self.__gain))
            if ret != 0:
                logger.error("start grabbing fail! ret[0x%x]" % ret)
                self.init_ok = False

            # ch:获取数据包大小 | en:Get payload size
            stParam = MVCC_INTVALUE()
            memset(byref(stParam), 0, sizeof(MVCC_INTVALUE))
            ret = self.cam.MV_CC_GetIntValue("PayloadSize", stParam)
            if ret != 0:
                logger.error("get payload size fail! ret[0x%x]" % ret)
                self.init_ok = False
            self.__nPayloadSize = stParam.nCurValue
            self.__data_buf = (c_ubyte * self.__nPayloadSize)()
            # ch:开始取流 | en:Start grab image
            ret = self.cam.MV_CC_StartGrabbing()
            if ret != 0:
                logger.error("start grabbing fail! ret[0x%x]" % ret)
                self.init_ok = False
            self.__stDeviceList = MV_FRAME_OUT_INFO_EX()
            memset(byref(self.__stDeviceList), 0, sizeof(self.__stDeviceList))
            self.init_ok = True
        else:
            self.init_ok = False

    def work_thread(self) -> bool:
        ret = self.cam.MV_CC_GetOneFrameTimeout(self.__data_buf, self.__nPayloadSize, self.__stDeviceList, 1000)
        if ret == 0:
            # logger.info("get one new_data: Width[%d], Height[%d], nFrameNum[%d]" % (
            #     self.__stDeviceList.nWidth, self.__stDeviceList.nHeight, self.__stDeviceList.nFrameNum))

            nRGBSize = self.__stDeviceList.nWidth * self.__stDeviceList.nHeight * 3
            stConvertParam = MV_CC_PIXEL_CONVERT_PARAM()
            memset(byref(stConvertParam), 0, sizeof(stConvertParam))
            stConvertParam.nWidth = self.__stDeviceList.nWidth
            stConvertParam.nHeight = self.__stDeviceList.nHeight
            stConvertParam.pSrcData = self.__data_buf
            stConvertParam.nSrcDataLen = self.__stDeviceList.nFrameLen
            stConvertParam.enSrcPixelType = self.__stDeviceList.enPixelType
            stConvertParam.enDstPixelType = PixelType_Gvsp_BGR8_Packed
            stConvertParam.pDstBuffer = (c_ubyte * nRGBSize)()
            stConvertParam.nDstBufferSize = nRGBSize

            ret = self.cam.MV_CC_ConvertPixelType(stConvertParam)
            if ret != 0:
                logger.error("convert pixel fail! ret[0x%x]" % ret)
                return False
            else:
                img_buff = (c_ubyte * stConvertParam.nDstLen)()
                memmove(byref(img_buff), stConvertParam.pDstBuffer, stConvertParam.nDstLen)
                self.__img = np.asarray(img_buff).reshape(self.__roi[3], self.__roi[2], 3)
                # self.__img = cv.copyMakeBorder(self.__img, 0, self.__roi[1], 0, 0, cv.BORDER_CONSTANT, value=(0, 0, 0))
                return True
        else:
            logger.error("get one new_data fail, ret[0x%x]" % ret)
            return False
            # return True

    def get_img(self) -> tuple[bool, np.ndarray]:
        if self.init_ok:
            result = self.work_thread()
            return result, self.__img
        else:
            # logger.error("init is failed dangerous!!!")
            return False, self.__img

    def destroy(self) -> None:
        # ch:停止取流 | en:Stop grab image
        try:
            ret = self.cam.MV_CC_StopGrabbing()
            if ret != 0:
                logger.error("stop grabbing fail! ret[0x%x]" % ret)

            # ch:关闭设备 | Close device
            ret = self.cam.MV_CC_CloseDevice()
            if ret != 0:
                logger.error("close deivce fail! ret[0x%x]" % ret)

            # ch:销毁句柄 | Destroy handle
            ret = self.cam.MV_CC_DestroyHandle()
            if ret != 0:
                logger.error("destroy handle fail! ret[0x%x]" % ret)
        except Exception:
            logger.exception("关闭相机时出现错误")
        self.init_ok = False

    def __del__(self):
        """
        保底销毁，防止程序意外退出时未释放相机资源
        """
        if self.init_ok:
            self.destroy()


if __name__ == "__main__":
    import time

    cv.namedWindow("test", cv.WINDOW_NORMAL)

    cam_test_config = HikCameraDriverConfigExt(
        roi=(0, 0, 3072, 2048),
        # camera_id="J87631625",  # 调整为要测试的相机的 ID
        # camera_id="J37877236",  # 调整为要测试的相机的 ID
        camera_id="00J59583857",  # 调整为要测试的相机的 ID
        exposure=15000,
        gain=20,
    )
    cam_test = Camera_HK(cam_test_config)
    t1 = time.time()
    count_fps = 0
    count_s = 0
    count_max = 35
    while True:
        if cam_test.init_ok:
            t2 = time.time()
            res, frame = cam_test.get_img()
            count_fps += 1
            frame_show = cv.resize(frame, (1024, 682))
            cv.imshow("test", frame_show)
            key = cv.waitKey(1)
            if t2 - t1 >= 8:
                fps = count_fps / (t2 - t1)
                count_fps = 0
                t1 = time.time()
                logger.info(f"fps {fps}")
            if key == ord('q') or not res or count_s >= count_max:
                cam_test.destroy()
                break
            if key == ord('s'):
                path = f"../resources/cam_data/{cam_test_config.camera_id}/{count_s}.jpg"
                cv.imwrite(path, frame)
                logger.info(path)
                count_s += 1
        else:
            break
    cv.destroyAllWindows()
