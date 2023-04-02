#!/usr/bin/env sh

# 调用 trtexec 为两个 .onnx 文件生成 TensorRT .engine

trtexec --onnx=net1.onnx --saveEngine=net1.engine
trtexec --onnx=net2.onnx --saveEngine=net2.engine
