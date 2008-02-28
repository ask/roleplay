
from roleplay import does, has_role
from roleplay.role import Role

# Create 2 roles

class rFoo(Role):
    def foo(self):
        return "rFoo::foo"

class rBar(Role):
    pass

# Combine them into a third role

class rFooBar(Role):
    pass

has_role(rFooBar, rFoo, rBar)

import inspect
assert Role in inspect.getmro(rFoo)
assert Role in inspect.getmro(rBar)
assert Role in inspect.getmro(rFooBar)
assert rFoo not in inspect.getmro(rFooBar)
assert rBar not in inspect.getmro(rFooBar)
                                                                                  
assert does(rFoo, rFoo)
assert does(rBar, rBar)
assert does(rFooBar, rFoo)
assert does(rFooBar, rBar)
assert does(rFooBar, rFooBar)

# create another role                                                             

class rBaz(Role):
    pass

has_role(rBaz, rFoo)

assert Role in inspect.getmro(rBaz)

assert does(rBaz, rFoo)
assert does(rBaz, rBaz)                                                                                  

# The role below (rFooBarBaz) will be getting rFoo twice, first                   
# from the rFooBar role, and then from rBaz role. If roles are                    
# not composed properly (see above), this will cause a method                     
# conflict to arise since rBaz and rFooBar will seem to both                      
# have a copy of &foo.                                                            
#                                                                                 
# Roles should *never* be composed into one another, and in fact,                 
# they should only be composed at the very last possible moment.                  
#                                                                                 
# The roles (and subroles) being composed need to be linearized                   
# into a list of unique roles (ordering is unimportant), and then                 
# composed into the class itself (following the method compostion                 
# rules).

class FooBarBaz(object):
    pass

has_role(FooBarBaz, rFooBar, rBaz)

does(FooBarBaz, rFoo)
does(FooBarBaz, rBar)
does(FooBarBaz, rFooBar)
does(FooBarBaz, rBaz)

import inspect
print inspect.getframeinfo(inspect.currentframe())[0].ljust(40) + ": OK! All tests passed."
