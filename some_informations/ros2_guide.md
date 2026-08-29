ROS2 数学表达式识别项目说明

环境：Ubuntu 22.04 + ROS2 Humble，工作空间在 /home/cx/ros_using/robot_ws。


一、工作空间结构

ros_using/
└── robot_ws/
    ├── src/
    │   ├── advanced_task/           # 进阶作业：摄像头识别算式并算结果
    │   │   ├── advanced_task/
    │   │   │   ├── display_node.py        # 设备A：白底 Times New Roman 全屏显示随机算式
    │   │   │   ├── recognition_node.py    # 设备B：取流、定位、识别、计算、发布
    │   │   │   ├── result_sub_node.py     # 设备B：订阅 /calculation_result 打印
    │   │   │   ├── math_generator.py      # 生成随机算式（保证结果是整数）
    │   │   │   └── recognition_node.py.bak # 旧版备份
    │   │   ├── launch/advanced.launch.py
    │   │   └── package.xml / setup.py / setup.cfg
    │   ├── calculation_interfaces/  # 进阶作业的消息
    │   │   └── msg/CalculationResult.msg
    │   ├── pub_sub/                 # 基础作业：发布/订阅节点（包名叫 demo_python_topic）
    │   │   └── demo_python_topic/{ID_pub_node.py, ID_sub_node.py}
    │   └── status_interfaces/       # 基础作业的消息 StudentInfo
    ├── build/  install/  log/       # 编译生成的，不用管

谁依赖谁：

advanced_task 依赖 calculation_interfaces（CalculationResult）
demo_python_topic 依赖 status_interfaces（StudentInfo）

自定义消息：

CalculationResult：string raw_expression（识别到的算式）、float64 result（结果）
StudentInfo：string student_id、string student_name


二、依赖安装

sudo apt install ttf-mscorefonts-installer   # Times New Roman 字体，显示端要用
pip3 install opencv-python numpy pillow sympy

不用装 Tesseract。识别是模板匹配做的（最后讲原因），模板用字体文件现画。


三、编译

colcon build
source install/setup.bash      # 每次开新终端都要 source 一下



四、运行

（一）进阶作业

设备A 和设备B 各开一个终端，都要先 source install/setup.bash。

设备A 显示算式（全屏白底黑字，按 q 退出）：

ros2 run advanced_task display_node

设备B 识别 + 订阅（一键）：

ros2 launch advanced_task advanced.launch.py

单独跑某个节点：

ros2 run advanced_task recognition_node --ros-args -p camera_device:=1
ros2 run advanced_task result_sub_node


（二）基础作业

ros2 run demo_python_topic ID_pub_node   # 发 StudentInfo 到 /ID
ros2 run demo_python_topic ID_sub_node   # 收并打印


五、识别和计算流程

recognition_node.py 一共五步：

1. 取流   摄像头一直读帧，定时器按 process_rate 挑最新一帧处理
2. 定位   高斯模糊 -> Canny 找边 -> 膨胀连边 -> 最大轮廓 -> boundingRect 框出屏幕
3. 识别   升采样+锐化 -> Otsu 二值化 -> 连通域切字 -> 模板匹配
4. 计算   SymPy simplify（×换成*、÷换成/）
5. 发布   发 CalculationResult 到 /calculation_result

为什么不用 OCR（Tesseract）：

算式的字符就 14 个：0-9 和 + - × ÷，字体固定是 Times New Roman。
试过 Tesseract，它在很清楚的图上也把 ÷ 读成 +（132÷3 读成 132+3），
而且 132+3 照样是合法算式，会当成正确答案发出去，还没法靠调参解决。

所以改成模板匹配：启动时用显示端同一个字体文件画 14 个字符模板，
每个切出来的字符跟模板比相似度，取最像的那个。这样 ÷ 就不会读错了。



