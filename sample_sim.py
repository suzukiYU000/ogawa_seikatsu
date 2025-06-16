import os
import sys
import math
import csv
import glob
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE
import tkinter as tk
from tkinter import filedialog, messagebox
import cv2

# ---- 設定パラメータ ----
SCREEN_SIZE   = (800, 600)
BG_COLOR      = (30, 30, 30)
PERSON_COLOR  = (200, 200, 50)
FLOWER_COLOR  = (50, 200, 200)
PERSON_RADIUS = 15
FLOWER_POS    = (SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2)
THRESHOLD     = 150   # ピクセル距離での閾値
MOVE_SPEED    = 200   # px/秒
FPS           = 30

def ask_image_folder():
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="Select folder containing segment_XXX.png")
    root.destroy()
    if not folder:
        messagebox.showinfo("No folder selected", "フォルダが選択されませんでした。プログラムを終了します。")
        sys.exit(1)
    return folder

def load_vitality_paths(img_dir):
    paths = sorted(glob.glob(os.path.join(img_dir, 'segment_*.png')))
    if not paths:
        messagebox.showerror("No images", "segment_*.png が見つかりませんでした。")
        sys.exit(1)
    return paths

# 状態管理クラス
class PersonState:
    def __init__(self):
        self.presence = False
        self.duration = 0.0
    def update(self, presence, dt):
        if presence == self.presence:
            self.duration += dt
        else:
            self.presence = presence
            self.duration = dt
        return self.presence, self.duration

class FlowerState:
    def __init__(self, vitality=100.0):
        self.vitality = vitality
        self.decay_rate   = 10.0
        self.recover_rate = 10.0
    def update(self, presence, dt):
        if presence:
            self.vitality -= self.decay_rate * dt
        else:
            self.vitality += self.recover_rate * dt
        self.vitality = max(0.0, min(100.0, self.vitality))
        return self.vitality

def main():
    # 1) 画像フォルダ選択
    img_dir = ask_image_folder()
    # 2) vitality用ファイルパス一覧
    vitality_paths = load_vitality_paths(img_dir)
    # 3) OpenCV で一括読み込み（PNG透過対応）
    cv2_images = [cv2.imread(p, cv2.IMREAD_UNCHANGED) for p in vitality_paths]
    # 4) OpenCV ウィンドウを準備
    cv2.namedWindow('Flower Vitality', cv2.WINDOW_AUTOSIZE)

    # Pygame 初期化
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Control Window")
    clock = pygame.time.Clock()

    person = PersonState()
    flower = FlowerState()
    px, py = 100, 100

    sensor_data = []
    time_log    = []
    total_time  = 0.0
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0
        total_time += dt

        # イベント処理
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                running = False

        # 矢印キーで移動
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  px -= MOVE_SPEED * dt
        if keys[pygame.K_RIGHT]: px += MOVE_SPEED * dt
        if keys[pygame.K_UP]:    py -= MOVE_SPEED * dt
        if keys[pygame.K_DOWN]:  py += MOVE_SPEED * dt

        # 距離→Presence判定
        dist = math.hypot(px - FLOWER_POS[0], py - FLOWER_POS[1])
        presence = (dist <= THRESHOLD)
        _, duration = person.update(presence, dt)
        vitality = flower.update(presence, dt)

        # センサーデータ記録
        sensor_data.append(presence)
        time_log.append(total_time)

        # --- コントロール画面の描画 ---
        screen.fill(BG_COLOR)
        # 閾値円
        pygame.draw.circle(screen, (80, 80, 80), FLOWER_POS, THRESHOLD, 1)
        # 花と人
        pygame.draw.circle(screen, FLOWER_COLOR, FLOWER_POS, 20)
        pygame.draw.circle(screen, PERSON_COLOR, (int(px), int(py)), PERSON_RADIUS)
        # ステータス表示
        font = pygame.font.SysFont(None, 24)
        txt = f"t={total_time:.1f}s  presence={presence}  dur={duration:.1f}s  vital={vitality:.1f}"
        screen.blit(font.render(txt, True, (255,255,255)), (10, SCREEN_SIZE[1]-30))
        pygame.display.flip()

        # --- 画像のみウィンドウへの表示（OpenCV）---
        idx = int((vitality / 100.0) * (len(cv2_images) - 1))
        img = cv2_images[idx]

        
        cv2.imshow('Flower Vitality', img)
        cv2.waitKey(1)

    # 終了処理
    pygame.quit()
    cv2.destroyAllWindows()

    # CSV出力
    out_csv = 'sensor_data.csv'
    with open(out_csv, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['time(sec)', 'presence(1=True)'])
        for t, p in zip(time_log, sensor_data):
            w.writerow([f"{t:.3f}", int(p)])
    print(f"Recorded sensor data → {out_csv}")

if __name__ == '__main__':
    main()
