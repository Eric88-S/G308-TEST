"""
advanced.launch.py — 进阶题一键启动文件
用法:
  ros2 launch advanced_task advanced.launch.py
  ros2 launch advanced_task advanced.launch.py camera_device:=0 process_rate:=3.0
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    camera_device_arg = DeclareLaunchArgument(
        'camera_device', default_value='0',
        description='摄像头设备编号'
    )
    frame_width_arg = DeclareLaunchArgument(
        'frame_width', default_value='1280',
        description='摄像头分辨率-宽'
    )
    frame_height_arg = DeclareLaunchArgument(
        'frame_height', default_value='720',
        description='摄像头分辨率-高'
    )
    preview_arg = DeclareLaunchArgument(
        'preview', default_value='true',
        description='是否显示预览窗口'
    )
    process_rate_arg = DeclareLaunchArgument(
        'process_rate', default_value='2.0',
        description='OCR识别频率（Hz），越高识别越快但CPU占用越高'
    )

    recognition_node = Node(
        package='advanced_task',
        executable='recognition_node',
        name='recognition_node',
        output='screen',
        parameters=[{
            'camera_device': LaunchConfiguration('camera_device'),
            'frame_width': LaunchConfiguration('frame_width'),
            'frame_height': LaunchConfiguration('frame_height'),
            'preview': LaunchConfiguration('preview'),
            'process_rate': LaunchConfiguration('process_rate'),
        }]
    )

    result_sub_node = Node(
        package='advanced_task',
        executable='result_sub_node',
        name='result_sub_node',
        output='screen'
    )

    return LaunchDescription([
        camera_device_arg,
        frame_width_arg,
        frame_height_arg,
        preview_arg,
        process_rate_arg,
        recognition_node,
        result_sub_node,
        LogInfo(msg='进阶题启动: 识别节点 + 结果订阅节点'),
    ])
