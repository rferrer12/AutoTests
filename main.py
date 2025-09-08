from zaber_motion import *
from zaber_motion import Units
from zaber_motion.ascii import Connection

with Connection.open_serial_port("COM3") as connection:
    connection.enable_alerts()

    device_list = connection.detect_devices()
    print("Found {} devices".format(len(device_list)))

    device = device_list[0]

    axisY = device.get_axis(1)
    axisX = device.get_axis(2)
    if not axisY.is_homed() and not axisX.is_homed():
      axisY.home()
      axisX.home()

    # Move to 10mm
    axisY.move_absolute(10, Units.LENGTH_MILLIMETRES)

    # Move by an additional 5mm
    axisX.move_absolute(5, Units.LENGTH_MILLIMETRES)
