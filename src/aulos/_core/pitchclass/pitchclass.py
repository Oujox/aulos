from .bases import BasePitchClass, BasePitchClassCollection


class PitchClassCollection[PITCHCLASS: BasePitchClass](BasePitchClassCollection[PITCHCLASS]):
    """
    Represents a collection of pitch classes.
    This class extends the BasePitchClassCollection and provides additional methods
    and properties to handle a collection of pitch classes, allowing for operations
    such as adding, removing, and querying pitch classes.
    """
