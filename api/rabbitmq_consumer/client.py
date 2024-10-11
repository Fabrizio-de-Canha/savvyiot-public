import pika
from pathlib import Path
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from models.messages import Message
from models.devices import Device
from db.session import session_maker

class RabbitConsumer():
    def __init__(self, queueName, callbackFunc, *args, **kwargs):
        self._queueName = queueName
        self._callback = callbackFunc

    def run(self):

        credentials = pika.PlainCredentials(os.getenv('RABBITMQ_USERNAME'), os.getenv('RABBITMQ_PASSWORD'))
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST'),
                                      credentials=credentials,
                                      virtual_host=os.getenv('RABBITMQ_VHOST')))

        channel = connection.channel()
        print(channel.connection)

        channel.basic_consume(on_message_callback=self._callback,
                              queue=self._queueName,
                              auto_ack=False)

        channel.start_consuming()       


class dbClient:
    def __init__(self):
        self.session: Session =  session_maker() 

    def addMessage(self, message: Message):
        try:
            self.session.add(message)
            # Update device here
            self.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
        
    def updateDevice(self, device: Device):
        try:
            if device.firmware_version:
                update_dict = dict(
                        last_reported = device.last_reported,
                        rssi = device.rssi,
                        firmware_version = device.firmware_version
                    )
            else:
                update_dict = dict(
                        last_reported = device.last_reported,
                        rssi = device.rssi
                    )
                
            if device.last_booted:
                update_dict['last_booted'] = device.last_booted

            stmt = insert(Device).values(
                    mac_id = device.mac_id, 
                    tenant =device.tenant, 
                    last_reported = device.last_reported,
                    rssi = device.rssi
                ).on_conflict_do_update(
                    index_elements=['mac_id'],  # The unique constraint or primary key to check conflicts on
                    set_= update_dict
                )
            
            self.session.execute(stmt)
            self.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
        
class UpdateDeviceException(Exception):
    """Raised when the device state could not be updated"""
    pass

class InsertMessageException(Exception):
    """Raised when the message could not be processed"""
    pass
