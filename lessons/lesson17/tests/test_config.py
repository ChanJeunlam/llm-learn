"""Lesson 17：纯离线测试配置优先级、异常分支和凭据脱敏。"""

# os.environ 是环境变量的真实来源。
import os
# sys.path 使测试可以导入独立的本课代码。
import sys
# tempfile 在测试完毕后自动删除示例 .env。
import tempfile
# unittest 提供离线断言及测试报告。
import unittest
# Path 用于定位课程文件。
from pathlib import Path
# patch.dict 在测试结束后恢复进程环境。
from unittest.mock import patch

# 定位 lesson17/code 目录。
CODE_DIR = Path(__file__).resolve().parents[1] / "code"
# 把源码路径加入 Python 模块查找列表。
sys.path.insert(0, str(CODE_DIR))
# 导入待测的数据类型、异常与配置加载函数。
from config import AppConfig, ConfigError, load_config


class ConfigTests(unittest.TestCase):
    """用临时文件和模拟环境测试，不连接 API。"""

    def test_defaults_offline(self) -> None:
        """缺少 .env 和 Key 的离线模式能使用非敏感默认值。"""
        # 建立与用户真实文件完全隔离的临时目录。
        with tempfile.TemporaryDirectory() as folder:
            # 清空所有环境变量，以保证测试可重复。
            with patch.dict(os.environ, {}, clear=True):
                # 使用不存在的 .env，且明确关闭密钥要求。
                c = load_config(Path(folder) / ".env", require_api_key=False)
                # 默认超时应为 30 秒。
                self.assertEqual(c.timeout_seconds, 30.0)
                # 默认最大输出上限为 500。
                self.assertEqual(c.max_output_tokens, 500)
                # 不应该虚构出有效 API Key。
                self.assertFalse(c.has_api_key)

    def test_dotenv_reads_missing_variables(self) -> None:
        """系统变量缺失时由 .env 文件补充配置。"""
        # 创建临时工作目录。
        with tempfile.TemporaryDirectory() as folder:
            # 定位临时 .env 文件。
            f = Path(folder) / ".env"
            # 写入纯粹虚构的模型名和非敏感测试参数。
            f.write_text("OPENAI_MODEL=file-model\nLLM_TIMEOUT_SECONDS=12.5\nLLM_MAX_OUTPUT_TOKENS=96\n", encoding="utf-8")
            # 清空系统变量，以便测试本地文件的真实作用。
            with patch.dict(os.environ, {}, clear=True):
                # 从指定 .env 读取配置。
                c = load_config(f, require_api_key=False)
                # 模型名称应来自文件。
                self.assertEqual(c.model, "file-model")
                # 浮点超时应正确转换。
                self.assertEqual(c.timeout_seconds, 12.5)
                # Token 上限应转换为整数。
                self.assertEqual(c.max_output_tokens, 96)

    def test_environment_wins(self) -> None:
        """系统变量优先级高于本地文件。"""
        # 使用临时目录作为不含真实秘密的测试环境。
        with tempfile.TemporaryDirectory() as folder:
            # 创建低优先级的测试配置文件。
            f = Path(folder) / ".env"
            # 文件指定 file-model。
            f.write_text("OPENAI_MODEL=file-model\n", encoding="utf-8")
            # 系统环境提前指定不同的 model 名称。
            with patch.dict(os.environ, {"OPENAI_MODEL": "system-model"}, clear=True):
                # 加载 .env，但 override=False 不得覆盖系统值。
                c = load_config(f, require_api_key=False)
                # 验证系统变量确实具有最高优先级。
                self.assertEqual(c.model, "system-model")

    def test_missing_key(self) -> None:
        """联网模式缺 Key 时必须返回清楚而安全的异常。"""
        # 清空系统变量，避免读取用户真实密钥。
        with patch.dict(os.environ, {}, clear=True):
            # 检查错误信息包括正确的配置变量名。
            with self.assertRaisesRegex(ConfigError, "OPENAI_API_KEY"):
                # 使用不存在的 .env 并采用默认联网要求。
                load_config(Path("/nonexistent/lesson17.env"))

    def test_invalid_timeout(self) -> None:
        """float 可识别的 inf 也不应被允许作为超时。"""
        # 通过系统环境提供一个不合法的正无穷值。
        with patch.dict(os.environ, {"LLM_TIMEOUT_SECONDS": "inf"}, clear=True):
            # 检查这一超时不进入配置对象。
            with self.assertRaises(ConfigError):
                # 无需 Key 的离线读取只验证参数。
                load_config(Path("/nonexistent/lesson17.env"), require_api_key=False)

    def test_invalid_token_limit(self) -> None:
        """非整数的最大输出 Token 值必须被拒绝。"""
        # 把上限写为小数文本，无法转换为整数。
        with patch.dict(os.environ, {"LLM_MAX_OUTPUT_TOKENS": "1.5"}, clear=True):
            # 配置加载应抛出预期的类型错误。
            with self.assertRaises(ConfigError):
                # 不连接任何在线服务。
                load_config(Path("/nonexistent/lesson17.env"), require_api_key=False)

    def test_repr_hides_key(self) -> None:
        """普通 repr 输出不能泄露测试用虚构 Key。"""
        # 构造绝对无效的测试密钥字符串。
        fake = "FAKE_TEST_SECRET_DO_NOT_USE"
        # 实例化只读配置对象，不调用模型。
        c = AppConfig("test-model", 10.0, 100, fake)
        # repr 中不应该包含这个秘密字段。
        self.assertNotIn(fake, repr(c))
        # 但对象仍然持有 Key，repr=False 并不等于加密。
        self.assertTrue(c.has_api_key)

    def test_empty_model(self) -> None:
        """存在但全为空格的模型名称必须被拒绝。"""
        # 创建一个可被 strip 清空的模型字符串。
        with patch.dict(os.environ, {"OPENAI_MODEL": "  "}, clear=True):
            # 检查加载过程中发生 ConfigError。
            with self.assertRaises(ConfigError):
                # 在不需要 API Key 的离线模式下执行。
                load_config(Path("/nonexistent/lesson17.env"), require_api_key=False)


if __name__ == "__main__":
    # 单独运行测试文件时执行所有测试。
    unittest.main()
