import logging

from .schemaregistry.client import CachedSchemaRegistryClient
from confluent_kafka.avro.serializer import SerializerError
from .schemaregistry.serializers import MessageSerializer

log = logging.getLogger(__name__)
class AvroProducer(object):
    '''
        Kafka Producer client which does avro schema encoding to messages.
        Handles schema registration, Message serialization.

        Constructor takes below parameters

        @:param: producer: confluent_kafka.Producer object
        @:param: message_serializer: Message Serializer object
    '''
    def __init__(self, producer, schema_registry_url, key_schema = None, value_schema = None):  # real signature unknown; restored from __doc__
        self._producer = producer
        _cash_client= CachedSchemaRegistryClient(url=schema_registry_url)
        self._serializer =  MessageSerializer(_cash_client)
        self.key_schema = key_schema
        self.value_schema = value_schema

    def produce(self, topic, value=None, key=None, *args, **kwargs):
        '''
            Sends message to kafka by encoding with specified avro schema
            @:param: topic: topic name
            @:param: value: A dictionary object
            @:param: value_schema : Avro schema for value
            @:param: key: A dictionary object
            @:param: key_schema : Avro schema for key
            @:exception: SerializerError
        '''
        # get schemas from  kwargs if defined
        key_schema = kwargs.pop('key_schema', None)
        value_schema = kwargs.pop('value_schema', None)

        # if key_schema is not initialized, fall back on default key_schema passed as construction param.
        if key_schema is None:
            key_schema=self.key_schema

        # if value_schema is not initialized, fall back on default value_schema passed as construction param.
        if value_schema is None:
            value_schema=self.value_schema

        if value is not None:
            if value_schema is not None:
                value = self._serializer.encode_record_with_schema(topic, value_schema, value)
            else:
                log.error("Schema required for value serialization")
                raise SerializerError("Avro schema required for value")

        if key is not None:
            if key_schema is not None:
                key = self._serializer.encode_record_with_schema(topic, key_schema, key, True)
            else:
                log.error("Schema required for key serialization")
                raise SerializerError("Avro schema required for key")

        self._producer.produce(topic, value, key, *args, **kwargs)

    def poll(self, timeout):
        self._producer.poll(timeout)

    def flush(self, *args, **kwargs):
        self._producer.flush(*args, **kwargs)