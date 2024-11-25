import typing as t


class classproperty(property):
    def __get__(self, _: t.Any, objtype: t.Any = None):
        return super(classproperty, self).__get__(objtype)
