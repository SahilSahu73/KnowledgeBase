# Abstract Base Classes (ABC)
Main goal of abc is to provide a standardized way to test whether an object adheres to a given specification.
Also prevents any attempt to instantiate a subclass that doesn't override a particular method in the superclass.
Using an abstract class, a class can derive identity from another class without any object inheritance.

## Declaring an Abstract Base Class
Rule - every abstract class must use ABCMeta metaclass.
ABCMeta metaclass provides a method called register method that can be invoked by its instance.
Using this register method any abc can become an ancestor of any arbitrary concrete class.

```python
import abc

class AbstractClass(metaclass=abc.ABCMeta):
  def abstractfunc(self):
    return None

print(AbstractClass.register(dict))
```

output:
<class 'dict'>

```python
print(issubclass(dict, AbstractClass))
```
output: True

## Why declare an Abstract Base Class
We need to consider the example of list-like object where you don't want to put a restriction of only
considering only list or a tuple.
To check if the instance is list or tuple we use isinstance this way:
> isinstance([], (list, tuple))

This *isinstance* check meets the purpose if you are accepting only a list or tuple.
But in the case of also accepting a list-like object, this above check will fail.
The above solution is not extensible for a developer who uses your library to send something else
other than a list or a tuple.

```python
import abc

class MySequence(metaclass=abc.ABCMeta):
  pass

MySequence.register(list)
MySequence.register(tuple)

a = [1, 2, 3]
b = ('x', 'y', 'z')

print('List instance: ', isinstance(a, MySequence))
print('Tuple instance: ', isinstance(b, MySequence))
print('Object instance: ', isinstance(object(), MySequence))

```
output:
List instance: True
Tuple instance: True
Object instance: False

Now if we consider a scenario where the developer expects a class object itself, in the above scenario it would return false.
But it can be achieved by creating a custom class and registering it with the abstract base class.

Here `MySequence` is an abstract class within the library. A developer can import it and register a custom class.

```python
import abc

class MySequence(metaclass = abc.ABCMeta):
  pass

class CustomListLikeObject(object):
  pass

MySequence.register(CustomListLikeObject)
print(isinstance(CustomListLikeObject, MySequence))
```
output:
True

So overall here we learnt how to instantiate a subclass and override a particular method in the superclass.
