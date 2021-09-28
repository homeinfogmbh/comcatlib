#! /usr/bin/env python3
"""Install script."""

from setuptools import setup


setup(
    name='comcatlib',
    use_scm_version={
        "local_scheme": "node-and-timestamp"
    },
    setup_requires=['setuptools_scm'],
    author='HOMEINFO - Digitale Informationssysteme GmbH',
    author_email='<info@homeinfo.de>',
    maintainer='Richard Neumann',
    maintainer_email='<r.neumann@homeinfo.de>',
    install_requires=[
        'argon2_cffi',
        'authlib',
        'cmslib',
        'configlib',
        'damage_report',
        'filedb',
        'flask',
        'his',
        'hisfs',
        'mdb',
        'peewee',
        'peeweeplus',
        'requests',
        'setuptools',
        'tenant2tenant',
        'werkzeug',
        'wsgilib'
    ],
    packages=[
        'comcatlib',
        'comcatlib.app',
        'comcatlib.messages',
        'comcatlib.oauth',
        'comcatlib.orm'
    ],
    data_files=[('/usr/local/share/comcatlib/', [
        'files/authorize.html', 'files/login.html'
    ])],
    description='Shared libraries for ComCat.'
)
