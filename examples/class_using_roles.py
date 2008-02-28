# $Id$
# $Source$
# $Author$
# $HeadURL$
# $Revision$
# $Date$
'''
    Example class using the revision role
'''

from roleplay import does, has_role
from examples.revisions import RevisionRole

class MyClass(object):
    table = "foo"
    primary_key = 'id'

    def hello(self):
        return self.save_revision()

has_role(MyClass, RevisionRole)

obj = MyClass()

obj.hello()

