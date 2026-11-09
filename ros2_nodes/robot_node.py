import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

class RobotNode(Node):
    def __init__(self, failure_mode="normal"):

        super().__init__('robot_node')
        
        self.failure_mode = failure_mode

        self.publisher = self.create_publisher(
            Float64, 
            'joint_feedback', 
            10)

        self.subscription = self.create_subscription(
            Float64,
            '/joint_command',
            self.command_callback,
            10)

    def command_callback(self, msg):

        angle = msg.data

        self.get_logger().info(
            f"Received command: {angle}"
        )

        # 故障模式1：不返回反馈
        if self.failure_mode == "timeout":

            self.get_logger().warning(
                "Simulating timeout: no feedback"
            )

            return

        feedback = Float64()

        # 故障模式2：返回错误反馈
        if self.failure_mode == "wrong_feedback":

            feedback.data = angle / 2

        # 正常模式
        else:

            feedback.data = angle

        self.publisher.publish(feedback)

#       feedback = Float64()
#
#        feedback.data = angle

#       self.publisher.publish(feedback)


def main():

    rclpy.init()

    node = RobotNode()

    try:
        rclpy.spin(node)

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
