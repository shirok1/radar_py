"""
YOLOv8 TensorRT 推理实现
"""

import os
import random
import time

import cv2
import numpy as np
# noinspection PyUnresolvedReferences
import pycuda.autoinit
import pycuda.driver as cuda
import tensorrt as trt
from loguru import logger

import config
from net.trt_logger import LoguruTrtLogger

CONF_THRESH = 0.55
IOU_THRESHOLD = 0.65
LEN_ONE_RESULT = 7


def get_img_path_batches(batch_size, img_dir):
    all_files = sum([[os.path.join(root, name)
                      for name in files
                      if name.split(".")[-1] in ["jpg", "png", "jpeg"]]
                     for root, _, files in os.walk(img_dir)], [])
    return [all_files[index:index + batch_size] for index in range(0, len(all_files), batch_size)]


def plot_one_box(x, img, color=None, label=None, line_thickness=None):
    """
    description: Plots one bounding box on image img,
                 this function comes from YoLov5 project.
    param:
        x:      a box likes [x1,y1,x2,y2]
        img:    a opencv image object
        color:  color to draw rectangle, such as (0,255,0)
        label:  str
        line_thickness: int
    return:
        no return

    """
    tl = (
            line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1
    )  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(
            img,
            label,
            (c1[0], c1[1] - 2),
            0,
            tl / 3,
            [225, 255, 255],
            thickness=tf,
            lineType=cv2.LINE_AA,
        )


def bbox_iou(box1, box2, x1y1x2y2=True):
    """
    description: compute the IoU of two bounding boxes
    param:
        box1: A box coordinate (can be (x1, y1, x2, y2) or (x, y, w, h))
        box2: A box coordinate (can be (x1, y1, x2, y2) or (x, y, w, h))
        x1y1x2y2: select the coordinate format
    return:
        iou: computed iou
    """
    if not x1y1x2y2:
        # Transform from center and width to exact coordinates
        b1_x1, b1_x2 = box1[:, 0] - box1[:, 2] / 2, box1[:, 0] + box1[:, 2] / 2
        b1_y1, b1_y2 = box1[:, 1] - box1[:, 3] / 2, box1[:, 1] + box1[:, 3] / 2
        b2_x1, b2_x2 = box2[:, 0] - box2[:, 2] / 2, box2[:, 0] + box2[:, 2] / 2
        b2_y1, b2_y2 = box2[:, 1] - box2[:, 3] / 2, box2[:, 1] + box2[:, 3] / 2
    else:
        # Get the coordinates of bounding boxes
        b1_x1, b1_y1, b1_x2, b1_y2 = box1[:, 0], box1[:, 1], box1[:, 2], box1[:, 3]
        b2_x1, b2_y1, b2_x2, b2_y2 = box2[:, 0], box2[:, 1], box2[:, 2], box2[:, 3]

    # Get the coordinates of the intersection rectangle
    inter_rect_x1 = np.maximum(b1_x1, b2_x1)
    inter_rect_y1 = np.maximum(b1_y1, b2_y1)
    inter_rect_x2 = np.minimum(b1_x2, b2_x2)
    inter_rect_y2 = np.minimum(b1_y2, b2_y2)
    # Intersection area
    inter_area = np.clip(inter_rect_x2 - inter_rect_x1 + 1, 0, None) * \
                 np.clip(inter_rect_y2 - inter_rect_y1 + 1, 0, None)
    # Union Area
    b1_area = (b1_x2 - b1_x1 + 1) * (b1_y2 - b1_y1 + 1)
    b2_area = (b2_x2 - b2_x1 + 1) * (b2_y2 - b2_y1 + 1)

    iou = inter_area / (b1_area + b2_area - inter_area + 1e-16)

    return iou


