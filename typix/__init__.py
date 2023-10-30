"""
### Typix
An advanced module to hide type handling code behind type annotations
"""
from sys import version_info

from .processor import processor
from .builtin_dynamic_types import Strict, Convert
from .utils import istypix, typecheck, match_generic_alias, display_type
from .context import Context
from .error import CheckResult, TypixError
from .main import Typix

__author__ = 'Julien BERTHET'

__all__ = [
    'processor',
    'istypix',
    'typecheck',
    'match_generic_alias',
    'display_type',
    'Context',
    'CheckResult',
    'TypixError',
    'Typix',
    'Strict',
    'Convert'
]

# Deprecated Version Warning
if version_info <= (3, 10):
    raise ImportWarning('This module require Python 3.10 or higher')