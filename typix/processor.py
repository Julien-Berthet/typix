from typing import get_type_hints, Any
from types import FunctionType

from .main import Typix
from .utils import istypix

def processor(func: FunctionType) -> FunctionType:
    """
    A decorator function that allow dynamic type
    to process arguments on the targeted function.

    ### Arguments
    * `func`: `function`\n
        The function to decorate
    
    ### Return
    * type `function`: The decorated function
    """
    def inner(*args) -> Any:
        """
        A modified version of the decorated function given by
        the `func` parameter in the parent scope. Handles argument
        and return value processing.
        
        ### Arguments
        * `*args`: `tuple`\n
            The arguments of the decorated function
        
        ### Return
        * type `Any`: The new return value of the function
        """
        # Get function arguments and typehints
        type_hints = get_type_hints(func)
        arguments = func.__code__.co_varnames
        
        # Get return typehint
        return_type_hint = None
        if 'return' in type_hints:
            return_type_hint: Typix = type_hints.pop('return')
        
        # Loop through the arguments
        new_args = []
        for argument, value in zip(arguments, args):
            # If has annotation
            if not argument in type_hints:
                new_args.append(value)
                continue
            
            type_hint: Typix = type_hints[argument]
            
            # If annotation is dynamic
            if not istypix(type_hint):
                new_args.append(value)
                continue
            
            # Configure context
            type_hint._arg = argument
            type_hint._func = func
            type_hint._value = value
            
            new_value = type_hint.process(*type_hint._args)
            new_args.append(new_value)
        
        # Return value handling
        return_value = func(*new_args)
        
        new_return_value = None
        if return_type_hint is not None:
            # Configure context
            return_type_hint._arg = 'return'
            return_type_hint._func = func
            return_type_hint._value = return_value
            
            # Process value
            new_return_value = return_type_hint.process(*return_type_hint._args)
        
        return new_return_value
    
    return inner
