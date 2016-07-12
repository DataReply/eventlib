# from confluent_kafka import Consumer
# running = True
# c = Consumer({'bootstrap.servers': 'localhost:9092', 'group.id': 'mygroup'})
# c.subscribe(['test'])
# while running:
#     msg = c.poll()
#     if not msg.error():
#         print('Received message: %s' % msg.value())
# c.close()

from eventlib import consume_events,stop_consuming_events,start_producer,send_event
import asyncio


async def consume_test( payload):
    print (payload)

import asyncio

@asyncio.coroutine
def chain(obj, *funcs):
    for f, *args in funcs:
        meth = getattr(obj, f)  # Look up the method on the object
        obj = yield from meth(*args)
    return obj


start_producer(topic=b"test",brokers="localhost:9092")





asyncio.ensure_future(consume_events(b"test",b"test-group","localhost:9092",consume_test))

for i in range(10):
    asyncio.ensure_future(send_event(b"test",{"test":"test"}))

asyncio.get_event_loop().run_forever()