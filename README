========================================
``roleplay:`` Python does Roles
========================================
:Version: 0.8 

Roleplay is an in-progress implementation of roles for Python. The current
state is that it passes the Perl6-Roles_ test suite, which is not the final
authority on Perl6 roles, but a Perl5 implementation.

=======================================
Synopsis
=======================================

Creating Roles
______________

>>> from roleplay.role import Role
        
>>> class LoadFrobulatorRole(Role):
...     '''
...         Simple role example.
...     '''
...
...     # Roles can use the '__requires__' attribute to define a set
...     # of attributes/methods the class using the role has to
...     # define (or else it would get an exception).
...     
...     __requires__ = ["has_frobulator"]
...
...     def save_frobulator(self, data):
...
...         # Do something with data
...         # .....
...         print "saving frobulator..."
...
...

>>> class SaveFrobulatorRole(Role):
...     '''
...         Another role example
...     '''
...
...
...     def load_frobulator(self, article_id):
...
...         # Do something with data
...         # .....
...         print "loading frobulator..."
...
...

Using Roles
___________

>>> from roleplay import has_role, does

>>> class Article(object): 
...     '''
...         This is our class using the roles.
...     '''
...
...     def __init__(self):
...         pass
...
...     def load_article(self, id):
...
...         if does(self, LoadFrobulatorRole):
...             self.load_frobulator(id)
...         # ... do other loading stuff ... #
... 
...     def save_article(self, data):
...         
...         if does(self, SaveFrobulatorRole):
...             self.save_frobulator(data)
...         # ... do other saving stuff ... #
...
...
...     # This is the requirement for RoleA.
...     def has_frobulator(self):
...         frobulator = config.lookup('frobulator')
...         return frobulator
...
...
... has_role(Article, LoadFrobulatorRole, SaveFrobulatorRole)
...
...
... article = Article()
... 
... art = article.load_article(13)
... article.save_article(art)
...

======================================
Installation
======================================

To install:

    >>> python ./setup.py install


Or via easy_install:

    >>> easy_install roleplay

        
=======================================
Acknowledgements
=======================================

Thanks to Rob Kinyon and Stevan Little for the Perl6-Roles_ test suite,
hope you don't mind me porting it to python :)


.. _Perl6-Roles: http://search.cpan.org/perldoc?Perl6::Role


