from PyQt6.uic.Compiler.misc import Literal
from zaber_motion import Units, Library
from zaber_motion.ascii import Connection, Axis, AxisType
from enum import Enum
import Constants

class Axes_List(Enum):
    AXIS_X = 1
    AXIS_Y = 2

AXIS_PORT = [Axes_List.AXIS_X.value, Axes_List.AXIS_Y.value]

Library.enable_device_db_store()

class XYStage:
    """
    Definition of a 2-axis XY stage connected to a Zaber controller

    Attributes:

    """
    units = None
    def __init__(self, connection_port: str):
        #self.connection = Connection.open_serial_port(connection_port)
        self.connection = Connection.open_iot("a1fa4d66-25a0-48f5-9fd9-10a2d3161dbf")
        self.device_list = self.connection.detect_devices()
        print("Found {} devices".format(len(self.device_list)))
        self.axes = {}
        for device in self.device_list:
            for i in range(device.axis_count):
                axis = device.get_axis(i+1)
                if axis.axis_type is AxisType.ROTARY:
                    units = Units.ANGLE_DEGREES
                else:
                    units = Units.LENGTH_MILLIMETRES
                limits = self._determine_relevant_stage_travel_limits(axis, units)
                self.axes[i] = {
                    "axis": axis,
                    "units": units,
                    "limits": limits
                }
        """
        print(")Homing all axes of device with address {}.".format(device.device_address))
        self.device.all_axes.home()
        """

    def _determine_relevant_stage_travel_limits(self, axis: Axis, units) -> tuple[float, float]:
        """
        Determine appropriate limits of stage travel to use as bounds for the slider.

        """
        limit_min = axis.settings.get("limit.min", units)
        limit_max = axis.settings.get("limit.max", units)
        return limit_min, limit_max

    def move_to(self, axis_num: int, abs_pos: float, move_vel: float):
        if abs_pos > self.axes[axis_num]["limits"][1]:
            pos = self.axes[axis_num]["limits"][1]
        elif abs_pos < self.axes[axis_num]["limits"][0]:
            pos = self.axes[axis_num]["limits"][0]
        else:
            pos = abs_pos
        vel = move_vel
        axis = self.axes[axis_num].get("axis")
        print("Moving axis {} to position {}".format(axis, pos))
        axis.move_absolute(pos, unit = Units.LENGTH_MILLIMETRES)

    def stop_move(self):
        for i in self.axes:
            axis = self.axes[i].get("axis")
            axis.stop()

    def home_all_axes(self):
        for device in self.device_list:
            print("Homing all axes of device with address {}.".format(device.device_address))
        self.connection.home_all()
