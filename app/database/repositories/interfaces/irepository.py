from typing import Generic, List, Optional, TypeVar

from app.common.types import T


class IRepository(Generic[T]):
    def add(self, entity: T) -> None:
        raise NotImplementedError

    def get(self, id: int) -> Optional[T]:
        raise NotImplementedError

    def get_all(self) -> List[T]:
        raise NotImplementedError

    def update(self, entity: T) -> None:
        raise NotImplementedError

    def delete(self, id: int) -> None:
        raise NotImplementedError
