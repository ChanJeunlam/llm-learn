# LLM Learn｜完整逐课学习总纲（COURSE_PLAN.md）

> 主仓库：`ChanJeunlam/llm-learn`；学习强度：每日 1–2 小时。**72 课 / 24 周**：每周 3 课讲解与编码，其余时间练习、复习、调试。课次数是教学单元而非日历日，必要时一课可分多天。第一至第十课已经学习，不重复讲，现从第十一课正式沉淀课程项目。

## 总目标与验收
1. 先具备 Git、HTTP、API、测试、自动部署的工程能力。
2. 再学数学、PyTorch、Transformer，实现能够训练与生成的 Mini-GPT。
3. 构建带证据引用的 RAG / Agent，掌握工具调用、评估和安全控制。
4. 完成可复现的微调、推理服务和最终综合系统。

## 每一课强制交付
- `lessons/lessonN/lecture.md`：中文讲义（完整理论、公式、操作、逐行代码解释、任务与验收）。
- `lessons/lessonN/lecture.tex`：相同知识内容的中文 XeLaTeX 版本，编译为 `lecture.pdf`；MD 与 TeX 的公式、代码及结论必须一致。
- `lessons/lessonN/code/`：本课全部代码，按模块、函数和关键/可执行行注释，含入口和错误处理。
- `lessons/lessonN/tests/`：离线可执行测试；纯理论课也需单独说明验证方式。
- `lessons/lessonN/results/verification.md`：真实命令、真实输出、运行条件、证据链接、尚未验证内容。
- `lessons/lessonN/README.md`：本课导航、依赖、快速命令与进度。

## 目录约定
只为实际已经制作的课程创建 `lessons/lessonN/`；未开始的课程仅在本总纲中规划，**不得提前标注完成**。第 1–10 课为已学习的先修内容，后续如需整理再逐课补档。

## 课程表（每课必须对应具体实践）

### 阶段 I｜Python 与工程基础（第 1–10 课，已学过，按需复习）

| 课次 | 核心知识 / 本课学习目标 | 代码与实践任务 | 完成验收标准 |
|---|---|---|---|
| **Lesson 1 · 安装 Python、VS Code 与虚拟环境** | 解释解释器/环境隔离，创建独立环境 | hello.py 与环境检查 | 能够在终端选择虚拟环境并运行 |
| **Lesson 2 · 变量、类型、字符串与数值运算** | 理解 str/int/float/bool 和格式化输出 | 类型与基础计算程序 | 能预测输出并定位类型错误 |
| **Lesson 3 · 列表、元组、集合与字典** | 掌握索引、切片和键值结构 | Token 样例容器 | 能访问、增删和遍历数据 |
| **Lesson 4 · 条件判断与布尔逻辑** | 理解比较、and/or/not 和短路求值 | 输入合法性检查器 | 正确处理边界条件 |
| **Lesson 5 · 循环与推导式** | 掌握 for/while/range/zip/enumerate | 批处理样例 | 能解释循环变量和退出条件 |
| **Lesson 6 · 函数、作用域与类型注解** | 理解参数、返回值、默认值、docstring | 可复用文本函数 | 能写输入输出和边界测试 |
| **Lesson 7 · 文件 I/O、CSV 与 JSON** | 了解编码、路径和文件异常 | JSON/CSV 读写程序 | 完成无数据丢失的往返读取 |
| **Lesson 8 · 异常、日志与调试** | try/except、traceback、logging、断点 | 错误定位练习 | 区分异常类型并复现问题 |
| **Lesson 9 · 模块、包、pip 与依赖** | 导入机制、requirements、版本兼容 | 多模块项目 | 在干净虚拟环境重装运行 |
| **Lesson 10 · unittest 与命令行参数** | 测试结构、assert、argparse | CLI 小工具及测试 | 跑通自动测试并解释失败输出 |

### 阶段 II｜Git、HTTP 与第一款 LLM 应用（第 11–24 课）

