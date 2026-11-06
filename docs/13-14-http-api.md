# 第 13–14 课：HTTP、API、JSON

## 原理
HTTP 是请求/响应协议。请求包含 method、URL、headers、body；响应包含 status code、headers、body。JSON 是常见的数据交换格式。

示例：
```http
POST /echo HTTP/1.1
Host: 127.0.0.1:8765
Content-Type: application/json

{"text": "你好，HTTP！"}
```

服务端返回 `200` 和 `{"received":"你好，HTTP！","length":8}`。常见状态码：200 成功、400 参数有误、401 未授权、404 路径不存在、415 内容类型错误、429 被限流。

## 操作步骤
在 `projects/first-llm-app` 安装依赖后，终端 A 执行：
```powershell
python api_server.py
```

终端 B 执行：
```powershell
python http_client.py
python -m unittest discover -s tests -v
```

阅读 `requests.get(url, timeout=5)`、`requests.post(url,json=payload,timeout=5)`、`response.status_code`、`response.json()`。

## 练习
1. 发送 JSON 格式的中文文本，解释 HTTP 的编码。
2. 将 `/echo` 改为 `/missing`，观察 404。
3. 发送缺少 `text` 字段的请求，观察 400。
4. 为 API 新增一个不含敏感信息的 `/version` 路由，并添加测试。

## 验收
讲清楚 HTTP 与 API 的区别；能够在本地成功收发 GET/POST，并独立解释状态码和 JSON。
