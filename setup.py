#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    "PyMySQL"
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='dedupe',
    version='0.1.0',
    description="Actio corporation's deduping algorithm",
    author="Nik Liolios",
    author_email='nliolios@exeter.edu',
    url='https://github.com/nliolios24/dedupe',
    packages=[
        'dedupe',
    ],
    package_dir={
        'dedupe': 'src',
    },
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='dedupe',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
