"""Lesson 17：从环境变量与 .env 安全加载 LLM 配置。

用途：不访问网络、不调用付费 API；可用 python code/config.py --offline 检查配置。
配置来源：系统环境变量 > 本课本地 .env > 代码中的非敏感默认值。
安全限制：不会打印完整 API Key；测试只使用假的示例密钥。
"""

# argparse 将命令行选项转换为程序可读的参数。
import argparse
# math.isfinite 排除无穷大和 NaN 等非法超时值。
import math
# os.getenv 从进程环境中读取字符串配置。
import os
# dataclass 简化配置对象；field 控制私有字段的显示。
from dataclasses import dataclass, field
# Path 定位本课文件夹和 .env。
from pathlib import Path
# load_dotenv 读取本地配置文件，默认不会覆盖系统变量。
from dotenv import load_dotenv


# 自定义异常区分配置错误与真实网络 API 错误。
class ConfigError(ValueError):
    """配置缺失、格式不正确或超出允许范围时抛出。"""


# frozen 防止创建后意外重新赋值，但不提供密钥加密。
@dataclass(frozen=True)
class AppConfig:
    """经过验证的配置，模型名、超时秒数、Token 上限和私有 Key。

    参数：model 为模型 ID；timeout_seconds 单位秒；
    max_output_tokens 为正整数；api_key 为不应打印的秘密。
    """

    # 选择有访问权限的模型 ID。
    model: str
    # 设置网络超时时间（秒）。
    timeout_seconds: float
    # 控制大模型最大输出 Token 数。
    max_output_tokens: int
    # 防止普通 print(config) 将 Key 输出到日志。
    api_key: str = field(repr=False)

    # 属性让外部代码不用读取 Key 就知道是否已配置。
    @property
    def has_api_key(self) -> bool:
        """只返回是否存在凭据，不输出凭据本身。"""
        # 空字符串为 False，非空字符串为 True。
        return bool(self.api_key)


def parse_timeout(value: str) -> float:
    """把环境文本转换为 0–120 秒内的有限正数，否则抛 ConfigError。"""
    try:
        # 将字符串转换为 float。
        timeout = float(value)
    except ValueError as error:
        # 出错时只报告字段名称，不回显用户传入的原始内容。
        raise ConfigError("LLM_TIMEOUT_SECONDS 必须是数字") from error
    # 禁止 inf、nan、负值、零和高于 120 的超时。
    if not math.isfinite(timeout) or not 0 < timeout <= 120:
        # 返回安全的边界提示。
        raise ConfigError("LLM_TIMEOUT_SECONDS 必须在 0 到 120 秒之间")
    # 以秒为单位返回合法的超时配置。
    return timeout


def parse_max_tokens(value: str) -> int:
    """把环境文本转换为 1–8192 的整数 Token 上限，否则抛 ConfigError。"""
    try:
        # int 会拒绝 "1.5" 等非整数文本。
        tokens = int(value)
    except ValueError as error:
        # 报错只显示配置名称，避免泄露意外输入的秘密。
        raise ConfigError("LLM_MAX_OUTPUT_TOKENS 必须是整数") from error
    # 在调用收费 API 前检查教学用途允许的 Token 上限。
    if not 1 <= tokens <= 8192:
        # 过小或过大的值都明确拒绝。
        raise ConfigError("LLM_MAX_OUTPUT_TOKENS 必须介于 1 与 8192")
    # 返回已验证的最大输出 Token 数。
    return tokens


def load_config(env_file: Path | None = None, require_api_key: bool = True) -> AppConfig:
    """读取配置并执行验证。

    参数：env_file 默认为本课 .env；require_api_key 为是否强制要求 Key。
    返回：AppConfig。异常：ConfigError。
    """
    # 使用代码文件自身路径定位 lesson17，不依赖终端启动目录。
    lesson_folder = Path(__file__).resolve().parents[1]
    # 支持单元测试提供临时 .env 路径以隔离真实环境。
    dotenv_path = env_file if env_file is not None else lesson_folder / ".env"
    # override=False：系统已存在的环境变量保持最高优先级。
    load_dotenv(dotenv_path=dotenv_path, override=False)
    # 未配置模型时使用教学默认值，其他环境可通过 OPENAI_MODEL 覆盖。
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini").strip()
    # 非空模型名称是发送请求之前的基本校验。
    if not model:
        # 不打印可疑输入值，只指出错误配置名。
        raise ConfigError("OPENAI_MODEL 不能为空")
    # 将文本超时转换为已经验证的正浮点数。
    timeout = parse_timeout(os.getenv("LLM_TIMEOUT_SECONDS", "30"))
    # 将 Token 上限转换为已经验证的正整数。
    max_tokens = parse_max_tokens(os.getenv("LLM_MAX_OUTPUT_TOKENS", "500"))
    # API Key 只从环境中读取，绝不能硬编码在源文件内。
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    # 正常联网应强制要求密钥，离线练习可明确关闭这一要求。
    if require_api_key and not api_key:
        # 安全报错不会暴露任何密钥内容。
        raise ConfigError("缺少 OPENAI_API_KEY；请使用环境变量或未提交的 .env")
    # 生成只读配置实例，后续业务代码按字段访问。
    return AppConfig(model, timeout, max_tokens, api_key)


def main() -> None:
    """CLI 配置检查入口；--offline 不要求 Key，也不连接网络。"""
    # 创建可以显示 --help 的命令行解析器。
    parser = argparse.ArgumentParser(description="Lesson 17：LLM 配置安全检查")
    # --offline 是不连接大模型服务的学习模式。
    parser.add_argument("--offline", action="store_true", help="允许不设置 API Key")
    # 获取解析后的布尔开关。
    options = parser.parse_args()
    try:
        # 离线模式允许无 Key，正常模式则要求存在 Key。
        config = load_config(require_api_key=not options.offline)
    except ConfigError as error:
        # 配置不合格时以非零退出码结束，而非报告运行成功。
        parser.exit(2, f"配置错误：{error}\n")
    # 只打印可以公开的模型名称。
    print(f"模型名称：{config.model}")
    # 打印以秒计量的超时时间。
    print(f"超时：{config.timeout_seconds:g} 秒")
    # 打印最大输出 Token 上限。
    print(f"最大输出：{config.max_output_tokens} tokens")
    # 只报告是否存在 Key，绝不打印 Key 本身。
    print(f"API Key 已配置：{'是' if config.has_api_key else '否'}")


if __name__ == "__main__":
    # 仅直接运行脚本时调用 CLI，import 时不自动执行。
    main()
