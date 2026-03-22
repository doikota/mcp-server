# src/utils/profiler.py
import cProfile
import pstats
from contextlib import contextmanager
from pathlib import Path

@contextmanager
def profile(name="profile", top_n=10):
    """コードのプロファイリングを行うコンテキストマネージャー

    Args:
        name: プロファイル結果のファイル名
        top_n: 表示する上位N個の結果
    """
    profiler = cProfile.Profile()
    profiler.enable() # 計測開始

    try:
        yield profiler # ← with ブロックの中身がここで実行される
    finally:
        profiler.disable() # 計測終了（必ず実行される）

        # 結果の集計
        stats = pstats.Stats(profiler)
        stats.strip_dirs()              # ファイルパスを短く整形
        stats.sort_stats('cumulative')  # 累積時間順で並べ替え

        # コンソールに出力
        print(f"\n=== Performance Profile: {name} ===")
        stats.print_stats(top_n)  # 上位n件をコンソールに表示

        # ファイルに保存（詳細分析用）
        profile_dir = Path("profiles")
        profile_dir.mkdir(exist_ok=True)
        stats.dump_stats(profile_dir / f"{name}.prof")

# テストコード
if __name__ == "__main__":
    import time

    with profile("test_profile"):
        # サンプルの重い処理
        total = 0
        for i in range(1000000):
            total += i
        time.sleep(1)  # シミュレーションのための遅延

    print(f"Total: {total}")