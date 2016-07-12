# Python Schema Registry Client

A Python client used to interact with [Confluent](http://confluent.io/)'s
[schema registry](https://github.com/confluentinc/schema-registry).  Supports Python 2.6 and 2.7.  This also works within a virtual env.

The API is heavily based off of the existing Java API of [Confluent schema registry](https://github.com/confluentinc/schema-registry).

# Installation

Run `python setup.py install` from the source root.

This library will be available via `pip` in the future.

# Example Usage


```python


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


```

# Running Tests

```
pip install unittest2
unit2 discover -s test
```

Tests use unittest2 due to unittest being different between 2.6 and 2.7.

# License

The project is licensed under the Apache 2 license.
