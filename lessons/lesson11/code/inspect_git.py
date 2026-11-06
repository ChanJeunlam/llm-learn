"""Lesson 11：检查本地 Git 仓库状态与提交；仅调用本机 git，不修改仓库。"""

# 导入 argparse，用于解析命令行中可选的仓库目录参数。
import argparse
# 导入 subprocess，以参数列表安全执行本地 Git 命令。
import subprocess
# 导入 Path，以独立于操作系统的方式管理文件路径。
from pathlib import Path


def run_git(directory: Path, *arguments: str) -> str:
    """在指定仓库执行 Git 子命令，返回标准输出；失败时抛出异常。"""
    # 构造完整 Git 命令；不用 shell=True，以避免命令注入。
    command = ["git", "-C", str(directory), *arguments]
    # 执行命令，检查非零返回码，并把字节解码为文本。
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    # 去掉输出头尾的换行，但不改变内部内容。
    return completed.stdout.strip()


def summarize_repository(directory: Path) -> dict[str, str]:
    """读取分支、工作区状态与最新提交，返回可序列化的摘要字典。"""
    # 查询 HEAD 对应的当前分支；如果是 detached HEAD 可能返回 HEAD。
    branch = run_git(directory, "rev-parse", "--abbrev-ref", "HEAD")
    # 使用 porcelain 格式读取工作区，便于程序进行后续处理。
    status = run_git(directory, "status", "--short")
    # 读取最新一次提交的短哈希和主题，不修改仓库历史。
    latest = run_git(directory, "log", "-1", "--pretty=%h %s")
    # 把三个字段合成为字典，供打印或下一课做 JSON 化。
    return {"branch": branch, "status": status, "latest_commit": latest}


def main() -> None:
    """解析路径、调用 Git 状态检查函数，并输出用户可读的结果。"""
    # 创建命令行解析器，并描述这个工具的用途。
    parser = argparse.ArgumentParser(description="Lesson 11: Git 仓库状态查询")
    # 接受可选目录参数；默认检查当前工作目录。
    parser.add_argument("directory", nargs="?", default=".")
    # 把命令行字符串转换为结构化参数。
    arguments = parser.parse_args()
    # 将指定目录转换为绝对路径，避免工作目录歧义。
    directory = Path(arguments.directory).resolve()
    try:
        # 读取 Git 摘要；git 不存在或目录不合法时可能失败。
        summary = summarize_repository(directory)
    except (FileNotFoundError, subprocess.CalledProcessError) as error:
        # 明确说明操作失败，而不是捏造分支和提交结果。
        parser.exit(1, f"Git 检查失败: {error}\n")
    # 逐个输出摘要字段，让读者理解 Git 的三个常用视角。
    for key, value in summary.items():
        # 对空工作区状态使用明确说明，避免误认为漏掉输出。
        print(f"{key}: {value or '(clean)'}")


if __name__ == "__main__":
    # 只在直接运行本文件时调用入口，import 时不自动检查仓库。
    main()

