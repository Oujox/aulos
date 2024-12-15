import typing as t
from ..quality import QualityComponent


def validate(components: tuple[QualityComponent]) -> bool:

    def validate_empty(components: tuple[QualityComponent]):
        return not len(components) == 0

    def validate_uniques(reversed: tuple[QualityComponent]):
        uniques = set((c.group, c.index) for c in reversed)
        if not len(uniques) == len(reversed):
            return False
        return True

    def validate_enable(reversed: tuple[QualityComponent]):
        enable: tuple[int] = ()
        for c in reversed:
            if all(z[0] == z[1] for z in zip(enable, c.enable)):
                if len(enable) < len(c.enable):
                    enable = c.enable
            else:
                return False
        return True

    if not all(isinstance(c, QualityComponent) for c in components):
        return False

    reversed_components = tuple(
        sorted(components, key=lambda c: (c.group, c.index), reverse=True)
    )
    return all(
        [
            validate_empty(reversed_components),
            validate_uniques(reversed_components),
            validate_enable(reversed_components),
        ]
    )


DEFAULT_QUALITY_VALIDATOR: t.Callable[[tuple[QualityComponent]], bool] = validate
DEFAULT_QUALITY_COMPONENTS: t.Final[tuple[QualityComponent]] = (
    QualityComponent("", 1, 0, (0, 4, 7)),
    QualityComponent("m", 1, 0, (0, 3, 7)),
    QualityComponent("dim", 1, 0, (0, 3, 6), alterations={10: 9}),
    QualityComponent("aug", 1, 0, (0, 4, 8)),
    QualityComponent("sus2", 1, 0, (0, 2, 7)),
    QualityComponent("sus4", 1, 0, (0, 5, 7)),
    QualityComponent("6", 2, 0, (0, 4, 7, 9)),
    QualityComponent("7", 2, 0, (0, 4, 7, 10)),
    QualityComponent("M7", 2, 0, (0, 4, 7, 11)),
    QualityComponent("b5", 3, 0, (0, 4, 7), alterations={7: 6}, brackets=True),
    QualityComponent("#5", 3, 0, (0, 4, 7), alterations={7: 8}, brackets=True),
    QualityComponent("omit5", 3, 0, (0, 4, 7), enable=(1, 1, 0), brackets=True),
    QualityComponent("omit3", 3, 0, (0, 4, 7), enable=(1, 0, 1), brackets=True),
    QualityComponent("omit1", 3, 0, (0, 4, 7), enable=(0, 1, 1), brackets=True),
    QualityComponent("add2", 4, 0, (0, 4, 7), extensions=(2,)),
    QualityComponent("add6", 4, 0, (0, 4, 7), extensions=(9,)),
    QualityComponent("add9", 4, 0, (0, 4, 7), extensions=(14,), enable=(1, 1, 1, 0, 1)),
    QualityComponent(
        "add11", 4, 0, (0, 4, 7), extensions=(17,), enable=(1, 1, 1, 0, 0, 1)
    ),
    QualityComponent(
        "add13", 4, 0, (0, 4, 7), extensions=(21,), enable=(1, 1, 1, 0, 0, 0, 1)
    ),
    QualityComponent("9", 5, 0, (0, 4, 7, 11, 14), brackets=True),
    QualityComponent("b9", 5, 0, (0, 4, 7, 11, 13), brackets=True),
    QualityComponent("#9", 5, 0, (0, 4, 7, 11, 15), brackets=True),
    QualityComponent("11", 5, 1, (0, 4, 7, 11, 14, 17), brackets=True),
    QualityComponent("#11", 5, 1, (0, 4, 7, 11, 14, 18), brackets=True),
    QualityComponent("13", 5, 2, (0, 4, 7, 14, 11, 17, 21), brackets=True),
    QualityComponent("b13", 5, 2, (0, 4, 7, 11, 14, 17, 20), brackets=True),
)
