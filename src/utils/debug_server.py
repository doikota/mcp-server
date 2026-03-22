# src/debug_server.py
import os
import debugpy

def setup_remote_debugging():
    """リモートデバッグを有効化"""
    if os.getenv("ENABLE_REMOTE_DEBUG", "").lower() == "true":
        debug_port = int(os.getenv("DEBUG_PORT", "5678"))
        debugpy.listen(("0.0.0.0", debug_port))

        print(f"Remote debugging enabled on port {debug_port}")
        print("Waiting for debugger to attach...")

        # デバッガーの接続を待つ（オプション）
        if os.getenv("WAIT_FOR_DEBUGGER", "").lower() == "true":
            debugpy.wait_for_client()
            print("Debugger attached!")

# サーバー起動時に呼び出し
if __name__ == "__main__":
    setup_remote_debugging()
    # MCPサーバーの起動処理
