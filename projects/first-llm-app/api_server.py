"""第13–14课：本地 HTTP/JSON 教学服务器。只绑定 127.0.0.1，不可作为生产服务器。"""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


class DemoHandler(BaseHTTPRequestHandler):
    def reply_json(self, status: int, data: dict) -> None:
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:
        if self.path == "/health":
            self.reply_json(200, {"status": "ok", "message": "本地API运行正常"})
        else:
            self.reply_json(404, {"error": "path_not_found"})

    def do_POST(self) -> None:
        if self.path != "/echo":
            self.reply_json(404, {"error": "path_not_found"})
            return
        if not self.headers.get("Content-Type", "").startswith("application/json"):
            self.reply_json(415, {"error": "expected_application_json"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 10_000:
                self.reply_json(400, {"error": "invalid_body_length"})
                return
            payload = json.loads(self.rfile.read(length))
        except (ValueError, UnicodeDecodeError):
            self.reply_json(400, {"error": "invalid_json"})
            return
        if not isinstance(payload, dict) or not isinstance(payload.get("text"), str):
            self.reply_json(400, {"error": "text_must_be_string"})
            return
        self.reply_json(200, {"received": payload["text"], "length": len(payload["text"])})


def main() -> None:
    server = ThreadingHTTPServer(("127.0.0.1", 8765), DemoHandler)
    print("本地 API: http://127.0.0.1:8765  (Ctrl+C 停止)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
