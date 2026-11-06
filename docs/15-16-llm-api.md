# 第 15–16 课：首次调用大模型 API 与多轮聊天

## 原理
Python SDK 负责发出 HTTPS 请求；服务器端模型执行推理。API 调用不是训练模型，也不是在本地运行权重。

## 操作
```powershell
cd projects/first-llm-app
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:OPENAI_API_KEY = Read-Host "API Key"
$env:OPENAI_MODEL = "gpt-4.1-mini"
.\.venv\Scripts\python.exe chatbot.py
```

程序使用 `client.responses.create(model=..., instructions=..., input=..., previous_response_id=..., store=True)`，通过 `response.output_text` 取得文本。

- `/reset`：清空本地保存的 `previous_response_id`，开始新对话。
- `/exit`：结束程序。
- `usage.input_tokens` 与 `usage.output_tokens`：了解 Token 用量。
- `previous_response_id`：把对话链接到上一条服务器端响应，并不意味着后续 Token 免费。
- `store=True`：用于本次教学示例的会话衔接；实际涉及敏感数据时应重新设计数据保留方案。

## 练习
1. 比较单轮问答与多轮追问。
2. 测试 `/reset` 是否清除上文链接。
3. 故意取消密钥，观察程序安全退出。
4. 将模型名配置为你有权使用的另一模型，比较 Token 与响应质量。

## 验收
能独立完成 API 调用与异常处理。**在线调用尚未验证**，必须使用本人 Key 和额度才能测通。

官方参考：https://platform.openai.com/docs/api-reference/responses ；https://platform.openai.com/docs/quickstart
