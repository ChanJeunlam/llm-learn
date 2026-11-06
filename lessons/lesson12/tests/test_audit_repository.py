"""Lesson 12：使用临时目录测试仓库结构审计函数。"""

# 导入 unittest 单元测试框架。
import unittest
# 导入 tempfile 隔离每次测试的文件。
import tempfile
# 导入 sys 配置本课模块路径。
import sys
# 导入 Path 组合目录。
from pathlib import Path

# 计算本课 code 目录的位置。
CODE_DIR = Path(__file__).resolve().parents[1] / "code"
# 将 code 目录插入模块查找路径。
sys.path.insert(0, str(CODE_DIR))
# 导入待测审计函数及必要路径清单。
from audit_repository import REQUIRED_FILES, find_missing_files


class RepositoryAuditTests(unittest.TestCase):
    """分别覆盖空仓库和文件完整的仓库。"""

    def test_missing_required_files(self) -> None:
        """空目录应该报告所有必要文件缺失。"""
        # 临时目录在 with 退出后自动清理。
        with tempfile.TemporaryDirectory() as temp:
            # 把路径转换成 Path。
            root = Path(temp)
            # 运行结构审计并获得缺失清单。
            missing = find_missing_files(root)
            # 数量必须等于要求检查的全部文件数。
            self.assertEqual(len(missing), len(REQUIRED_FILES))

    def test_complete_required_files(self) -> None:
        """人为创建必要文件后，审计应该全部通过。"""
        # 创建隔离的临时目录。
        with tempfile.TemporaryDirectory() as temp:
            # 构造临时仓库的根路径。
            root = Path(temp)
            # 遍历要求创建的相对路径。
            for relative in REQUIRED_FILES:
                # 创建临时文件的完整路径。
                destination = root / relative
                # 递归创建父目录，保证多层 GitHub 工作流路径可写。
                destination.parent.mkdir(parents=True, exist_ok=True)
                # 写入非空内容，模拟已经存在的仓库文件。
                destination.write_text("demo", encoding="utf-8")
            # 结构合格时没有缺失路径。
            self.assertEqual(find_missing_files(root), [])


if __name__ == "__main__":
    # 支持单独运行本课测试。
    unittest.main()

