from zaber_motion import Units, Library
from zaber_motion.ascii import Connection, Axis, AxisType
from enum import Enum

SERIAL_PORT = "COMx"

class Axes_List(Enum):
    AXIS_X = 1
    AXIS_Y = 2

AXIS_PORT = [Axes_List.AXIS_X.value, Axes_List.AXIS_Y.value]

class XYStage:
    """
    Definition of a 2-axis XY stage connected to a Zaber controller

    Attributes:

    """

    def __init__(self):
        self.connection = Connection.open_serial_port(SERIAL_PORT)
        self.device = self.connection.detect_devices()[0]
        self.axes = {}
        for port in AXIS_PORT:
            axis = self.device.get_axis(port)
            units = Units.ANGLE_DEGREES if axis.axis_type is AxisType.ROTARY else Units.LENGTH_MILLIMETRES
            limits = self._determine_relevant_stage_travel_limits(axis, units)
            self.axes[port] = {
                "axis": axis,
                "units": units,
                "limits": limits
            }
        print("Homing all axes of device with address {}.".format(device.device_address))
        self.device.all_axes.home()

    def _determine_relevant_stage_travel_limits(self, axis, units) -> tuple[float, float]:
        """
        Determine appropriate limits of stage travel to use as bounds for the slider.

        """
        limit_min = axis.settings.get("limit.min", units)
        limit_max = axis.settings.get("limit.max", units)
        return limit_min, limit_max

