import redis.asyncio as redis
import asyncio

REDIS_URL = "redis://redis:6379"
pubsub_instances = {}  # canal -> tarea

async def subscribe_to_channel(channel: str, callback):
    if channel in pubsub_instances:
        return  # ya hay listener

    client = redis.from_url(REDIS_URL)
    pubsub = client.pubsub()
    await pubsub.subscribe(channel)
    
    p

    async def reader():
        async for message in pubsub.listen():
            if message["type"] == "message":
                data = message["data"].decode()
                await callback(data)

    task = asyncio.create_task(reader())
    pubsub_instances[channel] = task  # para evitar doble listener

async def publish_to_channel(channel: str, message: str):
    client = redis.from_url(REDIS_URL)
    await client.publish(channel, message)


# async def unsubscribe_from_channel(channel: str):
#     instance = pubsub_instances.get(channel)
#     if instance:
#         task = instance["task"]
#         pubsub = instance["pubsub"]

#         task.cancel()
#         try:
#             await task
#         except asyncio.CancelledError:
#             pass

#         await pubsub.unsubscribe(channel)
#         await pubsub.close()

#         del pubsub_instances[channel]