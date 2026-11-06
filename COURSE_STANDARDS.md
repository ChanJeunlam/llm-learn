# COURSE_STANDARDS.md｜LLM Learn 强制课程工程规范

**版本：2026-11-06。适用范围：所有 `lessons/lessonN`、代码、讲义、GitHub Actions、结果记录。违反以下约束的课程不能标记为完成。**

## 1. 一课一目录（必须）
```text
llm-learn/
├── README.md
├── COURSE_PLAN.md                 # 全部 72 课的目标、任务与验收
├── COURSE_STANDARDS.md            # 本规范
├── lessons/
│   ├── lesson11/
│   │   ├── README.md
│   │   ├── lecture.md             # Markdown 详细讲义
│   │   ├── lecture.tex            # 同内容的可编译 LaTeX
│   │   ├── lecture.pdf            # GitHub Actions 编译生成
│   │   ├── code/                  # 本课所有代码、依赖
│   │   ├── tests/                 # 本课独立离线测试
│   │   └── results/
│   │       └── verification.md    # 本课真实运行证据
│   ├── lesson12/
│   └── ...
└── .github/workflows/
    ├── course-code-ci.yml
    └── course-latex.yml
```
不得在根目录或 `projects/` 混放不同课的练习代码、脚本和报告；跨课复用时显式引用上课目录，或另行建立有文档的共享库。不得把课程 11–12、13–14、15–16 合并为一课。

## 2. 双格式讲义（必须）
每节课同时维护 **lecture.md 与 lecture.tex**；章节语义、计算公式、演示代码、练习与验收必须一致。讲义至少包含：
1. 课题、先修知识、学习时间、最终成果；
2. 概念与工程背景、术语英文、完整原理及可核对公式；
3. 环境安装/命令、所有命令的预期行为、跨平台注意点；
4. 逐行代码和逐函数解释（输入、输出、异常、为什么这么写）；
5. 实际运行方法与预期结果（与真实运行区分）；
6. 常见错误、练习题、客观验收标准、官方资料来源。

LaTeX 采用 UTF-8 + `ctexart` + **XeLaTeX**，优先使用 `Noto Serif CJK SC` / `Noto Sans CJK SC`。复杂公式用 `amsmath`；代码使用 `fvextra` / `Verbatim`，支持长行换行。**不得只用 TeX 占位文字或把 Markdown 文件扩展名改成 .tex**。

本地编译（每课在自身目录执行）：
```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build lecture.tex
pdfinfo build/lecture.pdf
pdftotext build/lecture.pdf - | head
```
GitHub Actions 对每个 `lecture.tex` 自动编译、校验 PDF 非空、页数和中文文本提取，保存 Actions Artifacts；主分支自动提交稳定产物 `lecture.pdf`。**失败必须报错，禁止 `continue-on-error: true` 将编译失败伪装为成功**。

## 3. 源码注释强制标准（必须）
- 每个 `.py` 文件顶部：**模块 docstring**，说明目的、数据来源/是否模拟、执行方式和限制。
- 每个函数/类：**中文 docstring**，准确解释功能、参数、返回、异常、调用关系。
- 每个算法阶段：**整体流程注释**，说明步骤与工程意义。
- **每一条有教学意义的可执行语句都要有逐行/邻行中文解释**，包括 import、赋值、计算、条件、循环、HTTP 调用、异常处理、输出；单纯右括号、结构分隔符和格式排版不强制机械注释。
- 关键计算必须注明输入输出单位、形状、边界条件与数值精度；函数关键参数必须写清。
- 禁止只写“执行下一步”“处理数据”之类无信息量的伪注释；不得复制产生歧义的通用 AI 文案。
- 代码注释与讲义解释必须一致，注释修改不能影响可执行性。
- 一律不硬编码 API Key、访问令牌、私人数据；需要在线付费 API 时先给出离线模拟验证。
- 不应在教学注释中泄露密钥、用户输入或设备敏感信息。
- GitHub Actions 加入静态注释覆盖检查（保证模块与函数有 docstring、可执行代码旁有解释），其余语义质量人工检查。

## 4. 结果、测试与科学可复现性（必须）
- `tests/` 至少包含正常路径和关键异常/边界路径；在线模型请求使用 Mock，默认 CI 不花钱。
- `results/verification.md` 必须记录日期、环境、运行命令、实际输出或证据来源、通过/失败、未验证项。
- 逐一标明：**代码已提交 / 静态审查 / 本地执行 / Actions 成功 / 在线真实 API 验证**。
- API 回答若未经本人 Key 真实执行，必须标记 **未执行**，不能写成通过。
- 课程讲义或工具里的模拟数据必须明确为合成/示例；不得冒充实验测量值。
- 构建 PDF 必须检验 `pdfinfo`、`pdftotext`，并保存 SHA256 摘要。
- 生成的 `*.aux`、`*.log`、`*.fls`、`*.fdb_latexmk` 不纳入仓库；只提交指定 PDF 成品。

## 5. GitHub Actions 约定
- `course-code-ci.yml`：Python 版本、语法、unittest、注释质量审查、资料目录结构检查。
- `course-latex.yml`：安装 XeLaTeX、`texlive-lang-chinese`、`latexmk`、Noto CJK 字体、poppler，逐课编译、验证、上传 PDF；仅可信主分支发布。
- 参考 [traffic-v8-v9-build.yml](https://github.com/ChanJeunlam/scientific-agent-skills/blob/main/.github/workflows/traffic-v8-v9-build.yml) 的安装、`latexmk`、`pdfinfo`、`sha256sum`、Artifacts、自动提交模式。
- Workflow 只对相关源码变化触发，PDF 发布提交使用 `[skip ci]` 且不监听 PDF 路径，避免递归运行。
- PR/不受信任分支不授予写权限、不暴露密钥；自动提交冲突应明显失败，不能声称发布成功。

## 6. 每课完成的定义（Definition of Done）
至少同时满足：
- [ ] `COURSE_PLAN.md` 已明确本课目标和验收
- [ ] 每课目录文件完整
- [ ] MD 与 TeX 内容对应、XeLaTeX 编译成功
- [ ] 全部源文件逐行/函数/模块注释达标
- [ ] 单元测试及 CI 通过
- [ ] 课程 PDF 发布或清楚说明未发布原因
- [ ] `results/verification.md` 附真实证据
- [ ] README 链接有效、版本/限制明确
