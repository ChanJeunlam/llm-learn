"""Lesson 15：FakeClient 离线验证 API 参数和密钥安全分支。"""

# 导入 unittest 编写断言。
import unittest
# 导入 types 创建简单的模拟响应对象。
from types import SimpleNamespace
# 导入 sys 调整 Python 模块搜索路径。
import sys
# 导入 Path 获取待测源代码目录。
from pathlib import Path

# 将本课代码目录加入模块搜索路径。
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
# 导入用户需要理解的单次问答函数。
from first_call import ask_once


class FakeResponses:
    """模拟 Responses API，不发起 HTTP 网络连接。"""

    def __init__(self) -> None:
        """保存最近一次 create 调用参数，供单元测试核对。"""
        # 使用 None 表示还没有收到 create 调用。
        self.last_kwargs = None

    def create(self, **kwargs):
        """记录请求并返回固定模拟回答。"""
        # 保存请求参数，便于测试内容和模型名称。
        self.last_kwargs = kwargs
        # 返回具有 output_text 属性的轻量模拟结果。
        return SimpleNamespace(output_text="模拟回答：自注意力对上下文加权。")


class SingleCallTests(unittest.TestCase):
    """验证不调用外部 API 时的参数传递与输入检查。"""

    def test_mock_call(self) -> None:
        """注入客户端应成功得到模型文本并传递正确参数。"""
        # 创建 FakeResponses，它只在本进程内工作。
        responses = FakeResponses()
        # 组装具有 responses 属性的简化客户端。
        client = SimpleNamespace(responses=responses)
        # 用明确的演示模型名和问题调用待测函数。
        answer = ask_once("什么是注意力？", client=client, model="mock-model")
        # 验证返回的是模拟而非真实付费模型回答。
        self.assertIn("模拟回答", answer)
        # 验证传入的模型参数没有被覆盖。
        self.assertEqual(responses.last_kwargs["model"], "mock-model")
        # 验证 SDK 接收到原始问题文本。
        self.assertEqual(responses.last_kwargs["input"], "什么是注意力？")

    def test_reject_blank_prompt(self) -> None:
        """空白问题应在发起 SDK 调用前被拒绝。"""
        # 验证函数在无效输入时抛出 ValueError。
        with self.assertRaises(ValueError):
            # 使用空白输入执行测试，预计不会触发网络。
            ask_once("   ", client=SimpleNamespace())


if __name__ == "__main__":
    # 支持直接执行此测试文件。
    unittest.main()

