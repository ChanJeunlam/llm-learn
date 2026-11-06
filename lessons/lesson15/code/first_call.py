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

