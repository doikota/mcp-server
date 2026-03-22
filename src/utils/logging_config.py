# src/utils/logging_config.py
import logging
import sys
from pathlib import Path
from datetime import datetime

def setup_logging(level="INFO", log_to_file=True):
    """MCPサーバー用のロギング設定

    Args:
        level: ログレベル（DEBUG, INFO, WARNING, ERROR, CRITICAL）
        log_to_file: ファイルへのログ出力を有効にするか

    Returns:
        設定済みのloggerインスタンス
    """
    # ログディレクトリの作成
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # フォーマッターの設定
    formatter = logging.Formatter(
        '%(levelname)s [%(asctime)s] %(name)s %(filename)s:%(lineno)d : %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # ルートロガーの設定
    logger = logging.getLogger("mcp_server")
    logger.setLevel(level)

    # コンソールハンドラー
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # ファイルハンドラー（日付ごとにローテーション）
    if log_to_file:
        log_file = log_dir / f"mcp-server-{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

if __name__ == "__main__":
    logger = setup_logging(level="DEBUG")
    logger.log(msg="MCPサーバーのロギングが初期化されました。", level=logging.INFO)
