from abc import abstractmethod

import pytest
from ipromise import AbstractBaseClass, implements, overrides, overridable


class A(AbstractBaseClass):

    @abstractmethod
    def f(self):
        raise NotImplementedError


class B(A):

    @overridable
    @implements(A)
    def f(self):
        return 0

class C(B):

    @abstractmethod
    def f(self):
        raise NotImplementedError


class D(AbstractBaseClass):

    def f(self):
        return 1


class E(B):
    @overrides(B)
    def f(self):
        return 1


class F(AbstractBaseClass):
    @abstractmethod
    @overridable
    def f(self):
        raise NotImplementedError


class G(AbstractBaseClass):
    f = None


class H(AbstractBaseClass):
    pass


# Tests from ipromise.py.
# -----------------------------------------------------------------------------
def test_not_a_base_class():
    with pytest.raises(TypeError):
        class X(A):
            @overrides(B)
            def f(self):
                return 1

def test_somehow_abstract():
    # Somehow abstract in base class.
    class Y(C):
        @overrides(B)
        def f(self):
            return 1

def test_already_implemented():
    with pytest.raises(TypeError):
        # Already implemented in base class that does not inherit from B.
        class Z(B, D):
            @overrides(B)
            def f(self):
                return 1

# Tests from overrides.py.
# -----------------------------------------------------------------------------
def test_not_found():
    with pytest.raises(NotImplementedError):
        # Not found in interface class.
        class V(B):
            @overrides(B)
            def g(self):
                return 1

def test_is_abstract():
    # Is abstract in interface class.
    class W(B):
        @overrides(B)
        def f(self):
            return 1

def test_override_an_override():
    with pytest.raises(TypeError):
        # Overrides an override.
        class U(E):
            @overrides(E)
            def f(self):
                return 1

def test_overrides_and_implemented():

    with pytest.raises(TypeError):
        class S(B):
            @overrides(A)
            def f(self):
                return 1

def test_overridable_despite_base_class():

    with pytest.raises(TypeError):
        class T(B):
            @overridable
            def f(self):
                return 1


def test_cannot_instantiate_abstract_class():
    with pytest.raises(TypeError):
        F()  # TypeError … Can't instantiate abstract class …


def test_overrides():
    class F1(F):
        @overrides(F)
        def f(self):
            pass
    F1()


def test_implements():
    class F2(F):
        @implements(F)
        def f(self):
            pass
    F2()


def test_implements_overrides():
    class F3(F):
        @implements(F)
        @overrides(F)
        def f(self):
            pass
    F3()


def test_overrides_NotImplementedError_expected_type_function():
    with pytest.raises(NotImplementedError):
        class G1(G):
            @overrides(G)  # NotImplementedError … expected implemented type …
            def f(self):
                pass


def test_overrides_NotImplementedError_not_implemented():
    with pytest.raises(NotImplementedError):
        class H1(H):
            @overrides(H)  # NotImplementedError … not implemented …
            def f(self):
                pass
