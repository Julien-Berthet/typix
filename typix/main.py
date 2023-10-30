from typing import Optional, Any
from types import FunctionType

from .error import TypixError
from .context import Context

class Typix:
    """
    All dynamic types should inherit from this class.
    """
    def __init__(self, *args) -> None:
        """
        A dynamic type instance.\n
        You may overwrite this docstring by setting the `__doc__` property
        or by overloading the constructor.
        
        ### Arguments
        * `*args`: `tuple`\n
            The arguments of the dynamic type
        
        ### Return
        * type `NoneType`: Returns `None` as it is a constructor
        """
        # Arguments
        self._args = args
        
        # Context
        self._arg = None
        self._value = None
        self._func = None
        self._function_context = True
        
        # Store
        self._fail = None
    
    def process(self, *args):
        """
        The method called when an argument needs to be processed after being annotated with this
        dynamic type. This function is meant to be overloaded to implement a specific logic
        to this dynamic type. The default behavior of the method is to return the argument value
        without modifying or raising anything.
        
        ### Arguments
        * `*args`: `tuple`\n
            The parameters passed into the type
        
        ### Return
        * type `Any`: The new value of the argument
        
        ### Raises
        * `Any`: Whatever Exception the method raised
        """
        return self._value
    
    def error(self, exception: BaseException, fatal: Optional[bool] = False) -> Any:
        """
        Indicates an Exception in the typing procedure. The Exception won't raise
        unless it is fatal. A non-fatal error can also be raised by a parent type
        like the `Strict` dynamic type.
        
        ### Arguments
        * `exception`: `BaseException`\n
            The exception to indicate. Must derive from BaseException but can be of type `str`:
            In that case it will be converted to default `TypixException`
        * `fatal`: `Optional[bool]`\n
            Whether or not the error is fatal.
            Defaults to `False`.
        
        ### Return
        * type `Any`: The default value, unless an Exception is raised
        
        ### Raises
        * `Any`\n
            The thrown Exception if the error is fatal
        """
        if isinstance(exception, str):
            exception = TypixError(exception)
        
        self._fail = exception
        if fatal:
            raise self._fail
        return self._value
        
    @property
    def args(self) -> tuple:
        """
        ### Property
        `args`: `tuple`\n
            The arguments passed into the dynamic type
        """
        return self._args
    
    @property
    def argument(self) -> str:
        """
        ### Property
        `argument`: `str`\n
            The current argument name in a function context
        """
        return self._arg
    
    @property
    def value(self) -> Any:
        """
        ### Property
        `value`: `Any`\n
            The value returned by the dynamic type
        """
        return self._value
    
    @property
    def func(self) -> FunctionType | None:
        """
        ### Property
        `func`: `function`\n
            The current function in a function context
        """
        return self._func
    
    @property
    def fail(self) -> BaseException | None:
        """
        ### Property
        `fail`: `BaseException`\n
            The error returned by the dynamic type
        """
        return self._fail
    
    @property
    def function_context(self) -> bool | None:
        """
        ### Property
        `function_context`: `bool`\n
            Whether or not the dynamic type is processed in a function context.
            For example, if it is processed as a type annotation, it will recieve
            a function context. Otherwise, in the `typecheck` function for example
            it won't unless a context object is passed from a child.
        """
        return self._function_context
    
    @property
    def context(self) -> Context:
        """
        ### Property
        `context`: `Context`\n
            A 'bundle' object containing data about the current target argument. It can
            be passed from child to parent to relay errors for example.
        """
        return Context(self._arg, self._func)