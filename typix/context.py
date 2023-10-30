from types import FunctionType

class Context:
    """
    A class containing argument data to use in a non-function context.
    Should not be instanciated directly.
    """
    def __init__(self, arg_name: str = None, func: FunctionType = None):
        """
        A class containing argument data to use in a non-function context.
        Should not be instanciated directly.
        
        ### Arguments
        * `arg_name`: `Optional[str]`\n
            The name of the argument
        * `func`: `Optional[function]`\n
            The function containing the argument
            
        ### Return
        * type `NoneType`: Returns `None` as it is a constructor
        """
        self.__arg_name = arg_name
        self.__func = func
        
    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"<{class_name}: {repr(self.__arg_name)}>"
    
    @property
    def arg_name(self) -> str:
        """
        ### Property
        `arg_name`: `str`\n
            The name of the argument
        """
        return self.__arg_name
    
    @property
    def func(self) -> FunctionType:
        """
        ### Property
        `func`: `function`\n
            The function containing the argument
        """
        return self.__func