from typing import Optional

import tensorrt as trt
from loguru import logger


class LoguruTrtLogger(trt.ILogger):
    """
    用于将 TensorRT 的日志输出到 loguru 的 logger 中
    """

    def __init__(self, update: Optional[dict] = None):
        trt.ILogger.__init__(self)
        if update is None:
            update = {}
        self.logger = logger.patch(lambda record: record.update(update))
        self.severity_map = {
            trt.Logger.Severity.VERBOSE: "DEBUG",
            trt.Logger.Severity.INFO: "INFO",
            trt.Logger.Severity.WARNING: "WARNING",
            trt.Logger.Severity.ERROR: "ERROR",
        }

    # noinspection PyMethodOverriding
    def log(self, severity: trt.Logger.Severity, msg: str):
        self.logger.log(self.severity_map.get(severity, "INFO"), msg)
