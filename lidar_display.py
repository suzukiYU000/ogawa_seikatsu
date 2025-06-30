import os
import sys
import time
import glob
from collections import deque
import tkinter as tk
from tkinter import filedialog, messagebox

try:
    import cv2
except ModuleNotFoundError:
    messagebox.showerror(
        "Missing dependency",
        "OpenCVがインストールされていません。\n"
        "ターミナルで `pip install opencv-python` を実行してください。",
    )
    sys.exit(1)

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

# ---- Detection parameters ----
NEAR_CM = 10.0     # minimum distance considered (cm)
FAR_CM = 60.0      # maximum distance considered as presence (cm)
HUNCHED_CM = 30.0  # below this value indicates hunched posture
WINDOW_SIZE = 5    # moving average window size


def classify_distance(dist_cm):
    """Return presence flag and hunched flag for a smoothed distance."""
    if dist_cm is None or dist_cm >= FAR_CM:
        return False, False
    if dist_cm >= NEAR_CM:
        presence = True
        hunched = dist_cm <= HUNCHED_CM
        return presence, hunched
    # below NEAR_CM is treated as no measurement
    return False, False


class PersonState:
    def __init__(self):
        self.presence = False
        self.duration = 0.0

    def update(self, presence, dt=1.0):
        if presence == self.presence:
            self.duration += dt
        else:
            self.presence = presence
            self.duration = dt
        return self.presence, self.duration


class FlowerState:
    def __init__(self, vitality=100.0):
        self.vitality = vitality
        self.decay_rate = 5.0
        self.recover_rate = 3.0

    def update(self, presence, dt=1.0):
        if presence:
            self.vitality -= self.decay_rate * dt
        else:
            self.vitality += self.recover_rate * dt
        self.vitality = max(0.0, min(100.0, self.vitality))
        return self.vitality


def display_image_for_vitality(vitality, image_paths):
    """Display an image chosen according to vitality."""
    n = len(image_paths)
    idx = int((vitality / 100.0) * (n - 1))
    path = image_paths[idx]
    img = cv2.imread(path)
    if img is not None:
        cv2.imshow('Lidar Display', img)
        cv2.waitKey(1)

def ask_image_folder():
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Select folder containing segment_XXX.png")
    root.destroy()
    if not folder:
        messagebox.showinfo("No folder selected", "フォルダが選択されませんでした。プログラムを終了します。")
        sys.exit(1)
    return folder


def load_image_paths(img_dir):
    paths = sorted(glob.glob(os.path.join(img_dir, 'segment_*.png')))
    if not paths:
        messagebox.showerror("No images", "segment_*.png が見つかりませんでした。")
        sys.exit(1)
    return paths


def main():
    img_dir = ask_image_folder()
    image_paths = load_image_paths(img_dir)
    cv2.namedWindow('Lidar Display', cv2.WINDOW_AUTOSIZE)

    ydlidar.os_init()
    ports = ydlidar.lidarPortList()
    port = '/dev/ydlidar'
    for p in ports.values():
        port = p
    print(f"Use lidar port: {port}")

    laser = ydlidar.CYdLidar()
    laser.setlidaropt(ydlidar.LidarPropSerialPort, port)
    laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 921600)
    laser.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
    laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_GS)
    laser.setlidaropt(ydlidar.LidarPropFixedResolution, True)
    laser.setlidaropt(ydlidar.LidarPropSupportMotorDtrCtrl, False)
    laser.setlidaropt(ydlidar.LidarPropSupportHeartBeat, False)

    history = deque(maxlen=WINDOW_SIZE)
    person = PersonState()
    flower = FlowerState()
    dt = 0.05

    try:
        _ = laser.initialize()
        _ = laser.turnOn()
        scan = ydlidar.LaserScan()

        while ydlidar.os_isOk():
            success = laser.doProcessSimple(scan)
            distance_cm = None
            if success:
                valid = [pt.range for pt in scan.points if pt.range >= 0.05]
                if len(valid) >= 5:
                    nearest5 = sorted(valid)[:5]
                    distance_cm = (sum(nearest5) / 5) * 100.0
                    history.append(distance_cm)
            else:
                sys.stderr.write("Failed to get Lidar Data\n")

            smooth_cm = sum(history) / len(history) if history else None
            presence, hunched = classify_distance(smooth_cm)
            person.update(presence, dt)
            vitality = flower.update(presence, dt)

            display_image_for_vitality(vitality, image_paths)

            if smooth_cm is not None:
                print(
                    f"dist={smooth_cm:.1f}cm presence={presence} hunched={hunched} vital={vitality:.1f}"
                )
            else:
                print(f"no data presence={presence} vital={vitality:.1f}")

            time.sleep(dt)

        laser.turnOff()
    finally:
        laser.disconnecting()
        ydlidar.os_shutdown()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
