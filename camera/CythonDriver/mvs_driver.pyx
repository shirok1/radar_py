import numpy as np
cimport numpy as np
from MvCameraControl cimport *
from MvErrorDefine cimport *

cdef class DeviceInfo:
    cdef MV_CC_DEVICE_INFO ffi_info
    @property
    def major_ver(self):
        return self.ffi_info.nMajorVer
    @property
    def minor_ver(self):
        return self.ffi_info.nMinorVer
    @property
    def mac_addr_high(self):
        return self.ffi_info.nMacAddrHigh
    @property
    def mac_addr_low(self):
        return self.ffi_info.nMacAddrLow
    @property
    def transport_layer(self):
        return self.ffi_info.nTLayerType
    @property
    def special_info(self):
        if self.ffi_info.nTLayerType == 1:
            return self.ffi_info.SpecialInfo.stGigEInfo
        elif self.ffi_info.nTLayerType == 4:
            return self.ffi_info.SpecialInfo.stUsb3VInfo
        elif self.ffi_info.nTLayerType == 8:
            return self.ffi_info.SpecialInfo.stCamLInfo
        else:
            return None
    @staticmethod
    cdef DeviceInfo from_ffi(MV_CC_DEVICE_INFO info):
        cdef DeviceInfo self = DeviceInfo.__new__(DeviceInfo)
        self.ffi_info = info
        return self

    def create_handle(self):
        cdef:
            unsigned int errno
            void * ffi_handle
        errno = MV_CC_CreateHandle(&ffi_handle, &self.ffi_info)
        check_error(errno, "MV_CC_CreateHandle")
        return Handle.from_ffi(ffi_handle)

cdef class Handle:
    cdef:
        void * ffi_handle
        Device device
        bool destroyed

    def __init__(self):
        self.device = None
        self.destroyed = False

    @staticmethod
    cdef Handle from_ffi(void * handle):
        cdef Handle self = Handle.__new__(Handle)
        self.ffi_handle = handle
        return self

    def destroy(self):
        if self.device is not None:
            self.device.close()
        cdef unsigned int errno
        errno = MV_CC_DestroyHandle(self.ffi_handle)
        check_error(errno, "MV_CC_DestroyHandle")
        self.destroyed = True

    # def open_device_scope(self, access_mode=1, switchover_key=0):
    #     return DeviceScope(self, access_mode, switchover_key)

    def open_device(self, access_mode=1, switchover_key=0):
        if self.device is not None:
            raise RuntimeError("Device already opened, check your code")
        self.device = Device(self, access_mode, switchover_key)
        return self.device

    def __del__(self):
        # TODO: warn that destroy should be manually called
        if not self.destroyed:
            self.destroy()
    pass

