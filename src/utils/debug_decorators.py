# src/utils/debug_decorators.py
import time
import functools
from typing import Callable, Any
import traceback
import logging_config

logger = logging_config.setup_logging("DEBUG", log_to_file=False)

def log_execution_time(func: Callable) -> Callable:
    """関数の実行時間を測定しログに記録するデコレーター"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        func_name = func.__name__

        try:
            # 関数の実行
            result = await func(*args, **kwargs)

            # 実行時間の計算とログ
            execution_time = time.time() - start_time
            logger.info(
                f"{func_name} completed successfully in {execution_time:.3f}s"
            )

            # 実行時間が長い場合は警告
            if execution_time > 5.0:
                logger.warning(
                    f"{func_name} took {execution_time:.3f}s - "
                    "consider optimization"
                )

            return result

        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(
                f"{func_name} failed after {execution_time:.3f}s: {e}\n"
                f"Traceback: {traceback.format_exc()}"
            )
            raise

    return wrapper

@log_execution_time
async def test_task(duration: float):
    """指定された時間だけ待機するサンプル関数"""
    await asyncio.sleep(duration)
    return f"Waited for {duration} seconds"

# テスト実行
if __name__ == "__main__":
    import asyncio
    result1 = asyncio.run(test_task(2))  # 2秒待機
    print(f"2秒後：{result1}")
    result2 = asyncio.run(test_task(6))  # 6秒待機（警告が出るはず）
    print(f"6秒後：{result2}")
