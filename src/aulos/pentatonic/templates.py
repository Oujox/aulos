"""五文字連鎖のテンプレート。西洋式の音程名や和音記号を仮定しない."""

from aulos.base import ChainInterval
from aulos.base import Template
from aulos.base import Templates

chords = Templates(
    (
        Template("", (ChainInterval(0, 0), ChainInterval(4, -2), ChainInterval(3, -1))),
        Template("open", (ChainInterval(0, 0), ChainInterval(1, 0), ChainInterval(0, 1))),
    )
)
scales = Templates(
    (
        Template(
            "natural",
            (
                ChainInterval(0, 0),
                ChainInterval(2, -1),
                ChainInterval(4, -2),
                ChainInterval(1, 0),
                ChainInterval(3, -1),
            ),
        ),
    )
)
