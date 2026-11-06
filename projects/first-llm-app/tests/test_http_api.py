"""离线 HTTP 自动化测试：不调用外部 API，不产生模型费用。"""
import threading
import unittest
from http.server import ThreadingHTTPServer

import requests
from api_server import DemoHandler


class HttpAPITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), DemoHandler)
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=3)

    def test_health_get(self):
        response = requests.get(f"{self.base}/health", timeout=3)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_json_post(self):
        response = requests.post(f"{self.base}/echo", json={"text": "你好"}, timeout=3)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"received": "你好", "length": 2})

    def test_bad_request(self):
        response = requests.post(f"{self.base}/echo", json={"wrong": 1}, timeout=3)
        self.assertEqual(response.status_code, 400)

    def test_not_found(self):
        response = requests.get(f"{self.base}/missing", timeout=3)
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
