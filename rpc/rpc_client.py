#!/usr/bin/env python
import pika
import uuid


class RpcClient(object):

    def __init__(self):

        credentials = pika.PlainCredentials(
            username='guest',
            password='guest'
        )
        parameters = pika.ConnectionParameters(
            host='107.178.209.84',
            port=5672,
            credentials=credentials
        )
        self.connection = pika.BlockingConnection(parameters)

        self.channel = self.connection.channel()

        result = self.channel.queue_declare('', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, queue_prefix):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_prefix + '_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(queue_prefix)
        )

        while self.response is None:
            self.connection.process_data_events()

        return self.response
