from status_interfaces.msg import StudentInfo
import rclpy
from rclpy.node import Node

class IDPubNode(Node):
    def __init__(self,node_name):
        super().__init__(node_name)
        self.get_logger().info(f'{node_name}启动')
        self.ID_publisher=self.create_publisher(StudentInfo,'ID',20)
        self.create_timer(1,self.timer_callback)

    def timer_callback(self):
        msg=StudentInfo()
        msg.student_id='2025115922'
        msg.student_name='陈想'
        self.ID_publisher.publish(msg)
        self.get_logger().info(f'发布了{msg}')


def main():
    rclpy.init()
    node=IDPubNode('ID_pub')
    rclpy.spin(node)
    rclpy.shutdown()