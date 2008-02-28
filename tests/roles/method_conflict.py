'''
    method_conflict: Adopted from Perl6::Roles t/002_method_conflict.t
'''
#import nose

from roleplay import Role
from roleplay.keyword import has_role, does
from roleplay.meta import RoleConflictDetected

class rFoo(Role):
    def foo(self):
        return "rFoo::foo"
    def baz(self):
        return "rFoo::baz"

class rBar(Role):
    def bar(self): 
        return 'rBar::bar'
    def baz(self):
        return 'rBar::baz'


class FooBarWithConflict(object):
    pass

foobarwithconflict_conflicts = 0
try:
    has_role(FooBarWithConflict, rFoo, rBar)
except RoleConflictDetected:
    foobarwithconflict_conflicts = 1

assert foobarwithconflict_conflicts


class FooBarWithOutConflict(object):
    def baz(self):
        return "FooBar::With::Out::Conflict::baz"

foobarwithoutconflict_resolved = 1
try:
    has_role(FooBarWithOutConflict, rFoo, rBar)
except RoleConflictDetected:
    foobarwithoutconflict_resolved = 1
    pass
finally:
    assert foobarwithoutconflict_resolved
    

assert hasattr(FooBarWithOutConflict, 'baz');
assert hasattr(FooBarWithOutConflict, 'foo');
assert hasattr(FooBarWithOutConflict, 'bar');

assert FooBarWithOutConflict().baz() == "FooBar::With::Out::Conflict::baz"
assert FooBarWithOutConflict().foo() == "rFoo::foo"
assert FooBarWithOutConflict().bar() == "rBar::bar"


# Now create a role which consumes both
class rFooBar(Role):
    def foo_bar(self):
        return "rFooBar::foo_bar"

subroles_not_consumed = 1
try:
    has_role(rFooBar, rFoo, rBar)
except RoleConflictDetected:
    subroles_not_consumed = 0
finally:
    assert subroles_not_consumed



assert does(rFooBar, rFoo);
assert does(rFooBar, rBar);
assert not hasattr(rFooBar, 'baz')
assert hasattr(rFooBar, 'foo_bar')

# Now compose it and get the conflict:

class FooBarWithConflict2(object):
    pass

foobarwithconflict2_conflicts = 0
try:
    has_role(FooBarWithConflict2, rFooBar)
except RoleConflictDetected:
    foobarwithconflict2_conflicts = 1

from roleplay.meta import MetaRole
meta = MetaRole()

assert foobarwithconflict2_conflicts

## now compose, and let it get dis-ambiguated

class FooBarWithOutConflict2(object):
    def baz(self):
        return "FooBar::With::Out::Conflict2::baz"

foobarwithoutconflict2_resolved = 1
try:
    has_role(FooBarWithOutConflict2, rFooBar)
except RoleConflictDetected:
    foobarwithoutconflict2_resolved = 0
finally:
    assert foobarwithoutconflict2_resolved

assert hasattr(FooBarWithOutConflict2, 'baz')
assert hasattr(FooBarWithOutConflict2, 'foo')
assert hasattr(FooBarWithOutConflict2, 'bar')
assert hasattr(FooBarWithOutConflict2, 'foo_bar')

assert FooBarWithOutConflict2().foo_bar() == 'rFooBar::foo_bar'
assert FooBarWithOutConflict2().baz() == 'FooBar::With::Out::Conflict2::baz'
assert FooBarWithOutConflict2().foo() == 'rFoo::foo'
assert FooBarWithOutConflict2().bar() == 'rBar::bar'


# Now resolve the method conflict in the role    

class rFooBar2(Role):
    def baz(self):
        return "rFooBar2::baz"

rfoobar2_subroles_not_consumed = 1
try:
    has_role(rFooBar2, rFoo, rBar)
except RoleConflictDetected:
    rfoobar2_subroles_not_consumed = 0
finally:
    assert rfoobar2_subroles_not_consumed

assert does(rFooBar2, rFoo)
assert does(rFooBar2, rBar)

assert hasattr(rFooBar2, 'baz')











class rBaz(Role):
    def floober(self):
        return "rBaz::floober"

class rFooBarBaz(Role):
    pass

rfoobarbaz_subroles_not_consumed = 1
try:
    has_role(rFooBarBaz, rFooBar, rBaz)
except RoleConflictDetected:
    rfoobarbaz_subroles_not_consumed = 0
finally:
    assert rfoobarbaz_subroles_not_consumed


class FooBarBazWithConflict(object):
    pass

foobarbaz_conflict = 0
try:
    has_role(FooBarBazWithConflict, rFooBarBaz)
except RoleConflictDetected:
    foobarbaz_conflict = 1
finally:
    assert foobarbaz_conflict

class FooBarBazWithOutConflict(object):
    def baz(self):
        return "FooBarBaz::With::Out::Conflict::baz"

foobarbaz_resolved_conflict = 1
try:
    has_role(FooBarBazWithOutConflict, rFooBarBaz)
except RoleConflictDetected:
    foobarbaz_resolved_conflict = 0
finally:
    assert foobarbaz_resolved_conflict

assert hasattr(FooBarBazWithOutConflict, 'baz')
assert hasattr(FooBarBazWithOutConflict, 'foo')
assert hasattr(FooBarBazWithOutConflict,'bar')
assert hasattr(FooBarBazWithOutConflict,'floober')

assert does(FooBarBazWithOutConflict,rFoo)
assert does(FooBarBazWithOutConflict,rBar)
assert does(FooBarBazWithOutConflict,rFooBar)
assert does(FooBarBazWithOutConflict,rBaz)

assert FooBarBazWithOutConflict().baz() == "FooBarBaz::With::Out::Conflict::baz"
assert FooBarBazWithOutConflict().foo() == "rFoo::foo"
assert FooBarBazWithOutConflict().bar() == "rBar::bar"
assert FooBarBazWithOutConflict().floober() == "rBaz::floober"

import inspect
print inspect.getframeinfo(inspect.currentframe())[0].ljust(40) + ": OK! All tests passed."

## OK!
