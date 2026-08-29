from status_interfaces.msg import StudentInfo
import rclpy
from rclpy.node import Node

class IDSubNode(Node):
    def __init__(self,node_name):
        super().__init__(node_name)
        self.get_logger().info(f'{node_name}接受启动')
        self.ID_subscriber=self.create_subscription(StudentInfo,'ID',self.ID_callback,20)

    def ID_callback(self,msg):
        self.get_logger().info(f'get ID:{msg.student_id}, get name:{msg.student_name}')

def main():
    rclpy.init()
    node=IDSubNode('ID_sub')
    rclpy.spin(node)
    rclpy.shutdown()