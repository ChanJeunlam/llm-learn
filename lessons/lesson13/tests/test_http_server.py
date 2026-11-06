"""Lesson 13：标准库 HTTP 服务的本机真实套接字离线测试。"""

# 导入 unittest 进行断言。
import unittest
# 导入 threading 让服务器在测试期间运行。
import threading
# 导入 json 解析服务器的响应体。
import json
# 导入 urllib.request，发出不依赖第三方库的 HTTP 请求。
from urllib.request import urlopen
# 导入 urllib.error，验证 404 响应。
from urllib.error import HTTPError
# 导入服务器以分配临时端口。
from http.server import ThreadingHTTPServer
# 导入 sys 配置本课代码路径。
import sys
# 导入 Path 计算相对路径。
from pathlib import Path

# 将本课 code 目录加入 import 路径。
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
# 导入要测试的 HTTP 请求处理器。
from http_server import DemoHandler


class ServerTests(unittest.TestCase):
    """真实监听随机本地端口以验证请求响应。"""

    @classmethod
    def setUpClass(cls) -> None:
        """启动仅监听本机的临时 HTTP 服务。"""
        # 端口号 0 由操作系统自动分配可用端口。
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), DemoHandler)
        # 构造实际分配端口对应的基础 URL。
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"
        # 创建后台线程，避免阻塞测试主线程。
        cls.worker = threading.Thread(target=cls.server.serve_forever, daemon=True)
        # 开始接受测试 HTTP 请求。
        cls.worker.start()

    @classmethod
    def tearDownClass(cls) -> None:
        """关闭服务器并释放网络资源。"""
        # 通知 HTTP 服务器停止接收请求。
        cls.server.shutdown()
        # 显式释放 socket。
        cls.server.server_close()
        # 等待工作线程最多 3 秒退出。
        cls.worker.join(timeout=3)

    def test_health(self) -> None:
        """GET /health 应返回 200 与状态 JSON。"""
        # 打开本地健康检查接口。
        with urlopen(f"{self.base}/health", timeout=3) as response:
            # 检查 HTTP 请求成功。
            self.assertEqual(response.status, 200)
            # 将响应字节解码后解析 JSON。
            payload = json.loads(response.read().decode("utf-8"))
            # 确认服务状态为 ok。
            self.assertEqual(payload["status"], "ok")

    def test_unknown_route(self) -> None:
        """不存在的 GET 路由必须返回 HTTP 404。"""
        # 验证 urllib 在 404 时抛出 HTTPError。
        with self.assertRaises(HTTPError) as raised:
            # 请求服务器没有注册的路径。
            urlopen(f"{self.base}/missing", timeout=3)
        # 确认不是其他网络错误而是预期的 404。
        self.assertEqual(raised.exception.code, 404)


if __name__ == "__main__":
    # 支持单独运行测试文件。
    unittest.main()

