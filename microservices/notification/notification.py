import requests as r
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import pika
import os
from datetime import datetime

# Set environment variables ; will be stored in .env file
# os.environ['BROKER_HOSTNAME'] = 'localhost'
# os.environ['BROKER_PORT'] = '5672'
# os.environ['DH_URI'] = 'http://esdwatchdog.com:5000'


# Extract values from environment variables
broker_hostname = os.environ.get('BROKER_HOSTNAME')
broker_port = os.environ.get('BROKER_PORT')
dh_uri = os.environ.get('DH_URI')


# Initiate connection to message broker
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=broker_hostname, port=broker_port, virtual_host='watchdog', heartbeat=0, credentials=pika.PlainCredentials('admin', 'password')))

try:
    channel = connection.channel()
except Exception as e:
    print("An error occured when establishing connection to message broker")
    raise e

# Set up exchange name if doesn't exist
exchange_name = "healthcheck_direct"
channel.exchange_declare(exchange=exchange_name, exchange_type='direct')

# receive request from Healthcheck
def receiveRequest():

    # Set up queue for receiving messages
    queue_name = 'notifications'
    notificaitonqueue = channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key='healthcheck.notify')

    # Configure queue and begin event loop for consuming messages
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=processRequest)
    channel.start_consuming()

def processRequest(channel, method, properties, body):

    print("Received a request from healthcheck...")

    parsed_request = json.loads(body)

    # Send message to telegram user
    sendMessage(parsed_request)
    channel.basic_ack(delivery_tag=method.delivery_tag)


def telegram_bot_sendtext(chat_id, message):
    
    bot_token = '1129690128:AAFzGAL-Rur8QAZyjG2_62f5tvQvOKjv29w'
    # bot_chatID = '-1001260714304'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + message

    response = r.get(send_text)

    return response.json()

def sendMessage(data):
    events = data['events']
    for event in events:
        endpoint = event['endpoint']
        chat_ids = event['chat_id']
        timestamp = event['timestamp']
        dt = datetime.fromtimestamp(timestamp)          # dt = 2018-12-25 09:27:53 (format)
        status = event['status']
        if status == 'unhealthy':
            message = "Hey! Your endpoint <" + endpoint + "> has been DOWN since " + str(dt) + "!"
        else:
             message = "Hey! Your endpoint <" + endpoint + "> has been UP since " + str(dt) + "!"

        for chat in chat_ids:
            response = telegram_bot_sendtext(chat, message)
        print(response)



if __name__ == '__main__':
    receiveRequest()


# test = telegram_bot_sendtext("-393119922")
# print(test)