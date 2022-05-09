
import pytest


from django_uzi import inject



xfail = pytest.mark.xfail
parametrize = pytest.mark.parametrize


def basic_test():
    @inject
    def func(req):
        pass
    