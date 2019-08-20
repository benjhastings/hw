sentinel = object()  # Unique instance that cannot be passed as an argument


class ObjectDict(dict):
    """
    Makes a dictionary behave like an object, with attribute-style access.
    """

    def __init__(self, arg=sentinel):
        """
        This method is only called after __new__ returns an ObjectDict
        instance. The __init__ method actually initialises the values
        in the underlying dict.
        """
        if arg is sentinel:  # Called without args
            arg = {}
        for (k, v) in arg.items():
            self[k] = od_type(v)

    def __getattr__(self, name: str):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        value = od_type(value)
        super().__setitem__(name, value)

    def __dir__(self):
        return sorted(self.keys)


def od_type(arg=sentinel):
    """
    This recursive dict subclass converts a dict into an ObjectDict,
    which can use attribute access to retrieve and set keys.
    Floats, ints, strings and existing ObjectDicts are simply
    returned. Lists are transformed into lists of ObjectDicts.
    The __init__ method will only be called for ObjectDicts,
    since only then is the argument class is the same as the returned value.
    When a dict is passed in, standard dict creation is called.
    """
    if arg is sentinel:
        return ObjectDict()
    elif isinstance(arg, (int, float, str, ObjectDict)):
        return arg
    elif isinstance(arg, list):
        return list(od_type(x) for x in arg)
    elif isinstance(arg, dict):
        return ObjectDict(arg)
    else:
        raise ValueError(f"{type(arg)} objects cannot be ObjectDicts")
