from pathlib import Path
from typing import (
    Generic,
    Type,
    Dict,
    List,
    Tuple,
    Optional,
    Any,
    Union,
    ClassVar,
    Callable as _Callable,
    Iterable,
    Iterator,
    TypeVar,
    Awaitable,
    overload,
)

from .providers import Provider, Self, ProviderParent


C_Base = TypeVar("C_Base", bound="Container")
C = TypeVar("C", bound="DeclarativeContainer")
C_Overriding = TypeVar("C_Overriding", bound="DeclarativeContainer")
T = TypeVar("T")
TT = TypeVar("TT")


class WiringConfiguration:
    modules: List[Any]
    packages: List[Any]
    from_package: Optional[str]
    auto_wire: bool
    def __init__(self, modules: Optional[Iterable[Any]] = None, packages: Optional[Iterable[Any]] = None, from_package: Optional[str] = None, auto_wire: bool = True) -> None: ...


class Container:
    provider_type: Type[Provider] = Provider
    providers: Dict[str, Provider]
    dependencies: Dict[str, Provider]
    overridden: Tuple[Provider]
    wiring_config: WiringConfiguration
    auto_load_config: bool = True
    __self__: Self
    def __init__(self) -> None: ...
    def __deepcopy__(self, memo: Optional[Dict[str, Any]]) -> Provider: ...
    def __setattr__(self, name: str, value: Union[Provider, Any]) -> None: ...
    def __getattr__(self, name: str) -> Provider: ...
    def __delattr__(self, name: str) -> None: ...
    def set_providers(self, **providers: Provider): ...
    def set_provider(self, name: str, provider: Provider) -> None: ...
    def override(self, overriding: Union[Container, Type[Container]]) -> None: ...
    def override_providers(self, **overriding_providers: Union[Provider, Any]) -> ProvidersOverridingContext[C_Base]: ...
    def reset_last_overriding(self) -> None: ...
    def reset_override(self) -> None: ...
    def is_auto_wiring_enabled(self) -> bool: ...
    def wire(self, modules: Optional[Iterable[Any]] = None, packages: Optional[Iterable[Any]] = None, from_package: Optional[str] = None) -> None: ...
    def unwire(self) -> None: ...
    def init_resources(self) -> Optional[Awaitable]: ...
    def shutdown_resources(self) -> Optional[Awaitable]: ...
    def load_config(self) -> None: ...
    def apply_container_providers_overridings(self) -> None: ...
    def reset_singletons(self) -> SingletonResetContext[C_Base]: ...
    def check_dependencies(self) -> None: ...
    def from_schema(self, schema: Dict[Any, Any]) -> None: ...
    def from_yaml_schema(self, filepath: Union[Path, str], loader: Optional[Any]=None) -> None: ...
    def from_json_schema(self, filepath: Union[Path, str]) -> None: ...
    @overload
    def resolve_provider_name(self, provider: Provider) -> str: ...
    @classmethod
    @overload
    def resolve_provider_name(cls, provider: Provider) -> str: ...
    @property
    def parent(self) -> Optional[ProviderParent]: ...
    @property
    def parent_name(self) -> Optional[str]: ...
    def assign_parent(self, parent: ProviderParent) -> None: ...
    @overload
    def traverse(self, types: Optional[Iterable[Type[TT]]] = None) -> Iterator[TT]: ...
    @classmethod
    @overload
    def traverse(cls, types: Optional[Iterable[Type[TT]]] = None) -> Iterator[TT]: ...


class DynamicContainer(Container): ...


class DeclarativeContainer(Container):
    cls_providers: ClassVar[Dict[str, Provider]]
    inherited_providers: ClassVar[Dict[str, Provider]]
    def __init__(self, **overriding_providers: Union[Provider, Any]) -> None: ...
    @classmethod
    def override(cls, overriding: Union[Container, Type[Container]]) -> None: ...
    @classmethod
    def override_providers(cls, **overriding_providers: Union[Provider, Any]) -> ProvidersOverridingContext[C_Base]: ...
    @classmethod
    def reset_last_overriding(cls) -> None: ...
    @classmethod
    def reset_override(cls) -> None: ...


class ProvidersOverridingContext(Generic[T]):
    def __init__(self, container: T, overridden_providers: Iterable[Union[Provider, Any]]) -> None: ...
    def __enter__(self) -> T: ...
    def __exit__(self, *_: Any) -> None: ...


class SingletonResetContext(Generic[T]):
    def __init__(self, container: T): ...
    def __enter__(self) -> T: ...
    def __exit__(self, *_: Any) -> None: ...


def override(container: Type[C]) -> _Callable[[Type[C_Overriding]], Type[C_Overriding]]: ...


def copy(container: Type[C]) -> _Callable[[Type[C_Overriding]], Type[C_Overriding]]: ...


def is_container(instance: Any) -> bool: ...
