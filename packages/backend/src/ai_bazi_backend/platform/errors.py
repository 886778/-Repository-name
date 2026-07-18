from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ErrorDescriptor:
    code: str
    title: str
    detail: str
    retryable: bool = False


class PlatformError(Exception):
    """Technical failure with a stable, safe-to-expose descriptor."""

    descriptor = ErrorDescriptor(
        code="SYSTEM-001",
        title="平台暂时不可用",
        detail="请求暂时无法完成，请稍后重试。",
        retryable=True,
    )

    def __init__(self, *, cause: Exception | None = None) -> None:
        super().__init__(self.descriptor.detail)
        self.__cause__ = cause


class ConfigurationError(PlatformError):
    descriptor = ErrorDescriptor(
        code="SYSTEM-CONFIG-001",
        title="服务配置无效",
        detail="服务无法使用当前配置安全启动。",
    )


class DependencyUnavailableError(PlatformError):
    descriptor = ErrorDescriptor(
        code="SYSTEM-DEPENDENCY-001",
        title="依赖服务暂时不可用",
        detail="必要的依赖服务暂时不可用，请稍后重试。",
        retryable=True,
    )


__all__ = [
    "ConfigurationError",
    "DependencyUnavailableError",
    "ErrorDescriptor",
    "PlatformError",
]
