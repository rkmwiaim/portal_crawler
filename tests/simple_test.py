from typing import Iterator
from typing import TypeVar

from functional.pipeline import Sequence
from functional import seq

Item = TypeVar('item')
class Stream(Sequence, Iterator[Item]):
    pass




def get_seq() -> Stream[dict]:
    try:
        d = {'a': 1, 'b': 2}
        a = [d, d, d]
        # a = ['a', 'b', 'c']
        # return a
        raise ValueError()
        return seq(a)
    except:
        pass


r = get_seq()
print(r)
print(type(r))


