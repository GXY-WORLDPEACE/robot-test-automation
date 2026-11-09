class Robotcontroller:

    def __init__(self, hardware=None):

        self.connected = False

        self.position = 0

        self.hardware = hardware

    def connect(self):

        self.connected = True

        return True

    def move_joint(self, angle):

        if not self.connected:
            raise RuntimeError("Robot not connected")

        if not isinstance(angle, (int, float)) or isinstance(angle, bool):
            raise TypeError("Angle must be a number")

        if angle < -180 or angle > 180:
            raise ValueError("Angle out of range")

        if self.hardware is not None:

            result = self.hardware.send_command(angle)

            if result != "OK":
                raise RuntimeError("Hardware command failed")

        self.position = angle

        return True

    def get_position(self):

        return self.position

    def disconnect(self):

        self.connected = False