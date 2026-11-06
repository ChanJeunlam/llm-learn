# Lesson 12｜GitHub 分支、PR 与自动化 CI

**学习目标：** 会使用 feature 分支、PR 和 GitHub Actions；编写仓库结构自动审计程序。

**先修：** Lesson 11。　**建议时间：** 90–120 分钟。

## 本课原理

### GitHub 协作流程

从 main 切出 feature 分支、提交并 push，在 GitHub 打开 Pull Request；通过 Files changed 检查差异，等待 Actions 通过，再进行合并。PR 是协作审查流程而不是 Git 原生命令。

### CI 是什么

CI 指提交后自动执行语法检查、单元测试、静态审查。失败时要读取作业步骤、退出码、标准输出与报错堆栈，禁止继续声称验证成功。对外部贡献的 PR 不应自动授权付费服务或密钥。

### 仓库审计程序

REQUIRED_FILES 列出课程总纲、规范和工作流；find_missing_files 使用 Path.is_file 返回缺失路径；main 把结构检查结果转换成进程退出码。该函数可被测试复用。

### 练习命令

先执行 python lessons/lesson12/code/audit_repository.py --root .；再运行 git switch -c feature/lesson12-practice，提交文档更改并创建 PR，观察 CI 日志。

## 核心关系或公式

$$
\mathrm{CI}=\mathrm{syntax\ check}+\mathrm{tests}+\mathrm{artifact\ verification}
$$

## 实操：本课全部示例源码

完整的本课源码如下，模块顶部、每个函数及每条关键语句均附解释。源文件是可执行的，不是伪代码。

```python
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
```

## 自动测试、练习与验收

- PR 能独立创建并说明安全合并策略。
- 能够指出 Actions 的失败步骤。
- 审计程序对空仓库与完整仓库的测试都通过。

从本课目录运行 `python -m unittest discover -s tests -v`；真实运行证据请阅读 [验证记录](results/verification.md)。

## 官方参考

Git：https://git-scm.com/docs ；GitHub：https://docs.github.com/en/actions ；HTTP：https://developer.mozilla.org/en-US/docs/Web/HTTP ；OpenAI Responses API：https://platform.openai.com/docs/api-reference/responses。
