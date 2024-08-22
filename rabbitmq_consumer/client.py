from fastapi import HTTPException
import pika
from pathlib import Path
import os
from dotenv import load_dotenv
import sys 
from sqlalchemy.orm import Session

dotenv_path = Path('.ENV')
sys.path.append(str(Path(__file__).parent.parent) + "/api")
from models.messages import Message
from db.session import session_maker

class RabbitConsumer():
    def __init__(self, queueName, callbackFunc, *args, **kwargs):
        self._queueName = queueName
        self._callback = callbackFunc

    def run(self):
        load_dotenv(dotenv_path=dotenv_path)
        print(os.getenv('RABBITMQ_VHOST'))

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
        
    def updateDevice():
        pass

