"""
result_sub_node.py — 设备B：结果订阅节点
订阅 /calculation_result 话题，在终端输出识别到的原始表达式和计算结果。
注意：不得写死题目或答案，所有内容从话题消息中获取。
"""

import rclpy
from rclpy.node import Node
from calculation_interfaces.msg import CalculationResult  # 自定义消息


class ResultSubNode(Node):
    """
    结果订阅节点：
      订阅话题 /calculation_result (CalculationResult)
      接收消息后在终端打印原始表达式和答案。
    """

    def __init__(self):
        super().__init__('result_sub_node')

        # 订阅 /calculation_result 话题，队列深度 10
        self.subscription = self.create_subscription(
            CalculationResult,
            '/calculation_result',
            self.result_callback,
            10  # QoS 队列深度
        )

        self.get_logger().info('结果订阅节点启动，等待识别结果...')

    def result_callback(self, msg):
        """
        话题回调函数：
        收到 CalculationResult 消息后，在终端格式化输出。
        参数:
            msg: CalculationResult 消息，包含 raw_expression（原始表达式）和 result（计算结果）
        """
        # 格式化输出：去掉小数部分多余的 0
        if msg.result == int(msg.result):
            result_str = str(int(msg.result))
        else:
            result_str = str(msg.result)

        self.get_logger().info(
            f'识别到的原始表达式: {msg.raw_expression}, '
            f'计算结果: {result_str}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = ResultSubNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
