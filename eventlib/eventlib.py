
# -*- coding: utf-8 -*-
import asyncio
from datetime import datetime
import json
# import os
import uuid
from .schemaregistry.client import CachedSchemaRegistryClient
from .schemaregistry.serializers import MessageSerializer, Util
from confluent_kafka import Producer, Consumer,KafkaException
import os

__all__ = ["consume_events",
           "stop_consuming_events",
           "send_event", "start_producer",
           "stop_producer"]

registry_client = None
registry_serializer = None
consumers = {}
producers = {}

def create_registry_client(registry=None):
    """
    Internal function to create the client lazily
    while caching it to avoid new connections.
    """
    global registry_client
    global registry_serializer
    if not registry_client:
        if not registry:
            registry = os.environ.get('SCHEMA_REGISTRY', 'http://localhost:8081')
        registry_client = CachedSchemaRegistryClient(url=registry)
        registry_serializer = MessageSerializer(registry_client)
    return registry_client,registry_serializer

async def consume_events(topic, group, brokers, callback, schema=None,registry=None,delay=0.01,**kwargs):
    """
    Connect to the Kafka endpoint and start consuming
    messages from the given `topic`.
    The given callback is applied on each
    message.
    """    
    global consumer
    if topic in consumers:
        raise RuntimeError("A consumer already exists for topic: %s" % topic)

    if (not registry_serializer or not registry_client) and registry:
        r_client,serializer = create_registry_client(registry)


    consumer = Consumer({'bootstrap.servers': brokers, 'group.id': group,
              'default.topic.config': {'auto.offset.reset': 'largest'}})
    consumer.subscribe([topic])
    consumers[topic] = consumer


    try:
        while True:
            message = consumer.poll(1)
            if message:
               if not message.error():
                   if registry:
                       message = serializer.decode_message(message.value())
                   else:
                       message = message.value()

                   await callback(message)
                   consumer.commit()
            else:
                   await asyncio.sleep(delay)
    except KafkaException as ex:
        pass
    else:
        consumer.close()
    finally:
        consumers.pop(topic, None)


async def stop_consuming_events(topic):
    """
    Notify the consumer's flag that it is
    not running any longer.
    The consumer will properly terminate at its
    next iteration.
    """
    global consumer
    if topic and topic in consumers:
        consumer = consumers[topic]
        consumer.close()
        while topic in consumers:
            await asyncio.sleep(0.5)


def start_producer(topic, brokers,registry=None):
    """
    Start an event producer in the background.
    """
    global producers
    producers[topic]  = Producer({'bootstrap.servers': brokers})

    if registry!=None:
       _ = create_registry_client(registry)


async def stop_producer():
    """
    Stop the producer associated to the
    given topic.
    """
    global producer
    producer.stop()


async def send_event(topic, event,schema=None):
    """
    Push event to the given topic. If no
    producer exists for this topic, a :exc:`RuntimeError`
    is raised.
    """
    global producers
    producer = producers[topic]
    if producer==None:
        raise RuntimeError("No event senders initialized for '%s'" % topic)

    if (not registry_serializer or not registry_client) and schema:
        raise RuntimeError("No Schema Registry Client initialized")

    if isinstance(event, dict):
        if schema:
            event = registry_serializer.encode_record_with_schema(topic,schema,event)
        else:
            event = json.dumps(event).encode('utf-8')
    #,on_delivery=lambda a,b:(a,b)
    producer.produce(topic, event)
    print("wrote")
    #producer.flush()
