from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class QualityComponent:
    name: str
    group: int
    index: int
    intervals: tuple[int]
    diminution: tuple[int]
    enable: tuple[int] = field(default_factory=tuple)
    extensions: tuple[int] = field(default_factory=tuple)
    alterations: dict[int, int] = field(default_factory=dict)
    brackets: bool = field(default=False)

    def __post_init__(self):
        if not len(self.enable):
            enable = tuple(1 for _ in range(len(self.intervals)))
            object.__setattr__(self, "enable", enable)


@dataclass(frozen=True, slots=True)
class Quality:
    components: tuple[QualityComponent]

    @property
    def name(self) -> str:
        name: str = ""
        pre: QualityComponent | None = None

        for c in self.components:
            if pre is not None:
                if c.brackets and not pre.brackets:
                    name += "("
                if c.brackets and pre.brackets:
                    name += ","
                if not c.brackets and pre.brackets:
                    name += ")"
            name += c.name
            pre = c

        if pre.brackets:
            name += ")"
        return name

    @property
    def intervals(self) -> tuple[int]:
        intervals: list[int] = []
        extensions: set[int] = set()
        alterations: dict[int, int] = {}

        for rc in self.reversed:
            rc_intervals = [x + y for x, y in zip(rc.intervals, rc.diminution)]
            intervals = rc_intervals + intervals[len(rc_intervals) :]
            extensions.update(rc.extensions)
            alterations.update(rc.alterations)
        intervals.extend(extensions)

        for k, v in alterations.items():
            if k in intervals:
                intervals.remove(k)
                intervals.append(k + v)

        intervals.sort()
        return intervals

    @property
    def reversed(self):
        return tuple(
            sorted(self.components, key=lambda c: (c.group, c.index), reverse=True)
        )
