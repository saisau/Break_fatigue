import subprocess
import time
import sys
import os


def main():
    print("🚀 研究用データ収集システムを起動します...")
    
    # Pythonの実行コマンド（環境によって 'python' か 'python3' か自動判定）
    python_cmd = sys.executable

    try:
        # 1. Recorder (記録係) をバックグラウンドで起動
        # stdout=subprocess.DEVNULL でコンソールにログを出さずに裏で静かに動かす
        recorder = subprocess.Popen([python_cmd, "recorder.py"])
        print(f"   ✅ Recorder Started (PID: {recorder.pid})")

        # 2. Monitor (監視・通知係) を起動
        monitor = subprocess.Popen([python_cmd, "monitor.py"])
        print(f"   ✅ Monitor Started (PID: {monitor.pid})")

        print("⚡ システム稼働中... (Ctrl+C で全停止)")
        
        # 親プロセスが終了しないように待機し続ける
        recorder.wait()
        monitor.wait()

    except KeyboardInterrupt:
        print("\n🛑 停止信号を受信しました。子プロセスを終了します...")
    finally:
        # 終了時に必ず子プロセスも道連れにして殺す（ゾンビプロセス防止）
        if 'recorder' in locals(): recorder.terminate()
        if 'monitor' in locals(): monitor.terminate()
        print("👋 システムを終了しました。")


if __name__ == "__main__":
    # カレントディレクトリをこのファイルの場所に固定（自動起動時のパスずれ防止）
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()

