import time

import pytest
import rclpy

from rclpy.executors import SingleThreadedExecutor

from ros2_nodes.robot_node import RobotNode
from ros2_nodes.test_client import ROS2TestClient


@pytest.fixture
def test_system(request):

    failure_mode = getattr(
        request,
        "param",
        "normal"
    )

    rclpy.init()

    robot = RobotNode(failure_mode=failure_mode)

    client = ROS2TestClient()

    executor = SingleThreadedExecutor()

    executor.add_node(robot)
    executor.add_node(client)

    # 等待 Publisher 和 Subscriber 完成发现
    deadline = time.monotonic() + 5.0

    while time.monotonic() < deadline:

        if (
            client.publisher.get_subscription_count() > 0
            and robot.publisher.get_subscription_count() > 0
        ):
            break

        executor.spin_once(timeout_sec=0.1)

    try:

        assert client.publisher.get_subscription_count() > 0
        assert robot.publisher.get_subscription_count() > 0

        yield robot, client, executor

    finally:

        executor.remove_node(robot)
        executor.remove_node(client)

        executor.shutdown()

        robot.destroy_node()
        client.destroy_node()

        rclpy.shutdown()


def test_normal_feedback(test_system):

    robot, client, executor = test_system

    client.send_command(90)

    feedback = client.wait_for_feedback(
        executor,
        timeout=2.0
    )

    assert feedback == pytest.approx(90.0)


@pytest.mark.parametrize(
    "test_system",
    ["timeout"],
    indirect=True
)

def test_feedback_timeout(test_system):

    robot, client, executor = test_system

    client.send_command(90)

    with pytest.raises(TimeoutError):

        client.wait_for_feedback(
            executor,
            timeout=0.5
        )


@pytest.mark.parametrize(
    "test_system",
    ["wrong_feedback"],
    indirect=True
)
def test_wrong_feedback(test_system):

    robot, client, executor = test_system

    client.send_command(90)

    feedback = client.wait_for_feedback(
        executor,
        timeout=2.0
    )

    assert feedback != pytest.approx(90.0)

    assert feedback == pytest.approx(45.0)