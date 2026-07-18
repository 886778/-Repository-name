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


def test_backend_modules_do_not_import_platform_or_runtime_composition() -> None:
    module_imports = imported_modules(PROJECT_ROOT / "packages/backend/src/ai_bazi_backend/modules")

    forbidden_prefixes = (
        "ai_bazi_backend.bootstrap",
        "ai_bazi_backend.platform",
        "ai_bazi_backend.projections",
    )
    assert not any(name.startswith(forbidden_prefixes) for name in module_imports)


def test_platform_does_not_depend_on_business_modules_or_projections() -> None:
    platform_imports = imported_modules(
        PROJECT_ROOT / "packages/backend/src/ai_bazi_backend/platform"
    )

    forbidden_prefixes = (
        "ai_bazi_backend.modules",
        "ai_bazi_backend.projections",
    )
    assert not any(name.startswith(forbidden_prefixes) for name in platform_imports)


def test_domain_does_not_import_framework_or_infrastructure() -> None:
    domain_root = PROJECT_ROOT / "packages/backend/src/ai_bazi_backend/modules"
    imports = imported_modules(domain_root)
    forbidden_prefixes = (
        "fastapi",
        "pydantic",
        "asyncpg",
        "redis",
        "sqlalchemy",
        "ai_bazi_backend.platform",
        "ai_bazi_backend.bootstrap",
        "apps",
    )
    assert not any(name.startswith(forbidden_prefixes) for name in imports)


def test_calculation_kernel_has_no_io_or_ai_dependency() -> None:
    kernel_root = PROJECT_ROOT / "packages/backend/src/ai_bazi_backend/modules/chart_calculation"
    imports = imported_modules(kernel_root)
    forbidden_prefixes = (
        "socket",
        "urllib",
        "http",
        "httpx",
        "requests",
        "asyncpg",
        "redis",
        "sqlalchemy",
        "ai_bazi_backend.modules.ai",
        "ai_bazi_backend.modules.ai_analysis",
        "ai_bazi_backend.platform",
    )
    assert not any(name.startswith(forbidden_prefixes) for name in imports)
