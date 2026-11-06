# Lesson 16｜多轮聊天与服务器端会话关联

- [中文 Markdown 讲义](lecture.md)
- [中文 XeLaTeX 讲义](lecture.tex)
- PDF：`lecture.pdf`，由 GitHub Actions 编译并发布
- [本课代码](code/)
- [本课测试](tests/)
- [真实验证记录](results/verification.md)

## 如何运行
在本目录执行：
```bash
python code/chatbot.py
```

运行离线单元测试：
```bash
python -m unittest discover -s tests -v
```

如需第三方依赖先安装 `code/requirements.txt`。Lesson 13 为持续监听服务；Lesson 14 需要先启动 Lesson 13。Lesson 15–16 的在线调用需要您本人提供 API Key，默认单元测试仅使用 Mock，不会产生 API 费用。

