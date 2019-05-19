import os
import sys

from setuptools import setup, find_packages

if sys.version_info < (3, 5, 3):
    sys.exit('Python 3.5.3 is the minimum required version')

PROJECT_ROOT = os.path.dirname(__file__)

long_description = ""

with open(os.path.join(PROJECT_ROOT, 'README.rst')) as file_:
    long_description = file_.read()

INSTALL_REQUIRES = [
    'async_timeout==3.0.1',
    'aiohttp==3.5.4'
]

TEST_REQUIRES = INSTALL_REQUIRES + [
    'pytest',
    'pytest-asyncio',
],

# This means you can do pip install .[test] for testing deps.
extras = {
    "test": TEST_REQUIRES,
}

setup(
    name='ufaas_dockerapi',
    version="0.1.0",
    python_requires='>=3.5.3',
    description="An async Docker API client designed to meet the requirements \
of uFaaS.",
    long_description=long_description,
    url='https://gitlab.com/DDevine/ufaas-dockerapi/',
    author='Daniel Devine',
    author_email='devine@ddevnet.net',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=INSTALL_REQUIRES,
    tests_require=TEST_REQUIRES,
    extras_require=extras,
)
