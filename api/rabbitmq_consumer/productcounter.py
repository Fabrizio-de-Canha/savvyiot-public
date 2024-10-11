from models import Message, Device
from .client import RabbitConsumer, dbClient, UpdateDeviceException, InsertMessageException
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
            deliveryTag = method.delivery_tag
            jsonBody = json.loads(body)

            if(routing_key.split(".")[3].lower() == 'data'): 
                message_timestamp = jsonBody["timestamp"]
                rssi = jsonBody['rssi']
                succeeded = False
                for i in jsonBody['data']:
                    message: Message = Message(
                        timestamp = datetime.fromtimestamp(i['timestamp'], tz=timezone.utc),
                        value = i['value'],
                        value_type = i['type'],
                        message_timestamp=datetime.fromtimestamp(message_timestamp, tz=timezone.utc), 
                        tenant= tenantId, 
                        device_mac = deviceMac
                        )
                    
                    succeeded: bool = sqlClient.addMessage(message=message)

                if succeeded:
                    #Ack message
                    device: Device = Device(
                        mac_id = deviceMac,
                        tenant = tenantId,
                        rssi = rssi,
                        last_reported = datetime.fromtimestamp(jsonBody['timestamp'], tz=timezone.utc)
                    )

                    if(sqlClient.updateDevice(device=device)):
                        ch.basic_ack(delivery_tag=deliveryTag)
                    else:
                        raise UpdateDeviceException(f'failed to update device table for {tenantId}/{deviceMac}')
                else:
                    #requeue
                    raise InsertMessageException(f'failed to insert message from device {tenantId}/{deviceMac}')

                print(deliveryTag)
            elif (routing_key.split(".")[3].lower() == 'status'):
                rssi = jsonBody['rssi']

                device: Device = Device(
                     mac_id = deviceMac,
                     tenant = tenantId,
                     rssi = rssi,
                     last_reported = datetime.fromtimestamp(jsonBody['timestamp'], tz=timezone.utc),
                     firmware_version = jsonBody['firmware_version']
                )

                succeeded: bool = sqlClient.updateDevice(device=device)

                if succeeded:
                     ch.basic_ack(delivery_tag=deliveryTag)
                else:
                    raise UpdateDeviceException(f'failed to update device table for {tenantId}/{deviceMac}')
            elif(routing_key.split(".")[3].lower() == 'startup'):
                rssi = jsonBody['rssi']

                print(f'{deviceMac} booted')

                device: Device = Device(
                     mac_id = deviceMac,
                     tenant = tenantId,
                     rssi = rssi,
                     last_reported = datetime.fromtimestamp(jsonBody['timestamp'], tz=timezone.utc),
                     last_booted = datetime.fromtimestamp(jsonBody['timestamp'], tz=timezone.utc),
                     firmware_version = jsonBody['firmware_version']
                )

                succeeded: bool = sqlClient.updateDevice(device=device)

                if succeeded:
                     ch.basic_ack(delivery_tag=deliveryTag)
                else:
                    raise UpdateDeviceException(f'failed to update device table for {tenantId}/{deviceMac}')
            else :
                ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as e:
            print('failed to process message')
            print(e)

            ch.basic_publish(
                exchange='',
                body=body,
                routing_key='dev-requeue',
            )

            ch.basic_ack(delivery_tag=method.delivery_tag)
              

consumer = RabbitConsumer(queueName="dev", callbackFunc=callback_func)

# sqlClient.addMessage(message=message)
consumer.run()