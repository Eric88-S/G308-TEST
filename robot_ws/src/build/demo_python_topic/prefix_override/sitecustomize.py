import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/cx/ros_using/robot_ws/src/install/demo_python_topic'
