import requests as r
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import pika
import os

app = Flask(__name__)

@app.route("/send_message/<bot_chatID>", methods=['POST'])
def telegram_bot_sendtext(bot_chatID):
    
    bot_token = '1129690128:AAFzGAL-Rur8QAZyjG2_62f5tvQvOKjv29w'
    # bot_chatID = '-1001260714304'
    bot_message = "TESTING EH"
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = r.get(send_text)

    return response.json()

# Set environment variables ; will be stored in .env file
os.environ['BROKER_HOSTNAME'] = 'localhost'
os.environ['BROKER_PORT'] = '5672'
os.environ['DH_URI'] = 'http://esdwatchdog.com:5000'


# Extract values from environment variables
broker_hostname = os.environ.get('BROKER_HOSTNAME')
broker_port = os.environ.get('BROKER_PORT')
dh_uri = os.environ.get('DH_URI')


# Initiate connection to message broker
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=broker_hostname, port=broker_port, virtual_host='watchdog'))

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

def processReport(channel, method, properties, body):

    print("Received a request from healthcheck...")

    request = json.loads(body)
    print(request)



# if __name__ == '__main__':
#     app.run(port=5000, debug=True)

test = telegram_bot_sendtext("-393119922")
print(test)