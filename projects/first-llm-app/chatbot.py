"""第15–16课：OpenAI Responses API 多轮聊天。需要单独的 API 额度和 OPENAI_API_KEY。"""
import os

from openai import OpenAI, OpenAIError

# 通过环境变量切换有权限的模型，无需改动应用逻辑。
MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
INSTRUCTIONS = (
    "你是一位严谨、易懂的 Python 与科学计算辅导老师。"
    "用中文回答，遇到不确定信息应明确说明，不要编造实验数据。"
)


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        print("缺少 OPENAI_API_KEY。请在终端设置环境变量，勿将密钥写入代码。")
        return

    client = OpenAI(timeout=45.0, max_retries=2)
    previous_response_id = None
    print(f"LLM 聊天助手启动（模型：{MODEL}）")
    print("输入 /reset 开始新对话，/exit 退出。")

    while True:
        try:
            question = input("\n你> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n再见！")
            break
        if not question:
            continue
        if question.lower() in {"/exit", "/quit"}:
            break
        if question.lower() == "/reset":
            previous_response_id = None
            print("已开始新的对话。")
            continue

        request_data = {
            "model": MODEL,
            "instructions": INSTRUCTIONS,
            "input": question,
            "max_output_tokens": 500,
            "store": True,
        }
        if previous_response_id is not None:
            request_data["previous_response_id"] = previous_response_id
        try:
            result = client.responses.create(**request_data)
        except OpenAIError as exc:
            print("API 调用失败：", exc)
            print("检查密钥、额度、模型权限与网络后重试。")
            continue

        print("助手>", result.output_text or "（本次无可显示的文本）")
        previous_response_id = result.id
        if result.usage:
            print("[tokens] 输入:", result.usage.input_tokens,
                  "输出:", result.usage.output_tokens)


if __name__ == "__main__":
    main()
