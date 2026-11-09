import time

import pytest
import rclpy

from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor

from std_msgs.msg import Float64

from ros2_nodes.robot_node import RobotNode


@pytest.fixture
def ros2_environment():

    rclpy.init()

    robot_node = RobotNode()

    test_node = Node("test_node")

    executor = SingleThreadedExecutor()

    executor.add_node(robot_node)
    executor.add_node(test_node)

    yield robot_node, test_node, executor

    executor.remove_node(robot_node)
    executor.remove_node(test_node)

    executor.shutdown()

    robot_node.destroy_node()
    test_node.destroy_node()

    rclpy.shutdown()


def test_joint_command(ros2_environment):

    robot_node, test_node, executor = ros2_environment

    received_messages = []

    publisher = test_node.create_publisher(
        Float64,
        "/joint_command",
        10
    )

    subscription = test_node.create_subscription(
        Float64,
        "/joint_feedback",
        lambda msg: received_messages.append(msg.data),
        10
    )

    # 等待 ROS2 Publisher / Subscriber 完成发现
    deadline = time.monotonic() + 5.0

    while time.monotonic() < deadline:

        if (
            publisher.get_subscription_count() > 0
            and robot_node.publisher.get_subscription_count() > 0
        ):
            break

        executor.spin_once(timeout_sec=0.1)

    assert publisher.get_subscription_count() > 0
    assert robot_node.publisher.get_subscription_count() > 0

    command = Float64()
    command.data = 90.0

    publisher.publish(command)

    deadline = time.monotonic() + 5.0

    while time.monotonic() < deadline:

        executor.spin_once(timeout_sec=0.1)

        if received_messages:
            break

    assert received_messages

    assert received_messages[0] == pytest.approx(90.0)