# Setup
try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

import eventlib

install_requires = []

version = '.'.join([str(eventlib.__version__[i]) for i in range(3)])

from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements("requirements.txt", session=False)

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(ir.req) for ir in install_reqs]

setup(
    name = 'eventlib',
    version = version,
    packages = ['eventlib',
                'eventlib.schemaregistry'],
    install_requires = reqs,

    # metadata for upload to PyPI
    author = 'Data Reply',
    description = 'Asyncio Kafka Event library',
    keywords = 'asyncio kafka event',
    extras_require = {
        'fastavro': ['fastavro'],
        'confluent-kafka':['confluent-kafka']
    },
    test_requires = ['unittest2']
)