class YOLOv8TRT(object):
    """
    YOLOv8 类，包装了使用 TensorRT 的推理过程，包含前后处理
    """

    def __init__(self, engine_file_path: str):
        """
        初始化函数
        :param engine_file_path: engine 文件路径
        """
        engine_base_name = os.path.basename(engine_file_path)
        logger.info(f"加载 {engine_base_name} 中...")

        self.ctx = cuda.Device(0).make_context()  # 生成一个 pycuda 的 context 对象（使用第 0 个 CUDA 设备，即 GPU0，一般是独显）

        stream = cuda.Stream()  # 生成 CUDA 流，即一个 GPU 上的操作队列

        runtime = trt.Runtime(LoguruTrtLogger({"function": "v8", "line": engine_base_name}))  # 创建 TensorRT 的 Runtime

        # 反序列化生成 engine
        with open(engine_file_path, "rb") as f:
            engine = runtime.deserialize_cuda_engine(f.read())
        context = engine.create_execution_context()

        host_inputs = []
        cuda_inputs = []
        host_outputs = []
        cuda_outputs = []
        bindings = []

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
        # self.batch_size = engine.max_batch_size
        self.batch_size = 1

    def infer(self, raw_image_generator):
        # threading.Thread.__init__(self)
        # 该方法将 ctx 置于 context 栈的栈顶
        self.ctx.push()

        stream = self.stream
        context = self.context
        host_inputs = self.host_inputs
        cuda_inputs = self.cuda_inputs
        host_outputs = self.host_outputs
        cuda_outputs = self.cuda_outputs
        bindings = self.bindings
        # 保存原始输入图像
        batch_image_raw = []
        batch_origin_h = []
        batch_origin_w = []
        batch_input_image = np.empty(shape=[self.batch_size, 3, self.input_h, self.input_w])
        for batch_index, image_raw in enumerate(raw_image_generator):
            input_image, image_raw, origin_h, origin_w = self.preprocess_image(image_raw)
            batch_image_raw.append(image_raw)
            batch_origin_h.append(origin_h)
            batch_origin_w.append(origin_w)
            np.copyto(batch_input_image[batch_index], input_image)
        batch_input_image = np.ascontiguousarray(batch_input_image)

        np.copyto(host_inputs[0], batch_input_image.ravel())  # 将输入的图像传入 host 主机内存

        start = time.time()
        cuda.memcpy_htod_async(cuda_inputs[0], host_inputs[0], stream)  # 将主机上存储的输入数据传入 GPU
        context.execute_async_v2(bindings=bindings, stream_handle=stream.handle)  # 进行推理过程
        cuda.memcpy_dtoh_async(host_outputs[0], cuda_outputs[0], stream)  # 将推理得到的输入数据从 GPU 拉回到主机
        stream.synchronize()  # 等待所有 CUDA 操作停止，然后继续
        end = time.time()

        self.ctx.pop()  # 将 self 弹出，不再激活 注意 pop 是 static 方法

        # Here we use the first row of output in that batch_size = 1
        output = host_outputs[0]

        # 后处理
        for batch_index in range(self.batch_size):
            result_boxes, result_scores, result_classid = self.post_process(
                output, batch_origin_h[batch_index], batch_origin_w[batch_index]
            )
            # 绘制框和标签
            for box_index in range(len(result_boxes)):
                box = result_boxes[box_index]
                plot_one_box(
                    box,
                    batch_image_raw[batch_index],
                    label="{}:{:.2f}".format(
                        categories[int(result_classid[box_index])], result_scores[box_index]
                    ),
                )
        return batch_image_raw, end - start

    def destroy(self):
        # Remove any context from the top of the context stack, deactivating it.
        self.ctx.pop()

    def preprocess_image(self, raw_bgr_image):
        """
        description: Convert BGR image to RGB,
                     resize and pad it to target size, normalize to [0,1],
                     transform to NCHW format.
        param:
            input_image_path: str, image path
        return:
            image:  the processed image
            image_raw: the original image
            h: original height
            w: original width
        """
        image_raw = raw_bgr_image
        h, w, c = image_raw.shape
        image = cv2.cvtColor(image_raw, cv2.COLOR_BGR2RGB)
        # Calculate widht and height and paddings
        r_w = self.input_w / w
        r_h = self.input_h / h
        if r_h > r_w:
            tw = self.input_w
            th = int(r_w * h)
            tx1 = tx2 = 0
            ty1 = int((self.input_h - th) / 2)
            ty2 = self.input_h - th - ty1
        else:
            tw = int(r_h * w)
            th = self.input_h
            tx1 = int((self.input_w - tw) / 2)
            tx2 = self.input_w - tw - tx1
            ty1 = ty2 = 0
        # Resize the image with long side while maintaining ratio
        image = cv2.resize(image, (tw, th))
        # Pad the short side with (128,128,128)
        image = cv2.copyMakeBorder(
            image, ty1, ty2, tx1, tx2, cv2.BORDER_CONSTANT, None, (128, 128, 128)
        )
        image = image.astype(np.float32)
        # Normalize to [0,1]
        image /= 255.0
        # HWC to CHW format:
        image = np.transpose(image, [2, 0, 1])
        # CHW to NCHW format
        image = np.expand_dims(image, axis=0)
        # Convert the image to row-major order, also known as "C order":
        image = np.ascontiguousarray(image)
        return image, image_raw, h, w

    def xywh2xyxy(self, origin_h, origin_w, x):
        """
        description:    Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
        param:
            origin_h:   height of original image
            origin_w:   width of original image
            x:          A boxes numpy, each row is a box [center_x, center_y, w, h]
        return:
            y:          A boxes numpy, each row is a box [x1, y1, x2, y2]
        """
        y = np.zeros_like(x)
        r_w = self.input_w / origin_w
        r_h = self.input_h / origin_h
        if r_h > r_w:
            y[:, 0] = x[:, 0] - x[:, 2] / 2
            y[:, 2] = x[:, 0] + x[:, 2] / 2
            y[:, 1] = x[:, 1] - x[:, 3] / 2 - (self.input_h - r_w * origin_h) / 2
            y[:, 3] = x[:, 1] + x[:, 3] / 2 - (self.input_h - r_w * origin_h) / 2
            y /= r_w
        else:
            y[:, 0] = x[:, 0] - x[:, 2] / 2 - (self.input_w - r_h * origin_w) / 2
            y[:, 2] = x[:, 0] + x[:, 2] / 2 - (self.input_w - r_h * origin_w) / 2
            y[:, 1] = x[:, 1] - x[:, 3] / 2
            y[:, 3] = x[:, 1] + x[:, 3] / 2
            y /= r_h

        return y

    def post_process(self, output, origin_h, origin_w):
        """
        处理网络输出，得到最终的 boxes、scores、classes
        :param output:     协议待补
        :param origin_h:   原始图像的高
        :param origin_w:   原始图像的宽
        :returns:
            result_boxes: finally boxes, a boxes numpy, each row is a box [x1, y1, x2, y2]
            result_scores: finally scores, a numpy, each element is the score correspoing to box
            result_classid: finally classid, a numpy, each element is the classid correspoing to box
        """
        # Get the num of boxes detected
        output = np.reshape(output, (7, -1)).T
        # choose = np.max(output[:, 4:6], axis=1) > CONF_THRESH
        # output = output[choose]
        max_arg = np.argmax(output[:, 4:6], axis=1).reshape(-1)
        max_num = np.max(output[:, 4:6], axis=1).reshape(-1)

        # NMS 非最大抑制
        boxes = self.xywh2xyxy(origin_h, origin_w, output[:, :4])
        boxes[:, 0] = np.clip(boxes[:, 0], 0, origin_w - 1)
        boxes[:, 2] = np.clip(boxes[:, 2], 0, origin_w - 1)
        boxes[:, 1] = np.clip(boxes[:, 1], 0, origin_h - 1)
        boxes[:, 3] = np.clip(boxes[:, 3], 0, origin_h - 1)
        indices = np.array(
            cv2.dnn.NMSBoxes(boxes.tolist(), max_num.tolist(), CONF_THRESH, IOU_THRESHOLD)).reshape(-1)
        result_boxes = boxes[indices] if len(indices.tolist()) else np.array([])
        result_scores = max_num[indices] if len(indices.tolist()) else np.array([])
        result_classid = max_arg[indices] if len(indices.tolist()) else np.array([])
        return result_boxes, result_scores, result_classid


if __name__ == "__main__":
    engine_file_path = config.best_engine

    categories = ["car", "watcher", "base"]

    yolo = YOLOv8TRT(engine_file_path)
    try:
        logger.info(f'batch size is {yolo.batch_size}')

        image_dir = "/home/shiroki/radar_jicheng_record/label_batch/qzz"
        image_path_batches = get_img_path_batches(yolo.batch_size, image_dir)

        for batch in image_path_batches:
            img_with_boxes, use_time = yolo.infer(map(cv2.imread, batch))
            for i, img_path in enumerate(batch):
                cv2.imshow("result", img_with_boxes[i])
                cv2.pollKey()
            logger.info("input->{}, time->{:.2f}ms", batch, use_time * 1000)
    finally:
        # destroy the instance
        yolo.destroy()
