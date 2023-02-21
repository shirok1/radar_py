cdef extern from "MvCameraControl.h":
    enum DeviceType:
        MV_UNKNOW_DEVICE = 0x00000000  # 未知设备类型，保留意义 Unknown Device Type, Reserved
        MV_GIGE_DEVICE = 0x00000001  # GigE设备类型 GigE Device
        MV_1394_DEVICE = 0x00000002  # 1394-a/b 设备 1394-a/b Device
        MV_USB_DEVICE = 0x00000004  # USB 设备 USB Device
        MV_CAMERALINK_DEVICE = 0x00000008  # CamLink设备 CamLink Device

    enum MvGvspPixelType:
        PixelType_Gvsp_Undefined = -1
        PixelType_Gvsp_Mono1p = 16842807
        PixelType_Gvsp_Mono2p = 16908344
        PixelType_Gvsp_Mono4p = 17039417
        PixelType_Gvsp_Mono8 = 17301505
        PixelType_Gvsp_Mono8_Signed = 17301506
        PixelType_Gvsp_Mono10 = 17825795
        PixelType_Gvsp_Mono10_Packed = 17563652
        PixelType_Gvsp_Mono12 = 17825797
        PixelType_Gvsp_Mono12_Packed = 17563654
        PixelType_Gvsp_Mono14 = 17825829
        PixelType_Gvsp_Mono16 = 17825799
        PixelType_Gvsp_BayerGR8 = 17301512
        PixelType_Gvsp_BayerRG8 = 17301513
        PixelType_Gvsp_BayerGB8 = 17301514
        PixelType_Gvsp_BayerBG8 = 17301515
        PixelType_Gvsp_BayerGR10 = 17825804
        PixelType_Gvsp_BayerRG10 = 17825805
        PixelType_Gvsp_BayerGB10 = 17825806
        PixelType_Gvsp_BayerBG10 = 17825807
        PixelType_Gvsp_BayerGR12 = 17825808
        PixelType_Gvsp_BayerRG12 = 17825809
        PixelType_Gvsp_BayerGB12 = 17825810
        PixelType_Gvsp_BayerBG12 = 17825811
        PixelType_Gvsp_BayerGR10_Packed = 17563686
        PixelType_Gvsp_BayerRG10_Packed = 17563687
        PixelType_Gvsp_BayerGB10_Packed = 17563688
        PixelType_Gvsp_BayerBG10_Packed = 17563689
        PixelType_Gvsp_BayerGR12_Packed = 17563690
        PixelType_Gvsp_BayerRG12_Packed = 17563691
        PixelType_Gvsp_BayerGB12_Packed = 17563692
        PixelType_Gvsp_BayerBG12_Packed = 17563693
        PixelType_Gvsp_BayerGR16 = 17825838
        PixelType_Gvsp_BayerRG16 = 17825839
        PixelType_Gvsp_BayerGB16 = 17825840
        PixelType_Gvsp_BayerBG16 = 17825841
        PixelType_Gvsp_RGB8_Packed = 35127316
        PixelType_Gvsp_BGR8_Packed = 35127317
        PixelType_Gvsp_RGBA8_Packed = 35651606
        PixelType_Gvsp_BGRA8_Packed = 35651607
        PixelType_Gvsp_RGB10_Packed = 36700184
        PixelType_Gvsp_BGR10_Packed = 36700185
        PixelType_Gvsp_RGB12_Packed = 36700186
        PixelType_Gvsp_BGR12_Packed = 36700187
        PixelType_Gvsp_RGB16_Packed = 36700211
        PixelType_Gvsp_BGR16_Packed = 36700235
        PixelType_Gvsp_RGBA16_Packed = 37748836
        PixelType_Gvsp_BGRA16_Packed = 37748817
        PixelType_Gvsp_RGB10V1_Packed = 35651612
        PixelType_Gvsp_RGB10V2_Packed = 35651613
        PixelType_Gvsp_RGB12V1_Packed = 35913780
        PixelType_Gvsp_RGB565_Packed = 34603061
        PixelType_Gvsp_BGR565_Packed = 34603062
        PixelType_Gvsp_YUV411_Packed = 34340894
        PixelType_Gvsp_YUV422_Packed = 34603039
        PixelType_Gvsp_YUV422_YUYV_Packed = 34603058
        PixelType_Gvsp_YUV444_Packed = 35127328
        PixelType_Gvsp_YCBCR8_CBYCR = 35127354
        PixelType_Gvsp_YCBCR422_8 = 34603067
        PixelType_Gvsp_YCBCR422_8_CBYCRY = 34603075
        PixelType_Gvsp_YCBCR411_8_CBYYCRYY = 34340924
        PixelType_Gvsp_YCBCR601_8_CBYCR = 35127357
        PixelType_Gvsp_YCBCR601_422_8 = 34603070
        PixelType_Gvsp_YCBCR601_422_8_CBYCRY = 34603076
        PixelType_Gvsp_YCBCR601_411_8_CBYYCRYY = 34340927
        PixelType_Gvsp_YCBCR709_8_CBYCR = 35127360
        PixelType_Gvsp_YCBCR709_422_8 = 34603073
        PixelType_Gvsp_YCBCR709_422_8_CBYCRY = 34603077
        PixelType_Gvsp_YCBCR709_411_8_CBYYCRYY = 34340930
        PixelType_Gvsp_RGB8_Planar = 35127329
        PixelType_Gvsp_RGB10_Planar = 36700194
        PixelType_Gvsp_RGB12_Planar = 36700195
        PixelType_Gvsp_RGB16_Planar = 36700196
        PixelType_Gvsp_Jpeg = 2149056513
        PixelType_Gvsp_Coord3D_ABC32f = 39846080
        PixelType_Gvsp_Coord3D_ABC32f_Planar = 39846081
        PixelType_Gvsp_Coord3D_AC32f = 36176066
        PixelType_Gvsp_COORD3D_DEPTH_PLUS_MASK = 2182873089
        PixelType_Gvsp_Coord3D_ABC32 = 2187341825
        PixelType_Gvsp_Coord3D_AB32f = 2185244674
        PixelType_Gvsp_Coord3D_AB32 = 2185244675
        PixelType_Gvsp_Coord3D_AC32f_64 = 37748930
        PixelType_Gvsp_Coord3D_AC32f_Planar = 37748931
        PixelType_Gvsp_Coord3D_AC32 = 2185244676
        PixelType_Gvsp_Coord3D_A32f = 18874557
        PixelType_Gvsp_Coord3D_A32 = 2166370309
        PixelType_Gvsp_Coord3D_C32f = 18874559
        PixelType_Gvsp_Coord3D_C32 = 2166370310
        PixelType_Gvsp_Coord3D_ABC16 = 36700345
        PixelType_Gvsp_Coord3D_C16 = 17825976
        PixelType_Gvsp_HB_Mono8 = 2164785153
        PixelType_Gvsp_HB_Mono10 = 2165309443
        PixelType_Gvsp_HB_Mono10_Packed = 2165047300
        PixelType_Gvsp_HB_Mono12 = 2165309445
        PixelType_Gvsp_HB_Mono12_Packed = 2165047302
        PixelType_Gvsp_HB_Mono16 = 2165309447
        PixelType_Gvsp_HB_BayerGR8 = 2164785160
        PixelType_Gvsp_HB_BayerRG8 = 2164785161
        PixelType_Gvsp_HB_BayerGB8 = 2164785162
        PixelType_Gvsp_HB_BayerBG8 = 2164785163
        PixelType_Gvsp_HB_BayerRBGG8 = 2164785222
        PixelType_Gvsp_HB_BayerGR10 = 2165309452
        PixelType_Gvsp_HB_BayerRG10 = 2165309453
        PixelType_Gvsp_HB_BayerGB10 = 2165309454
        PixelType_Gvsp_HB_BayerBG10 = 2165309455
        PixelType_Gvsp_HB_BayerGR12 = 2165309456
        PixelType_Gvsp_HB_BayerRG12 = 2165309457
        PixelType_Gvsp_HB_BayerGB12 = 2165309458
        PixelType_Gvsp_HB_BayerBG12 = 2165309459
        PixelType_Gvsp_HB_BayerGR10_Packed = 2165047334
        PixelType_Gvsp_HB_BayerRG10_Packed = 2165047335
        PixelType_Gvsp_HB_BayerGB10_Packed = 2165047336
        PixelType_Gvsp_HB_BayerBG10_Packed = 2165047337
        PixelType_Gvsp_HB_BayerGR12_Packed = 2165047338
        PixelType_Gvsp_HB_BayerRG12_Packed = 2165047339
        PixelType_Gvsp_HB_BayerGB12_Packed = 2165047340
        PixelType_Gvsp_HB_BayerBG12_Packed = 2165047341
        PixelType_Gvsp_HB_YUV422_Packed = 2182086687
        PixelType_Gvsp_HB_YUV422_YUYV_Packed = 2182086706
        PixelType_Gvsp_HB_RGB8_Packed = 2182610964
        PixelType_Gvsp_HB_BGR8_Packed = 2182610965
        PixelType_Gvsp_HB_RGBA8_Packed = 2183135254
        PixelType_Gvsp_HB_BGRA8_Packed = 2183135255
        PixelType_Gvsp_HB_RGB16_Packed = 2184183859
        PixelType_Gvsp_HB_BGR16_Packed = 2184183883
        PixelType_Gvsp_HB_RGBA16_Packed = 2185232484
        PixelType_Gvsp_HB_BGRA16_Packed = 2185232465
    ctypedef unsigned char __u_char
    ctypedef unsigned short __u_short
    ctypedef unsigned int __u_int
    ctypedef unsigned long __u_long
    ctypedef signed char __int8_t
    ctypedef unsigned char __uint8_t
    ctypedef short __int16_t
    ctypedef unsigned short __uint16_t
    ctypedef int __int32_t
    ctypedef unsigned int __uint32_t
    ctypedef long __int64_t
    ctypedef unsigned long __uint64_t
    ctypedef __int8_t __int_least8_t
    ctypedef __uint8_t __uint_least8_t
    ctypedef __int16_t __int_least16_t
    ctypedef __uint16_t __uint_least16_t
    ctypedef __int32_t __int_least32_t
    ctypedef __uint32_t __uint_least32_t
    ctypedef __int64_t __int_least64_t
    ctypedef __uint64_t __uint_least64_t
    ctypedef long __quad_t
    ctypedef unsigned long __u_quad_t
    ctypedef long __intmax_t
    ctypedef unsigned long __uintmax_t
    ctypedef unsigned long __dev_t
    ctypedef unsigned int __uid_t
    ctypedef unsigned int __gid_t
    ctypedef unsigned long __ino_t
    ctypedef unsigned long __ino64_t
    ctypedef unsigned int __mode_t
    ctypedef unsigned long __nlink_t
    ctypedef long __off_t
    ctypedef long __off64_t
    ctypedef int __pid_t
    ctypedef struct __fsid_t:
        int __val[2]
    ctypedef long __clock_t
    ctypedef unsigned long __rlim_t
    ctypedef unsigned long __rlim64_t
    ctypedef unsigned int __id_t
    ctypedef long __time_t
    ctypedef unsigned int __useconds_t
    ctypedef long __suseconds_t
    ctypedef long __suseconds64_t
    ctypedef int __daddr_t
    ctypedef int __key_t
    ctypedef int __clockid_t
    ctypedef void * __timer_t
    ctypedef long __blksize_t
    ctypedef long __blkcnt_t
    ctypedef long __blkcnt64_t
    ctypedef unsigned long __fsblkcnt_t
    ctypedef unsigned long __fsblkcnt64_t
    ctypedef unsigned long __fsfilcnt_t
    ctypedef unsigned long __fsfilcnt64_t
    ctypedef long __fsword_t
    ctypedef long __ssize_t
    ctypedef long __syscall_slong_t
    ctypedef unsigned long __syscall_ulong_t
    ctypedef __off64_t __loff_t
    ctypedef char * __caddr_t
    ctypedef long __intptr_t
    ctypedef unsigned int __socklen_t
    ctypedef int __sig_atomic_t
    ctypedef __int8_t int8_t
    ctypedef __int16_t int16_t
    ctypedef __int32_t int32_t
    ctypedef __int64_t int64_t
    ctypedef __uint8_t uint8_t
    ctypedef __uint16_t uint16_t
    ctypedef __uint32_t uint32_t
    ctypedef __uint64_t uint64_t
    ctypedef __int_least8_t int_least8_t
    ctypedef __int_least16_t int_least16_t
    ctypedef __int_least32_t int_least32_t
    ctypedef __int_least64_t int_least64_t
    ctypedef __uint_least8_t uint_least8_t
    ctypedef __uint_least16_t uint_least16_t
    ctypedef __uint_least32_t uint_least32_t
    ctypedef __uint_least64_t uint_least64_t
    ctypedef signed char int_fast8_t
    ctypedef long int_fast16_t
    ctypedef long int_fast32_t
    ctypedef long int_fast64_t
    ctypedef unsigned char uint_fast8_t
    ctypedef unsigned long uint_fast16_t
    ctypedef unsigned long uint_fast32_t
    ctypedef unsigned long uint_fast64_t
    ctypedef long intptr_t
    ctypedef unsigned long uintptr_t
    ctypedef __intmax_t intmax_t
    ctypedef __uintmax_t uintmax_t
    ctypedef char bool
    struct _MV_GIGE_DEVICE_INFO_:
        unsigned int nIpCfgOption
        unsigned int nIpCfgCurrent
        unsigned int nCurrentIp
        unsigned int nCurrentSubNetMask
        unsigned int nDefultGateWay
        unsigned char chManufacturerName[32]
        unsigned char chModelName[32]
        unsigned char chDeviceVersion[32]
        unsigned char chManufacturerSpecificInfo[48]
        unsigned char chSerialNumber[16]
        unsigned char chUserDefinedName[16]
        unsigned int nNetExport
        unsigned int nReserved[4]
    ctypedef _MV_GIGE_DEVICE_INFO_ MV_GIGE_DEVICE_INFO
    struct _MV_USB3_DEVICE_INFO_:
        unsigned char CrtlInEndPoint
        unsigned char CrtlOutEndPoint
        unsigned char StreamEndPoint
        unsigned char EventEndPoint
        unsigned short idVendor
        unsigned short idProduct
        unsigned int nDeviceNumber
        unsigned char chDeviceGUID[64]
        unsigned char chVendorName[64]
        unsigned char chModelName[64]
        unsigned char chFamilyName[64]
        unsigned char chDeviceVersion[64]
        unsigned char chManufacturerName[64]
        unsigned char chSerialNumber[64]
        unsigned char chUserDefinedName[64]
        unsigned int nbcdUSB
        unsigned int nReserved[3]
    ctypedef _MV_USB3_DEVICE_INFO_ MV_USB3_DEVICE_INFO
    struct _MV_CamL_DEV_INFO_:
        unsigned char chPortID[64]
        unsigned char chModelName[64]
        unsigned char chFamilyName[64]
        unsigned char chDeviceVersion[64]
        unsigned char chManufacturerName[64]
        unsigned char chSerialNumber[64]
        unsigned int nReserved[38]
    ctypedef _MV_CamL_DEV_INFO_ MV_CamL_DEV_INFO
    union pxdgen_anon__MV_CC_DEVICE_INFO__0:
        MV_GIGE_DEVICE_INFO stGigEInfo
        MV_USB3_DEVICE_INFO stUsb3VInfo
        MV_CamL_DEV_INFO stCamLInfo
    struct _MV_CC_DEVICE_INFO_:
        unsigned short nMajorVer
        unsigned short nMinorVer
        unsigned int nMacAddrHigh
        unsigned int nMacAddrLow
        unsigned int nTLayerType
        unsigned int nReserved[4]
        pxdgen_anon__MV_CC_DEVICE_INFO__0 SpecialInfo
    ctypedef _MV_CC_DEVICE_INFO_ MV_CC_DEVICE_INFO
    struct _MV_NETTRANS_INFO_:
        int64_t nReviceDataSize
        int nThrowFrameCount
        unsigned int nNetRecvFrameCount
        int64_t nRequestResendPacketCount
        int64_t nResendPacketCount
    ctypedef _MV_NETTRANS_INFO_ MV_NETTRANS_INFO
    struct _MV_CC_DEVICE_INFO_LIST_:
        unsigned int nDeviceNum
        MV_CC_DEVICE_INFO * pDeviceInfo[256]
    ctypedef _MV_CC_DEVICE_INFO_LIST_ MV_CC_DEVICE_INFO_LIST
    struct _MV_CHUNK_DATA_CONTENT_:
        unsigned char * pChunkData
        unsigned int nChunkID
        unsigned int nChunkLen
        unsigned int nReserved[8]
    ctypedef _MV_CHUNK_DATA_CONTENT_ MV_CHUNK_DATA_CONTENT
    struct _MV_FRAME_OUT_INFO_:
        unsigned short nWidth
        unsigned short nHeight
        MvGvspPixelType enPixelType
        unsigned int nFrameNum
        unsigned int nDevTimeStampHigh
        unsigned int nDevTimeStampLow
        unsigned int nReserved0
        int64_t nHostTimeStamp
        unsigned int nFrameLen
        unsigned int nLostPacket
        unsigned int nReserved[2]
    ctypedef _MV_FRAME_OUT_INFO_ MV_FRAME_OUT_INFO
    union pxdgen_anon__MV_FRAME_OUT_INFO_EX__0:
        MV_CHUNK_DATA_CONTENT * pUnparsedChunkContent
        int64_t nAligning
    struct _MV_FRAME_OUT_INFO_EX_:
        unsigned short nWidth
        unsigned short nHeight
        MvGvspPixelType enPixelType
        unsigned int nFrameNum
        unsigned int nDevTimeStampHigh
        unsigned int nDevTimeStampLow
        unsigned int nReserved0
        int64_t nHostTimeStamp
        unsigned int nFrameLen
        unsigned int nSecondCount
        unsigned int nCycleCount
        unsigned int nCycleOffset
        float fGain
        float fExposureTime
        unsigned int nAverageBrightness
        unsigned int nRed
        unsigned int nGreen
        unsigned int nBlue
        unsigned int nFrameCounter
        unsigned int nTriggerIndex
        unsigned int nInput
        unsigned int nOutput
        unsigned short nOffsetX
        unsigned short nOffsetY
        unsigned short nChunkWidth
        unsigned short nChunkHeight
        unsigned int nLostPacket
        unsigned int nUnparsedChunkNum
        pxdgen_anon__MV_FRAME_OUT_INFO_EX__0 UnparsedChunkList
        unsigned int nReserved[36]
    ctypedef _MV_FRAME_OUT_INFO_EX_ MV_FRAME_OUT_INFO_EX
    struct _MV_FRAME_OUT_:
        unsigned char * pBufAddr
        MV_FRAME_OUT_INFO_EX stFrameInfo
        unsigned int nRes[16]
    ctypedef _MV_FRAME_OUT_ MV_FRAME_OUT
    struct _MV_DISPLAY_FRAME_INFO_:
        void * hWnd
        unsigned char * pData
        unsigned int nDataLen
        unsigned short nWidth
        unsigned short nHeight
        MvGvspPixelType enPixelType
        unsigned int nRes[4]
    ctypedef _MV_DISPLAY_FRAME_INFO_ MV_DISPLAY_FRAME_INFO
    enum MV_SAVE_IAMGE_TYPE:
        MV_Image_Undefined = 0
        MV_Image_Bmp = 1
        MV_Image_Jpeg = 2
        MV_Image_Png = 3
        MV_Image_Tif = 4
    struct _MV_SAVE_IMAGE_PARAM_T_:
        unsigned char * pData
        unsigned int nDataLen
        MvGvspPixelType enPixelType
        unsigned short nWidth
        unsigned short nHeight
        unsigned char * pImageBuffer
        unsigned int nImageLen
        unsigned int nBufferSize
        MV_SAVE_IAMGE_TYPE enImageType
    ctypedef _MV_SAVE_IMAGE_PARAM_T_ MV_SAVE_IMAGE_PARAM
    struct _MV_SAVE_IMAGE_PARAM_T_EX_:
        unsigned char * pData
        unsigned int nDataLen
        MvGvspPixelType enPixelType
        unsigned short nWidth
        unsigned short nHeight
        unsigned char * pImageBuffer
        unsigned int nImageLen
        unsigned int nBufferSize
        MV_SAVE_IAMGE_TYPE enImageType
        unsigned int nJpgQuality
        unsigned int iMethodValue
        unsigned int nReserved[3]
    ctypedef _MV_SAVE_IMAGE_PARAM_T_EX_ MV_SAVE_IMAGE_PARAM_EX
    enum _MV_IMG_ROTATION_ANGLE_:
        MV_IMAGE_ROTATE_90 = 1
        MV_IMAGE_ROTATE_180 = 2
        MV_IMAGE_ROTATE_270 = 3
    ctypedef _MV_IMG_ROTATION_ANGLE_ MV_IMG_ROTATION_ANGLE
    struct _MV_CC_ROTATE_IMAGE_PARAM_T_:
        MvGvspPixelType enPixelType
        unsigned int nWidth
        unsigned int nHeight
        unsigned char * pSrcData
        unsigned int nSrcDataLen
        unsigned char * pDstBuf
        unsigned int nDstBufLen
        unsigned int nDstBufSize
        MV_IMG_ROTATION_ANGLE enRotationAngle
        unsigned int nRes[8]
    ctypedef _MV_CC_ROTATE_IMAGE_PARAM_T_ MV_CC_ROTATE_IMAGE_PARAM
    enum _MV_IMG_FLIP_TYPE_:
        MV_FLIP_VERTICAL = 1
        MV_FLIP_HORIZONTAL = 2
    ctypedef _MV_IMG_FLIP_TYPE_ MV_IMG_FLIP_TYPE
    struct _MV_CC_FLIP_IMAGE_PARAM_T_:
        MvGvspPixelType enPixelType
        unsigned int nWidth
        unsigned int nHeight
        unsigned char * pSrcData
        unsigned int nSrcDataLen
        unsigned char * pDstBuf
        unsigned int nDstBufLen
        unsigned int nDstBufSize
        MV_IMG_FLIP_TYPE enFlipType
        unsigned int nRes[8]
    ctypedef _MV_CC_FLIP_IMAGE_PARAM_T_ MV_CC_FLIP_IMAGE_PARAM
    struct _MV_PIXEL_CONVERT_PARAM_T_:
        unsigned short nWidth
        unsigned short nHeight
        MvGvspPixelType enSrcPixelType
        unsigned char * pSrcData
        unsigned int nSrcDataLen
        MvGvspPixelType enDstPixelType
        unsigned char * pDstBuffer
        unsigned int nDstLen
        unsigned int nDstBufferSize
        unsigned int nRes[4]
    ctypedef _MV_PIXEL_CONVERT_PARAM_T_ MV_CC_PIXEL_CONVERT_PARAM
    enum _MV_CC_GAMMA_TYPE_:
        MV_CC_GAMMA_TYPE_NONE = 0
        MV_CC_GAMMA_TYPE_VALUE = 1
        MV_CC_GAMMA_TYPE_USER_CURVE = 2
        MV_CC_GAMMA_TYPE_LRGB2SRGB = 3
        MV_CC_GAMMA_TYPE_SRGB2LRGB = 4
    ctypedef _MV_CC_GAMMA_TYPE_ MV_CC_GAMMA_TYPE
    struct _MV_CC_GAMMA_PARAM_T_:
        MV_CC_GAMMA_TYPE enGammaType
        float fGammaValue
        unsigned char * pGammaCurveBuf
        unsigned int nGammaCurveBufLen
        unsigned int nRes[8]
    ctypedef _MV_CC_GAMMA_PARAM_T_ MV_CC_GAMMA_PARAM
    struct _MV_CC_FRAME_SPEC_INFO_:
        unsigned int nSecondCount
        unsigned int nCycleCount
        unsigned int nCycleOffset
        float fGain
        float fExposureTime
        unsigned int nAverageBrightness
        unsigned int nRed
        unsigned int nGreen
        unsigned int nBlue
        unsigned int nFrameCounter
        unsigned int nTriggerIndex
        unsigned int nInput
        unsigned int nOutput
        unsigned short nOffsetX
        unsigned short nOffsetY
        unsigned short nFrameWidth
        unsigned short nFrameHeight
        unsigned int nReserved[16]
    ctypedef _MV_CC_FRAME_SPEC_INFO_ MV_CC_FRAME_SPEC_INFO
    struct _MV_CC_HB_DECODE_PARAM_T_:
        unsigned char * pSrcBuf
        unsigned int nSrcLen
        unsigned int nWidth
        unsigned int nHeight
        unsigned char * pDstBuf
        unsigned int nDstBufSize
        unsigned int nDstBufLen
        MvGvspPixelType enDstPixelType
        MV_CC_FRAME_SPEC_INFO stFrameSpecInfo
        unsigned int nRes[8]
    ctypedef _MV_CC_HB_DECODE_PARAM_T_ MV_CC_HB_DECODE_PARAM
    enum _MV_RECORD_FORMAT_TYPE_:
        MV_FormatType_Undefined = 0
        MV_FormatType_AVI = 1
    ctypedef _MV_RECORD_FORMAT_TYPE_ MV_RECORD_FORMAT_TYPE
    struct _MV_CC_RECORD_PARAM_T_:
        MvGvspPixelType enPixelType
        unsigned short nWidth
        unsigned short nHeight
        float fFrameRate
        unsigned int nBitRate
        MV_RECORD_FORMAT_TYPE enRecordFmtType
        char * strFilePath
        unsigned int nRes[8]
    ctypedef _MV_CC_RECORD_PARAM_T_ MV_CC_RECORD_PARAM
    struct _MV_CC_INPUT_FRAME_INFO_T_:
        unsigned char * pData
        unsigned int nDataLen
        unsigned int nRes[8]
    ctypedef _MV_CC_INPUT_FRAME_INFO_T_ MV_CC_INPUT_FRAME_INFO
    enum _MV_CAM_ACQUISITION_MODE_:
        MV_ACQ_MODE_SINGLE = 0
        MV_ACQ_MODE_MUTLI = 1
        MV_ACQ_MODE_CONTINUOUS = 2
    ctypedef _MV_CAM_ACQUISITION_MODE_ MV_CAM_ACQUISITION_MODE
    enum _MV_CAM_GAIN_MODE_:
        MV_GAIN_MODE_OFF = 0
        MV_GAIN_MODE_ONCE = 1
        MV_GAIN_MODE_CONTINUOUS = 2
    ctypedef _MV_CAM_GAIN_MODE_ MV_CAM_GAIN_MODE
    enum _MV_CAM_EXPOSURE_MODE_:
        MV_EXPOSURE_MODE_TIMED = 0
        MV_EXPOSURE_MODE_TRIGGER_WIDTH = 1
    ctypedef _MV_CAM_EXPOSURE_MODE_ MV_CAM_EXPOSURE_MODE
    enum _MV_CAM_EXPOSURE_AUTO_MODE_:
        MV_EXPOSURE_AUTO_MODE_OFF = 0
        MV_EXPOSURE_AUTO_MODE_ONCE = 1
        MV_EXPOSURE_AUTO_MODE_CONTINUOUS = 2
    ctypedef _MV_CAM_EXPOSURE_AUTO_MODE_ MV_CAM_EXPOSURE_AUTO_MODE
    enum _MV_CAM_TRIGGER_MODE_:
        MV_TRIGGER_MODE_OFF = 0
        MV_TRIGGER_MODE_ON = 1
    ctypedef _MV_CAM_TRIGGER_MODE_ MV_CAM_TRIGGER_MODE
    enum _MV_CAM_GAMMA_SELECTOR_:
        MV_GAMMA_SELECTOR_USER = 1
        MV_GAMMA_SELECTOR_SRGB = 2
    ctypedef _MV_CAM_GAMMA_SELECTOR_ MV_CAM_GAMMA_SELECTOR
    enum _MV_CAM_BALANCEWHITE_AUTO_:
        MV_BALANCEWHITE_AUTO_OFF = 0
        MV_BALANCEWHITE_AUTO_ONCE = 2
        MV_BALANCEWHITE_AUTO_CONTINUOUS = 1
    ctypedef _MV_CAM_BALANCEWHITE_AUTO_ MV_CAM_BALANCEWHITE_AUTO
    enum _MV_CAM_TRIGGER_SOURCE_:
        MV_TRIGGER_SOURCE_LINE0 = 0
        MV_TRIGGER_SOURCE_LINE1 = 1
        MV_TRIGGER_SOURCE_LINE2 = 2
        MV_TRIGGER_SOURCE_LINE3 = 3
        MV_TRIGGER_SOURCE_COUNTER0 = 4
        MV_TRIGGER_SOURCE_SOFTWARE = 7
        MV_TRIGGER_SOURCE_FrequencyConverter = 8
    ctypedef _MV_CAM_TRIGGER_SOURCE_ MV_CAM_TRIGGER_SOURCE
    enum _MV_GIGE_TRANSMISSION_TYPE_:
        MV_GIGE_TRANSTYPE_UNICAST = 0
        MV_GIGE_TRANSTYPE_MULTICAST = 1
        MV_GIGE_TRANSTYPE_LIMITEDBROADCAST = 2
        MV_GIGE_TRANSTYPE_SUBNETBROADCAST = 3
        MV_GIGE_TRANSTYPE_CAMERADEFINED = 4
        MV_GIGE_TRANSTYPE_UNICAST_DEFINED_PORT = 5
        MV_GIGE_TRANSTYPE_UNICAST_WITHOUT_RECV = 65536
        MV_GIGE_TRANSTYPE_MULTICAST_WITHOUT_RECV = 65537
    ctypedef _MV_GIGE_TRANSMISSION_TYPE_ MV_GIGE_TRANSMISSION_TYPE
    struct _MV_ALL_MATCH_INFO_:
        unsigned int nType
        void * pInfo
        unsigned int nInfoSize
    ctypedef _MV_ALL_MATCH_INFO_ MV_ALL_MATCH_INFO
    struct _MV_MATCH_INFO_NET_DETECT_:
        int64_t nReviceDataSize
        int64_t nLostPacketCount
        unsigned int nLostFrameCount
        unsigned int nNetRecvFrameCount
        int64_t nRequestResendPacketCount
        int64_t nResendPacketCount
    ctypedef _MV_MATCH_INFO_NET_DETECT_ MV_MATCH_INFO_NET_DETECT
    struct _MV_MATCH_INFO_USB_DETECT_:
        int64_t nReviceDataSize
        unsigned int nRevicedFrameCount
        unsigned int nErrorFrameCount
        unsigned int nReserved[2]
    ctypedef _MV_MATCH_INFO_USB_DETECT_ MV_MATCH_INFO_USB_DETECT
    struct _MV_IMAGE_BASIC_INFO_:
        unsigned short nWidthValue
        unsigned short nWidthMin
        unsigned int nWidthMax
        unsigned int nWidthInc
        unsigned int nHeightValue
        unsigned int nHeightMin
        unsigned int nHeightMax
        unsigned int nHeightInc
        float fFrameRateValue
        float fFrameRateMin
        float fFrameRateMax
        unsigned int enPixelType
        unsigned int nSupportedPixelFmtNum
        unsigned int enPixelList[64]
        unsigned int nReserved[8]
    ctypedef _MV_IMAGE_BASIC_INFO_ MV_IMAGE_BASIC_INFO
    enum MV_XML_InterfaceType:
        IFT_IValue = 0
        IFT_IBase = 1
        IFT_IInteger = 2
        IFT_IBoolean = 3
        IFT_ICommand = 4
        IFT_IFloat = 5
        IFT_IString = 6
        IFT_IRegister = 7
        IFT_ICategory = 8
        IFT_IEnumeration = 9
        IFT_IEnumEntry = 10
        IFT_IPort = 11
    enum MV_XML_AccessMode:
        AM_NI = 0
        AM_NA = 1
        AM_WO = 2
        AM_RO = 3
        AM_RW = 4
        AM_Undefined = 5
        AM_CycleDetect = 6
    enum MV_XML_Visibility:
        V_Beginner = 0
        V_Expert = 1
        V_Guru = 2
        V_Invisible = 3
        V_Undefined = 99
    struct _MV_EVENT_OUT_INFO_:
        char EventName[128]
        unsigned short nEventID
        unsigned short nStreamChannel
        unsigned int nBlockIdHigh
        unsigned int nBlockIdLow
        unsigned int nTimestampHigh
        unsigned int nTimestampLow
        void * pEventData
        unsigned int nEventDataSize
        unsigned int nReserved[16]
    ctypedef _MV_EVENT_OUT_INFO_ MV_EVENT_OUT_INFO
    struct _MV_CC_FILE_ACCESS_T:
        const char * pUserFileName
        const char * pDevFileName
        unsigned int nReserved[32]
    ctypedef _MV_CC_FILE_ACCESS_T MV_CC_FILE_ACCESS
    struct _MV_CC_FILE_ACCESS_PROGRESS_T:
        int64_t nCompleted
        int64_t nTotal
        unsigned int nReserved[8]
    ctypedef _MV_CC_FILE_ACCESS_PROGRESS_T MV_CC_FILE_ACCESS_PROGRESS
    struct _MV_TRANSMISSION_TYPE_T:
        MV_GIGE_TRANSMISSION_TYPE enTransmissionType
        unsigned int nDestIp
        unsigned short nDestPort
        unsigned int nReserved[32]
    ctypedef _MV_TRANSMISSION_TYPE_T MV_TRANSMISSION_TYPE
    struct _MV_ACTION_CMD_INFO_T:
        unsigned int nDeviceKey
        unsigned int nGroupKey
        unsigned int nGroupMask
        unsigned int bActionTimeEnable
        int64_t nActionTime
        const char * pBroadcastAddress
        unsigned int nTimeOut
        unsigned int bSpecialNetEnable
        unsigned int nSpecialNetIP
        unsigned int nReserved[14]
    ctypedef _MV_ACTION_CMD_INFO_T MV_ACTION_CMD_INFO
    struct _MV_ACTION_CMD_RESULT_T:
        unsigned char strDeviceAddress[16]
        int nStatus
        unsigned int nReserved[4]
    ctypedef _MV_ACTION_CMD_RESULT_T MV_ACTION_CMD_RESULT
    struct _MV_ACTION_CMD_RESULT_LIST_T:
        unsigned int nNumResults
        MV_ACTION_CMD_RESULT * pResults
    ctypedef _MV_ACTION_CMD_RESULT_LIST_T MV_ACTION_CMD_RESULT_LIST
    struct _MV_XML_NODE_FEATURE_:
        MV_XML_InterfaceType enType
        MV_XML_Visibility enVisivility
        char strDescription[512]
        char strDisplayName[64]
        char strName[64]
        char strToolTip[512]
        unsigned int nReserved[4]
    ctypedef _MV_XML_NODE_FEATURE_ MV_XML_NODE_FEATURE
    struct _MV_XML_NODES_LIST_:
        unsigned int nNodeNum
        MV_XML_NODE_FEATURE stNodes[128]
    ctypedef _MV_XML_NODES_LIST_ MV_XML_NODES_LIST
    struct _MV_XML_FEATURE_Value_:
        MV_XML_InterfaceType enType
        char strDescription[512]
        char strDisplayName[64]
        char strName[64]
        char strToolTip[512]
        unsigned int nReserved[4]
    ctypedef _MV_XML_FEATURE_Value_ MV_XML_FEATURE_Value
    struct _MV_XML_FEATURE_Base_:
        MV_XML_AccessMode enAccessMode
    ctypedef _MV_XML_FEATURE_Base_ MV_XML_FEATURE_Base
    struct _MV_XML_FEATURE_Integer_:
        char strName[64]
        char strDisplayName[64]
        char strDescription[512]
        char strToolTip[512]
        MV_XML_Visibility enVisivility
        MV_XML_AccessMode enAccessMode
        int bIsLocked
        int64_t nValue
        int64_t nMinValue
        int64_t nMaxValue
        int64_t nIncrement
        unsigned int nReserved[4]
    ctypedef _MV_XML_FEATURE_Integer_ MV_XML_FEATURE_Integer
    struct _MV_XML_FEATURE_Boolean_:
        char strName[64]
        char strDisplayName[64]
        char strDescription[512]
        char strToolTip[512]
        MV_XML_Visibility enVisivility
        MV_XML_AccessMode enAccessMode
        int bIsLocked
        bint bValue
        unsigned int nReserved[4]
    ctypedef _MV_XML_FEATURE_Boolean_ MV_XML_FEATURE_Boolean
    struct _MV_XML_FEATURE_Command_:
        char strName[64]
        char strDisplayName[64]
        char strDescription[512]
        char strToolTip[512]
        MV_XML_Visibility enVisivility
        MV_XML_AccessMode enAccessMode
        int bIsLocked
        unsigned int nReserved[4]
    ctypedef _MV_XML_FEATURE_Command_ MV_XML_FEATURE_Command
    struct _MV_XML_FEATURE_Float_:
        char strName[64]
        char strDisplayName[64]
        char strDescription[512]
        char strToolTip[512]
        MV_XML_Visibility enVisivility
        MV_XML_AccessMode enAccessMode
        int bIsLocked
        double dfValue
        double dfMinValue
        double dfMaxValue
        double dfIncrement
        unsigned int nReserved[4]
    ctypedef _MV_XML_FEATURE_Float_ MV_XML_FEATURE_Float
    struct _MV_XML_FEATURE_String_:
        char strName[64]
        char strDisplayName[64]
        char strDescription[512]
        char strToolTip[512]
        MV_XML_Visibility enVisivility
        MV_XML_AccessMode enAccessMode
        int bIsLocked
        char strValue[64]
        unsigned int nReserved[4]
    ctypedef _MV_XML_FEATURE_String_ MV_XML_FEATURE_String
    struct _MV_XML_FEATURE_Register_:
        char strName[64]
        char strDisplayName[64]
        char strDescription[512]
        char strToolTip[512]
        MV_XML_Visibility enVisivility
        MV_XML_AccessMode enAccessMode
        int bIsLocked
        int64_t nAddrValue
        unsigned int nReserved[4]
    ctypedef _MV_XML_FEATURE_Register_ MV_XML_FEATURE_Register
    struct _MV_XML_FEATURE_Category_:
        char strDescription[512]
        char strDisplayName[64]
        char strName[64]
        char strToolTip[512]
        MV_XML_Visibility enVisivility
        unsigned int nReserved[4]
    ctypedef _MV_XML_FEATURE_Category_ MV_XML_FEATURE_Category
    struct _MV_XML_FEATURE_EnumEntry_:
        char strName[64]
        char strDisplayName[64]
        char strDescription[512]
        char strToolTip[512]
        int bIsImplemented
        int nParentsNum
        MV_XML_NODE_FEATURE stParentsList[8]
        MV_XML_Visibility enVisivility
        int64_t nValue
        MV_XML_AccessMode enAccessMode
        int bIsLocked
        int nReserved[8]
    ctypedef _MV_XML_FEATURE_EnumEntry_ MV_XML_FEATURE_EnumEntry
    struct _MV_XML_FEATURE_Enumeration_:
        MV_XML_Visibility enVisivility
        char strDescription[512]
        char strDisplayName[64]
        char strName[64]
        char strToolTip[512]
        int nSymbolicNum
        char strCurrentSymbolic[64]
        char strSymbolic[64][64]
        MV_XML_AccessMode enAccessMode
        int bIsLocked
        int64_t nValue
        unsigned int nReserved[4]
    ctypedef _MV_XML_FEATURE_Enumeration_ MV_XML_FEATURE_Enumeration
    struct _MV_XML_FEATURE_Port_:
        MV_XML_Visibility enVisivility
        char strDescription[512]
        char strDisplayName[64]
        char strName[64]
        char strToolTip[512]
        MV_XML_AccessMode enAccessMode
        int bIsLocked
        unsigned int nReserved[4]
    ctypedef _MV_XML_FEATURE_Port_ MV_XML_FEATURE_Port
    union pxdgen_anon__MV_XML_CAMERA_FEATURE__0:
        MV_XML_FEATURE_Integer stIntegerFeature
        MV_XML_FEATURE_Float stFloatFeature
        MV_XML_FEATURE_Enumeration stEnumerationFeature
        MV_XML_FEATURE_String stStringFeature
    struct _MV_XML_CAMERA_FEATURE_:
        MV_XML_InterfaceType enType
        pxdgen_anon__MV_XML_CAMERA_FEATURE__0 SpecialFeature
    ctypedef _MV_XML_CAMERA_FEATURE_ MV_XML_CAMERA_FEATURE
    struct _MVCC_ENUMVALUE_T:
        unsigned int nCurValue
        unsigned int nSupportedNum
        unsigned int nSupportValue[64]
        unsigned int nReserved[4]
    ctypedef _MVCC_ENUMVALUE_T MVCC_ENUMVALUE
    struct _MVCC_INTVALUE_T:
        unsigned int nCurValue
        unsigned int nMax
        unsigned int nMin
        unsigned int nInc
        unsigned int nReserved[4]
    ctypedef _MVCC_INTVALUE_T MVCC_INTVALUE
    struct _MVCC_INTVALUE_EX_T:
        int64_t nCurValue
        int64_t nMax
        int64_t nMin
        int64_t nInc
        unsigned int nReserved[16]
    ctypedef _MVCC_INTVALUE_EX_T MVCC_INTVALUE_EX
    struct _MVCC_FLOATVALUE_T:
        float fCurValue
        float fMax
        float fMin
        unsigned int nReserved[4]
    ctypedef _MVCC_FLOATVALUE_T MVCC_FLOATVALUE
    struct _MVCC_STRINGVALUE_T:
        char chCurValue[256]
        int64_t nMaxLength
        unsigned int nReserved[2]
    ctypedef _MVCC_STRINGVALUE_T MVCC_STRINGVALUE
    unsigned int MV_CC_GetSDKVersion()
    int MV_CC_EnumerateTls()
    int MV_CC_EnumDevices(unsigned int, MV_CC_DEVICE_INFO_LIST *)
    int MV_CC_EnumDevicesEx(unsigned int, MV_CC_DEVICE_INFO_LIST *, const char *)
    bint MV_CC_IsDeviceAccessible(MV_CC_DEVICE_INFO *, unsigned int)
    int MV_CC_SetSDKLogPath(const char *)
    int MV_CC_CreateHandle(void**, MV_CC_DEVICE_INFO *)
    int MV_CC_CreateHandleWithoutLog(void**, MV_CC_DEVICE_INFO *)
    int MV_CC_DestroyHandle(void *)
    int MV_CC_OpenDevice(void *, unsigned int, unsigned short)
    int MV_CC_CloseDevice(void *)
    bint MV_CC_IsDeviceConnected(void *)
    int MV_CC_RegisterImageCallBackEx(void *, void (*)(unsigned char *, MV_FRAME_OUT_INFO_EX *, void *), void *)
    int MV_CC_RegisterImageCallBackForRGB(void *, void (*)(unsigned char *, MV_FRAME_OUT_INFO_EX *, void *), void *)
    int MV_CC_RegisterImageCallBackForBGR(void *, void (*)(unsigned char *, MV_FRAME_OUT_INFO_EX *, void *), void *)
    int MV_CC_StartGrabbing(void *)
    int MV_CC_StopGrabbing(void *)
    int MV_CC_GetImageForRGB(void *, unsigned char *, unsigned int, MV_FRAME_OUT_INFO_EX *, int)
    int MV_CC_GetImageForBGR(void *, unsigned char *, unsigned int, MV_FRAME_OUT_INFO_EX *, int)
    int MV_CC_GetImageBuffer(void *, MV_FRAME_OUT *, unsigned int)
    int MV_CC_FreeImageBuffer(void *, MV_FRAME_OUT *)
    int MV_CC_GetOneFrameTimeout(void *, unsigned char *, unsigned int, MV_FRAME_OUT_INFO_EX *, unsigned int)
    int MV_CC_ClearImageBuffer(void *)
    int MV_CC_Display(void *, void *)
    int MV_CC_DisplayOneFrame(void *, MV_DISPLAY_FRAME_INFO *)
    int MV_CC_SetImageNodeNum(void *, unsigned int)
    int MV_CC_GetDeviceInfo(void *, MV_CC_DEVICE_INFO *)
    int MV_CC_GetAllMatchInfo(void *, MV_ALL_MATCH_INFO *)
    int MV_CC_GetIntValue(void *, const char *, MVCC_INTVALUE *)
    int MV_CC_GetIntValueEx(void *, const char *, MVCC_INTVALUE_EX *)
    int MV_CC_SetIntValue(void *, const char *, unsigned int)
    int MV_CC_SetIntValueEx(void *, const char *, int64_t)
    int MV_CC_GetEnumValue(void *, const char *, MVCC_ENUMVALUE *)
    int MV_CC_SetEnumValue(void *, const char *, unsigned int)
    int MV_CC_SetEnumValueByString(void *, const char *, const char *)
    int MV_CC_GetFloatValue(void *, const char *, MVCC_FLOATVALUE *)
    int MV_CC_SetFloatValue(void *, const char *, float)
    int MV_CC_GetBoolValue(void *, const char *, bint *)
    int MV_CC_SetBoolValue(void *, const char *, bint)
    int MV_CC_GetStringValue(void *, const char *, MVCC_STRINGVALUE *)
    int MV_CC_SetStringValue(void *, const char *, const char *)
    int MV_CC_SetCommandValue(void *, const char *)
    int MV_CC_InvalidateNodes(void *)
    int MV_CC_LocalUpgrade(void *, const void *)
    int MV_CC_GetUpgradeProcess(void *, unsigned int *)
    int MV_CC_ReadMemory(void *, void *, int64_t, int64_t)
    int MV_CC_WriteMemory(void *, const void *, int64_t, int64_t)
    int MV_CC_RegisterExceptionCallBack(void *, void (*)(unsigned int, void *), void *)
    int MV_CC_RegisterAllEventCallBack(void *, void (*)(MV_EVENT_OUT_INFO *, void *), void *)
    int MV_CC_RegisterEventCallBackEx(void *, const char *, void (*)(MV_EVENT_OUT_INFO *, void *), void *)
    int MV_GIGE_ForceIpEx(void *, unsigned int, unsigned int, unsigned int)
    int MV_GIGE_SetIpConfig(void *, unsigned int)
    int MV_GIGE_SetNetTransMode(void *, unsigned int)
    int MV_GIGE_GetNetTransInfo(void *, MV_NETTRANS_INFO *)
    int MV_GIGE_SetGvspTimeout(void *, unsigned int)
    int MV_GIGE_GetGvspTimeout(void *, unsigned int *)
    int MV_GIGE_SetGvcpTimeout(void *, unsigned int)
    int MV_GIGE_GetGvcpTimeout(void *, unsigned int *)
    int MV_GIGE_SetRetryGvcpTimes(void *, unsigned int)
    int MV_GIGE_GetRetryGvcpTimes(void *, unsigned int *)
    int MV_CC_GetOptimalPacketSize(void *)
    int MV_GIGE_SetResend(void *, unsigned int, unsigned int, unsigned int)
    int MV_GIGE_SetResendMaxRetryTimes(void *, unsigned int)
    int MV_GIGE_GetResendMaxRetryTimes(void *, unsigned int *)
    int MV_GIGE_SetResendTimeInterval(void *, unsigned int)
    int MV_GIGE_GetResendTimeInterval(void *, unsigned int *)
    int MV_GIGE_SetTransmissionType(void *, MV_TRANSMISSION_TYPE *)
    int MV_GIGE_IssueActionCommand(MV_ACTION_CMD_INFO *, MV_ACTION_CMD_RESULT_LIST *)
    int MV_XML_GetGenICamXML(void *, unsigned char *, unsigned int, unsigned int *)
    int MV_CC_SaveImageEx2(void *, MV_SAVE_IMAGE_PARAM_EX *)
    int MV_CC_RotateImage(void *, MV_CC_ROTATE_IMAGE_PARAM *)
    int MV_CC_FlipImage(void *, MV_CC_FLIP_IMAGE_PARAM *)
    int MV_CC_ConvertPixelType(void *, MV_CC_PIXEL_CONVERT_PARAM *)
    int MV_CC_SetBayerCvtQuality(void *, unsigned int)
    int MV_CC_SetBayerGammaParam(void *, MV_CC_GAMMA_PARAM *)
    int MV_CC_HB_Decode(void *, MV_CC_HB_DECODE_PARAM *)
    int MV_CC_FeatureSave(void *, const char *)
    int MV_CC_FeatureLoad(void *, const char *)
    int MV_CC_FileAccessRead(void *, MV_CC_FILE_ACCESS *)
    int MV_CC_FileAccessWrite(void *, MV_CC_FILE_ACCESS *)
    int MV_CC_GetFileAccessProgress(void *, MV_CC_FILE_ACCESS_PROGRESS *)
    int MV_CC_StartRecord(void *, MV_CC_RECORD_PARAM *)
    int MV_CC_InputOneFrame(void *, MV_CC_INPUT_FRAME_INFO *)
    int MV_CC_StopRecord(void *)
    int MV_CC_GetImageInfo(void *, MV_IMAGE_BASIC_INFO *)
    void * MV_CC_GetTlProxy(void *)
    int MV_XML_GetRootNode(void *, MV_XML_NODE_FEATURE *)
    int MV_XML_GetChildren(void *, MV_XML_NODE_FEATURE *, MV_XML_NODES_LIST *)
    int MV_XML_GetNodeFeature(void *, MV_XML_NODE_FEATURE *, void *)
    int MV_XML_UpdateNodeFeature(void *, MV_XML_InterfaceType, void *)
    int MV_XML_RegisterUpdateCallBack(void *, void (*)(MV_XML_InterfaceType, void *, MV_XML_NODES_LIST *, void *),
                                      void *)
    int MV_CC_GetOneFrame(void *, unsigned char *, unsigned int, MV_FRAME_OUT_INFO *)
    int MV_CC_GetOneFrameEx(void *, unsigned char *, unsigned int, MV_FRAME_OUT_INFO_EX *)
    int MV_CC_RegisterImageCallBack(void *, void (*)(unsigned char *, MV_FRAME_OUT_INFO *, void *), void *)
    int MV_CC_SaveImage(MV_SAVE_IMAGE_PARAM *)
    int MV_CC_SaveImageEx(MV_SAVE_IMAGE_PARAM_EX *)
    int MV_GIGE_ForceIp(void *, unsigned int)
    int MV_CC_RegisterEventCallBack(void *, void (*)(unsigned int, void *), void *)
    int MV_CC_GetWidth(void *, MVCC_INTVALUE *)
    int MV_CC_SetWidth(void *, const unsigned int)
    int MV_CC_GetHeight(void *, MVCC_INTVALUE *)
    int MV_CC_SetHeight(void *, const unsigned int)
    int MV_CC_GetAOIoffsetX(void *, MVCC_INTVALUE *)
    int MV_CC_SetAOIoffsetX(void *, const unsigned int)
    int MV_CC_GetAOIoffsetY(void *, MVCC_INTVALUE *)
    int MV_CC_SetAOIoffsetY(void *, const unsigned int)
    int MV_CC_GetAutoExposureTimeLower(void *, MVCC_INTVALUE *)
    int MV_CC_SetAutoExposureTimeLower(void *, const unsigned int)
    int MV_CC_GetAutoExposureTimeUpper(void *, MVCC_INTVALUE *)
    int MV_CC_SetAutoExposureTimeUpper(void *, const unsigned int)
    int MV_CC_GetBrightness(void *, MVCC_INTVALUE *)
    int MV_CC_SetBrightness(void *, const unsigned int)
    int MV_CC_GetFrameRate(void *, MVCC_FLOATVALUE *)
    int MV_CC_SetFrameRate(void *, const float)
    int MV_CC_GetGain(void *, MVCC_FLOATVALUE *)
    int MV_CC_SetGain(void *, const float)
    int MV_CC_GetExposureTime(void *, MVCC_FLOATVALUE *)
    int MV_CC_SetExposureTime(void *, const float)
    int MV_CC_GetPixelFormat(void *, MVCC_ENUMVALUE *)
    int MV_CC_SetPixelFormat(void *, const unsigned int)
    int MV_CC_GetAcquisitionMode(void *, MVCC_ENUMVALUE *)
    int MV_CC_SetAcquisitionMode(void *, const unsigned int)
    int MV_CC_GetGainMode(void *, MVCC_ENUMVALUE *)
    int MV_CC_SetGainMode(void *, const unsigned int)
    int MV_CC_GetExposureAutoMode(void *, MVCC_ENUMVALUE *)
    int MV_CC_SetExposureAutoMode(void *, const unsigned int)
    int MV_CC_GetTriggerMode(void *, MVCC_ENUMVALUE *)
    int MV_CC_SetTriggerMode(void *, const unsigned int)
    int MV_CC_GetTriggerDelay(void *, MVCC_FLOATVALUE *)
    int MV_CC_SetTriggerDelay(void *, const float)
    int MV_CC_GetTriggerSource(void *, MVCC_ENUMVALUE *)
    int MV_CC_SetTriggerSource(void *, const unsigned int)
    int MV_CC_TriggerSoftwareExecute(void *)
    int MV_CC_GetGammaSelector(void *, MVCC_ENUMVALUE *)
    int MV_CC_SetGammaSelector(void *, const unsigned int)
    int MV_CC_GetGamma(void *, MVCC_FLOATVALUE *)
    int MV_CC_SetGamma(void *, const float)
    int MV_CC_GetSharpness(void *, MVCC_INTVALUE *)
    int MV_CC_SetSharpness(void *, const unsigned int)
    int MV_CC_GetHue(void *, MVCC_INTVALUE *)
    int MV_CC_SetHue(void *, const unsigned int)
    int MV_CC_GetSaturation(void *, MVCC_INTVALUE *)
    int MV_CC_SetSaturation(void *, const unsigned int)
    int MV_CC_GetBalanceWhiteAuto(void *, MVCC_ENUMVALUE *)
    int MV_CC_SetBalanceWhiteAuto(void *, const unsigned int)
    int MV_CC_GetBalanceRatioRed(void *, MVCC_INTVALUE *)
    int MV_CC_SetBalanceRatioRed(void *, const unsigned int)
    int MV_CC_GetBalanceRatioGreen(void *, MVCC_INTVALUE *)
    int MV_CC_SetBalanceRatioGreen(void *, const unsigned int)
    int MV_CC_GetBalanceRatioBlue(void *, MVCC_INTVALUE *)
    int MV_CC_SetBalanceRatioBlue(void *, const unsigned int)
    int MV_CC_GetFrameSpecInfoAbility(void *, MVCC_INTVALUE *)
    int MV_CC_SetFrameSpecInfoAbility(void *, const unsigned int)
    int MV_CC_GetDeviceUserID(void *, MVCC_STRINGVALUE *)
    int MV_CC_SetDeviceUserID(void *, const char *)
    int MV_CC_GetBurstFrameCount(void *, MVCC_INTVALUE *)
    int MV_CC_SetBurstFrameCount(void *, const unsigned int)
    int MV_CC_GetAcquisitionLineRate(void *, MVCC_INTVALUE *)
    int MV_CC_SetAcquisitionLineRate(void *, const unsigned int)
    int MV_CC_GetHeartBeatTimeout(void *, MVCC_INTVALUE *)
    int MV_CC_SetHeartBeatTimeout(void *, const unsigned int)
    int MV_GIGE_GetGevSCPSPacketSize(void *, MVCC_INTVALUE *)
    int MV_GIGE_SetGevSCPSPacketSize(void *, const unsigned int)
    int MV_GIGE_GetGevSCPD(void *, MVCC_INTVALUE *)
    int MV_GIGE_SetGevSCPD(void *, const unsigned int)
    int MV_GIGE_GetGevSCDA(void *, unsigned int *)
    int MV_GIGE_SetGevSCDA(void *, unsigned int)
    int MV_GIGE_GetGevSCSP(void *, unsigned int *)
    int MV_GIGE_SetGevSCSP(void *, unsigned int)
    int MV_CAML_SetDeviceBauderate(void *, unsigned int)
    int MV_CAML_GetDeviceBauderate(void *, unsigned int *)
    int MV_CAML_GetSupportBauderates(void *, unsigned int *)
    int MV_CAML_SetGenCPTimeOut(void *, unsigned int)
    int MV_USB_SetTransferSize(void *, unsigned int)
    int MV_USB_GetTransferSize(void *, unsigned int *)
    int MV_USB_SetTransferWays(void *, unsigned int)
    int MV_USB_GetTransferWays(void *, unsigned int *)
