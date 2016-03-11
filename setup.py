#!/usr/bin/env python
from setuptools import setup


setup(
    name='gssapi_console',
    version='1.0.0',
    author='The Python GSSAPI Team',
    author_email='sross@redhat.com',
    packages=['gssapi_console'],
    scripts=['gssapi-console.py'],
    description='An interactive tool for testing Python GSSAPI programs',
    long_description=open('README.md').read(),
    license='LICENSE.txt',
    url="https://github.com/pythongssapi/python-gssapi",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Security',
    ],
    keywords=['gssapi', 'security'],
    entry_points={
        'gssapi_console.drivers': [
            'krb5 = gssapi_console.drivers:Krb5Console',
        ],
        'yalpt.env_drivers': [
            'gssapi = gssapi_console.yalpt_driver:GSSAPIYalptDriver',
        ],
    },
    install_requires=[
        'gssapi',
        'k5test',
        'six'
    ]
)
