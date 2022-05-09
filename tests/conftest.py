import asyncio
import operator
from unittest.mock import MagicMock, Mock, NonCallableMagicMock
import pytest
import typing as t
from uzi import is_injectable
from uzi.containers import Container
from uzi.injectors import Injector
from uzi.providers import Provider

from uzi._dependency import Dependency
from uzi.scopes import Scope






@pytest.fixture
def new_args():
    return ()

@pytest.fixture
def new_kwargs():
    return {}


@pytest.fixture
def new(cls, new_args, new_kwargs):
    return lambda *a, **kw: cls(*a, *new_args[len(a):], **{**new_kwargs, **kw})


@pytest.fixture
def immutable_attrs(cls):
    return ()


@pytest.fixture
def value_factory_spec():
    return object

@pytest.fixture
def value_factory(value_factory_spec):
    return MagicMock(value_factory_spec, wraps=value_factory_spec)



@pytest.fixture
def MockContainer():
    def make(spec=Container, **kw):
        mi: Container = NonCallableMagicMock(spec, **kw)
        mi._dro_entries_.return_value = (mi,)
        mi.__bool__.return_value = True
        mi.__hash__.return_value = id(mi)
        mi.__getitem__.return_value = None
        return mi
    return MagicMock(type[Container], wraps=make)




@pytest.fixture
def MockBinding():
    def make(abstract=None, graph=None, **kw):
        mk = MagicMock(Dependency)

        if not abstract is None:
            kw['abstract'] = abstract

        if not graph is None:
            kw['graph'] = graph
        
        kw.setdefault('is_async', False)

        for k,v in kw.items():
            setattr(mk, k, v)
        return mk

    return MagicMock(type[Dependency], wraps=make)




@pytest.fixture
def MockInjector(MockGraph):
    def make(spec=Injector, *, graph=None, parent=True, **kw):
        mi: Injector = NonCallableMagicMock(spec, **kw)
        mi.__bool__.return_value = True
        mi.graph = graph or MockGraph()
        def mock_dep(k):
            if getattr(k, 'is_async', False):
                # mi = Mock()
                # def wrap(*a, **kw):
                #     return asyncio.sleep(0, mi)
                mk = MagicMock(asyncio.sleep)
            else:
                mk = MagicMock(t.Callable)
            return mk

        for k,v in kw.items():
            setattr(mi, k, v)

        deps = {}
        mi.__getitem__ = mi.find_local = Mock(wraps=lambda k: deps.get(k) or deps.setdefault(k, mock_dep(k)))
        mi.__setitem__ = Mock(wraps=lambda k, v: deps.__setitem__(k, v))

        return mi
    return MagicMock(type[Injector], wraps=make)




@pytest.fixture
def MockProvider(MockBinding):
    def make(spec=Provider, **kw):
        mi: Provider = NonCallableMagicMock(spec, **kw)
        deps = {}
        def mock_dep(a, s):
            if not (a, s) in deps:
                deps[a,s] = MockBinding(a, s, provider=mi)
            return deps[a,s]

        mi.resolve = MagicMock(wraps=mock_dep)
        mi.container = None
        mi.set_container = MagicMock(wraps=lambda c: (mi.container and mi) or setattr(mi, 'container', c) or mi)
        for k,v in kw.items():
            setattr(mi, k, v)

        return mi
    return MagicMock(type[Provider], wraps=make)



@pytest.fixture
def MockGraph(MockContainer, MockBinding):
    def make(spec=Scope, *, parent=True, **kw):
        mi = NonCallableMagicMock(spec, **kw)
        mi.container = cm = MockContainer()
        mi.maps = dict.fromkeys((cm, MockContainer())).keys()
        mi.__contains__ = MagicMock(operator.__contains__, wraps=lambda k: deps.get(k) or is_injectable(k)) 
        
        deps = {}
        mi.__getitem__ = mi.find_local = Mock(wraps=lambda k: deps[k] if k in deps else deps.setdefault(k, MockBinding(abstract=k, graph=mi)))
        mi.__setitem__ = Mock(wraps=lambda k, v: deps.__setitem__(k, v))

        if parent:
            mi.parent = make(parent=parent-1) if parent is True else parent
            mi.find_remote = mi.parent.__getitem__

        for k,v in kw.items():
            setattr(mi, k, v)

        return mi
    return MagicMock(type[Container], wraps=make)


@pytest.fixture
def mock_container(MockContainer):
    return MockContainer()


@pytest.fixture
def mock_graph(MockGraph):
    return MockGraph()


@pytest.fixture
def mock_provider(MockProvider):
    return MockProvider()



@pytest.fixture
def mock_injector(MockInjector, mock_graph):
    return MockInjector(graph=mock_graph)




