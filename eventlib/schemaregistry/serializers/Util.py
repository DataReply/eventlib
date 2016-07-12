"""
Basic utilities for handling avro schemas
"""
from avro import schema


def hash_func(self):
    """ Monkey patching the avro library's schema module's RecordSchema class.
    
    Patching the https://github.com/apache/avro/blob/trunk/lang/py3/avro/schema.py as the RecordSchema doesn't have a __hash__ function, but it has an __eq__ function, which means that instances
    of RecordSchema are not hashable, so they cannot be added to dicts or sets, see bug I raised at https://issues.apache.org/jira/browse/AVRO-1737
    Hopefully this function later will get added as __hash__ method to the RecordSchema class in the avro.schema module and this monkey patching won't be required anymore
    """
    return hash(str(self))

schema.RecordSchema.__hash__ = hash_func


def parse_schema_from_string(schema_str):
    """Parse a schema given a schema string"""
    return schema.Parse(schema_str)

def parse_schema_from_file(schema_path):
    """Parse a schema from a file path"""
    with open(schema_path) as f:
        return parse_schema_from_string(f.read())
