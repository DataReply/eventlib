# Setup
try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

import eventlib

install_requires = []

version = '.'.join([str(eventlib.__version__[i]) for i in range(3)])

setup(
    name = 'eventlib',
    version = version,
    packages = ['eventlib',
                'eventlib.schemaregistry'],
    install_requires = [
        "pykafka",
        "avro-python3"

    ],

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
