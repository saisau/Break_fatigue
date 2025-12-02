import time


class JITAIEngine:
    def __init__(self):
        self.last_break_time = 0
        self.min_interval_sec = 30 * 60  # 休憩間隔: 最低30分は空ける
        self.fatigue_history = []        # 直近の疲労判定履歴

    def decide_intervention(self, is_fatigued, current_time=None):
        """
        介入（休憩提案）を行うべきか判断する
        Return: (bool, string) -> (介入するか, 理由)
        """
        if current_time is None:
            current_time = time.time()

        # 1. クールダウン期間のチェック
        time_since_last = current_time - self.last_break_time
        if time_since_last < self.min_interval_sec:
            return False, "Cooldown period"

        # 2. 疲労状態のチェック
        # ノイズ対策: 「今回疲労」かつ「前回も疲労」の場合のみ提案（2回連続ルール）
        self.fatigue_history.append(is_fatigued)
        if len(self.fatigue_history) > 2:
            self.fatigue_history.pop(0)
            
        if len(self.fatigue_history) == 2 and all(self.fatigue_history):
            # 介入決定！
            self.last_break_time = current_time # 休憩したと仮定（実際はUIでYesを押した時だが簡易化）
            return True, "Fatigue detected continuously"
            
        return False, "Condition not met"


# 動作確認用
if __name__ == "__main__":
    engine = JITAIEngine()
    engine.min_interval_sec = 0 # テスト用に0秒に
    print(engine.decide_intervention(False)) # -> False
    print(engine.decide_intervention(True))  # -> False (1回目)
    print(engine.decide_intervention(True))  # -> True (2回連続)

