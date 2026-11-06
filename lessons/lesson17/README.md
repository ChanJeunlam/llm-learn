# Lesson 17｜环境变量、配置管理与 API Key 安全

- [Markdown 完整讲义](lecture.md)
- [XeLaTeX 讲义](lecture.tex)
- [逐行注释的配置代码](code/config.py)
- [8 项离线测试](tests/test_config.py)
- [真实运行与验证结果](results/verification.md)

## 运行（Windows PowerShell）
```powershell
py -m pip install -r lessons/lesson17/code/requirements.txt
py lessons/lesson17/code/config.py --offline
py -m unittest discover -s lessons/lesson17/tests -v
```

`.env.example` 是模板，可复制成同目录 `.env`，但严禁把真实 `.env` 或 API Key 上传到 Git。
本课不执行任何需要付费的模型调用。
