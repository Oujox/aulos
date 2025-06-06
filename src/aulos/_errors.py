class ValidationError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)

    def __str__(self) -> str:
        return f"[ValidationError]: {self.message}"


__all__ = [
    "ValidationError",
]
