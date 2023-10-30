from typing import Any

from .context import Context

class TypixError(BaseException):
    """
    Common base class for all exceptions related to the `Typix` module
    """
    pass
    
class CheckResult:
    """
    This object is returned by the `typecheck` function. It contains
    a `state`: whether of not the check is successful and an `exception`
    if the state is `False`. If this object is used in an `if` statement,
    it will take the value of it's state.
    """
    def __init__(
        self,
        state: bool,
        exception: BaseException = None,
        value: Any = None,
        context: Context = None
    ):
        """
        This object is returned by the `typecheck` function. It contains
        a `state`: whether of not the check is successful and an `exception`
        if the state is `False`. If this object is used in an `if` statement,
        it will take the value of it's state.
        
        ### Arguments
        * `state`: `bool`\n
            The state of the check result
        * `exception`: `Optional[BaseException]`\n
            The exception of the check result.
            Defaults to `None`
        * `value`: `Optional[Any]`\n
            The processed value given by the typecheck.
            Defaults to `None`
        * `context`: `Optional[Context]`\n
            Additional data about the argument and the function.
            Useful in that case because invoking `typecheck` does
            not provide argument or function data. Must be provided
            for dynamic type that use function context
            Defaults to `None`
        
        ### Return
        * type `NoneType`: Returns `None` as it is the constructor
        """
        self.__state = state
        self.__exception = exception
        self.__value = value
        self.__context = context
        
    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"<{class_name}: {self.__state}>"
    
    def __bool__(self) -> bool:
        return self.__state
    
    @property
    def state(self) -> bool:
        """
        ### Property
        `state`: `bool`\n
            The state of the check result
        """
        return self.__state
        
    @property
    def exception(self) -> BaseException:
        """
        ### Property
        `exception`: `BaseException`\n
            The exception of the check result
        """
        return self.__exception

    @property
    def value(self) -> Any:
        """
        ### Property
        `value`: `Any`\n
            The processed value given by the typecheck.
        """
        return self.__value
    
    @property
    def context(self) -> Context:
        """
        ### Property
        `context`: `Context`\n
            Additional data about the argument and the function.
            Useful in that case because invoking `typecheck` does
            not provide argument or function data. Must be provided
            for dynamic type that use function context
            Defaults to `None`
        """
        return self.__context