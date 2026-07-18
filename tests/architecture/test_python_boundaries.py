import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def imported_modules(source_root: Path) -> set[str]:
    modules: set[str] = set()
    for source_file in source_root.rglob("*.py"):
        tree = ast.parse(source_file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module)
    return modules


def test_api_and_worker_do_not_import_each_other() -> None:
    api_imports = imported_modules(PROJECT_ROOT / "apps/api/src")
    worker_imports = imported_modules(PROJECT_ROOT / "apps/worker/src")

    assert not any(name.startswith("ai_bazi_worker") for name in api_imports)
    assert not any(name.startswith("ai_bazi_api") for name in worker_imports)
