from .ipromise import AbstractBaseClass

__all__ = ['overridable', 'overrides']


def overridable(method):
    if hasattr(method, '__overrides_from__'):
        raise TypeError(
            f"{method.__name__} cannot be decorated both overridable and "
            "overrides")
    method.__overridable__ = None
    return method


def overrides(interface_class):
    if not isinstance(interface_class, type):
        raise TypeError

    def decorated_method(method):
        if hasattr(method, '__overridable__'):
            raise TypeError(
                f"{method.__name__} cannot be decorated both overridable and "
                "overrides")
        if method.__name__ not in vars(interface_class):
            raise TypeError(
                f"{method.__name__} not found in interface class "
                f"{interface_class.__name__}")
        def func():
            pass
        bases_value = getattr(interface_class, method.__name__)
        if type(bases_value) is not type(func):
            raise NotImplementedError(
                f"method {method.__name__} is an @overrides "
                f"but that is implemented as type {type(bases_value)} "
                f"in base class {interface_class}, expected implemented "
                f"type {type(func)}")
        if hasattr(bases_value, '__overrides_from__'):
            raise TypeError(
                f"The method {method.__name__} @overrides a method in "
                f"the interface class {interface_class.__name__}, "
                f"but that method @overrides from a higher-level interface "
                f"class {getattr(bases_value, '__overrides_from__')}")
#       if not hasattr(bases_value, '__overridable__'):
#           raise TypeError(
#               f"{method.__name__} is not decorated overridable in "
#               f"the interface class {interface_class.__name__}")
        # You are allowed to override abstract methods since a method can
        # be abstract and have a reasonable definition.  For example,
        # AbstractContextManager.__exit__.
#       if getattr(bases_value, "__isabstractmethod__", False):
#           raise TypeError(
#               f"{method.__name__} is abstract in interface class "
#               f"{interface_class.__name__}")
        method.__overrides_from__ = interface_class
        return method

    return decorated_method
