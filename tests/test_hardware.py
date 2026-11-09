from robot.controller import Robotcontroller
from robot.hardware import RobotHardware

def test_robot_hardware_command(mocker):
    hardware = RobotHardware()
    fake_send = mocker.patch.object(hardware, 'send_command', return_value="OK")
    robot = Robotcontroller(hardware)
    robot.connect()
    result = robot.move_joint(90)
    assert result is True
    fake_send.assert_called_once_with(90)