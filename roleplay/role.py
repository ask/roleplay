# -*- coding: ascii -*-
# $Id$
# $Source$
# $Author$
# $HeadURL$
# $Revision$
# $Date$
'''
    pyrole.role:

        Module for creating roles.

    author: Ask Solem <askh@opera.com>
    Copyright (c) Ask Solem. Released under the GPLv2, see the
    LICENSE file for a full copy of the license.
'''

__version__     = '0.8'
__author__      = 'Ask Solem <askh@opera.com'
__authority__   = 'pypi:ASK'

from roleplay.meta import MetaRole
from roleplay.meta import CommonRole

class ClassDoesNotFulfillRequirement(Exception):
    ''' Tried to apply role to the class, but the class didn't fulfill
        all requirements of the role. (Probably missing method/attribute)
    '''

class Role(CommonRole):
    ''' -------------------------------------------  --- ---- -   - -  - -
        Base class for Roles.

        New roles inherits from this.
    ---------------------------------------------------------------------- '''
    meta = MetaRole()

    def __init__(self, instance, **kwargs):
        self.meta.init_attributes(self, for_class=instance, role_args=kwargs)

    def check_requires(self, with_class):
        '''
            The role can have a 'requires' attribute containing a list of
            attribute-names that the user class has to implement to do the
            role. This method will check that all requirements are fulfilled.
        '''
        # Check if we have requirements at all
        if not hasattr(self, '__requires__'):
            return True
        if not len(self.__requires__):
            return True
        
        for requirement in self.__requires__:
            if not hasattr(with_class, requirement):
                raise ClassDoesNotFulfillRequirement(requirement)
        return True


# Local Variables:
#   mode: cpython
#   cpython-indent-level: 4
#   fill-column: 78
# End:
# vim: expandtab tabstop=4 shiftwidth=4 shiftround
