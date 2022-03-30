"""
Initializing the Python package
"""

X = {
    '1', 2,
    "3",
    f'4'
}


def func(arg: int, kwarg: dict = None):
    """ Func """
    return arg


__version__ = '1.0'

__all__ = (
    'X',
)
