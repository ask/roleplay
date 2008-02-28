# -*- coding: ascii -*-
# $Id$
# $Source$
# $Author$
# $HeadURL$
# $Revision$
# $Date$
'''
    roleplay.inheritable:

        Base class with method versions of does() and has_role().

        You don't really have to inherit from this class, you can just as well
        import the function versions from the roleplay top-level module.

            from roleplay import does, has_role

        However, if you already have a common base class for all your objects, or you
        maintain a metaclass, this module could be the thing for you.

    author: Ask Solem <askh@opera.com>
    Copyright (c) Ask Solem. Released under the GPLv2, see the
    LICENSE file for a full copy of the license.

'''

__version__     = '0.8'
__author__      = 'Ask Solem <askh@opera.com'
__authority__   = 'pypi:ASK'

import roleplay.keyword

class RoleObject(object):
    '''
        Base class with method versions of does() and has_role().

        Example usage:

            from some.module import SomeRole

            class MyClass(RoleObject):
                
                def __init__(self):
                    self.has_role(SomeRole)

                def do_something(self):

                    # Test if we support the SomeRole role, if so we get    
                    # extra functonality.
                    if self.does('SomeRole'):
                        self.some_method_SomeRole_defines()

    '''

    def has_role(self, *args, **kwargs):
        '''
            Method version of roleplay.has_role

            %{role} must be class, not object instance.

            Example:

                self.has_role(RoleClass)
        '''
        roleplay.keyword.has_role(self, *args, **kwargs)

    def does(self, role):
        '''
            Method version of roleplay.does

            Returns True if this class supports the role.

            %(role) can be instance, class or string.

            Example:

                has_comment_support = self.does('Comments')
        '''
        roleplay.keyword.does(self, role)


# Local Variables:
#   mode: cpython
#   cpython-indent-level: 4
#   fill-column: 78
# End:
# vim: expandtab tabstop=4 shiftwidth=4 shiftround
    




