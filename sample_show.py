# display_vitality_images.py
# vitalityに応じて生成済みPNGを選択表示するスクリプト
# 必要なパッケージ:
#   pip install opencv-python

import os
import sys
import time
import glob
import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt

# OpenCVインポートと依存チェック
try:
    import cv2
except ModuleNotFoundError:
    messagebox.showerror(
        "Missing dependency",
        "OpenCVがインストールされていません。\n"
        "ターミナルで `pip install opencv-python` を実行してください。"
    )
    sys.exit(1)

# センサデータサンプル: True=人あり, False=人なし
# sensor_data = [True] * 50 + [False] * 30 + [True] * 40 + [False] * 60
# sin(wt)*cos(2wt)波で人の有無をシミュレート　0より大きい場合は人がいるとする
def generate_sensor_data(length=200, frequency=0.1):
    """
    センサデータを生成する関数
    :param length: int, データの長さ
    :param frequency: float, 周波数
    :return: list of bool, 人がいるかどうかのリスト
    """
    import numpy as np
    t = np.arange(length)
    data = np.sin(frequency * t) * np.cos(2 * frequency * t) * np.sin(2 * frequency * t)
    sample_data = [x > 0 for x in data]

    # sample_dataをグラフで表示 Trueの時は1, Falseの時は0
    data_for_plot = [1 if x else 0 for x in sample_data]
    plt.plot(t, data_for_plot, label='Sensor Data')
    plt.xlabel('Time')
    plt.ylabel('Presence (1=True, 0=False)')
    plt.title('Generated Sensor Data')
    plt.legend()
    plt.grid()
    plt.show()  # グラフを表示
    return sample_data

sensor_data = generate_sensor_data(200, frequency=0.1)

def detect_person(sample):
    """
    人検出関数（サンプルデータをそのまま返す）
    """
    return bool(sample)

class PersonState:
    def __init__(self):
        self.presence = False
        self.duration = 0.0  # 継続秒数

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
        self.decay_rate = 5.0    # 座り状態で1秒あたり減少量
        self.recover_rate = 3.0  # 立ち状態で1秒あたり回復量

    def update(self, presence, dt=1.0):
        if presence:
            self.vitality -= self.decay_rate * dt
        else:
            self.vitality += self.recover_rate * dt
        self.vitality = max(0.0, min(100.0, self.vitality))
        return self.vitality


def display_image_for_vitality(vitality, image_paths):
    """
    vitality(0-100) に応じて対応する画像を選び、表示
    """
    n = len(image_paths)
    # vitality 0→最小インデックス, 100→最大インデックス
    idx = int((vitality / 100.0) * (n - 1))
    path = image_paths[idx]
    img = cv2.imread(path)
    if img is None:
        return
    cv2.imshow('Flower Vitality', img)
    cv2.waitKey(1)


def main():
    # 画像フォルダ選択
    root = tk.Tk()
    root.withdraw()
    img_dir = filedialog.askdirectory(
        title="Select folder containing segment_XXX.png"
    )
    if not img_dir:
        messagebox.showinfo("No folder selected", "フォルダが選択されませんでした。終了します。")
        return

    # PNGファイルをソートしてリスト化
    image_paths = sorted(
        glob.glob(os.path.join(img_dir, 'segment_*.png'))
    )
    if not image_paths:
        messagebox.showerror("No images", "segment_*.png が見つかりませんでした。")
        return

    # シミュレーション
    person = PersonState()
    flower = FlowerState()
    dt = 1.0

    for t, sample in enumerate(sensor_data):
        presence = detect_person(sample)
        _, duration = person.update(presence, dt)
        vitality = flower.update(presence, dt)
        print(f"t={t*dt:.0f}s, presence={presence}, 継続時間={duration:.0f}s -> vital={vitality:.1f}")
        display_image_for_vitality(vitality, image_paths)
        time.sleep(0.1)

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
