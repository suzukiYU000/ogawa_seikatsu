
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
    """Fetch and print the average of the 5 nearest points ≥ 5 cm from a GS-series YDLidar."""
    # 初期化
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
    laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_GS)
    laser.setlidaropt(ydlidar.LidarPropFixedResolution, True)
    laser.setlidaropt(ydlidar.LidarPropSupportMotorDtrCtrl, False)
    laser.setlidaropt(ydlidar.LidarPropSupportHeartBeat, False)

    try:
        # 初期化／ヘルスチェック（結果に関わらずスキャン開始）
        _ = laser.initialize()
        _ = laser.turnOn()
        scan = ydlidar.LaserScan()

        while ydlidar.os_isOk():
            success = laser.doProcessSimple(scan)
            if success:
                # 5cm以上の点を抽出
                valid_ranges = [pt.range for pt in scan.points if pt.range >= 0.05]
                # 点数が5点以上あれば平均を計算
                if len(valid_ranges) >= 5:
                    nearest5 = sorted(valid_ranges)[:5]
                    average = sum(nearest5) / 5
                    print(f"Average of 5 nearest points (>=5cm): {average:.3f} m")
                else:
                    # 点数不足時はスキップ
                    pass
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
