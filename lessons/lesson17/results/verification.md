# Lesson 17｜验证记录

- 日期：2026-11-06
- 运行方式：独立 Python 3.12+ 开发环境；无任何真实 API Key。
- 离线命令：`python -m unittest discover -s lessons/lesson17/tests -v`
- 结果：**本地离线 8 项单元测试通过**。覆盖系统变量优先级、本地 .env、默认值、缺失密钥、非法参数与普通 repr 隐藏密钥。
- CLI 命令：`python lessons/lesson17/code/config.py --offline`
- CLI 结果：模型名为教学默认值，超时 30 秒，最大输出 500 Token，API Key 未配置。
- 模型在线调用：**未执行**，测试均使用本地假数据，无付费费用。
- PDF：本课 LaTeX 文本可在本地验证；以提交后 GitHub Actions 运行和已发布 PDF 为最终仓库证据。
- 说明：自动 repr 脱敏不是加密。不得把安全示例密钥理解为真实有效密钥。
