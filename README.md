### 2022赛季南工骁鹰雷达站

---

*2022赛季**第二代**雷达站仍然参考了2021年上海交通大学的开源方案*

##### 环境配置

| 系统 | ubuntu20.04      |
| :----: | :-----------: |
|      |    python3.8    |
|      |    pyqt5        |
|      |    cudnn8       |
|      |    tensorrt8    |
|      |    cuda11.6     |

- ##### 计划

    - [X]  对串口类进行修改，在封一层
    - [X]  修改第二版ui，增大主视角显示，删除副视角
    - [ ]  增加决策树（if-else嗯写，时间不够力）
    - [X]  观察敌方补弹信息
    - [ ]  增加信息管理类和显示类，把信息统一到一起进行处理
    - [X]  德劳内三角定位和激光雷达定位融合
    - [ ]  英雄吊射基地视角放大
    - [ ]  搬运网络和相机类至c++，通过socket通信传递信息

- ##### 代码架构
    - 之后在写
- ##### 关于第二版雷达站
    - c++ rust代码部分暂不上传
    - 目前还在绝赞研发中，代码目前不能用
