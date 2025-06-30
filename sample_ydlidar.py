import time
import sys

try:
    import ydlidar
except ModuleNotFoundError:
    sys.stderr.write(
        "YDLidar python bindings are not installed.\n"
        "Build and install them with:\n"
        "  cd YDLidar-SDK && python3 setup.py install\n"
    )
    sys.exit(1)


def main():
    """Fetch and print scan data from YDLidar."""
    ydlidar.os_init()
    ports = ydlidar.lidarPortList()
    port = "/dev/ydlidar"
    for p in ports.values():
        port = p
    print(f"Use lidar port: {port}")

    laser = ydlidar.CYdLidar()
    laser.setlidaropt(ydlidar.LidarPropSerialPort, port)
    laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 230400)
    laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TRIANGLE)
    laser.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
    laser.setlidaropt(ydlidar.LidarPropScanFrequency, 10.0)
    laser.setlidaropt(ydlidar.LidarPropSampleRate, 9)
    laser.setlidaropt(ydlidar.LidarPropSingleChannel, False)

    try:
        if laser.initialize() and laser.turnOn():
            scan = ydlidar.LaserScan()
            while ydlidar.os_isOk():
                success = laser.doProcessSimple(scan)
                if success:
                    print(f"Scan received[{scan.stamp}]: {scan.points.size()} points")
                    for pt in scan.points:
                        print(f" angle: {pt.angle:.2f} deg  range: {pt.range:.3f} m")
                else:
                    print("Failed to get Lidar Data")
                time.sleep(0.05)
            laser.turnOff()
    finally:
        laser.disconnecting()
        ydlidar.os_shutdown()


if __name__ == "__main__":
    main()
