"""Lesson 16：用离线 FakeResponses 验证续聊、重置和异常分支。"""

# 导入 unittest 组织多种会话场景。
import unittest
# 导入 SimpleNamespace 生成简单的假 SDK 响应对象。
from types import SimpleNamespace
# 导入 sys 使测试可以加载独立课程代码。
import sys
# 导入 Path 定位本课代码目录。
from pathlib import Path

# 把 lesson16/code 加入 Python 的模块搜索路径。
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
# 导入待测的会话控制类。
from chatbot import Conversation


class FakeResponses:
    """模拟每轮响应并记录请求参数，不调用真实模型。"""

    def __init__(self) -> None:
        """初始化请求历史列表。"""
        # 空列表表示尚未进行过任何调用。
        self.calls = []

    def create(self, **kwargs):
        """保存输入参数并生成递增的假响应 ID。"""
        # 保存该轮调用快照，方便检查上下文。
        self.calls.append(kwargs)
        # 用调用次数构造不会重复的模拟 ID。
        response_id = f"fake-{len(self.calls)}"
        # 返回具有 id 与 output_text 属性的模拟响应。
        return SimpleNamespace(id=response_id, output_text=f"模拟回复 {response_id}")


class ConversationTests(unittest.TestCase):
    """测试多轮链接、重置操作和空输入行为。"""

    def test_follow_up_and_reset(self) -> None:
        """第二轮应传上一轮 ID；重置后不再传 ID。"""
        # 创建离线 Responses 模拟接口。
        fake = FakeResponses()
        # 将假接口包装成 OpenAI SDK 相似的对象结构。
        client = SimpleNamespace(responses=fake)
        # 创建实际的会话控制对象，不触发网络请求。
        conversation = Conversation(client, model="mock-model")
        # 第一轮没有上一轮 ID。
        conversation.ask("第一轮")
        # 第二轮应沿用第一轮生成的响应 ID。
        conversation.ask("第二轮")
        # 验证模型请求携带了第一轮的 ID。
        self.assertEqual(fake.calls[1]["previous_response_id"], "fake-1")
        # 清除本地会话关联状态。
        conversation.reset()
        # 重置后提交第三轮问题。
        conversation.ask("新的第一轮")
        # 验证新会话请求不再携带旧 ID。
        self.assertNotIn("previous_response_id", fake.calls[2])

    def test_empty_input(self) -> None:
        """空白文本不应该触发假或真实模型调用。"""
        # 创建请求历史为空的假 API。
        fake = FakeResponses()
        # 构建使用假 API 的对话对象。
        conversation = Conversation(SimpleNamespace(responses=fake))
        # 空白输入应立即拒绝。
        with self.assertRaises(ValueError):
            # 提交空白文本，以触发参数校验分支。
            conversation.ask(" ")
        # 没有任何模型调用被记录。
        self.assertEqual(fake.calls, [])


if __name__ == "__main__":
    # 直接执行此文件时运行全部测试。
    unittest.main()

