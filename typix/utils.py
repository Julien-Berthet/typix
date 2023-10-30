from inspect import isclass
from types import GenericAlias
from typing import Any, Iterable, Mapping, _SpecialForm, Union
import collections.abc as collection
from abc import ABCMeta

from .main import Typix
from .error import CheckResult
from .context import Context

# Type Alias for the `typing._GenericAlias` protected class
# Used in `typecheck` to target `GenericAlias` with typing class support
_TypingGenericAlias = type(Iterable[int])
_TypingType = type(Iterable)

def istypix(obj: Any) -> bool:
    """
    Utility function to check if a type is derived
    from `Typix` or not. Supports type instances.
    
    ### Arguments
    * `obj`: `Any`\n
        The object to check
    
    ### Return
    * type `bool`: Whether or not the object is derived from `Typix`
    
    .. doctest
        >>> istypix(Typix)
        True
        >>> istypix(Typix())
        True
        >>> istypix(int)
        False
        >>> istypix(5)
        False
    """
    if isclass(obj):
        return issubclass(obj, Typix)
    else:
        return issubclass(obj.__class__, Typix)
    
def match_generic_alias(value: Any, alias: GenericAlias) -> bool:
    """
    Utility function that allow support for
    [GenericAlias](https://docs.python.org/3/library/types.html?highlight=genericalias#types.GenericAlias)
    type checking.
    
    ### Arguments
    * `value`: `Any`\n
        The value to typecheck
    * `alias`: `GenericAlias`\n
        The `GenericAlias` to check with
    
    ### Return
    * type `bool`: Whether or not the typecheck is successful
    
    ### Raises
    * `NotImplementedError`\n
        When trying to use an instance of `typing._SpecialForm` as `GenericAlias`
    
    .. doctest
        >>> match_generic_alias([], list[int])
        True
        >>> match_generic_alias([0, 1, 2], list[int])
        True
        >>> match_generic_alias([0, 1, 2, 3.0], list[int])
        False
        >>> match_generic_alias([0, 1, 2, 3.0], list[int, float])
        True
        >>> match_generic_alias((1, 2, 3), list[int])
        False
        >>> match_generic_alias((1, 2, 3), Iterable[int])
        True
        >>> match_generic_alias({}, dict[str])
        False
        >>> match_generic_alias({}, dict[str, int])
        True
        >>> match_generic_alias({'number': 5}, dict[str, int])
        True
        >>> match_generic_alias(0, _SpecialForm(lambda _: _))
        Traceback (most recent call last):
            ...
        NotImplementedError: typing._SpecialForm is currently not supported
    """
    # NOTE: Probably never will be implemented due to 
    # the new __class_getitem__ special method. Also, leads
    # to confusing code, when trying to implement the support.
    if isinstance(alias, _SpecialForm):
        raise NotImplementedError("typing._SpecialForm is currently not supported")
    
    alias_origin = alias.__origin__
    alias_args = alias.__args__
    
    # Prevent errors due to instanciating `typing` special classes (ex. Iterable)
    alias_origin_instance = alias_origin
    if type(alias_origin) is not ABCMeta:
        alias_origin_instance = alias_origin()
    
    # Needs to match the orgin
    if not isinstance(value, alias_origin):
        return False

    # Needs to match any of the given type arguments
    if alias_origin is collection.Mapping or isinstance(alias_origin_instance, Mapping):
        if len(alias_args) < 2:
            return False
        
        key_type = alias_args[0]
        value_types = alias_args[1:]
        
        keys_typecheck = all(isinstance(key, key_type) for key in value.keys())
        value_typecheck = all(isinstance(val, value_types) for val in value.values())
        
        return keys_typecheck and value_typecheck
    
    if alias_origin is collection.Iterable or isinstance(alias_origin_instance, Iterable):
        return all(isinstance(arg, alias_args) for arg in value)
    
    # Always defaults to False
    return False

def typecheck(value: Any, type_: Any, context: Context = None) -> CheckResult:
    """
    A utility function that check the type of a value. Supports
    dynamic types and `GenericAlias`.
    
    ### Arguments
    * `value`: `Any`\n
        The value to check the value from
    * `type_`: `Any`\n
        The type to check the value with
    * `context`: `Optional[Context]`\n
        Additional data about the argument and the function.
        Useful in that case because invoking `typecheck` does
        not provide argument or function data. Must be provided
        for dynamic type that use function context
    
    ### Return
    * type `CheckResult`: An object containing the state of the
    typecheck and and any exception thrown during the check
    
    .. doctest
        >>> typecheck(0, int)
        <CheckResult: True>
        >>> typecheck(0.0, int)
        <CheckResult: False>
        >>> typecheck([], list[int])
        <CheckResult: True>
        >>> typecheck([0, 1, 2], list[int])
        <CheckResult: True>
        >>> typecheck([0.0, 1.0, 2.0], list[int])
        <CheckResult: False>
        >>> typecheck([0, 1, 2.0], list[int])
        <CheckResult: False>
        >>> typecheck((0, 1, 2), list[int])
        <CheckResult: False>
    """
    # Tuple recursive support
    if isinstance(type_, tuple):
        return CheckResult(
            any(typecheck(value, t).state for t in type_),
            value = value,
            context = context
        )
    
    # GenericAlias support
    elif isinstance(type_, (GenericAlias, _TypingGenericAlias)):
        return CheckResult(
            match_generic_alias(value, type_),
            value = value,
            context = context
        )
    
    # Dynamic Type support
    elif istypix(type_):
        type_._value = value
        type_._function_context = False
        new_value = type_.process(*type_._args)
        
        # Add context data if present
        if context:
            type_._arg = context.arg_name
            type_._func = context.func
            
        return CheckResult(
            type_._fail is None,
            type_._fail,
            value = new_value,
            context = context
        )
    
    # Standard type check
    else:
        return CheckResult(
            isinstance(value, type_),
            value = value,
            context = context
        )

def display_type(type_: Any) -> str:
    """
    Generates a string display for a given type. Supports GenericAlias,
    class instances, and special types from the `typing` module.
    
    ### Arguments
    * `type_`: `Any`\n
        The type to display
    
    ### Return
    * type `str`: A string reprensenting the type as text
    """
    # `GenericAlias` support
    if type(type_) is GenericAlias:
        return str(type_)
    
    # `typing._GenericAlias` support
    elif type(type_) is _TypingGenericAlias:
        return f"{type_.__origin__.__name__}[{', '.join(a.__name__ for a in type_.__args__)}]"
    
    # type input support
    elif isclass(type_):
        return type_.__name__
    
    # typing sepecial type input support
    elif type(type_) is _TypingType:
        return type_.__origin__.__name__
    
    # instance input support
    else:
        return type(type_).__name__