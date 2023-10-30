# Typix
## An advanced module to hide type handling code behind type annotations

> Version: 1.0.0

By **Julien BERTHET**
* [GitHub](https://github.com/Julien-Berthet)

### This module adds:
* Dynamic Types: types that can check or modify the annotated values at runtime
* `typing` support
* Utility functions to improve type handling

### Installing
* **PyPI**  
> `pip install typix`

### Quickstart
This section will describe some of the useful features of the module to easely get started with it.

> **Using Dynamic Types on a function**
```py
from typix import processor, Strict

# The `@processor` decorator will allow 
# dynamic type support on this function
@processor
def test(my_arg: Strict(int)):
    # Here, we annotate `my_arg` with the `Strict` dynamic type
    print("test:", my_arg)
```

The `Strict` dynamic type is a built-in dynamic type that allow strong
typing on function arguments. To use it, it must wrap a child type.

```py
>>> test(1)
test: 1
>>> test('a')
Traceback (most recent call last):
    ...
typix.error.TypixError: Strict constraint failed
```

We can also use other dynamic types like `Convert`. This type will automatically convert the value to the given type. Here is an example

```py
from typix import processor, Strict, Convert

@processor
def test(my_arg: Strict(int), my_other_arg: Convert(float)):
    print("test:", my_arg, my_other_arg)
```

```py
>>> test(1, 5)
test: 1 5.0
```

Finally a dynamic type can wrap another dynamic type to create a **Compound Dynamic Type**. In the following example we use strong typing with `Strict` on the type conversion with `Convert`.  
`Convert` won't raise any error by itself, so `Strict` will implement that.

```py
from typix import processor, Strict, Convert

@processor
def test(my_arg: Strict(Convert(int))):
    print("test:", my_arg)
```

```py
>>> test(1.0)
test: 1
>>> test("Hello World!")
Traceback (most recent call last):
    ...
typix.error.TypixError: Strict constraint failed: Cannot convert 'str' to 'int'
```

> **Type checking with the `typecheck` function**

In a non-function context, type checking a value is often needed. This module provides the `typecheck` function that allow dynamic type checking
with some extra features.  
The function takes is defined like this:  
`typecheck(value, type_, context = None)`  
It works like the `isinstance` built-in function but it supports `GenericAliases` like `list[int]` and dynamic types. The function will return a `CheckResult` object containing data about the typecheck but it can be used as a boolean value. Hence, it can be used in an `if` statement directly. The context parameter is needed when the dynamic type needs argument data. In this case, the `typecheck` function shouldn't be used or argument data should be passed with the context argument using a `Context` object. Thus, the `Context` object is not meant to be used directly, but for edge cases.  
Here is an example of the usage of the `typecheck` function:

```py
>>> typecheck(0, int) # Simple use case with static types
<CheckResult: True>
>>> typecheck([1, 2, 3], list[int]) # GenericAlias support
<CheckResult: True>
>>> typecheck(0.0, Strict(int)) # In this case an error can be raised by typecheck
Traceback (most recent call last):
    ...
typix.error.TypixError: Strict constraint failed
```

> Custom Dynamic Types

In this final section we will see how to create dynamic types. The process is
very easy.

```py
from typix import Typix, typecheck

class Greeting(Typix):
    def process(self, greeting_type, person):
        if not typecheck(self.value, str):
            return self.error("The argument value should be a 'str'")
        return f"{greeting_type} {person}! Here is the argument value: {self.value}"
```

We create a class with the name of the type that inherits `Typix`. Then we overload the `process` method, and we define the parameters of the type.  
`self` will contain context information if needed.  
The return value of the function will become the new value of the annotated argument.  
If an unwanted value goes into the argument, we should return an error. Not with a `raise`
statement but by returning `self.error` with the error message as
the argument. The error also takes a optional argument `fatal`. If an error is fatal, this error will be raised at runtime, else, it won't be raised at all but it will be written in the context and a parent type like `Strict` can access it and raise it as a fatal error. That is how contexts works. Every typecheck, either in a function or not: context contains returned errors, the current value and argument and function data to be accessed by parent types. A `CheckResult` object returned by the `typecheck` function can also be used as context.  
In real conditions, we can use the newly made type like this:
```py
from typix import processor

@processor
def test(my_arg: Greeting("Hello", "Paul")):
    print(my_arg)
```
```py
>>> test("I like berries")
Hello Paul! Here is the argument value: I like berries
>>> test(5) # This returns an non-fatal error. Thus, it will return the default value.
5
```