| 课次 | 核心知识 / 本课学习目标 | 代码与实践任务 | 完成验收标准 |
|---|---|---|---|
| **Lesson 11 · Git 工作区、暂存区与提交** | 掌握 init/status/add/commit/log/diff；理解快照 | 提交历史检查小程序和操作练习 | 能够自行提交、定位改动和回退实验分支 |
| **Lesson 12 · GitHub、分支、PR 与 CI** | 远程、push/pull、分支、PR、Actions | 仓库结构核验程序与 CI | 创建 PR，解释 CI 结果和冲突处理 |
| **Lesson 13 · HTTP 原理与本地服务器** | 请求行、headers、JSON、GET/POST、状态码 | 仅监听本机的 HTTP 服务器 | curl 或客户端能收到正确 JSON 和 4xx |
| **Lesson 14 · Python HTTP 客户端与测试** | requests、timeout、raise_for_status、错误分支 | HTTP 客户端及端到端测试 | 离线通过正常/错误场景测试 |
| **Lesson 15 · 第一次调用大模型 API** | API Key 环境变量、Responses API、输入输出 | 单轮问答脚本及模拟测试 | 区分离线 mock 与真实付费调用 |
| **Lesson 16 · 多轮对话与会话管理** | previous_response_id、/reset、Token 使用统计 | 命令行聊天程序及假客户端测试 | 多轮能续聊，重置后新会话 |
| **Lesson 17 · 环境变量、配置与密钥安全** | dotenv 思想、配置优先级、敏感信息禁入库 | 配置模块与安全检查 | 缺密钥能清楚报错且不泄露凭据 |
| **Lesson 18 · Streaming 流式输出** | Server-Sent Events 与流式 Token 输出 | 流式聊天 CLI | 能处理中断与事件乱序/异常 |
| **Lesson 19 · Structured Outputs 结构化结果** | JSON Schema、Pydantic 验证与解析 | 结构化信息抽取器 | 错误结构能被拒绝并回退 |
| **Lesson 20 · 重试、超时、限速与预算** | 指数退避、幂等性、429、成本预算 | 健壮 API 封装 | 失败模拟不无限重试 |
| **Lesson 21 · 日志、可观测性和追踪** | 请求 ID、耗时、错误率、脱敏日志 | 请求追踪模块 | 日志不含 API Key/个人输入 |
| **Lesson 22 · asyncio 与并发请求** | 协程、任务组、信号量、并发限额 | 批量问答工具 | 并发上限可控且错误可定位 |
| **Lesson 23 · FastAPI 包装应用** | HTTP 路由、Pydantic、OpenAPI、错误响应 | 问答 REST API | 本地文档可查看，测试通过 |
| **Lesson 24 · 第一阶段综合工程项目** | 整合 CLI、API、配置、日志、测试、CI | first-llm-service v1 | 干净环境一条命令运行测试 |

### 阶段 III｜数学、数值计算与机器学习（第 25–32 课）

| 课次 | 核心知识 / 本课学习目标 | 代码与实践任务 | 完成验收标准 |
|---|---|---|---|
| **Lesson 25 · 向量与内积** | 向量长度、余弦相似度及其几何含义 | 二维相似度可视化 | 手算与 NumPy 一致 |
| **Lesson 26 · 矩阵乘法与维度** | 形状、转置、广播、矩阵分解概念 | 线性层矩阵计算 | 解释 (batch,dim) 变换 |
| **Lesson 27 · 导数与链式法则** | 偏导、复合函数、链式求导 | 数值差分验证 | 数值梯度与解析梯度近似 |
| **Lesson 28 · 梯度下降** | 学习率、损失曲线、梯度方向 | 拟合简单函数 | 能解释震荡与收敛 |
| **Lesson 29 · 概率、条件概率与 Softmax** | 条件概率、归一化、采样与熵 | 概率采样实验 | 概率和为 1 且实验可重复 |
| **Lesson 30 · 优化算法 SGD / Adam** | 动量、指数移动平均、权重衰减 | 优化器对比 | 用相同初始条件比较 |
| **Lesson 31 · 损失函数与过拟合** | MSE、交叉熵、偏差方差 | 训练/验证曲线 | 识别过拟合并提出改进 |
| **Lesson 32 · NumPy 数组与向量化** | ndarray、shape、dtype、广播与矩阵运算 | 小型张量计算库 | 与纯 Python 结果一致 |

### 阶段 IV｜PyTorch 与深度学习实践（第 33–40 课）

