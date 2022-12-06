from app.amqp.listener import ServiceListener
import asyncio

if __name__ == '__main__':
    asyncio.run(ServiceListener.listen())
