# -*- coding: ascii -*-
# $Id$
# $Source$
# $Author$
# $HeadURL$
# $Revision$
# $Date$
'''
    roleplay.meta:

        This module handles internal role metadata and the introspection
        necessary to install roles and mixin classes.

    author: Ask Solem <askh@opera.com>
    Copyright (c) Ask Solem. Released under the GPLv2, see the
    LICENSE file for a full copy of the license.
'''

__version__     = '0.8'
__author__      = 'Ask Solem <askh@opera.com'
__authority__   = 'pypi:ASK'

import os
import sys
import types
import inspect
from   itertools import ifilter
from   inspect   import isbuiltin

DEBUG = 1

roles_defines_attrs = "__is_role__ check_requires for_class role_args meta".split()
role_bases = "roleplay.meta.CommonRole roleplay.role.Role __builtin__.object".split()

# ############ Exceptions ###################################

class AttributeIsPrototypeError(Exception):
    ''' The attribute is only a prototype and is not accessible '''

class RoleConflictDetected(Exception):
    ''' Method was already defined an already applied role '''

class RoleInheritsFromRole(Exception):
    ''' Roles can not inherit from each other. Use them as roles instead '''

# ############# Utility functions ###########################

def _get_class(cls):
    if isinstance(cls, object):
        if hasattr(cls, '__name__'):
            return cls
        else:   # is instance
            return cls.__class__

def _get_id(cls):
    if inspect.isclass(cls):
        return ".".join((inspect.getmodule(cls).__name__, cls.__name__))
    return cls # <-- is (probably) instance

# ############# Classes #####################################

# Common identifiable base class
class CommonRole(object):
    ''' All roles must inherit from this role. '''
    @classmethod
    def __is_role__(cls):
        return True

# The registry. (Stores role+class metadata)
class MetaRoleRegistry(object):
    '''
        Keeps track of classes and their roles,
        roles and their roles, and so on.

        The registry is a singleton class.
    '''
    _shared_state     = { }
    _role_registry    = { }
    _delayed_roles    = { }
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_state
        return obj

    def has_role(self, cls_path):
        if cls_path in self._role_registry:
            return 1
        return 0

    def get_roles_for_class(self, cls):
        name = _get_id(cls)
        if name not in self._role_registry:
            self._role_registry[name] = { }
        return self._role_registry[name]

    def get_delayed_roles_for(self, cls):
        name = _get_id(cls)
        if name not in self._delayed_roles:
            self._delayed_roles[name] = [ ]
        return self._delayed_roles[name]


