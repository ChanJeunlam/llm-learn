# Lesson 15｜首次调用 OpenAI Responses API

**学习目标：** 掌握安全密钥注入、SDK 请求与响应、Token 输出限制，并完成离线 Mock 验证。

**先修：** Lesson 14 HTTP 与 JSON。　**建议时间：** 90–120 分钟。

## 本课原理

### API 与模型计算的边界

Python SDK 封装 HTTPS、鉴权与响应解析；远程服务执行 LLM 推理。调用 API 并不意味着训练或本地运行 Transformer 权重。

### Responses API 参数

client.responses.create(model=...,input=...,max_output_tokens=...)；model 指目标模型，input 是输入内容，max_output_tokens 控制输出上限，output_text 是可展示文本。

### 保护密钥与费用

OPENAI_API_KEY 仅由环境变量读取，不能写进源码或 Git 仓库。ChatGPT 订阅与 API 计费不同，建议先设预算。默认模型可用 OPENAI_MODEL 覆盖，应按本人账户权限选择。

### 验证策略

测试使用 FakeResponses 记录 create 的参数，并返回固定的模拟 output_text；这证明程序参数正确，不证明在线模型可用。真实 API 运行需使用本人有额度的 Key，记录真实的成功/失败日志。

## 核心关系或公式

$$
C\simeq\frac{N_{\mathrm{in}}P_{\mathrm{in}}+N_{\mathrm{out}}P_{\mathrm{out}}}{10^{6}}
$$

## 实操：本课全部示例源码

完整的本课源码如下，模块顶部、每个函数及每条关键语句均附解释。源文件是可执行的，不是伪代码。

```python
"""Lesson 15：安全地执行一次 OpenAI Responses API 调用，支持离线注入假客户端。"""

# 导入 os，通过环境变量管理 API Key 和模型名。
import os
# 导入 SDK 客户端和错误基类；仅在真实调用时访问服务端。
from openai import OpenAI, OpenAIError

# 教学默认模型可通过 OPENAI_MODEL 环境变量覆盖。
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def ask_once(prompt: str, client=None, model: str = DEFAULT_MODEL) -> str:
    """向 Responses API 发送一次文本请求；可注入 mock 客户端；返回回复文本。"""
    # 拒绝空白输入，避免无意义的付费调用。
    if not prompt.strip():
        # 明确告知调用方输入不符合要求。
        raise ValueError("问题文本不能为空")
    # 只有真实客户端未注入时才需要读取 API Key。
    if client is None:
        # 环境变量不存在说明尚不具备在线调用条件。
        if not os.getenv("OPENAI_API_KEY"):
            # 不显示密钥，仅提示安全配置步骤。
            raise RuntimeError("请先配置 OPENAI_API_KEY 环境变量")
        # 创建 SDK 客户端，控制超时和网络失败时的重试次数。
        client = OpenAI(timeout=45, max_retries=1)
    # 向指定模型提交文本，限制最大输出 Token 以减少误用成本。
    response = client.responses.create(model=model, input=prompt, max_output_tokens=400)
    # SDK 的 output_text 是由响应中可显示文本提取的内容。
    return response.output_text


def main() -> None:
    """在命令行执行首次真实 API 调用，并处理配置及网络错误。"""
    # 本课的问题专门围绕下一阶段要学的 Transformer 概念。
    question = "用简明中文解释 Transformer 中自注意力的作用。"
    try:
        # 调用封装函数并获得模型文本回答。
        answer = ask_once(question)
    except (OpenAIError, RuntimeError, ValueError) as error:
        # 将配置或 SDK 异常说明打印出来，不泄露任何令牌。
        print("调用失败:", error)
        # 不把失败误写为在线成功验证。
        return
    # 成功时显示真实返回的文本内容。
    print("模型回答:", answer)


if __name__ == "__main__":
    # 只有直接运行该文件才发起可能收费的请求。
    main()
```

## 自动测试、练习与验收

- 空问题在请求前被拒绝。
- Mock 客户端收到正确的 model、input、max_output_tokens。
- 不会提交 API Key；真实在线调用尚未验证时必须如实注明。

从本课目录运行 `python -m unittest discover -s tests -v`；真实运行证据请阅读 [验证记录](results/verification.md)。

## 官方参考

Git：https://git-scm.com/docs ；GitHub：https://docs.github.com/en/actions ；HTTP：https://developer.mozilla.org/en-US/docs/Web/HTTP ；OpenAI Responses API：https://platform.openai.com/docs/api-reference/responses。
