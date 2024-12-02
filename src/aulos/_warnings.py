import warnings


def _formatwarning(message, category, filename, lineno, line=None):
    return (
        f"\033[93m{category.__name__}\033[0m: {message} "
        f"\033[90m(in {filename}:{lineno})\033[0m\n"
    )


warnings.formatwarning = _formatwarning


__all__ = []