| 课次 | 核心知识 / 本课学习目标 | 代码与实践任务 | 完成验收标准 |
|---|---|---|---|
| **Lesson 33 · PyTorch Tensor 入门** | tensor 创建、shape、device、dtype | Tensor 计算脚本 | 能解释维度和类型错误 |
| **Lesson 34 · autograd 自动微分** | requires_grad、backward、计算图 | 梯度验证程序 | 手算结果与自动微分一致 |
| **Lesson 35 · 线性回归从零实现** | 参数、前向计算、损失、反向传播 | 线性拟合实验 | 损失下降且验证数据合理 |
| **Lesson 36 · MLP 多层感知机** | Linear、激活函数、隐藏层 | 分类 MLP | 画出网络层数与形状 |
| **Lesson 37 · 训练循环和 DataLoader** | batch、epoch、optimizer、scheduler | 完整训练脚本 | 记录可复现日志和曲线 |
| **Lesson 38 · 验证、指标和数据泄漏** | train/val/test、precision/recall、early stop | 模型评估脚本 | 明确数据切分及指标 |
| **Lesson 39 · GPU、随机种子和混合精度** | CUDA、显存、AMP、determinism | CPU/GPU 性能基准 | 说明硬件与随机性限制 |
| **Lesson 40 · 神经网络阶段项目** | 构建可复现分类器或回归器 | 训练代码、权重、结果报告 | 测试通过并可复训 |

### 阶段 V｜Tokenizer、Transformer 与小 GPT（第 41–52 课）

| 课次 | 核心知识 / 本课学习目标 | 代码与实践任务 | 完成验收标准 |
|---|---|---|---|
| **Lesson 41 · 文本 Tokenization** | 字符/BPE/特殊 Token 和上下文窗口 | 迷你 tokenizer | 能编码解码示例 |
| **Lesson 42 · Embedding 与词向量** | 索引查表、embedding 维度和含义 | Embedding 层实验 | 解释形状和近邻关系 |
| **Lesson 43 · 位置编码** | 绝对位置、正弦编码、RoPE 概念 | 位置编码可视化 | 比较不同位置向量 |
| **Lesson 44 · 缩放点积注意力** | Q、K、V、Softmax 逐步手算 | 单头注意力手算脚本 | 张量输出与手算一致 |
| **Lesson 45 · QKV 矩阵及维度推导** | Wq/Wk/Wv、batch/head 维度 | 矩阵注意力程序 | 每一步形状匹配 |
| **Lesson 46 · 多头与因果掩码** | multi-head、mask、dropout | Masked Attention | 未来 Token 不被看到 |
| **Lesson 47 · 残差连接与归一化** | LayerNorm、RMSNorm、稳定性 | 归一化实验 | 数值检查正常无 NaN |
| **Lesson 48 · 前馈网络与激活函数** | FFN、GELU、SwiGLU | Transformer FFN | 解释参数量估算 |
| **Lesson 49 · Transformer Block** | 组合注意力、归一化和 FFN | 完整 Block | 测试输入输出形状 |
| **Lesson 50 · Mini-GPT 前向传播** | decoder-only、自回归 logits | 最小 GPT 模型 | 成功前向并统计参数 |
| **Lesson 51 · 语言模型数据与训练** | 滑动窗口、next-token loss、checkpoint | 小语料训练脚本 | 损失趋势可复现 |
| **Lesson 52 · 采样与生成策略** | temperature、top-k/top-p、KV cache 概念 | 文本生成器 | 解释不同采样行为 |

### 阶段 VI｜RAG、工具调用与 Agent（第 53–64 课）

