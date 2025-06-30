import time
import sys
import math
import matplotlib.pyplot as plt

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
    """Fetch scan data at hardware 10 Hz but:
       – plot at 0.5 Hz
       – skip any point where range == 0.0 (no print, no plot)
    """
    ydlidar.os_init()

    port = "/dev/ttyUSB0"
    print(f"Use lidar port: {port}")

    laser = ydlidar.CYdLidar()
    # --- 通信設定 ---
    laser.setlidaropt(ydlidar.LidarPropSerialPort, port)
    laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 921600)
    laser.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
    # --- GS5 固有設定 ---
    laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_GS)
    #laser.setlidaropt(ydlidar.LidarPropProtocolVersion, 2)
    laser.setlidaropt(ydlidar.LidarPropFixedResolution, True)
    laser.setlidaropt(ydlidar.LidarPropScanFrequency, 10.0)
    laser.setlidaropt(ydlidar.LidarPropSampleRate, 4)
    # laser.setlidaropt(ydlidar.LidarPropEnableCorrection, True)
    for prop in (
        ydlidar.LidarPropSupportMotorDtrCtrl,
        ydlidar.LidarPropSupportHeartBeat
        #ydlidar.LidarPropSupportZero,
        # ydlidar.LidarPropSupportInversion,
        #ydlidar.LidarPropSupportRotation,
        #ydlidar.LidarPropSupportModule,
        #ydlidar.LidarPropSupportBaseplate,
        #ydlidar.LidarPropSupportDebug,
    ):
        laser.setlidaropt(prop, False)

    try:
        laser.initialize()
        laser.turnOn()
        scan = ydlidar.LaserScan()

        # === matplotlib 非ブロッキング描画準備 ===
        plt.ion()
        fig, ax = plt.subplots(figsize=(6,6))
        plt.show(block=False)
        ax.set_aspect("equal")
        ax.set_xlabel("X [m]")
        ax.set_ylabel("Y [m]")

        last_plot = time.time()
        plot_interval = 2.0  # 秒 (0.5 Hz)

        while ydlidar.os_isOk():
            if not laser.doProcessSimple(scan):
                time.sleep(0.05)
                continue

            now = time.time()
            if now - last_plot < plot_interval:
                continue

            # 0.0m の点は完全に無視（リストにも追加せず、プリントもしない）
            valid_points = [p for p in scan.points if p.range >= 0.1]
            if not valid_points:
                last_plot = now
                continue

            # ヘッダーだけ一度プリント
            print(f"Scan received[{scan.stamp}]: {len(valid_points)} points")
            # 個々の点をプリント（range==0 はここに来ない）
            for p in valid_points:
                print(f"  angle: {p.angle:.2f} deg  range: {p.range:.3f} m")

            # 極座標→直交座標
            xs = [p.range * math.cos(math.radians(p.angle)) for p in valid_points]
            ys = [p.range * math.sin(math.radians(p.angle)) for p in valid_points]

            # 描画更新
            ax.clear()
            ax.scatter(xs, ys, s=5)
            ax.set_xlim(-1, 1)
            ax.set_ylim(-0.01, 0.5)
            ax.set_aspect("equal")
            ax.set_title(f"点数: {len(xs)}  {time.strftime('%H:%M:%S')}")
            fig.canvas.draw()
            fig.canvas.flush_events()

            last_plot = now

        laser.turnOff()

    finally:
        laser.disconnecting()
        ydlidar.os_shutdown()
        plt.ioff()
        plt.show()


if __name__ == "__main__":
    main()
