ctypedef enum MvError:
    MV_OK = 0x00000000  # 成功，无错误 Successed, no error

    # 通用错误码定义:范围0x80000000-0x800000FF
    # Definition of General error code
    MV_E_HANDLE = 0x80000000  # 错误或无效的句柄 Error or invalid handle
    MV_E_SUPPORT = 0x80000001  # 不支持的功能 Not supported function
    MV_E_BUFOVER = 0x80000002  # 缓存已满 Buffer overflow
    MV_E_CALLORDER = 0x80000003  # 函数调用顺序错误 Function calling order error
    MV_E_PARAMETER = 0x80000004  # 错误的参数 Incorrect parameter
    MV_E_RESOURCE = 0x80000006  # 资源申请失败 Applying resources failed
    MV_E_NODATA = 0x80000007  # 无数据 No data
    MV_E_PRECONDITION = 0x80000008  # 前置条件有误，或运行环境已发生变化 Precondition error, or running environment changed
    MV_E_VERSION = 0x80000009  # 版本不匹配 Version mismatches
    MV_E_NOENOUGH_BUF = 0x8000000A  # 传入的内存空间不足 Insufficient memory
    MV_E_ABNORMAL_IMAGE = 0x8000000B  # 异常图像，可能是丢包导致图像不完整 Abnormal image, maybe incomplete image because of lost packet
    MV_E_LOAD_LIBRARY = 0x8000000C  # 动态导入DLL失败 Load library failed
    MV_E_NOOUTBUF = 0x8000000D  # 没有可输出的缓存 No Available Buffer
    MV_E_UNKNOW = 0x800000FF  # 未知的错误 Unknown error

    # GenICam系列错误:范围0x80000100-0x800001FF
    # GenICam Series Error Codes: Range from 0x80000100 to 0x800001FF
    MV_E_GC_GENERIC = 0x80000100  # 通用错误 General error
    MV_E_GC_ARGUMENT = 0x80000101  # 参数非法 Illegal parameters
    MV_E_GC_RANGE = 0x80000102  # 值超出范围 The value is out of range
    MV_E_GC_PROPERTY = 0x80000103  # 属性 Property
    MV_E_GC_RUNTIME = 0x80000104  # 运行环境有问题 Running environment error
    MV_E_GC_LOGICAL = 0x80000105  # 逻辑错误 Logical error
    MV_E_GC_ACCESS = 0x80000106  # 节点访问条件有误 Node accessing condition error
    MV_E_GC_TIMEOUT = 0x80000107  # 超时 Timeout
    MV_E_GC_DYNAMICCAST = 0x80000108  # 转换异常 Transformation exception
    MV_E_GC_UNKNOW = 0x800001FF  # GenICam未知错误 GenICam unknown error

    # GigE_STATUS对应的错误码:范围0x80000200-0x800002FF
    # GigE_STATUS Error Codes: Range from 0x80000200 to 0x800002FF
    MV_E_NOT_IMPLEMENTED = 0x80000200  # 命令不被设备支持 The command is not supported by device
    MV_E_INVALID_ADDRESS = 0x80000201  # 访问的目标地址不存在 The target address being accessed does not exist
    MV_E_WRITE_PROTECT = 0x80000202  # 目标地址不可写 The target address is not writable
    MV_E_ACCESS_DENIED = 0x80000203  # 设备无访问权限 No permission
    MV_E_BUSY = 0x80000204  # 设备忙，或网络断开 Device is busy, or network disconnected
    MV_E_PACKET = 0x80000205  # 网络包数据错误 Network data packet error
    MV_E_NETER = 0x80000206  # 网络相关错误 Network error
    MV_E_IP_CONFLICT = 0x80000221  # 设备IP冲突 Device IP conflict

    # USB_STATUS对应的错误码:范围0x80000300-0x800003FF
    # USB_STATUS Error Codes: Range from 0x80000300 to 0x800003FF
    MV_E_USB_READ = 0x80000300  # 读usb出错 Reading USB error
    MV_E_USB_WRITE = 0x80000301  # 写usb出错 Writing USB error
    MV_E_USB_DEVICE = 0x80000302  # 设备异常 Device exception
    MV_E_USB_GENICAM = 0x80000303  # GenICam相关错误 GenICam error
    MV_E_USB_BANDWIDTH = 0x80000304  # 带宽不足  该错误码新增 Insufficient bandwidth, this error code is newly added
    MV_E_USB_DRIVER = 0x80000305  # 驱动不匹配或者未装驱动 Driver mismatch or unmounted drive
    MV_E_USB_UNKNOW = 0x800003FF  # USB未知的错误 USB unknown error

    # 升级时对应的错误码:范围0x80000400-0x800004FF
    # Upgrade Error Codes: Range from 0x80000400 to 0x800004FF
    MV_E_UPG_FILE_MISMATCH = 0x80000400  # 升级固件不匹配 Firmware mismatches
    MV_E_UPG_LANGUSGE_MISMATCH = 0x80000401  # 升级固件语言不匹配 Firmware language mismatches
    MV_E_UPG_CONFLICT = 0x80000402  # 升级冲突（设备已经在升级了再次请求升级即返回此错误） Upgrading conflicted (repeated upgrading requests during device upgrade)
    MV_E_UPG_INNER_ERR = 0x80000403  # 升级时相机内部出现错误 Camera internal error during upgrade
    MV_E_UPG_UNKNOW = 0x800004FF  # 升级时未知错误 Unknown error during upgrade
