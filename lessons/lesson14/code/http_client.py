"""Lesson 14：带超时、HTTP 状态检查与 JSON 解析的客户端。"""

# 导入 argparse，以允许配置服务器 URL。
import argparse
# 导入 requests，发送 GET 与 POST HTTP 请求。
import requests


def request_json(base_url: str, path: str, text: str | None = None) -> dict:
    """向本地服务发送 GET 或 POST，返回 JSON 字典；失败时抛异常。"""
    # 规范化 URL，避免多余的斜线影响拼接。
    url = base_url.rstrip("/") + path
    # 如果 text 缺省，则执行简单的 GET 查询。
    if text is None:
        # 设置超时，避免服务器卡住导致客户端无限等待。
        response = requests.get(url, timeout=5)
    else:
        # 以 JSON 请求体发送 POST，requests 自动设置相应 Content-Type。
        response = requests.post(url, json={"text": text}, timeout=5)
    # 如果 HTTP 状态为 4xx 或 5xx，抛出带状态码的异常。
    response.raise_for_status()
    # 解析响应 JSON；非法 JSON 会触发解码异常。
    payload = response.json()
    # 防御性检查：期望本教学接口始终返回 JSON 对象。
    if not isinstance(payload, dict):
        # 结构不满足契约时主动报错。
        raise ValueError("服务端没有返回 JSON 对象")
    # 将解析结果交给函数调用方。
    return payload


def main() -> None:
    """执行一次健康检查和一次中文 JSON 回显请求。"""
    # 创建命令行参数解析器，支持传入服务器地址。
    parser = argparse.ArgumentParser(description="Lesson 14 HTTP 客户端")
    # 默认访问 Lesson 13 的本机服务器。
    parser.add_argument("--base-url", default="http://127.0.0.1:8765")
    # 解析用户实际输入的参数。
    arguments = parser.parse_args()
    try:
        # 请求健康检查，验证服务可以访问。
        health = request_json(arguments.base_url, "/health")
        # 显示健康检查结构化结果。
        print("GET /health:", health)
        # 通过 POST 提交中文文本，让服务器回显。
        echoed = request_json(arguments.base_url, "/echo", "你好，HTTP！")
        # 展示回显响应与字符长度。
        print("POST /echo:", echoed)
    except (requests.RequestException, ValueError) as error:
        # 报错时说明服务器或 JSON 可能有问题，不声称调用成功。
        parser.exit(1, f"HTTP 请求失败: {error}\n")


if __name__ == "__main__":
    # 被别的脚本导入时不自动发起网络请求。
    main()

