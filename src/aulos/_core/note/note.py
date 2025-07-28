from .bases import BaseNote, BaseNoteCollection


class NoteCollection[NOTE: BaseNote](BaseNoteCollection[NOTE]):
    """
    Represents a collection of notes.
    This class extends the BaseNoteCollection and provides additional methods
    and properties to handle a collection of notes, allowing for operations
    such as adding, removing, and querying notes.
    """
