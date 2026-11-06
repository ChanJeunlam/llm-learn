# Lesson 12｜真实运行与验收记录

- **日期：** 2026-11-06
- **源码位置：** `lessons/lesson12/code/`
- **离线测试命令：** `python -m unittest discover -s lessons/lesson12/tests -v`
- **实际结果：** 2 项单元测试通过。六课总计 13 项，Python 3.12、语法检查、课程目录和中文注释静态检查全部成功。
- **GitHub Actions 证据：** https://github.com/ChanJeunlam/llm-learn/actions/runs/42154364620
- **静态审计：** `PASS: 6 节课程目录、源码与注释静态审计通过`；已核对 Markdown、LaTeX 中的完整源码与 `code/` 文件文本一致。
- **PDF 编译：** 已部署中文 XeLaTeX 工作流，首轮因缺少 `pzdr.tfm` 失败（https://github.com/ChanJeunlam/llm-learn/actions/runs/42154364625）。已按照参考论文 Workflow 补装 `texlive-fonts-recommended`；重试进行中：https://github.com/ChanJeunlam/llm-learn/actions/runs/42154612642 。**尚未记录为成功**。
- **真实模型调用：** 本课不需要调用外部付费大模型。
- **限制：** 所有示例为教学程序，本地 HTTP 端口只绑定 127.0.0.1；不应将教学服务暴露到公网。

## 验收等级
- 代码已提交：是。
- 六课静态审查：通过。
- 当前版本 GitHub Actions 离线测试：通过。
- GitHub Actions 中文 PDF 编译：等待本次重试的最终结果。
- 在线付费模型验证：未执行。
