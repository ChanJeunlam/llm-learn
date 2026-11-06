# LLM Learn｜大模型开发系统课程

本仓库是大模型系统学习的唯一主仓库，统一维护课程 Markdown 讲义、可运行代码、测试与真实运行结果。

当前章节：第 11–16 课——Git/GitHub、HTTP/JSON/API、OpenAI Responses API 多轮聊天。

## 导航
- [学习路线](docs/ROADMAP.md)
- [第 11–12 课：Git、GitHub 与代码管理](docs/11-12-git-github.md)
- [第 13–14 课：HTTP、JSON 与 API](docs/13-14-http-api.md)
- [第 15–16 课：LLM API 与多轮聊天](docs/15-16-llm-api.md)
- [实战项目代码](projects/first-llm-app/)
- [验证记录](results/2026-11-06-lessons-11-16.md)
- [课程维护规范](docs/CONTRIBUTING_COURSE.md)

## 快速开始
```powershell
git clone https://github.com/ChanJeunlam/llm-learn.git
cd llm-learn/projects/first-llm-app
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

运行本地 HTTP 服务：`python api_server.py`，另一终端运行 `python http_client.py`。如需调用付费大模型 API，在当前终端设置 `OPENAI_API_KEY`，再运行 `python chatbot.py`。

## 基本规范
- 禁止提交 API Key、`.env`、个人对话、敏感数据。
- 本地测试与在线模型调用的验证等级必须明确区分。
- 每次课程更新配套讲义、源码、测试结果和变更记录。
- GitHub Actions 仅执行离线测试，不触发付费 API 请求。
