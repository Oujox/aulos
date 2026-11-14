"""体系や規約との不整合を区別して捕捉するための例外."""


class NotationError(ValueError):
    """記譜体系の構造や対応範囲が不適合である."""


class TemperamentError(ValueError):
    """調律写像が対象の音程や操作に対応しない."""


class RepresentationError(ValueError):
    """綴りを指定の表現規約で表示できない."""


class RhythmError(ValueError):
    """拍子や周期リズムが対象の時刻や操作に対応しない."""
