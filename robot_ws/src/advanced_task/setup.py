from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'advanced_task'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # 安装 launch 文件
        (os.path.join('share', package_name, 'launch'),
         glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='cx',
    maintainer_email='cx@todo.todo',
    description='ROS2 进阶题：摄像头识别数学表达式并计算结果',
    license='Apache-2.0',
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            # 三个可执行节点
            'display_node = advanced_task.display_node:main',
            'recognition_node = advanced_task.recognition_node:main',
            'result_sub_node = advanced_task.result_sub_node:main',
        ],
    },
)
