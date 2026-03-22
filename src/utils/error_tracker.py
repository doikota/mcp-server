# src/utils/error_tracker.py
from datetime import datetime
from typing import Dict, List, Any
import json
import traceback
import logging_config

class ErrorTracker:
    """エラーの追跡と分析のためのクラス"""

    def __init__(self):
        self.errors: List[Dict[str, Any]] = []
        self.error_counts: Dict[str, int] = {}

    def log_error(self, error: Exception, context: Dict[str, Any]) -> None:
        """エラーを記録し、統計情報を更新"""
        error_type = type(error).__name__

        # エラー情報の構造化
        error_info = {
            "timestamp": datetime.now().isoformat(),
            "type": error_type,
            "message": str(error),
            "context": context,
            "stack_trace": traceback.format_exc()
        }

        # エラーリストに追加
        self.errors.append(error_info)

        # エラーカウントの更新
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1

        # ログに記録
        logger = logging_config.setup_logging()
        logger.error(f"Error tracked: {json.dumps(error_info, indent=2)}")

        # 特定のエラーが頻発している場合は警告
        if self.error_counts[error_type] > 10:
            logger.critical(
                f"Error '{error_type}' has occurred {self.error_counts[error_type]} times!"
            )

    def get_error_summary(self) -> Dict[str, Any]:
        """エラーの統計情報を取得"""
        return {
            "total_errors": len(self.errors),
            "error_counts": self.error_counts,
            "recent_errors": self.errors[-10:]  # 直近10件
        }

# テストコード
if __name__ == "__main__":
    tracker = ErrorTracker()
    try:
        raise ValueError("Test error")
    except Exception as e:
        tracker.log_error(e, {"function": "main", "input": "test"})

    summary = tracker.get_error_summary()
    print(json.dumps(summary, indent=2))
