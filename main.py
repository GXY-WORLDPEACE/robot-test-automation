from robot.controller import Robotcontroller
from robot.hardware import RobotHardware

hardware = RobotHardware()
robot = Robotcontroller(hardware)

robot.connect()
robot.move_joint(90)

print("Robot position:", robot.get_position())  # Output: 90
robot.disconnect()

