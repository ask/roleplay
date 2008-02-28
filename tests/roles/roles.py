'''
    simple.t: Adopted from Perl6::Roles t/001_roles.t
'''
#import nose

from roleplay import Role
from roleplay.keyword import has_role, does
from roleplay.meta import RoleInheritsFromRole

#nose.run()

class Bark(Role):
    def talk(self):
        return "woof"

class Animal(Role):
    def eat(self):
        return "munch"
    def sleep(self):
        return "zzz"


class Dog(object):
    def wag(self):
        return "tail"
    def eat(self):
        return "slobber"

has_role(Dog, Bark, Animal)

class Doberman(Dog):
    pass

class DobermanPinscher(Doberman):
    pass

class NoRoles(object):
    pass

class NoRolesChild(NoRoles):
    pass
  
for dog_type in (Dog, ): #Doberman, DobermanPinscher):
        for dog in (dog_type, dog_type()):
            assert hasattr(dog, 'eat')
            assert hasattr(dog, 'wag')
            assert hasattr(dog, 'talk')
            assert hasattr(dog, 'sleep')

            assert does(dog, dog)

assert not does(NoRoles, Dog)
assert not does(NoRolesChild, Dog)


# Roles can not inherit from other roles

class BadRole(Animal):
    pass

class ThisShouldCrash(object):
    pass

role_inheriting_from_role_crashes = 0
try:
    has_role(ThisShouldCrash, BadRole)
except RoleInheritsFromRole:
    role_inheriting_from_role_crashes = 1
assert role_inheriting_from_role_crashes

# ... try another one

class BadRole2(Role, Dog):
    pass

class ThisShouldCrash2(object):
    pass

role2_inheriting_from_role_crashes = 0
try:
    has_role(ThisShouldCrash2, BadRole2)
except RoleInheritsFromRole:
    role2_inheriting_from_role_crashes = 1

assert role2_inheriting_from_role_crashes

import inspect
print inspect.getframeinfo(inspect.currentframe())[0].ljust(40) + ": OK! All tests passed."
