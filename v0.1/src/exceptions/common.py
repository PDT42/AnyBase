"""
:Author: PDT
:Since: 2020/07/01

These are exceptions common throughout the whole project.
"""


class IllegalStateException(Exception):
    pass


class KeyConstraintException(Exception):
    pass


class MissingArgumentException(Exception):
    pass


class MissingKeyException(Exception):
    pass


class InvalidArgumentError(Exception):
    pass


class InvalidTypeError(Exception):
    pass


class OutdatedDataException(Exception):
    pass
