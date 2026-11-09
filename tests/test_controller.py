from robot.controller import Robotcontroller
import pytest
@pytest.fixture
def robot():
    controller = Robotcontroller()
    controller.connect()
    yield controller
    controller.disconnect()

def test_move_without_connection():

    robot = Robotcontroller()

    with pytest.raises(RuntimeError):

        robot.move_joint(90)

def test_robot_controller(robot):

    assert robot.connected is True

#def test_robot_movement(robot):

 #   result = robot.move_joint(90)

  #  assert result is True

   # assert robot.get_position() == 90

@pytest.mark.parametrize(
    "angle",
    [-181, 181, -999, 999]
)

def test_invalid_angles(robot, angle):

    with pytest.raises(ValueError):

        robot.move_joint(angle)
