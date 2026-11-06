"""第13–14课：利用 requests 调用本地 HTTP API。先启动 api_server.py。"""
import requests

BASE_URL = "http://127.0.0.1:8765"


def main() -> None:
    try:
        health = requests.get(f"{BASE_URL}/health", timeout=5)
        print("GET /health ->", health.status_code, health.json())
        health.raise_for_status()

        payload = {"text": "你好，HTTP！"}
        answer = requests.post(f"{BASE_URL}/echo", json=payload, timeout=5)
        print("POST /echo ->", answer.status_code, answer.json())
        answer.raise_for_status()
    except requests.RequestException as exc:
        print("请求失败：请先确认本地服务器已启动。", exc)


if __name__ == "__main__":
    main()
