"""课次讲义 PDF 质量验证：检查页数、中文可提取性和编译日志。"""

# 导入 argparse 解析 PDF 路径与对应课次。
import argparse
# 导入 hashlib 为构建产物计算稳定 SHA256。
import hashlib
# 导入 re 检索 PDF 页数、中文以及 LaTeX 警告。
import re
# 导入 subprocess 执行 pdfinfo 和 pdftotext。
import subprocess
# 导入 Path 处理跨平台 PDF 文件路径。
from pathlib import Path


def run_text_command(command: list[str]) -> str:
    """运行外部只读 PDF 检查命令，返回文本结果；失败时抛异常。"""
    # 使用参数列表执行，不启用 shell，避免路径注入。
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    # 返回实际 stdout，调用方自行按需解析。
    return result.stdout


def verify_pdf(pdf_path: Path, lesson_number: int) -> dict[str, str]:
    """核验 PDF 存在、页数、文本、中文字符、日志；返回内容哈希。"""
    # 先判断文件是否已被 XeLaTeX 实际生成。
    if not pdf_path.is_file():
        # 缺少生成文件必须立即阻止发布。
        raise AssertionError(f"PDF 不存在: {pdf_path}")
    # 检查 PDF 大小，过滤空白或明显损坏的占位文件。
    if pdf_path.stat().st_size < 6000:
        # 明确拒绝过小文件，不把扩展名作为构建成功证据。
        raise AssertionError(f"PDF 过小: {pdf_path}")
    # 使用 pdfinfo 提取真正的 PDF 元信息。
    info = run_text_command(["pdfinfo", str(pdf_path)])
    # 从 pdfinfo 输出中解析 Pages 字段。
    pages = re.search(r"^Pages:\s*(\d+)", info, flags=re.MULTILINE)
    # 教程包含正文和带注释的代码，原则上至少应该有两页。
    if pages is None or int(pages.group(1)) < 2:
        # 报告页数异常而不继续发布。
        raise AssertionError(f"PDF 页数异常: {pdf_path}")
    # pdftotext 验证中文确实进入 PDF 而非只有图片或空页。
    visible = run_text_command(["pdftotext", str(pdf_path), "-"])
    # 在文本中必须能够提取到 lesson 标题。
    if f"Lesson {lesson_number}" not in visible:
        # 标题缺失意味着可能编译错课或 PDF 内容损坏。
        raise AssertionError(f"未提取到 Lesson {lesson_number} 标题")
    # 提取可见的中日韩统一表意文字数量。
    chinese_count = len(re.findall(r"[\u4e00-\u9fff]", visible))
    # 至少 80 个中文汉字，排除只有封面的占位讲义。
    if chinese_count < 80:
        # 报告中文提取不足，以检查字体或内容问题。
        raise AssertionError(f"PDF 中文文本过少: {chinese_count}")
    # 从 build 目录读取 latexmk 产生的原始 TeX 日志。
    log_file = pdf_path.with_suffix(".log")
    # 没有编译日志的产物无法完成本次流程核验。
    if not log_file.is_file():
        # 强制保留 CI 阶段的 LaTeX 编译日志供检测。
        raise AssertionError(f"缺少编译日志: {log_file}")
    # 使用容错编码读取不同 TeX Live 环境输出的编译信息。
    latex_log = log_file.read_text(encoding="utf-8", errors="replace")
    # 禁止在存在缺失引用或致命分页溢出时发布。
    if "undefined references" in latex_log.lower() or "Overfull \\vbox" in latex_log:
        # 告知排版错误不能被上传成功掩盖。
        raise AssertionError(f"LaTeX 引用或垂直溢出警告: {log_file}")
    # 以字节模式读取 PDF，计算 SHA256 用于结果追溯。
    digest = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
    # 返回可以写入执行摘要的具体核验数据。
    return {"pages": pages.group(1), "chinese_characters": str(chinese_count), "sha256": digest}


def main() -> None:
    """读取命令行参数并打印真实 PDF 验证信息。"""
    # 建立命令行解析器，并描述参数用途。
    parser = argparse.ArgumentParser(description="校验中文课程 PDF")
    # 必需参数一：已经编译生成的 PDF 位置。
    parser.add_argument("pdf", type=Path)
    # 必需参数二：该 PDF 预期所属的课程号。
    parser.add_argument("lesson_number", type=int)
    # 解析外部传入的文件与课次。
    arguments = parser.parse_args()
    # 校验 PDF 本体并获得验证元数据。
    evidence = verify_pdf(arguments.pdf.resolve(), arguments.lesson_number)
    # 输出可追溯的页数、中文字数和 SHA256。
    print(f"PASS: Lesson {arguments.lesson_number} PDF {evidence}")


if __name__ == "__main__":
    # 直接执行时启动 CLI 核验。
    main()
