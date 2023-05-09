"""
tensorrtx 代码
created by 李龙 2021/1
最终修改 by 李龙 2021/1/15
添加注释 by 林顺喆 2022/12/26
"""
import os

import numpy as np
# noinspection PyUnresolvedReferences
import pycuda.autoinit
import pycuda.driver as cuda
import tensorrt as trt
from loguru import logger

from net.trt_logger import LoguruTrtLogger


class YoLov5TRT(object):
    """
    YOLOv5 类，用于执行 TensorRT 推理操作
    """

    def __init__(self, engine_file_path):
        engine_base_name = os.path.basename(engine_file_path)
        logger.info(f"加载 {engine_base_name} 中...")

        self.ctx = cuda.Device(0).make_context()  # 生成一个 pycuda 的 context 对象（使用第 0 个 CUDA 设备，即 GPU0，一般是独显）

        stream = cuda.Stream(0)  # 生成 CUDA 流，即一个 GPU 上的操作队列
        runtime = trt.Runtime(LoguruTrtLogger({"function": "v5", "line": engine_base_name}))  # 创建 TensorRT 的 Runtime

        # 反序列化生成 engine
        with open(engine_file_path, "rb") as f:
            engine: trt.ICudaEngine = runtime.deserialize_cuda_engine(f.read())

        context: trt.IExecutionContext = engine.create_execution_context()

        host_inputs = []
        cuda_inputs = []
        host_outputs = []
        cuda_outputs = []
        bindings = []

        assert engine.max_batch_size == 1

        for binding in engine:  # 遍历 binding
            shape = engine.get_tensor_shape(binding)
            mode = engine.get_tensor_mode(binding)
            logger.debug(f"Binding {mode} {binding}: {shape}")

            size = trt.volume(shape)  # 计算内存空间大小
            dtype = trt.nptype(engine.get_tensor_dtype(binding))  # 内存空间的数据类型
            host_mem = cuda.pagelocked_empty(size, dtype)  # 为主机分配页锁定内存（避免进入磁盘模拟的低速虚拟内存）供 numpy 对象使用
            cuda_mem = cuda.mem_alloc(host_mem.nbytes)  # 分配设备内存，与页锁定内存等大
            # 将分配的设备内存记录于 bindings 列表
            # cuda_mem 的类型是 pycuda.driver.DeviceAllocation，可通过强制转换其为 int 类型，以取得在 IEContext 中的下标
            bindings.append(int(cuda_mem))

            # 根据 binding 是 input 或 output 类型，将内存记录于不同的列表
            if mode == trt.TensorIOMode.INPUT:
                self.input_w = shape[-1]
                self.input_h = shape[-2]
                host_inputs.append(host_mem)
                cuda_inputs.append(cuda_mem)
            elif mode == trt.TensorIOMode.OUTPUT:
                host_outputs.append(host_mem)
                cuda_outputs.append(cuda_mem)
            else:
                logger.error(f"{binding} 既不是输入也不是输出 {mode}")

        logger.info(f"加载 {engine_base_name} 完成，共有 {len(host_inputs)} 个输入，{len(host_outputs)} 个输出")

        # 保存到 self
        self.stream = stream
        self.context = context
        self.engine = engine
        self.host_inputs = host_inputs
        self.cuda_inputs = cuda_inputs
        self.host_outputs = host_outputs
        self.cuda_outputs = cuda_outputs
        self.bindings = bindings
        self.batch_size = 1

    def infer(self, batch_input_image: np.ndarray):
        # 激活
        # 该方法将 ctx 置于 context 栈的栈顶
        self.ctx.push()

        stream = self.stream
        context = self.context
        host_inputs = self.host_inputs
        cuda_inputs = self.cuda_inputs
        host_outputs = self.host_outputs
        cuda_outputs = self.cuda_outputs
        bindings = self.bindings

        np.copyto(host_inputs[0], batch_input_image.ravel())  # 将输入的图像传入 host 主机内存
        cuda.memcpy_htod_async(cuda_inputs[0], host_inputs[0], stream)  # 将主机上存储的输入数据传入 GPU
        context.execute_async_v2(bindings=bindings, stream_handle=stream.handle)  # 进行推理过程

        # 将推理得到的输入数据从 GPU 拉回到主机
        for i in range(len(host_outputs)):
            cuda.memcpy_dtoh_async(host_outputs[i], cuda_outputs[i], stream)

        stream.synchronize()  # 等待所有 CUDA 操作停止，然后继续
        self.ctx.pop()  # 将 self 弹出，不再激活 注意 pop 是 static 方法

        return host_outputs

    def __del__(self):
        logger.debug(f"正在析构 {self}")

        # 将 context 栈顶的 ICudaContext 对象弹出，不再激活
        self.stream.synchronize()
        self.ctx.pop()
        # self.ctx.detach()

        logger.debug(f"析构 {self} 结束")
