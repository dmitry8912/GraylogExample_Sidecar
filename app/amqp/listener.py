import asyncio
import json
import uuid
from typing import Any, Tuple

import aio_pika

from app.amqp.base import RabbitMqHandlerBase
from app.config import app_config
from app.context import request_id
from app.logging.graylog import logger


class ServiceListener(RabbitMqHandlerBase):
    __instance_listen_queue = 'service_1'

    @classmethod
    async def listen(cls):
        def response_parser(message: aio_pika.Message) -> Tuple[Any, bool]:
            response = json.loads(message.body.decode('utf-8'))
            request_id.set(response['request_id'])
            return response, False

        async for response in cls.basic_receive(cls.__instance_listen_queue,
                                         parser_callback=response_parser,
                                         exclusive_queue=True):
            logger.debug('New request')
            response['result'] = 200
            logger.debug('Processing success')
            await cls.basic_send(request_id.get(), json.dumps(response).encode('utf-8'))