class MetaRole(object):
    ''' -------------------------------------------  --- ---- -   - -  - -
        The class that does all the hard lifting.
        (The instructor? No the chef!)
        

        Probably only used by the Role class itself. If you want to
        subclass the role system, it's probably better to subclass Role
        rather than MetaRole.
    ---------------------------------------------------------------------- '''

    # ### Prototype attributes
    # only here so they can be skipped when mixing.
    for_class  = None
    role_args  = None
    meta       = None

    # ### Registry composite
    role_registry = MetaRoleRegistry()

    def get_linear_roles(self, role):
        current_roles = set()
        current_roles.add(role)
        role_name     = _get_id(role)

        # Consume delayed subroles
        for subrole in set(self.role_registry.get_delayed_roles_for(role_name)):
            current_roles.update( self.get_linear_roles(subrole) )

        return current_roles

    def apply(self, instance, *args, **kwargs):

        # ## Handle arguments
        # This is here so we can use this method like this:
        #   apply(MyClass, Role1, Role2, Role3)   # args
        #
        # or like this:
        #   apply(MyClass, [Role1, Role2, Role3]) # list
        #
        # or even like this:
        #   apply(MyClass, (Role1, Role2, Role3)) # tuple
        #
        if isinstance(args[0], tuple) or isinstance(args[0], list):
            args = args[0]

        # List of roles is converted to a set
        # (we don't want duplicates!)
        roles      = set(args)
        into_other = instance  # Just a handy alias
        conflicts  = { }
        methods_defined_in_roles = { }
        
        # Subroles should be composed later so register them and return
        # so they can be processed whenever a class uses this role.
        try:
            instance.__is_role__()
        except AttributeError:
            pass
        else:
            into_path = _get_id(into_other)
            delayed_roles_for = self.role_registry.get_delayed_roles_for(into_path)
            for role in roles:
                delayed_roles_for.append(role)
                self.__addrole__(into_other, role)
            return;


        # Get a linear list of roles to apply by summation
        linear_roles = set()
        for role in roles:
            linear_roles.update( self.get_linear_roles(role) )
       
        # Keep the classes symbol table in memory for quick
        # conflict detection.
        others_symtable = set( dir(into_other) )

        for role in linear_roles:
            role_path  = _get_id(role)


            # A role can never inherit from another role, only use them as
            # roles.
            for superclass in inspect.getmro(role):
               
                # We don't care if it inherits from itself 
                if role == superclass:
                    continue

                superclass_path = _get_id(superclass)
                if superclass_path in role_bases:
                    continue
                
                inherits_from_role = 0
                if CommonRole in inspect.getmro(superclass):
                    inherits_from_role = 1
                elif self.role_registry.has_role(superclass_path):
                    inherits_from_role = 1

                if inherits_from_role:
                    raise RoleInheritsFromRole, "role %s inherits from %s" % (
                        superclass_path, role_path
                    )
        
            # Create instance of the role and iterate over it's symbols
            irole = role(into_other)
            for symbol, symbol_ref in self._get_normalized_symtable(irole):
        
                if (not isbuiltin(symbol_ref)):
                    if not inspect.isclass(into_other) or symbol not in others_symtable:
                   
                        # Have we already seen this? Then it's a conflict 
                        if symbol in methods_defined_in_roles:
                            conflicts[symbol] = symbol_ref

                        # Flatten the symbol into the using class
                        setattr(into_other, symbol, symbol_ref)
                        methods_defined_in_roles[symbol] = role

            # Add and register the role for future reference
            self.__addrole__(into_other, role)
           
        # Conflict resolution
        if len(conflicts):
            sorted_conflicts = conflicts.keys()
            sorted_conflicts.sort()
            symbol = sorted_conflicts[0]
            raise RoleConflictDetected, "%s already defined in %s" % (
                symbol,
                _get_id(methods_defined_in_roles[symbol])
            )

        # Check requirements/excludes as late as possible
        for role in linear_roles:
            irole = role(into_other);
            if hasattr(role, 'check_requires'): # XXX No tests for this yet
                irole.check_requires(into_other)
            if hasattr(role, 'check_excludes'): # TODO Not implemented
                irole.check_excludes(into_other)

        # Reset conflicts for class
        conflicts = { }

    def __does__(self, cls, role):
        ''' private method doing the role lookup '''

        # If they have the same memory address, we could be pretty sure
        # they define the same interface, so return true.
        if cls is role:
            return True

        # If they have the same class path, we also return true.
        if _get_id(cls) == _get_id(role):
            return True

        superclasses = list(inspect.getmro( _get_class(cls) ))

        stream = list(superclasses);

        while (1):
            if not len(stream):
                break
            atom = stream.pop()
            # If the role is inherited we also return true.
            if _get_id(atom) == _get_id(role):
                return True

            roles_for = self.role_registry.get_roles_for_class(atom)
            role_name = _get_id(role)
                    
            if role_name in roles_for:
                return True

            [stream.append(l) for l in roles_for]

        return False

    def __addrole__(self, cls, role):
        ''' private method updating the role registry '''
        roles_for = self.role_registry.get_roles_for_class(cls)
        role_name = _get_id(role)
        if role_name in role_bases:
            return 
        roles_for[role_name] = True

    def init_attributes(self, cls, **kwargs):
        '''
            Initialize multiple attributes at once, with default values.
            Usually used within the __init__ method of a class.

            Example usage:

                class MyRole(Role):
                    meta = MetaRole()

                    def __init__(self, for_class):
                        meta.init_attributes(self,
                            for_class=for_class,
                        )

            This will initialize the attributes for_class
            with the default values passed when constructing the instance.
        '''
        [setattr(cls, name, value) for name, value in kwargs.iteritems()]


    def __getattribute__(self, attribute_name):
        ''' Same as the usual __getattr__ except it will raise an
            AttributeIsPrototypeError when accessing any attributes
            that just defines the instance of a real Role.
        '''
        if attribute_name in roles_defines_attrs:
            raise AttributeIsPrototypeError
        return super(MetaRole, self).__getattribute__(attribute_name)

    def _get_normalized_symtable(self, from_object):
        '''
            Get a list of normalized symbols from an object.

            This is like dir(from_object), except it will not contain
            symbols from builtin methods, the type metaclass,
            or the MetaRole class.
        '''
        results = []
        for symbol in dir(from_object):
            if symbol in skip_sym:
                continue
            value = getattr(from_object, symbol)
            if isinstance(value, types.MethodType):
                results.append((symbol, value))
        return results



'''
set: skip_sym
    Used by MetaRole._get_normalized_symtable_for() as a list of
    attributes/methods we don't export when doing a mixin.
'''  
skip_sym = set( dir(MetaRole) ) | set( roles_defines_attrs )

# Local Variables:
#   mode: cpython
#   cpython-indent-level: 4
#   fill-column: 78
# End:
# vim: expandtab tabstop=4 shiftwidth=4 shiftround
