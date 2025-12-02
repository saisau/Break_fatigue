import tkinter as tk
import threading
from feedback import log_feedback


class FeedbackWindow:
    def __init__(self, message, features):
        self.features = features
        self.root = tk.Tk()
        self.root.title("Fatigue Check")
        
        # UIセットアップ
        self._setup_window()
        self._create_widgets(message)
        
        # 20秒放置で自動消滅（作業の邪魔をしないため少し延長）
        self.root.after(20000, self.root.destroy)
        self.root.mainloop()

    def _setup_window(self):
        w, h = 400, 180  # ボタンが増えるので少し横長に
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = screen_w - w - 20
        y = screen_h - h - 60
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.attributes('-topmost', True)
        self.root.configure(bg="#f9f9f9")

    def _create_widgets(self, message):
        # 質問文
        lbl = tk.Label(self.root, text=f"今の「精神的疲労感」は？\n(1:元気 〜 5:限界)", 
                       font=("Meiryo", 11), bg="#f9f9f9", pady=15)
        lbl.pack()

        # ボタンを配置するフレーム
        btn_frame = tk.Frame(self.root, bg="#f9f9f9")
        btn_frame.pack(pady=5)

        # 1〜5のボタンをループで作る
        # 色のグラデーション: 緑(元気) -> 黄 -> 赤(疲労)
        colors = ["#e6ffe6", "#f2ffe6", "#ffffcc", "#ffe6cc", "#ffcccc"]
        labels = ["1\n元気", "2", "3\n普通", "4", "5\n限界"]

        for i in range(5):
            score = i + 1
            btn = tk.Button(
                btn_frame, 
                text=labels[i],
                bg=colors[i],
                width=6, height=2,
                # lambdaを使って、クリック時にそのスコア(score)を渡す
                command=lambda s=score: self._on_click(s)
            )
            btn.pack(side=tk.LEFT, padx=4)

    def _on_click(self, score):
        # 評価を保存して閉じる
        log_feedback(score, self.features)
        self.root.destroy()


def show_interactive_popup(message, features):
    threading.Thread(target=FeedbackWindow, args=(message, features), daemon=True).start()


if __name__ == "__main__":
    # デザイン確認用
    show_interactive_popup("テスト通知", {})
    import time
    time.sleep(10)
