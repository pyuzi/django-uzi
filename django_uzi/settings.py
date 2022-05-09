
from collections import abc
from django.conf import settings
from django.utils.module_loading import import_string


from uzi import Container, Scope

MAIN_SCOPE: type[Scope]
REQUEST_SCOPE: type[Scope]
MAIN_CONTAINERS: abc.Sequence[Container]
REQUEST_CONTAINERS: abc.Sequence[Container]



MAIN_SCOPE = settings.UZI_MAIN_SCOPE = getattr(settings, 'UZI_MAIN_SCOPE', 'uzi.scopes.Scope')
REQUEST_SCOPE = settings.UZI_REQUEST_SCOPE = getattr(settings, 'UZI_REQUEST_SCOPE', 'uzi.scopes.Scope')
MAIN_CONTAINERS = settings.UZI_MAIN_CONTAINERS = getattr(settings, 'UZI_MAIN_CONTAINERS', ())
REQUEST_CONTAINERS = settings.UZI_REQUEST_CONTAINERS = getattr(settings, 'UZI_REQUEST_CONTAINERS', ())


if isinstance(MAIN_SCOPE, str):
    MAIN_SCOPE = import_string(MAIN_SCOPE)


if isinstance(REQUEST_SCOPE, str):
    REQUEST_SCOPE = import_string(REQUEST_SCOPE)


assert issubclass(MAIN_SCOPE, Scope)
assert issubclass(REQUEST_SCOPE, Scope)

MAIN_CONTAINERS = list(MAIN_CONTAINERS)
for i,c in enumerate(MAIN_CONTAINERS):  
    if isinstance(c, str):
        MAIN_CONTAINERS[i] = c = import_string(c)
    assert isinstance(c, Container)
MAIN_CONTAINERS = tuple(MAIN_CONTAINERS)


REQUEST_CONTAINERS = list(REQUEST_CONTAINERS)
for i,c in enumerate(REQUEST_CONTAINERS):  
    if isinstance(c, str):
        REQUEST_CONTAINERS[i] = c = import_string(c)
    assert isinstance(c, Container)

REQUEST_CONTAINERS = tuple(REQUEST_CONTAINERS)
