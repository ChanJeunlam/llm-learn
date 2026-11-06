"""Lesson 11：在临时 Git 仓库中测试状态查询，不改变用户仓库。"""

# 导入 unittest，组织可重复执行的测试。
import unittest
# 导入 tempfile，提供测试结束即删除的工作目录。
import tempfile
# 导入 subprocess，初始化临时 Git 仓库。
import subprocess
# 导入 Path，统一管理临时路径。
from pathlib import Path
# 导入 sys，将本课代码目录放入模块搜索路径。
import sys

# 计算 test 文件所在课次的 code 路径。
CODE_DIR = Path(__file__).resolve().parents[1] / "code"
# 允许测试 import 本课主程序，不需要安装 Python 包。
sys.path.insert(0, str(CODE_DIR))
# 导入本课待测函数。
from inspect_git import run_git, summarize_repository


class GitInspectorTests(unittest.TestCase):
    """使用临时仓库检查 Git 命令封装与状态提取。"""

    def test_git_status_after_first_commit(self) -> None:
        """初始化并提交一次后，检查摘要可读取主分支与提交。"""
        # 使用临时目录避免污染仓库。
        with tempfile.TemporaryDirectory() as temp:
            # 把临时目录的字符串转成 Path。
            root = Path(temp)
            # 初始化主分支；git 对当前机器未安装的情况会明确失败。
            subprocess.run(["git", "init", "-b", "main", str(root)], check=True, capture_output=True)
            # 在本次仓库范围内配置测试身份，不改动全局 Git 配置。
            run_git(root, "config", "user.name", "Course Test")
            # 设置临时邮箱，仅用于创建测试提交。
            run_git(root, "config", "user.email", "course@example.invalid")
            # 创建第一个受版本控制的文本文件。
            (root / "hello.txt").write_text("hello", encoding="utf-8")
            # 把测试文件暂存到 Git。
            run_git(root, "add", "hello.txt")
            # 创建首次提交，满足读取 git log 的前置条件。
            run_git(root, "commit", "-m", "first")
            # 调用本课封装函数获得仓库摘要。
            summary = summarize_repository(root)
            # 验证当前分支为 main。
            self.assertEqual(summary["branch"], "main")
            # 验证首次提交可以被读取。
            self.assertIn("first", summary["latest_commit"])
            # 提交后不应再有未提交文件。
            self.assertEqual(summary["status"], "")


if __name__ == "__main__":
    # 支持直接运行此测试文件。
    unittest.main()

