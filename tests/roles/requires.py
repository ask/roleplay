
from roleplay import does, has_role
from roleplay.role import Role
from roleplay.role import ClassDoesNotFulfillRequirement

class rFoo(Role):
    __requires__ = ["sleep"]
    def foo(self):
        return "rFoo::foo"
    def use_sleeping(self, other):
        print str(self)
        return other.sleep()

class FooBar(object):
    pass

raises_on_missing_requirement = 0
try:
    has_role(FooBar, rFoo)
except ClassDoesNotFulfillRequirement:
    raises_on_missing_requirement = 1
assert raises_on_missing_requirement

class FooBarComplete(object):
    def sleep(self):
        return "FooBarComplete.sleep"

no_raise_on_complete = 1
try:
    has_role(FooBarComplete, rFoo)
except ClassDoesNotFulfillRequirement:
    no_raise_on_complete = 0
assert no_raise_on_complete
        
assert hasattr(FooBarComplete(), 'sleep')
assert hasattr(FooBarComplete(), 'use_sleeping')
assert FooBarComplete().use_sleeping(FooBarComplete()) == FooBarComplete().sleep()
