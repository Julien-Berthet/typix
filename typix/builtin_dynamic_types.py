from typing import Any

from .main import Typix
from .utils import typecheck, istypix, display_type

class Strict(Typix):
    """
    Returns a fatal error if its child returns any error
    
    ### Arguments
    * `type_`: `Any`\n
        The children type
    
    ### Return
    * type `Any`: If the children do not returns any error 
    * type `TypixError`: If the children returns any error
    """
    def process(self, type_: Any) -> Any:
        result = typecheck(self.value, type_)
        if result:
            return result.value
        else:
            if istypix(type_):
                return self.error(f"Strict constraint failed: {result.exception}", fatal=True)
            else:
                return self.error(f"Strict constraint failed", fatal=True)
            
class Convert(Typix):
    """
    Convert the value to the given type. If not possible returns a non-fatal error.
    
    ### Arguments
    * `type_`: `Any`\n
        The type to convert to
    
    ### Return
    * type `Any`: The converted value, if the type conversion does not raise any error
    * type `TypixError`: If the type conversion does raise an error
    """
    def process(self, type_: Any) -> Any:
        new_value = self.value
        try:
            new_value = type_(new_value)
        except ValueError:
            return self.error(f"Cannot convert '{display_type(self.value)}' to '{display_type(type_)}'")
        else:
            return new_value