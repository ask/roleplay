from roleplay import does, has_role
from roleplay.role import Role

class Base(Role):
    def base(self):
        return "Base.base"

class Foo(Role):
    def foo(self):
        return "foo.foo"

has_role(Foo, Base);

assert does(Foo, Base);

class Bar(Role):
    def bar(self):
        return "Bar.bar"

has_role(Bar, Foo)
assert does(Bar, Foo)
assert does(Bar, Base)

class Fubar(Role):
    def fubar(self):
        return "Fubar.fubar"
import inspect
print inspect.getframeinfo(inspect.currentframe())[0].ljust(40) + ": OK! All tests passed."
