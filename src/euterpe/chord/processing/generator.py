import typing as t
from collections import defaultdict
from itertools import product

from ..quality import Quality, QualityComponent


class QualityGenerator:
    components: tuple[QualityComponent, ...]

    def __init__(
        self,
        components: tuple[QualityComponent, ...],
        validator: t.Callable[[tuple[QualityComponent, ...]], bool],
    ):
        self.components = components
        self.validator = validator

    def __iter__(self):
        partitioned_components = tuple(
            i_componets + (None,)
            for g_componets in self.partition_by_group(self.components)
            for i_componets in self.partition_by_index(g_componets)
        )
        for producted_components in product(*partitioned_components):
            filtered = tuple(filter(None, producted_components))
            if self.validator(filtered):
                yield Quality(filtered)

    @classmethod
    def partition_by_group(
        cls, components: tuple[QualityComponent, ...]
    ) -> tuple[tuple[QualityComponent, ...], ...]:
        groups = defaultdict(list)
        for c in components:
            groups[c.group].append(c)
        return tuple(tuple(v) for _, v in groups.items())

    @classmethod
    def partition_by_index(
        cls, components: tuple[QualityComponent, ...]
    ) -> tuple[tuple[QualityComponent, ...], ...]:
        groups = defaultdict(list)
        for c in components:
            groups[c.index].append(c)
        return tuple(tuple(v) for _, v in groups.items())
