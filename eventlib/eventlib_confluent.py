# # -*- coding: utf-8 -*-
# import asyncio
# import json
# from datetime import datetime
#
# # import os
# import uuid
# from eventlib.schemaregistry.client import CachedSchemaRegistryClient
# from eventlib.schemaregistry.serializers import MessageSerializer
# from confluent_kafka import Producer,Consumer,KafkaException
# import os
# __all__ = ["consume_events",
#            "stop_consuming_events",
#            "send_event", "start_producer",
#            "stop_producer"]
#
# consumer_running = None
# kafka_client = None
# registry_client = None
# registry_serializer = None
# consumers = {}
# producers = {}
# schema ={}
#
# # from confluent_kafka import Producer
# #
# # p = Producer({'bootstrap.servers': 'mybroker,mybroker2'})
# # for data in some_data_source:
# #     p.produce('mytopic', data.encode('utf-8'))
# # p.flush()
# #
#
#
# def create_registry_client(registry=None):
#     """
#     Internal function to create the client lazily
#     while caching it to avoid new connections.
#     """
#     global registry_client
#     global registry_serializer
#     if not registry_client:
#         if not registry:
#             registry = os.environ.get('SCHEMA_REGISTRY', '127.0.0.1')
#         registry_client = CachedSchemaRegistryClient(url='http://localhost:8081')
#         registry_serializer = MessageSerializer(registry_client)
#     return registry_client,registry_serializer
#
# async def consume_events(topic,brokers,callback,default_topic_config= {'auto.offset.reset': 'smallest'},group="eventlib-group",schema=None,registry=None,delay=0.01,**kwargs):
#     """
#     Connect to the Kafka endpoint and start consuming
#     messages from the given `topic`.
#     The given callback is applied on each
#     message.
#     """
#     if topic in consumers:
#         raise RuntimeError("A consumer already exists for topic: %s" % topic)
#
#     if (not registry_serializer or not registry_client) and registry:
#         r_client,serializer = create_registry_client(registry)
#
#     conf = {'bootstrap.servers': brokers,
#          'group.id': group,
#          'default.topic.config':default_topic_config }
#
#     consumer = Consumer( **conf,**kwargs)
#     consumers[topic] = consumer
#
#     try:
#         while True:
#             message = consumer.poll(1)
#             if message is not None:
#                 if registry:
#                     message = serializer.decode_message(message.value)
#                 else:
#                     message =message.value
#
#                 await callback(message)
#             else:
#                 await asyncio.sleep(delay)
#     except KafkaException:
#         pass
#     else:
#         consumer.close()
#     finally:
#         consumers.pop(topic, None)
#
#
# async def stop_consuming_events(topic):
#     """
#     Notify the consumer's flag that it is
#     not running any longer.
#     The consumer will properly terminate at its
#     next iteration.
#     """
#     if topic and topic in consumers:
#         consumer = consumers[topic]
#         consumer.stop()
#         while topic in consumers:
#             await asyncio.sleep(0.5)
#
#
# async def start_producer(topic, brokers,registry=None):
#     """
#     Start an event producer in the background.
#     """
#     topic_name = brokers
#     topic = client(brokers).topics[topic]
#     producers[topic_name] = topic.get_producer()
#
#     if registry!=None:
#        _ = registry_client(registry)
#
#
# async def stop_producer(topic):
#     """
#     Stop the producer associated to the
#     given topic.
#     """
#     if topic in producers:
#         producer = producers.get(topic, None)
#         producer.stop()
#
#
# async def send_event(topic, event,schema=None):
#     """
#     Push event to the given topic. If no
#     producer exists for this topic, a :exc:`RuntimeError`
#     is raised.
#     """
#     if topic not in producers:
#         raise RuntimeError("No event senders initialized for '%s'" % topic)
#
#     if (not registry_serializer or not registry_client) and schema:
#         raise RuntimeError("No Schema Registry Client initialized")
#
#     if isinstance(event, dict):
#         if schema:
#             event = registry_serializer.encode_record_with_schema(topic,schema,event)
#         else:
#             event = json.dumps(event).encode('utf-8')
#
#     producer = producers[topic]
#     producer.produce(event)
#
