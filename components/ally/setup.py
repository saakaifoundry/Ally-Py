
'''
Created on Oct 1, 2013
 
@package: distribution_manager
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Cristian Domsa
 
Setup configuration for components/plugins needed for pypi.
'''

# --------------------------------------------------------------------

from setuptools import setup, find_packages

# --------------------------------------------------------------------

setup(     name='ally',
     author='Gabriel Nistor',
     author_email='gabriel.nistor@sourcefabric.org',
     py_modules=['application', 'package_extender'],
     long_description="This is the main component and is the application entry point. \n'This component provides also support for inversion of control container.\n'Basically this component contains general support for the application that is not in any way linked with a particular technology.",
     version='1.0',
     test_suite='__unit_test__',
     keywords=['Ally', 'REST'],
     classifiers=['Development Status :: 4 - Beta'],
     description='Ally framework - utilities component',

     packages=find_packages('.'),
     platforms=['all'],
     zip_safe=True,
     license='GPL v3',
     url='http://www.sourcefabric.org/en/superdesk/', # project home page
      )
