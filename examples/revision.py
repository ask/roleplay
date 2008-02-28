# -*- coding: ascii -*-
# $Id$
# $Source$
# $Author$
# $HeadURL$
# $Revision$
# $Date$
'''
    Example Role
'''

from roleplay.role import Role

class RevisionRole(Role):

    __requires__ = "table primary_key".split()

    def save_revision(self):
        print "saving revision..."

class DuplicateRevisionRole(Role):

    __requires__ = "table primary_key".split()

    def save_revision(self):
        print "saving revision..."

# Local Variables:
#   mode: cpython
#   cpython-indent-level: 4
#   fill-column: 78
# End:
# vim: expandtab tabstop=4 shiftwidth=4 shiftround
