
from threading import RLock
from uzi import Scope, Container, Injector

from .settings import MAIN_CONTAINERS, REQUEST_CONTAINERS, MAIN_SCOPE,REQUEST_SCOPE





_lock = RLock()


def _make_container(c: Container=None, *containers: Container, name=None):
    if containers:
        c = Container(name, c, *containers)
    elif not c:
        c = Container(name)
    return c 






__main_scope: Scope = None
def main_scope():
    global __main_scope
    if __main_scope is None:
        with _lock:
            if __main_scope is None:
                __main_scope = MAIN_SCOPE(_make_container(*MAIN_CONTAINERS, name='main'))
    return __main_scope



__request_scope: Scope = None
def request_scope():
    global __request_scope
    if __request_scope is None:
        with _lock:
            if __request_scope is None:
                main = main_scope()
                container = _make_container(*REQUEST_CONTAINERS, name='request')
                __request_scope = REQUEST_SCOPE(container, parent=main)
    return __request_scope
