import sys 
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent) + "/api")
from models.user import User 
from models.messages import Message 

from client import RabbitConsumer, dbClient
from pika.spec import Basic, BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
from datetime import datetime, timezone
import json

sqlClient = dbClient()

def callback_func(
                ch: BlockingChannel,
                method: Basic.Deliver,
                properties: BasicProperties,
                body: str):
        routing_key: str = method.routing_key
        try:
            tenantId = routing_key.split(".")[0]
            deviceMac = routing_key.split(".")[2]
            jsonBody = json.loads(body)
            timestamp = jsonBody["timestamp"]
            message: Message = Message(message=jsonBody,timestamp=datetime.fromtimestamp(timestamp, tz=timezone.utc), tenant= tenantId, device_mac = deviceMac)
            succeeded: bool = sqlClient.addMessage(message=message)
            deliveryTag = method.delivery_tag
            if succeeded:
                #Ack message
                ch.basic_ack(delivery_tag=deliveryTag)
            else:
                #requeue
                ch.basic_nack(delivery_tag=deliveryTag)

            print(deliveryTag)
        except Exception as e:
            print(e)
              

consumer = RabbitConsumer(queueName="dev", callbackFunc=callback_func)

# sqlClient.addMessage(message=message)
consumer.run()