| 课次 | 核心知识 / 本课学习目标 | 代码与实践任务 | 完成验收标准 |
|---|---|---|---|
| **Lesson 53 · Prompt Engineering 与安全边界** | system/developer/user 角色、模板与注入 | 提示词对比实验 | 定量比较错误率 |
| **Lesson 54 · 文本嵌入与语义检索** | 向量模型、相似度、索引 | 检索器 | 找回人工标注相关文档 |
| **Lesson 55 · 文档解析与切块** | PDF/Markdown 提取、chunk、metadata | 文档预处理管线 | 无内容丢失与重复定位 |
| **Lesson 56 · 向量数据库与索引** | FAISS 或 Chroma、top-k、过滤 | 本地索引 | 能重建与增量更新 |
| **Lesson 57 · 基础 RAG 与可靠引用** | 检索上下文、prompt、citation | 带来源文献问答 | 引用可回溯原文 |
| **Lesson 58 · RAG 评估与召回优化** | Recall@k、MRR、faithfulness | 评估集和指标脚本 | 先测再调 chunk/top-k |
| **Lesson 59 · Function Calling** | 工具 Schema、参数验证、权限 | 计算器/文件读取工具 | 无效参数被拒绝 |
| **Lesson 60 · 多步 Agent 工作流** | 规划、执行、观察、终止条件 | 多步骤工具代理 | 有步数上限与执行日志 |
| **Lesson 61 · LangGraph 状态机** | 节点、边、状态、检查点 | 状态化 Agent | 可暂停恢复和单元测试 |
| **Lesson 62 · MCP 与工具协议** | tool/resource、服务器连接、安全边界 | 本地 MCP 服务演示 | 限制可用工具并测试 |
| **Lesson 63 · Agent 安全与鲁棒性** | prompt injection、沙箱、人工批准 | 攻击样本测试 | 禁止越权和秘密外泄 |
| **Lesson 64 · 科研助手综合项目** | RAG + 计算工具 + 引用 + 审核 | 科研文档 Agent | 对比真实文档完成测评 |

### 阶段 VII｜微调、评估与工程部署（第 65–72 课）

| 课次 | 核心知识 / 本课学习目标 | 代码与实践任务 | 完成验收标准 |
|---|---|---|---|
| **Lesson 65 · 领域数据集构建** | 清洗、去重、许可、训练/验证切分 | 指令数据集 | 检查质量和数据来源 |
| **Lesson 66 · SFT 监督微调** | 数据格式、tokenization、loss masking | 小模型 SFT | 报告基线与增量 |
| **Lesson 67 · LoRA 低秩微调** | 冻结权重、低秩更新、rank/alpha | LoRA adapter | 对比全参可训练量 |
| **Lesson 68 · QLoRA 量化微调** | 4-bit、NF4、量化误差与显存 | QLoRA 实验 | 记录显存与质量差异 |
| **Lesson 69 · DPO 和偏好优化** | chosen/rejected、偏好损失、局限 | 偏好优化演示 | 避免把自动评分当真值 |
| **Lesson 70 · 模型评估与实验规范** | 固定测试集、泄漏检查、成本/延迟/质量 | 评估报告 | 可追溯模型与数据版本 |
| **Lesson 71 · 推理优化和模型服务** | 量化、KV Cache、batching、vLLM | 本地/远程推理服务 | 记录吞吐与延迟 |
| **Lesson 72 · 最终综合项目与部署** | Docker、FastAPI、RAG、Agent、模型评估、CI | 可部署 LLM 系统和总结报告 | 干净环境可复现且有安全说明 |

## 教学推进与版本策略
- 阶段 II 最初 6 课必须真正拆成 `lesson11` 到 `lesson16` 六个目录，禁止继续使用 `11-12` 合并目录。
- 每次更新必须同时提交该课 Markdown、TeX、程序、测试、验证记录（PDF 由 GitHub Actions 生成）。
- 代码全篇应有模块/函数/流程级注释；解释有教学价值的每条逻辑语句。不以注释覆盖语法错误或安全问题。
- 只公布真实测试结果；离线 Mock 不得冒充在线大模型 API 成功。
- 课程进度以 GitHub 提交及 CI 证据为准；没有 PDF 编译成功不可标记排版完成。

## 后续课程升级
每次课程结束评估内容、练习可执行性、依赖兼容和模型版本；外部 API 名称、价格、接口需按对应课次更新，不在总纲中写死。

## 官方参考
- Python https://docs.python.org/3/
- PyTorch https://docs.pytorch.org/tutorials/
- OpenAI Responses API https://platform.openai.com/docs/api-reference/responses
- Hugging Face https://huggingface.co/learn/llm-course/chapter1/1
- LangGraph https://docs.langchain.com/oss/python/langgraph/overview
- Git https://git-scm.com/doc；GitHub Actions https://docs.github.com/en/actions