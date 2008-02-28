
from roleplay import does, has_role
from roleplay.role import Role

class bark(Role):
    def talk(self):
        return "woof"

class sleeper(Role):
    def sleep(self):
        return 'snore'
    def talk(self):
        return 'zzz'

class Class(object):
    def sleep(self):
        return 'nite-nite'
   
assert not hasattr(Class, 'talk')   # The role is not composed at the class level
assert not hasattr(Class(), 'talk') # The role is not composed at the object level

obj = Class()
has_role(obj, bark)
assert not hasattr(Class, 'talk')
assert hasattr(obj, 'talk')

obj = Class()
assert obj.sleep() == "nite-nite"
has_role(obj, sleeper)
assert hasattr(obj, 'sleep')
assert hasattr(obj, 'talk')
assert obj.sleep() == 'snore' # The role silently overrides the class method
assert obj.talk()  == 'zzz'   # The role silently overrides the role's method


import inspect
print inspect.getframeinfo(inspect.currentframe())[0].ljust(40) + ": OK! All tests passed."
