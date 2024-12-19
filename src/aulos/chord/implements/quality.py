import typing as t

from ..quality import QualityComponent


def validate(components: tuple[QualityComponent]) -> bool:

    def validate_empty(components: tuple[QualityComponent]):
        return not len(components) == 0

    def validate_enable(reversed: tuple[QualityComponent]):
        enable: tuple[int] = ()
        for rc in reversed:
            if all(z[0] == z[1] for z in zip(enable, rc.enable)):
                if len(enable) < len(rc.enable):
                    enable = rc.enable
            else:
                return False
        return True

    def validate_alternations(reversed: tuple[QualityComponent]):
        # allowed quality
        if any(True for rc in reversed if rc.name == "dim"):
            return True

        intervals = []
        alternations = {}
        for rc in reversed:
            rc_intervals = [x + y for x, y in zip(rc.intervals, rc.diminution)]
            intervals = rc_intervals + intervals[len(rc_intervals) :]
            alternations.update(rc.alterations)
        return all(False for alt in alternations.keys() if alt not in intervals)

    if not all(isinstance(c, QualityComponent) for c in components):
        return False

    reversed_components = tuple(
        sorted(components, key=lambda c: (c.group, c.index), reverse=True)
    )
    return all(
        [
            validate_empty(reversed_components),
            validate_enable(reversed_components),
            validate_alternations(reversed_components),
        ]
    )


DEFAULT_QUALITY_VALIDATOR: t.Callable[[tuple[QualityComponent]], bool] = validate
DEFAULT_QUALITY_COMPONENTS: t.Final[tuple[QualityComponent]] = (
    QualityComponent(
        "",
        1,
        0,
        (0, 4, 7),
        (0, 0, 0),
    ),
    QualityComponent(
        "m",
        1,
        0,
        (0, 4, 7),
        (0, -1, 0),
    ),
    QualityComponent(
        "dim",
        1,
        0,
        (0, 4, 7),
        (0, -1, 0),
        alterations={7: -1, 10: -1},
    ),
    QualityComponent(
        "aug",
        1,
        0,
        (0, 4, 7),
        (0, 0, 0),
        alterations={7: 1},
    ),
    QualityComponent(
        "sus2",
        1,
        0,
        (0, 4, 7),
        (0, 0, 0),
        alterations={4: -2},
    ),
    QualityComponent(
        "sus4",
        1,
        0,
        (0, 4, 7),
        (0, 0, 0),
        alterations={4: 1},
    ),
    QualityComponent(
        "6",
        2,
        0,
        (0, 4, 7, 9),
        (0, 0, 0, 0),
    ),
    QualityComponent(
        "7",
        2,
        0,
        (0, 4, 7, 11),
        (0, 0, 0, -1),
    ),
    QualityComponent(
        "M7",
        2,
        0,
        (0, 4, 7, 11),
        (0, 0, 0, 0),
    ),
    QualityComponent(
        "9",
        3,
        0,
        (0, 4, 7, 11, 14),
        (0, 0, 0, 0, 0),
    ),
    QualityComponent(
        "b9",
        3,
        0,
        (0, 4, 7, 11, 14),
        (0, 0, 0, 0, -1),
    ),
    QualityComponent(
        "#9",
        3,
        0,
        (0, 4, 7, 11, 14),
        (0, 0, 0, 0, 1),
    ),
    QualityComponent(
        "11",
        3,
        0,
        (0, 4, 7, 11, 14, 17),
        (0, 0, 0, 0, 0, 0),
    ),
    QualityComponent(
        "#11",
        3,
        0,
        (0, 4, 7, 11, 14, 17),
        (0, 0, 0, 0, 0, 1),
    ),
    QualityComponent(
        "13",
        3,
        0,
        (0, 4, 7, 11, 14, 17, 21),
        (0, 0, 0, 0, 0, 0, 0),
    ),
    QualityComponent(
        "b13",
        3,
        0,
        (0, 4, 7, 11, 14, 17, 21),
        (0, 0, 0, 0, 0, 0, -1),
    ),
    QualityComponent(
        "add2",
        4,
        0,
        (0, 4, 7),
        (0, 0, 0),
        extensions=(2,),
    ),
    QualityComponent(
        "add6",
        4,
        0,
        (0, 4, 7),
        (0, 0, 0),
        extensions=(9,),
    ),
    QualityComponent(
        "add9",
        4,
        0,
        (0, 4, 7),
        (0, 0, 0),
        extensions=(14,),
        enable=(1, 1, 1, 0, 1),
    ),
    QualityComponent(
        "add11",
        4,
        0,
        (0, 4, 7),
        (0, 0, 0),
        extensions=(17,),
        enable=(1, 1, 1, 0, 0, 1),
    ),
    QualityComponent(
        "add13",
        4,
        0,
        (0, 4, 7),
        (0, 0, 0),
        extensions=(21,),
        enable=(1, 1, 1, 0, 0, 0, 1),
    ),
    QualityComponent(
        "b5",
        5,
        0,
        (0, 4, 7),
        (0, 0, 0),
        alterations={7: -1},
        brackets=True,
    ),
    QualityComponent(
        "#5",
        5,
        0,
        (0, 4, 7),
        (0, 0, 0),
        alterations={7: 1},
        brackets=True,
    ),
    QualityComponent(
        "b9",
        5,
        1,
        (0, 4, 7),
        (0, 0, 0),
        alterations={14: -1},
        brackets=True,
    ),
    QualityComponent(
        "#9",
        5,
        1,
        (0, 4, 7),
        (0, 0, 0),
        alterations={14: 1},
        brackets=True,
    ),
    QualityComponent(
        "b11",
        5,
        2,
        (0, 4, 7),
        (0, 0, 0),
        alterations={17: -1},
        brackets=True,
    ),
    QualityComponent(
        "#11",
        5,
        2,
        (0, 4, 7),
        (0, 0, 0),
        alterations={17: 1},
        brackets=True,
    ),
    QualityComponent(
        "b13",
        5,
        3,
        (0, 4, 7),
        (0, 0, 0),
        alterations={21: -1},
        brackets=True,
    ),
    QualityComponent(
        "#13",
        5,
        3,
        (0, 4, 7),
        (0, 0, 0),
        alterations={21: 1},
        brackets=True,
    ),
    QualityComponent(
        "omit5",
        6,
        0,
        (0, 4),
        (0, 0, 0),
        enable=(1, 1, 0),
    ),
    QualityComponent(
        "omit3",
        6,
        0,
        (0, 7),
        (0, 0, 0),
        enable=(1, 0, 1),
    ),
    QualityComponent(
        "omit1",
        6,
        0,
        (4, 7),
        (0, 0, 0),
        enable=(0, 1, 1),
    ),
)
