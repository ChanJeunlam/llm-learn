# LLM Learn｜大模型开发系统课程

本仓库是**唯一课程主仓库**。学习路径覆盖工程开发、数学、PyTorch、Transformer、Mini-GPT、RAG、Agent、微调与部署，按 72 个独立课次组织。每日 1–2 小时，预计 24 周以上（因实践难度调整）。

## 从这里开始
- **[完整 72 课课程表（每课目标/实践/验收）](COURSE_PLAN.md)**
- **[课程硬性规范：目录、双讲义、逐行注释、LaTeX、CI](COURSE_STANDARDS.md)**
- **[课程目录](lessons/)**：`lesson11` 到 `lesson17` 已建立；此前 1–10 课已学习，未伪造历史实验与讲义。
- **[GitHub Actions 运行历史](../../actions)**

## 每课文件
`lessons/lessonN/README.md`、`lecture.md`、`lecture.tex`、`code/`、`tests/`、`results/verification.md`，成功编译后发布 `lecture.pdf`。

## 当前进度
- 已学过：Lesson 1–10（用户已完成基础学习；不重讲）。
- 首批代码仓库整理：Lesson 11–17（Git/GitHub、HTTP、Responses API、环境配置与密钥安全）。
- **在线 API 实际调用需要本人的密钥和配额**，默认离线 CI 不产生费用。

## 自动化构建
- `course-code-ci.yml`：源码、注释、文档结构与离线单元测试。
- `course-latex.yml`：XeLaTeX 中文讲义 PDF 编译、文本验证、SHA256、Artifacts、主分支发布。

以后每次上新课，请先完成可复现代码与双讲义，再上传测试记录，而不是只在聊天里讲解。
