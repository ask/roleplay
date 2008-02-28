# -*- coding: ascii -*-
# $Id$
# $Source$
# $Author$
# $HeadURL$
# $Revision$
# $Date$
'''
    roleplay.keyword:

        Apply and test for roles.

    author: Ask Solem <askh@opera.com>
    Copyright (c) Ask Solem. Released under the GPLv2, see the
    LICENSE file for a full copy of the license.
'''

__version__     = '0.8'
__author__      = 'Ask Solem <askh@opera.com'
__authority__   = 'pypi:ASK'

from roleplay.meta import MetaRole
from roleplay.role import Role

DEBUG = 0
DOES_FRAME_STEP_MAX = 2

# this should be list(dir(Role)) when the Role baseclass is finished

class DoesOutsideClass(Exception):
    ''' does() must be used in a class definiton '''

def has_role(instance, *args, **kwargs):
    '''
        Applies the roles %{args} to your class instance.

        %{instance} must be a class instance object.
        %{args} must be a list of class objects, not instantiated classes.

        Example:

        has_role(self, RoleClass)

        has_role(self, RoleClass, OtherRoleClass)


    '''
    meta = MetaRole()
    meta.apply(instance, *args, **kwargs)

def does(instance, role):
    '''
        Returns True if %{instance} supports the role %(role).

        %(class) can be instance, class or string.
        %(role) can be instance, class or string.

        Example:

        has_comment_support = does(self, 'Comments')
    '''
    meta = MetaRole()
    return meta.__does__(instance, role)

''' XXX Not finished 
def doesx(role, **kwargs):
    caller = ""
    try:
        frame  = sys._getframe(1)
    except ValueError:
        raise DesOutsideClass;
    
    frameinfo   = inspect.getframeinfo(frame, context=1)
    module_file = frameinfo[0]
    cls         = frameinfo[2] 
    
    module_name, module_ext = os.path.splitext(module_file)
   
    module = sys.modules.get(module_name) 
    
    print "module: [%s], module_file: [%s], module_name: [%s], ext: [%s], class: [%s]" % (
        str(module), module_file, module_name, module_ext, cls
    )
'''


# Local Variables:
#   mode: cpython
#   cpython-indent-level: 4
#   fill-column: 78
# End:
# vim: expandtab tabstop=4 shiftwidth=4 shiftround
