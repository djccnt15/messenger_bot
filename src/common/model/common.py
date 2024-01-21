from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Id(BaseModel, Generic[T]):
    id: T
