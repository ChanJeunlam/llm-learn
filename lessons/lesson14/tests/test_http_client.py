"""Lesson 14：同时测试 GET、POST、HTTP 错误与输入错误。"""

# 导入 threading，在测试时运行 Lesson 13 的本地服务器。
import threading
# 导入 unittest 框架。
import unittest
# 导入 HTTP 服务器类。
from http.server import ThreadingHTTPServer
# 导入 Path 计算跨课路径。
from pathlib import Path
# 导入 sys 以导入两个课次的代码。
import sys
# 导入 requests 以识别预期的 HTTP 异常。
import requests

# 取得当前 lesson14 目录。
LESSON = Path(__file__).resolve().parents[1]
# 把 Lesson 14 的客户端目录放到 Python 模块查找路径。
sys.path.insert(0, str(LESSON / "code"))
# 把 Lesson 13 的服务器目录放到模块查找路径。
sys.path.insert(0, str(LESSON.parent / "lesson13" / "code"))
# 导入真实服务器处理器。
from http_server import DemoHandler
# 导入客户端待测函数。
from http_client import request_json


class ClientTests(unittest.TestCase):
    """使用真实的本地端口验证客户端的请求与异常处理。"""

    @classmethod
    def setUpClass(cls) -> None:
        """启动隔离的临时 HTTP 服务器。"""
        # 绑定本地 0 端口，让系统分配可用端口。
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), DemoHandler)
        # 拼出刚分配的本地服务器地址。
        cls.url = f"http://127.0.0.1:{cls.server.server_address[1]}"
        # 创建守护线程承载服务器循环。
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        # 启动服务线程。
        cls.thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        """每个测试类结束时回收服务器资源。"""
        # 请求退出服务循环。
        cls.server.shutdown()
        # 关闭服务器 socket。
        cls.server.server_close()
        # 最多等待 3 秒，避免测试程序悬挂。
        cls.thread.join(timeout=3)

    def test_get(self) -> None:
        """健康检查应成功返回预期字段。"""
        # 向 /health 发送 HTTP GET。
        data = request_json(self.url, "/health")
        # 验证服务返回 ok。
        self.assertEqual(data["status"], "ok")

    def test_post(self) -> None:
        """POST 中文 JSON 应返回相同文本及字符数。"""
        # 发出 POST 并解析为 Python 字典。
        data = request_json(self.url, "/echo", "你好")
        # 检查服务端没有更改正文。
        self.assertEqual(data, {"received": "你好", "length": 2})

    def test_404(self) -> None:
        """不存在路由时客户端应抛出 HTTPError。"""
        # 验证 404 不会被错误包装成成功结果。
        with self.assertRaises(requests.HTTPError):
            # 请求一个未注册路由。
            request_json(self.url, "/missing")

    def test_invalid_post_data(self) -> None:
        """向 /echo 发送 GET 应触发 415 或 404，而不是假成功。"""
        # GET /echo 路由并未在服务器提供。
        with self.assertRaises(requests.HTTPError):
            # 确认客户端调用方能够收到异常。
            request_json(self.url, "/echo")


if __name__ == "__main__":
    # 支持单独运行本课测试。
    unittest.main()

