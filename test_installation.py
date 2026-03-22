# test_installation.py
import asyncio
from mcp.server.lowlevel import Server
import mcp.types as types
import importlib.metadata

async def test_installation():
    """MCPインストールの検証"""
    print("MCPインストールテスト開始...")

    # バージョン確認
    print(f"✓ MCP version: {importlib.metadata.version("mcp")}")

    # サーバー作成のテスト
    server = None
    try:
        server = Server("test-server")
        print("✓ サーバー作成成功")
    except Exception as e:
        print(f"× サーバー作成失敗: {e}")
        exit(1)

    # ツール登録
    @server.list_tools()
    async def test_tool() -> list[types.Tool]:
        """テスト用ツール"""
        return [types.Tool(
            name="test_tool",
            description="テスト用ツール",
            inputSchema={"type": "object", "properties": {}}
        )]

    # ツール呼び出し
    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
        if name == "test_tool":
            return [types.TextContent(type="text", text="Hello MCP!")]
        raise ValueError(f"Unknown tool: {name}")

    # call_toolを呼び出して確認
    result = await call_tool("test_tool", {})
    print(result[0].text)
    assert result[0].text == "Hello MCP!", "期待したテキストと違う"
    print("✓ ツール呼び出し成功")

    print("\nインストール完了！MCPサーバー開発の準備ができました。")

if __name__ == "__main__":
    asyncio.run(test_installation())
