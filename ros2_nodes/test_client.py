import time

from rclpy.node import Node
from std_msgs.msg import Float64


class ROS2TestClient(Node):

    def __init__(self):

        super().__init__("ros2_test_client")

        self.received_messages = []

        self.publisher = self.create_publisher(
            Float64,
            "/joint_command",
            10
        )

        self.subscription = self.create_subscription(
            Float64,
            "/joint_feedback",
            self.feedback_callback,
            10
        )

    def feedback_callback(self, msg):

        self.received_messages.append(msg.data)

    def send_command(self, angle):

        msg = Float64()

        msg.data = float(angle)

        self.publisher.publish(msg)

    def wait_for_feedback(self, executor, timeout=2.0):

        deadline = time.monotonic() + timeout

        while time.monotonic() < deadline:

            executor.spin_once(timeout_sec=0.05)

            if self.received_messages:

                return self.received_messages[-1]

        raise TimeoutError(
            f"No feedback received within {timeout} seconds"
        )