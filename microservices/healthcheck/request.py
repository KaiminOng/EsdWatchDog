from flask import Flask, make_response, request, jsonify
import requests as r
import json
import pika
import os


# Extract values from environment variables
broker_hostname = os.environ.get('BROKER_HOSTNAME')
broker_port = os.environ.get('BROKER_PORT')
dh_uri = os.environ.get('DH_URI')

# Start flask app instance
app = Flask(__name__)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=broker_hostname, port=broker_port, heartbeat=0, virtual_host='watchdog', credentials=pika.PlainCredentials('admin', 'password')))

try:
    channel = connection.channel()
except Exception as e:
    print("An error occured when establishing connection to message broker")
    # raise e

# Set up exchange name if doesn't exist
exchange_name = "healthcheck_direct"
channel.exchange_declare(exchange=exchange_name, exchange_type='direct')


@app.route('/', methods=['GET', 'POST'])
def trigger_routine():

    # Query data handler for endpoints to check
    api_route = '/endpoint/dump'

    response = r.get(f"{dh_uri}{api_route}", timeout=5.0)

    try:
        response.raise_for_status()
    except Exception as e:
        print("Error occured when contacting data handler service")
        # raise e

    # Parse response
    endpoint_health = response.json().get('result', {})

    # Dump the status list locally
    with open('./current_status.txt', 'w') as o:
        json.dump(endpoint_health, o)

    request_message = json.dumps(
        {'urls': list(endpoint_health.keys())}, default=str)

    # {
    #     "endpoints" : [
    #         {
    #             "endpoint" : "http://yahoo.com",
    #             "status" : "healthy",
    #             "timestamp" : <>
    #         }
    #     ]
    # }


    # Declare and setup exchange queue
    request_queue_name = 'ping'
    request_routing_key = 'ping.healthcheck'
    reply_queue_name = 'ping.reply'

    channel.queue_declare(queue=request_queue_name, durable=True)
    channel.queue_bind(exchange=exchange_name,
                       queue=request_queue_name, routing_key=request_routing_key)
    channel.basic_publish(exchange=exchange_name, routing_key=request_routing_key, body=request_message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,
                              content_type='application/json',
                              reply_to=reply_queue_name)
                          )

    print("Request sent to ping service!")
    return make_response(jsonify({'status': 'success'}), 200)



if __name__ == '__main__':
    print("Listening for scheduled triggers...")
    app.run(host='0.0.0.0', port=5002)
