from types import MethodType
import typing as t 
from collections.abc import Callable
from functools import partial, update_wrapper

from uzi import providers







def inject(handler: Callable, /, *args, **kwds):
    if isinstance(handler, partial):
        func = handler.func
    else:
        func = handler      

    if hasattr(func, '__uzi_provider__'):
        raise ValueError(f'{handler!s} already wired')

    elif isinstance(func, MethodType):
        func, *args = func.__func__, func.__self__, *args

    provider = providers.Partial(func, *args, **kwds)

    def wrapper(req, *a, **kw):
        nonlocal provider
        return req.ctx._uzi_injector(provider, req, *a, **kw)
    
    update_wrapper(wrapper, func)
    wrapper.__uzi_provider__ = provider

    return wrapper
