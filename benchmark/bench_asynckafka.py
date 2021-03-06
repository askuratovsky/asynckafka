import asyncio

from asynckafka import Producer, Consumer

import config
import utils

loop = asyncio.get_event_loop()


async def fill_topic_with_messages():
    producer = Producer(
        brokers=config.KAFKA_URL,
        rdk_producer_config=config.RDK_PRODUCER_CONFIG,
        rdk_topic_config=config.RDK_TOPIC_CONFIG,
    )
    producer.start()

    messages_consumed = 0

    print(f"Preparing benchmark. Filling topic  {config.TOPIC} with "
          f"{config.MESSAGE_NUMBER} messages of {config.MESSAGE_BYTES} bytes "
          f"each one.")
    await asyncio.sleep(0.1)

    with utils.Timer() as timer:
        for _ in range(config.MESSAGE_NUMBER):
            messages_consumed += 1
            await producer.produce(config.TOPIC, config.MESSAGE)
        producer.stop()
    print(f"The producer time to send the messages is {timer.interval} "
          f"seconds.")
    utils.print_statistics(timer.interval)


async def consume_the_messages_stream_consumer():
    stream_consumer = Consumer(
        brokers=config.KAFKA_URL,
        topics=[config.TOPIC],
        rdk_consumer_config=config.RDK_CONSUMER_CONFIG,
        rdk_topic_config=config.RDK_TOPIC_CONFIG
    )
    stream_consumer.start()

    messages_consumed = 0

    print("Starting to consume the messages.")
    with utils.Timer() as timer:
        async for message in stream_consumer:
            messages_consumed += 1
            if messages_consumed == config.MESSAGE_NUMBER:
                stream_consumer.stop()
    print(f"The time used to consume the messages is {timer.interval} "
          f"seconds.")
    utils.print_statistics(timer.interval)


async def main_coro():
    await fill_topic_with_messages()
    await consume_the_messages_stream_consumer()


if __name__ == "__main__":
    loop.run_until_complete(main_coro())
