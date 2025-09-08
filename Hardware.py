from zaber_motion import Units, Library
from zaber_motion.ascii import Connection, Axis, AxisType

SERIAL_PORT = "COMx"
AXIS_X = 1
AXIS_Y = 2

class XYStage:
    """
    Definition of a 2-axis XY stage connected to a Zaber controller

    Attributes:

    """

    def __init__(self):
        connection = Connection.open_serial_port(SERIAL_PORT)
        devices = connection.detect_devices()
        axisX = devices[0].get_axis(AXIS_X)
        axisX_units = (
            Units.ANGLE_DEGREES if axisX.axis_type is AxisType.ROTARY else Units.LENGTH_MILLIMETRES
        )
        axisY = devices[1].get_axis(AXIS_Y)
        axisY_units = (
            Units.ANGLE_DEGREES if axisY.axis_type is AxisType.ROTARY else Units.LENGTH_MILLIMETRES
        )

