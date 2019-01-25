#! /usr/bin/env python3

from distutils.core import setup


setup(
    name='comcatlib',
    version='latest',
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='<info at homeinfo dot de>',
    maintainer='Richard Neumann',
    maintainer_email='<r dot neumann at homeinfo period de>',
    requires=[
        'argon2', 'configlib', 'flask', 'mdb', 'peewee', 'peeweeplus',
        'werkzeug'],
    packages=['comcatlib'],
    description='Shared libraries for ComCat.')
