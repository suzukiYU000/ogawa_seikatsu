# split_video_segments.py
# 動画を100個のPNG画像に分割し、Figures/flower_Nフォルダに保存する (OpenCV版)
# 必要なパッケージ:
#   pip install opencv-python

import os
import re
import math
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

# OpenCVのインポートと依存チェック
try:
    import cv2
except ModuleNotFoundError:
    messagebox.showerror(
        "Missing dependency",
        "OpenCVがインストールされていません。\n"
        "ターミナルで `pip install opencv-python` を実行してから再度お試しください。"
    )
    sys.exit(1)


def get_next_folder_number(base_dir, prefix='flower_'):
    """
    base_dir 内で prefix + 数字 のフォルダを調べ、存在しない最大の番号+1 を返す
    """
    os.makedirs(base_dir, exist_ok=True)
    existing = [d for d in os.listdir(base_dir)
                if os.path.isdir(os.path.join(base_dir, d)) and d.startswith(prefix)]
    numbers = []
    for d in existing:
        m = re.match(rf'{re.escape(prefix)}(\d+)$', d)
        if m:
            numbers.append(int(m.group(1)))
    return max(numbers) + 1 if numbers else 1


def extract_frames_as_png(video_path, output_dir, segments=100):
    """
    OpenCVを使ってvideo_pathを読み込み、segments個の代表フレームをPNGでoutput_dirに保存する
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise IOError(f"Cannot open video file: {video_path}")

    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step = frame_count / segments

    for i in range(segments):
        frame_idx = int(i * step)
        if frame_idx >= frame_count:
            break
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            continue

        filename = f'segment_{i+1:03d}.png'
        output_path = os.path.join(output_dir, filename)
        print(f'Saving frame {i+1} (frame {frame_idx}) to {output_path}')
        cv2.imwrite(output_path, frame)

    cap.release()


def main():
    # tkinterダイアログを非表示にしてファイル選択のみを表示
    root = tk.Tk()
    root.withdraw()
    video_path = filedialog.askopenfilename(
        title="Select video file",
        filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv"), ("All files", "*.*")],
        
    )
    if not video_path:
        messagebox.showinfo("No file selected", "No video file was selected. Exiting.")
        return

    base_dir = 'Figures'
    folder_number = get_next_folder_number(base_dir, prefix='flower_')
    output_dir = os.path.join(base_dir, f'flower_{folder_number}')
    os.makedirs(output_dir, exist_ok=True)

    try:
        extract_frames_as_png(video_path, output_dir, segments=100)
        messagebox.showinfo("Done", f"Videoから100枚のPNGを保存しました:\n{output_dir}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")


if __name__ == '__main__':
    main()