cdef class Device:
    cdef:
        Handle handle
        bool closed

    def __init__(self, handle: Handle, access_mode, switchover_key):
        self.handle = handle
        cdef unsigned int errno
        errno = MV_CC_OpenDevice(self.handle.ffi_handle, access_mode, switchover_key)
        check_error(errno, "MV_CC_OpenDevice")
        self.closed = False
    def close(self):
        cdef unsigned int errno
        errno = MV_CC_CloseDevice(self.handle.ffi_handle)
        check_error(errno, "MV_CC_CloseDevice")
        self.closed = True
        self.handle.device = None
    def __del__(self):
        # TODO: warn that close should be manually called
        if not self.closed:
            self.close()

    def get_int_value(self, name):
        cdef:
            unsigned int errno
            MVCC_INTVALUE value
        errno = MV_CC_GetIntValue(self.handle.ffi_handle, name.encode(), &value)
        check_error(errno, "MV_CC_GetIntValue")
        return value.nCurValue
    def set_int_value(self, name, value):
        cdef unsigned int errno
        errno = MV_CC_SetIntValue(self.handle.ffi_handle, name.encode(), value)
        check_error(errno, "MV_CC_SetIntValue")
        return

    def get_float_value(self, name):
        cdef:
            unsigned int errno
            MVCC_FLOATVALUE value
        errno = MV_CC_GetFloatValue(self.handle.ffi_handle, name.encode(), &value)
        check_error(errno, "MV_CC_GetFloatValue")
        return value.fCurValue
    def set_float_value(self, name, value):
        cdef unsigned int errno
        errno = MV_CC_SetFloatValue(self.handle.ffi_handle, name.encode(), value)
        check_error(errno, "MV_CC_SetFloatValue")
        return

    def get_enum_value(self, name):
        cdef:
            unsigned int errno
            MVCC_ENUMVALUE value
        errno = MV_CC_GetEnumValue(self.handle.ffi_handle, name.encode(), &value)
        check_error(errno, "MV_CC_GetEnumValue")
        return value.nCurValue
    def set_enum_value(self, name, value):
        cdef unsigned int errno
        errno = MV_CC_SetEnumValue(self.handle.ffi_handle, name.encode(), value)
        check_error(errno, "MV_CC_SetEnumValue")
        return

    def start_grabbing(self):
        cdef unsigned int errno
        errno = MV_CC_StartGrabbing(self.handle.ffi_handle)
        check_error(errno, "MV_CC_StartGrabbing")
    def stop_grabbing(self):
        cdef unsigned int errno
        errno = MV_CC_StopGrabbing(self.handle.ffi_handle)
        check_error(errno, "MV_CC_StopGrabbing")

    # def get_image_for_bgr(self):
    #     cdef:
    #         unsigned char *pData,
    #         unsigned int nDataSize
    #         MV_FRAME_OUT_INFO_EX *pFrameInfo
    #         unsigned int errno
    #     errno = MV_CC_GetImageForBGR(self.handle.ffi_handle, &frame, 1000)
    #     check_error(errno, "MV_CC_GetOneFrameTimeout")
    #     return frame
    # def get_image_buffer(self, timeout_ms=1000):
    #     cdef:
    #         MV_FRAME_OUT frame_struct
    #         unsigned int errno
    #         np.ndarray[np.uint8_t, ndim=2] frame
    #     errno = MV_CC_GetImageBuffer(self.handle.ffi_handle, &frame_struct, timeout_ms)
    #     check_error(errno, "MV_CC_GetImageBuffer")
    #     shape = (frame_struct.stFrameInfo.nHeight, frame_struct.stFrameInfo.nWidth)
    #     frame = np.empty(shape, dtype=np.uint8)
    #     count = frame_struct.stFrameInfo.nHeight * frame_struct.stFrameInfo.nWidth
    #     frame[:] = np.frombuffer(frame_struct.pBufAddr, count=count, dtype=np.uint8).reshape(shape)
    #     # frame.buf
    #     # frame = np.ndarray((frame_struct.stFrameInfo.nHeight, frame_struct.stFrameInfo.nWidth, 3), dtype=np.uint8, buffer=frame_struct.pBufAddr)
    #     errno = MV_CC_FreeImageBuffer(self.handle.ffi_handle, &frame_struct)
    #     check_error(errno, "MV_CC_FreeImageBuffer")
    #     return frame
    def get_image_to_buffer(self, np.ndarray[np.uint8_t] frame, timeout_ms=100):
        cdef:
            MV_FRAME_OUT_INFO_EX frame_info
            unsigned int errno
        errno = MV_CC_GetOneFrameTimeout(self.handle.ffi_handle, <unsigned char *> frame.data, frame.size, &frame_info,
                                         timeout_ms)
        check_error(errno, "MV_CC_GetOneFrameTimeout")
        return frame

# cdef class DeviceScope:
#     cdef:
#         Handle handle
#         unsigned int access_mode
#         unsigned short switchover_key
#         Device device
#
#     def __init__(self, handle, access_mode=1, switchover_key=0):
#         self.handle = handle
#         self.access_mode = access_mode
#         self.switchover_key = switchover_key
#     def __enter__(self):
#         cdef unsigned int errno
#         self.device = Device(self.handle, self.access_mode, self.switchover_key)
#     def __exit__(self, exc_type, exc_value, traceback):
#         cdef unsigned int errno
#         del self.device

cdef check_error(errno: int, func_name: str):
    if errno != MV_OK:
        raise Exception(f"{func_name} failed: 0x{errno:02x}")

cdef void * current_handle
def get_sdk_version():
    return MV_CC_GetSDKVersion()
def get_sdk_version_str():
    raw = MV_CC_GetSDKVersion()
    main = raw >> 24
    sub = (raw >> 16) & 0xFF
    revision = (raw >> 8) & 0xFF
    test = raw & 0xFF
    return f"v{main}.{sub}.{revision}.{test}"
def enum_devices(t_layer_type=4):
    cdef MV_CC_DEVICE_INFO_LIST dev_list
    cdef unsigned int errno
    errno = MV_CC_EnumDevices(t_layer_type, &dev_list)
    check_error(errno, "MV_CC_EnumDevices")

    # Use [0] to deref
    return [
        DeviceInfo.from_ffi(dev_list.pDeviceInfo[i][0])
        for i in range(dev_list.nDeviceNum)
    ]

# def CreateHandleWithoutLog(self, stDevInfo):
# def RegisterImageCallBackEx(self, CallBackFun, pUser):
# def SetImageNodeNum(self, nNum):
# def SetEnumValueByString(self, strKey, sValue):
# def GetBoolValue(self, strKey, BoolValue):
# def SetBoolValue(self, strKey, bValue):
# def GetStringValue(self, strKey, StringValue):
# def SetStringValue(self, strKey, sValue):
# def SetCommandValue(self, strKey):
# def RegisterExceptionCallBack(self, ExceptionCallBackFun, pUser):
# def RegisterEventCallBackEx(self, pEventName, EventCallBackFun, pUser):
# def SaveImageEx2(self, stSaveParam):
# def ConvertPixelType(self, stConvertParam):
# def FeatureSave(self, pFileName):
# def FeatureLoad(self, pFileName):
# def FileAccessRead(self, stFileAccess):
# def FileAccessWrite(self, stFileAccess):
# def GetFileAccessProgress(self, stFileAccessProgress):
# def GetOptimalPacketSize(self):
