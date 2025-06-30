import time
import sys

try:
    import ydlidar
except ModuleNotFoundError:
    sys.stderr.write(
        "YDLidar python bindings are not installed.\n"
        "Create a virtual environment and install them with:\n"
        "  python3 -m venv .venv\n"
        "  . .venv/bin/activate\n"
        "  pip install ./YDLidar-SDK\n"
    )
    sys.exit(1)


def main():
    """Fetch and print scan data from a GS-series YDLidar (e.g., GS5)."""
    ydlidar.os_init()
    ports = ydlidar.lidarPortList()
    port = "/dev/ydlidar"
    for p in ports.values():
        port = p
    print(f"Use lidar port: {port}")

    laser = ydlidar.CYdLidar()
    # 通信設定
    laser.setlidaropt(ydlidar.LidarPropSerialPort, port)
    laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 921600)
    laser.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)

    # GS5モデル向け設定
    laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_GS)            # GS系列プロトコル
    laser.setlidaropt(ydlidar.LidarPropFixedResolution, True)                  # 固定角度分解能
    laser.setlidaropt(ydlidar.LidarPropSupportMotorDtrCtrl, False)            # モーター制御チェックをスキップ
    laser.setlidaropt(ydlidar.LidarPropSupportHeartBeat, False) 
    # Unsupported checks for GS5
    laser.setlidaropt(ydlidar.LidarPropSupportMotorDtrCtrl, False)            # モーター制御チェックをスキップ
    laser.setlidaropt(ydlidar.LidarPropSupportHeartBeat, False)               # ハートビートチェックをスキップ
    laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_GS)
    laser.setlidaropt(ydlidar.LidarPropFixedResolution, True)                  # 固定角度分解能

    try:
        # initialize／health checkは通らない場合があるため、結果にかかわらずスキャン開始を試みる
        _ = laser.initialize()
        _ = laser.turnOn()
        scan = ydlidar.LaserScan()
        while ydlidar.os_isOk():
            success = laser.doProcessSimple(scan)
            if success:
                print(f"Scan received[{scan.stamp}]: {scan.points.size()} points")
                for pt in scan.points:
                    print(f" angle: {pt.angle:.2f} deg  range: {pt.range:.3f} m")
            else:
                sys.stderr.write("Failed to get Lidar Data\n")
            time.sleep(0.05)
        # スキャン停止
        laser.turnOff()
    finally:
        laser.disconnecting()
        ydlidar.os_shutdown()


if __name__ == "__main__":
    main()
