from typing import Iterator
from typing import TypeVar

from functional.pipeline import Sequence

Item = TypeVar('Item')


class Stream(Sequence, Iterator[Item]):
    pass
