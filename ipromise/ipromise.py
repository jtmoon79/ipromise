__all__ = ['AbstractBaseClass']


class AbstractBaseClass:

    def __init_subclass__(cls):
        super().__init_subclass__()

        # Assign the set of abstract method names to __abstractmethods__.
        # Python will not allow the class to be instantiated if this is not
        # empty.
        abstracts = {name
                     for name, value in vars(cls).items()
                     if getattr(value, "__isabstractmethod__", False)}
        # Add the abstract methods from the base classes.
        for base in cls.__bases__:
            for name in getattr(base, "__abstractmethods__", set()):
                value = getattr(cls, name, None)
                if getattr(value, "__isabstractmethod__", False):
                    abstracts.add(name)
        cls.__abstractmethods__ = frozenset(abstracts)

        # Check that for each method M implementing a method in class C:
        # * C is a base class of cls, and
        # * for all base classes B that define M,
        #   * M is abstract in B.
        for name, value in vars(cls).items():
            if not hasattr(value, "__implemented_from__"):
                continue
            interface_class = getattr(value, "__implemented_from__")
            if not issubclass(cls, interface_class):
                raise TypeError(
                    f"the interface class {interface_class.__name__} "
                    f"is not a base class of {cls.__name__}")
            for base in cls.__bases__:
                if not hasattr(base, name):
                    continue
                bases_value = getattr(base, name)
                if not getattr(bases_value, "__isabstractmethod__", False):
                    raise TypeError(f"the method {name} is already "
                                    f"implemented in base class "
                                    f"{base.__name__}")

        # For each method M overriding a method in class C:
        # * We already know that the method is defined in C.
        # * Check that C is a base class of cls, and
        # * for all base classes B that define M, either
        #   * M is abstract in B, or
        #   * B inherits from C.
        for name, value in vars(cls).items():
            if not hasattr(value, "__overrides_from__"):
                continue
            interface_class = getattr(value, "__overrides_from__")
            if not issubclass(cls, interface_class):
                raise TypeError(f"Interface class {interface_class.__name__} "
                                f"is not a base class of {cls.__name__}")

            abstract_bases = {}
            for base in cls.__bases__:
                if not hasattr(base, name):
                    continue
                bases_value = getattr(base, name)
                if not getattr(bases_value, "__isabstractmethod__", False):
                    if not issubclass(base, interface_class):
                        raise TypeError(
                            f"the method {name} is supposed to override a "
                            f"method defined in {interface_class.__name__}, "
                            f"but the base class {base.__name__} already "
                            f"implements it without inheriting from "
                            f"{interface_class.__name__}")
                # M can be abstract in B even if B inherits from C since
                # you are allowed to override abstract methods since a method
                # can be abstract and have a reasonable definition.  For
                # example, AbstractContextManager.__exit__.
