# First LLM App · 第 11–16 课

## 文件
- `api_server.py`：本地 HTTP 服务器，GET /health 与 POST /echo。
- `http_client.py`：发送 HTTP 请求、解析状态码和 JSON。
- `chatbot.py`：OpenAI Responses API 多轮聊天，/reset、/exit。
- `tests/test_http_api.py`：四项离线测试；无需模型密钥。

## 快速运行（Windows PowerShell）
```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

两个终端分别运行 `python api_server.py` 与 `python http_client.py`（使用已激活的虚拟环境）。

## 在线聊天（可能产生 API 费用）
```powershell
$env:OPENAI_API_KEY = Read-Host "API Key"
$env:OPENAI_MODEL = "gpt-4.1-mini"
python chatbot.py
```

注意：ChatGPT 订阅不等于 API 额度；`store=True` 会在服务端保存响应以便衔接上下文，勿输入敏感数据。不要提交 API Key、个人对话记录。

## 学习资料
参见仓库根目录 `docs/`。本项目仅为教学用途，不是生产级服务。
