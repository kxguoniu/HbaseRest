#-*- coding: utf-8 -*-
import base64
from collections import namedtuple

__all__ = ["CompareOp", "Comparable", "Operator"]

def _b64encode(value, altchars=None):
    if isinstance(value, str):
        return base64.b64encode(value.encode(), altchars=altchars).decode()
    elif isinstance(value, bytes):
        return base64.b64encode(value, altchars=altchars).decode()
    else:
        raise TypeError("argument 1 must be string or buffer, not %s" % type(value))

def _b64decode(value, altchars=None, validate=False):
    if isinstance(value, str):
        return base64.b64decode(value.encode(), altchars=altchars, validate=validate).decode()
    elif isinstance(value, bytes):
        return base64.b64decode(value, altchars=altchars, validate=validate).decode()

_CompareOp = namedtuple("CompareOp", "lt, le, eq, ne, ge, gt")
CompareOp = _CompareOp("LESS", "LESS_OR_EQUAL", "EQUAL", "NOT_EQUAL", "GREATER_OR_EQUAL", "GREATER")

_Comparable = namedtuple("Comparable", "default, pre, sub, re")
Comparable = _Comparable("BinaryComparator", "BinaryPrefixComparator", "SubStringComparator", "RegexStringComparator")

_Operator = namedtuple("Operator", "one, all")
Operator = _Operator("MUST_PASS_ONE", "MUST_PASS_ALL")