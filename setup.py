#! /usr/bin/env python3
"""Install script."""

from setuptools import setup


setup(
    name="comcatlib",
    use_scm_version={"local_scheme": "node-and-timestamp"},
    setup_requires=["setuptools_scm"],
    author="HOMEINFO - Digitale Informationssysteme GmbH",
    author_email="<info@homeinfo.de>",
    maintainer="Richard Neumann",
    maintainer_email="<r.neumann@homeinfo.de>",
    install_requires=[
        "argon2_cffi",
        "authlib",
        "cmslib",
        "configlib",
        "damage_report",
        "emaillib",
        "filedb",
        "firebase_admin",
        "flask",
        "marketplace",
        "mdb",
        "notificationlib",
        "oauth2gen",
        "peewee",
        "peeweeplus",
        "requests",
        "tenantcalendar",
        "tenantforum",
        "werkzeug",
        "wsgilib",
    ],
    packages=["comcatlib", "comcatlib.demo", "comcatlib.messages", "comcatlib.orm"],
    data_files=[
        ("/usr/local/share/comcatlib/", ["files/authorize.html", "files/login.html"])
    ],
    entry_points={
        "console_scripts": ["comcat-demo-reset = comcatlib.demo.manager:main"]
    },
    description="Shared libraries for ComCat.",
)
