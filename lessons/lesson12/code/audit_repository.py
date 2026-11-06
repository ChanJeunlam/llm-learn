"""Lesson 12：检查 LLM 课程仓库是否具备必要的目录和 CI 配置。"""

# 导入 argparse，允许命令行传入仓库根目录。
import argparse
# 导入 Path，进行跨平台路径检查。
from pathlib import Path

# 定义必要的仓库文件，列表本身即体现基础工程约束。
REQUIRED_FILES = (
    "README.md",
    "COURSE_PLAN.md",
    "COURSE_STANDARDS.md",
    ".github/workflows/course-code-ci.yml",
    ".github/workflows/course-latex.yml",
)


def find_missing_files(repository_root: Path) -> list[str]:
    """返回缺失文件的相对路径；没有缺失时返回空列表。"""
    # 初始化空列表，用于积累所有发现的问题。
    missing = []
    # 遍历预先定义的所有必须存在的相对路径。
    for relative_path in REQUIRED_FILES:
        # 与仓库根目录组合成完整路径。
        candidate = repository_root / relative_path
        # 若该路径不是实际存在的文件，则加入缺失清单。
        if not candidate.is_file():
            # 使用相对路径保存，避免测试日志依赖不同机器的路径。
            missing.append(relative_path)
    # 把结果返回给调用者，以便单元测试或 CLI 使用。
    return missing


def main() -> None:
    """检查指定的课程仓库，并用退出码区分合格与缺失。"""
    # 创建命令行解析器，说明输入参数的用途。
    parser = argparse.ArgumentParser(description="课程仓库基础结构审计")
    # 默认值向上寻找三层，得到本项目 Git 仓库的根目录。
    default_root = Path(__file__).resolve().parents[3]
    # 允许用户指定另外一个待检查的仓库目录。
    parser.add_argument("--root", type=Path, default=default_root)
    # 完成命令行参数解析。
    arguments = parser.parse_args()
    # 检查仓库的必要文件是否齐全。
    missing = find_missing_files(arguments.root.resolve())
    # 如果存在缺失文件，应该以失败退出码结束。
    if missing:
        # 显示每个缺失路径，便于定位问题。
        for item in missing:
            # 保持报错格式统一，供自动化日志检索。
            print("缺失:", item)
        # 退出码 1 表示审计不合格。
        parser.exit(1, "仓库结构不满足要求\n")
    # 只有全部通过时才输出成功提示。
    print("仓库核心文件检查通过。")


if __name__ == "__main__":
    # 直接执行本程序时运行主函数，导入时不会自动审计。
    main()

