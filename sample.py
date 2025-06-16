import time

# サンプル用センサデータ: True=人あり, False=人なし
sensor_data = [True] * 150 + [False] * 30 + [True] * 40 + [False] * 60

def detect_person(sample):
    """
    人検出関数
    :param sample: センササンプル（True/False）
    :return: bool
    """
    # サンプルデータをそのまま返す
    return bool(sample)

class PersonState:
    def __init__(self):
        self.presence = False
        self.duration = 0.0  # 継続秒数

    def update(self, presence, dt=1.0):
        """
        人の状態管理
        :param presence: bool, 人がいるか
        :param dt: float, 経過時間(秒)
        :return: self.presence, self.duration
        """
        if presence == self.presence:
            self.duration += dt
        else:
            self.presence = presence
            self.duration = dt
        return self.presence, self.duration

class FlowerState:
    def __init__(self, vitality=100.0):
        self.vitality = vitality  # 元気度 (0-100)
        # 毎秒の減衰・回復率
        self.decay_rate = 5.0    # 座り状態で1秒あたり減少量
        self.recover_rate = 3.0  # 立ち状態で1秒あたり回復量

    def update(self, presence, dt=1.0):
        """
        花の状態管理
        :param presence: bool, 人がいるか
        :param dt: float, 経過時間(秒)
        :return: vitality: float
        """
        if presence:
            # 人が座っている → 枯れる
            self.vitality -= self.decay_rate * dt
        else:
            # 人がいない → 回復
            self.vitality += self.recover_rate * dt

        # clamp
        self.vitality = max(0.0, min(100.0, self.vitality))
        return self.vitality


def display_flower_state(vitality):
    """
    花の状態表示
    :param vitality: float, 元気度
    :return: None
    """
    print(f"花の元気度: {vitality:.1f}/100")


def simulate(data, dt=1.0):
    person = PersonState()
    flower = FlowerState()

    for t, sample in enumerate(data):
        presence = detect_person(sample)
        _, duration = person.update(presence, dt)
        vitality = flower.update(presence, dt)
        print(f"t={t*dt:.0f}s, presence={presence}, 継続時間={duration:.0f}s -> ", end="")
        display_flower_state(vitality)
        time.sleep(0.1)  # デモ用に少し待つ


if __name__ == '__main__':
    simulate(sensor_data)
