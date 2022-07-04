---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.13.7
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

<!-- #region slideshow={"slide_type": "slide"} -->
## Step1: Using Traits

**Jonathan Rocher, Siddhant Wahal, Jason Chambless, Prabhu Ramachandran**

**SciPy 2022**

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Introduction to Traits

- **trait**: Python object attribute with additional characteristics
    - Typed attributes
    - Reactive
    - Observable
    - Cleaner code
    - Easy UI

<br/>

- https://docs.enthought.com/traits/
- https://github.com/enthought/traits/

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Why all this?

- No pain, no gain!

- Small change to thinking yields big benefits

- Do not mix GUI code with core model

- Build a clean model first

  - Easier to understand/maintain
  - Separation of concerns
  - Easier to test
  - Generally better reuse

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Trait features

- Initialization: default value
- Validation: strongly typed
- Deferral/Delegation: value delegation
- Notification: events
- Visualization: MVC, automatic GUI!

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## An example

<!-- #endregion -->

```python
from traits.api import Delegate, HasStrictTraits, Instance, Int, Str, observe

class Parent(HasStrictTraits):
    # INITIALIZATION: 'last_name' initialized to ''
    last_name = Str('')

```

```python
class Child(HasStrictTraits):
    age = Int
    # VALIDATION: 'father' must be Parent instance
    father = Instance(Parent)
    # DELEGATION: 'last_name' delegated to father's
    last_name = Delegate('father')
    # NOTIFICATION: Method called when 'age' changes
    def _age_changed(self, old, new):
        print('Age changed from %s to %s ' % (old, new))

```

<!-- #region slideshow={"slide_type": "slide"} -->
## Using this

<!-- #endregion -->

```python
joe = Parent()
joe.last_name = 'Johnson'
moe = Child()
moe.father = joe
```

```python
# Delegation
moe.last_name
```

```python
# Notification
moe.age = 10
```

```python
# Validation
moe.age = '1'
```

```python
# Visualization
moe.configure_traits()
```

- Live editing!

```python
%gui qt
```

```python
moe.edit_traits()
```

```python
moe.age = 21
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Predefined trait types

- Standard: `Bool, Complex, Int, Float, Str, Tuple, List, Dict`
- Constrained: `Range, Regex, Expression, ReadOnly`
- Special: `Date, Either/Union, Enum, Array, File, Color, Font, Button`
- Generic: `Instance, Any, Callable`
- Custom traits: 2D/3D plots etc.

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## `HasStrictTraits` vs. `HasStrictTraits`

- Better to use `HasStrictTraits`
- Will catch errors when you mistype or misspell an attribute
- Will not allow setting any attribute not already declared


<!-- #endregion -->


<!-- #region slideshow={"slide_type": "slide"} -->
## Notification example

<!-- #endregion -->

```python
class Parent(HasStrictTraits):
    last_name = Str('')


class Child(HasStrictTraits):
    age = Int
    father = Instance(Parent)

    def _age_changed(self, old, new):
        print('Age changed from %s to %s ' % (old, new))

    @observe('father.last_name')
    def _dad_name_updated(self, event):
        print('DAD name', self.father.last_name)

```

```python
dad = Parent(last_name='Zubizaretta')
c = Child(father=Parent)
```

```python
dad.last_name = 'Valderrama'
```

```python
def handler(event):
    print("handler", event.object, event.name, event.old, event.new)
```

```python
c = Child(father=Parent(last_name='Ram'))
c.observe(handler, 'father, age')
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Trait change notification

- Static: `def _<trait_name>_changed()`
- Decorator: `@observe('extended.trait.name')`
- Dynamic:

```obj.observe(handler, 'extended.trait.name')
```

- See documentation: https://docs.enthought.com/traits/traits_user_manual/notification.html

<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Exercise

- Modify the first example to produce the above example
- Add a `first_name` trait
- Add a `Bool` trait to specify if person is alive
- Add an `Enum` for the gender of the child


<!-- #endregion -->

<!-- #region slideshow={"slide_type": "slide"} -->
## Solution

<!-- #endregion -->

```python
from traits.api import Bool, Enum

class Parent(HasStrictTraits):
    last_name = Str('')


class Child(HasStrictTraits):
    age = Int
    father = Instance(Parent)
    first_name = Str('')
    alive = Bool(True)
    gender = Enum('female', 'male', 'neither')

    def _age_changed(self, old, new):
        print('Age changed from %s to %s ' % (old, new))

    @observe('father.last_name')
    def _dad_name_updated(self, event):
        print('Dad name', self.father.last_name)

```

```python
p = Parent(last_name='Ray')
c = Child(age=21, father=p, first_name='Romano', gender='male')
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Setting default values

- For simple cases, use the default of the trait
- For more complex cases use a special method
- A simple example

<!-- #endregion -->

```python
import datetime

from traits.api import HasStrictTraits, Date, Range

class Thing(HasStrictTraits):
    date = Date()
    age = Int(12)

    def _date_default(self):
        print('default')
        return datetime.datetime.today()
```


```python
t = Thing()
```

```python
type(c.age)
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Trait Lists


<!-- #endregion -->

```python
from traits.api import List

class Bowl(HasStrictTraits):
    fruits = List(Str)

    def _fruits_changed(self, o, n):
        print("Fruits changed", o, n)

```

```python
b = Bowl()
b.fruits = ['apple']
b.fruits.append('mango')
```

<!-- #region slideshow={"slide_type": "slide"} -->
## Trait List events

<!-- #endregion -->

```python
class Bowl(HasStrictTraits):
    fruits = List(Str)
    def _fruits_changed(self, o, n):
        print("Fruits changed", o, n)

    def _fruits_items_changed(self, list_event):
        print(list_event.index)
        print(list_event.removed)
        print(list_event.added)

```

```python
b = Bowl()
b.fruits = ['apple']
b.fruits.append('mango')
```

```python
def handler(event):
    print("h:", event)

b.observe(handler, 'fruits.items')
b.fruits.append('peach')
```

```python
# Remove the handler
b.observe(handler, 'fruits.items', remove=True)
```


<!-- #region slideshow={"slide_type": "slide"} -->
## Other events

- `TraitChangeEvent`
- `ListChangeEvent`
- `DictChangeEvent`
- `SetChangeEvent`

<!-- #endregion -->



<!-- #region slideshow={"slide_type": "slide"} -->
## Exercise time!

- Take the simple example
- Create a simple Traits model

<!-- #endregion -->