import pytest
from src.mt.note import PitchClass


def test_PitchClass_init_from_pitchname(setting, data_pitchnames):
    for pitchname in data_pitchnames:
        assert isinstance(PitchClass(pitchname, setting=setting), PitchClass)


def test_PitchClass_init_from_pitchclass(setting, data_pitchclasses):
    for pitchclass in data_pitchclasses:
        assert isinstance(PitchClass(pitchclass, setting=setting), PitchClass)


def test_PitchClass_init_from_pitchname_bench(benchmark, setting, data_pitchnames):

    def target(setting, data_pitchnames):
        for pitchname in data_pitchnames:
            _ = PitchClass(pitchname, setting=setting)

    benchmark.pedantic(
        target,
        kwargs={"setting": setting, "data_pitchnames": data_pitchnames},
        rounds=100,
        iterations=10,
    )


# def test_PitchClass_init_from_invalid_pitchclass(setting, data_pitchclasses):
#     for pitchclass in ["A"]:
#         with pytest.raises(ValueError):
#             _ = PitchClass(pitchclass, setting=setting)
