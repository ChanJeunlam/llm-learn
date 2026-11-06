"""课程结构与 Python 注释静态审计；不执行外部网络请求。"""

# 导入 ast，检查 Python 模块与函数是否含有标准 docstring。
import ast
# 导入 sys，使用退出码标记是否通过审计。
import sys
# 导入 tokenize，区分代码与注释，避免简单文本匹配误判。
import tokenize
# 导入 Path，跨平台遍历课程目录。
from pathlib import Path

# 获取当前脚本所在仓库的根目录，避免依赖调用方工作目录。
ROOT = Path(__file__).resolve().parents[1]
# 本次实际已制作的课次，需要每课均具备完整材料。
ACTIVE_LESSONS = tuple(range(11, 17))
# 所有课程共有的必须存在的文件或目录。
REQUIRED = ("README.md", "lecture.md", "lecture.tex",
            "code", "tests", "results/verification.md")


def audit_python_source(file_path: Path) -> list[str]:
    """检查指定 Python 源文件的语法、模块/函数 docstring 和注释覆盖。"""
    # 用 UTF-8 读取源代码，确保中文注释不会因为平台编码丢失。
    source = file_path.read_text(encoding="utf-8")
    # 创建空的问题清单，供 CI 最后汇总。
    errors = []
    try:
        # 解析 AST 以核实所有类和函数定义，而非使用正则猜测。
        tree = ast.parse(source, filename=str(file_path))
    except SyntaxError as error:
        # 语法错误直接记入问题清单并终止本文件后续检测。
        return [f"{file_path}: Python SyntaxError: {error}"]
    # 顶层必须有说明模块目的、用途和使用限制的文档字符串。
    if not ast.get_docstring(tree):
        # 缺少模块文档字符串时报告清晰路径。
        errors.append(f"{file_path}: 缺少模块 docstring")
    # 遍历当前源文件中所有 AST 节点。
    for node in ast.walk(tree):
        # 仅检查真实的函数、异步函数及类定义。
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            # 类和函数都需要用 docstring 说明作用，方便教学阅读。
            if not ast.get_docstring(node):
                # 记录具体函数或类名，以便定位修改。
                errors.append(f"{file_path}:{node.lineno} {node.name} 缺少 docstring")
    # 构造所有非空代码行，为注释密度提供保守的静态度量。
    code_lines = [line for line in source.splitlines()
                  if line.strip() and not line.lstrip().startswith("#")]
    # 构造单独注释行列表，主要检查逐行说明覆盖是否足够。
    comment_lines = [line for line in source.splitlines()
                     if line.lstrip().startswith("#")]
    # 如果教程源码过长但注释极少，说明没有达到逐行解释的底线。
    if code_lines and len(comment_lines) / len(code_lines) < 0.55:
        # 报告两类行数，便于定量追踪覆盖情况。
        errors.append(f"{file_path}: 中文逐行注释密度不足 "
                      f"({len(comment_lines)} comments / {len(code_lines)} code lines)")
    # 尽量检查实际使用了 Python 注释符，而不是只用空行充数。
    with file_path.open("rb") as handle:
        # tokenize 会把字符串中的 # 和真正注释区分开。
        actual_comments = [token for token in tokenize.tokenize(handle.readline)
                           if token.type == tokenize.COMMENT]
    # 当存在大量代码但少于 3 条真实注释时判定不合格。
    if len(code_lines) >= 15 and len(actual_comments) < 3:
        # 记录缺少可识别注释的审计问题。
        errors.append(f"{file_path}: 实际注释 Token 不足")
    # 返回本文件全部检测问题；列表为空意味着静态审查通过。
    return errors


def audit_course() -> list[str]:
    """检查六课目录、双格式讲义、代码、测试、验证记录和注释质量。"""
    # 初始化整个课程的错误列表。
    errors = []
    # 逐一核实已经制作的六节课，禁止只建空目录。
    for lesson_number in ACTIVE_LESSONS:
        # 当前课的约定路径为 lessons/lessonN。
        folder = ROOT / "lessons" / f"lesson{lesson_number}"
        # 检查课程文件是否按规范存在。
        for relative in REQUIRED:
            # 获得必要文件的完整路径。
            destination = folder / relative
            # 如果文件或目录不存在则记录错误。
            if not destination.exists():
                # 显示相对仓库根目录的可识别路径。
                errors.append(f"缺失：{destination.relative_to(ROOT)}")
        # 确认源代码与测试中至少各有一个 Python 文件。
        for subfolder in ("code", "tests"):
            # 当前子目录必须存在，方可继续深入扫描。
            directory = folder / subfolder
            # 不存在的目录已由 REQUIRED 检查报告，防止重复错误。
            if not directory.is_dir():
                # 跳过本目录，继续审计其他课。
                continue
            # 查找本课这个子目录中的全部 Python 源码。
            python_files = sorted(directory.rglob("*.py"))
            # 没有 Python 文件的教学单元不符合目前 11–16 课的要求。
            if not python_files:
                # 报告缺少代码/测试文件的位置。
                errors.append(f"缺少 Python 文件：{directory.relative_to(ROOT)}")
            # 逐个检查 Python 文件的函数 docstring 和逐行注释。
            for path in python_files:
                # 把单文件审计问题合并到课程问题清单中。
                errors.extend(audit_python_source(path))
    # 完整返回全部审计问题，不因发现一个错误就中止。
    return errors


def main() -> None:
    """输出检查摘要；失败时使用退出码 1 让 Actions 准确报红。"""
    # 执行全课程静态检查。
    errors = audit_course()
    # 若结果非空，需要把全部问题写入 CI 日志。
    if errors:
        # 逐条显示问题，避免隐藏后面的错误。
        for item in errors:
            # 使用固定的 ERROR 前缀，方便自动化日志检索。
            print("ERROR:", item)
        # 使用非零退出码，阻止 CI 误报成功。
        sys.exit(1)
    # 只有全部课程结构与注释满足要求时才打印通过。
    print(f"PASS: {len(ACTIVE_LESSONS)} 节课程目录、源码与注释静态审计通过")


if __name__ == "__main__":
    # 在直接运行工具时启动审计，作为模块导入不会产生副作用。
    main()
