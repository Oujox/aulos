from typing import ClassVar

import pytest

from src.aulos._core.utils.metaclass import SlotsGenerateMeta


class BaseClass(metaclass=SlotsGenerateMeta):
    attr1: int
    attr2: str
    attr3: ClassVar[float]


class DerivedClass(BaseClass):
    attr4: int
    attr5: ClassVar[float]


class DerivedClass3(BaseClass, slots_generate=False):
    attr6: int
    attr7: ClassVar[float]


class DerivedClass2(BaseClass):
    attr8: str
    attr9: ClassVar[float]
    __slots__ = ("attr8",)


def test_slots_generation():
    assert hasattr(BaseClass, "__slots__")
    assert hasattr(DerivedClass, "__slots__")
    assert hasattr(DerivedClass2, "__slots__")
    assert hasattr(DerivedClass3, "__slots__")
    assert BaseClass.__slots__ == ("attr1", "attr2")
    assert DerivedClass.__slots__ == ("attr4",)
    assert DerivedClass2.__slots__ == ("attr8",)
    assert DerivedClass3.__slots__ == ("attr1", "attr2")


def test_instance_creation():
    base_instance = BaseClass()
    base_instance.attr1 = 5
    base_instance.attr2 = "test"
    with pytest.raises(AttributeError):
        base_instance.new_attr = "should fail"

    derived_instance = DerivedClass()
    derived_instance.attr1 = 10
    derived_instance.attr2 = "test"
    derived_instance.attr4 = 15
    with pytest.raises(AttributeError):
        derived_instance.new_attr = "should fail"

    derived_instance3 = DerivedClass2()
    derived_instance3.attr1 = 10
    derived_instance3.attr2 = "test"
    derived_instance3.attr8 = 20
    with pytest.raises(AttributeError):
        derived_instance.new_attr = "should fail"

    derived_instance2 = DerivedClass3()
    derived_instance2.attr1 = 10
    derived_instance2.attr2 = "test"
    derived_instance2.attr6 = 20
    derived_instance2.new_attr = "new attr"
