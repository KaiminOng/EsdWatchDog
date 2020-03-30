
#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import json
import sys
import os
import random

# Communication patterns:
# Use a message-broker with 'direct' exchange to enable interaction
# Use a reply-to queue and correlation_id to get a corresponding reply
import pika
# If see errors like "ModuleNotFoundError: No module named 'pika'", need to
# make sure the 'pip' version used to install 'pika' matches the python version used.
import uuid
import csv

def create_healthcheck(healthcheck_input):
    """send list of end points according to healthcheck requirements"""
    # assume status==200 indicates success
    status = 200
    message = "Success"

    # Load the healthcheck info (from a file in this case; can use DB too, or receive from HTTP requests)
    try:
        with open(healthcheck_input) as sample_healthcheck_file:
            this_healthcheck = json.load(sample_healthcheck_file)
    except Exception as e:
        status = 501
        raise e
        message = "An error occurred in loading the healthcheck."
    finally:
        sample_healthcheck_file.close()
    if status!=200:
        print("Failed healthcheck request.")
        return {'status': status, 'message': message}

    # Create a new healthcheck: set up data fields in the healthcheck as a JSON object (i.e., a python dictionary)
    healthcheck = dict()
    healthcheck["chat_id"] = this_healthcheck['chat_id']
    healthcheck["urls"] = this_healthcheck['urls']

    # Return the newly created healthcheck when creation is succssful
    if status==200:
        print("OK healthcheck creation.")
        return healthcheck

def send_healthcheck(healthcheck):
    """Send request to quick check"""
    # default username / password to the borker are both 'guest'
    hostname = "localhost" # default broker hostname. Web management interface default at http://localhost:15672
    port = 5672 # default messaging port.
    # connect to the broker and set up a communication channel in the connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port))
        # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
        # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
    channel = connection.channel()

    # set up the exchange if the exchange doesn't exist
    exchangename="healthcheck_direct"
    channel.exchange_declare(exchange=exchangename, exchange_type='direct')

    # prepare the message body content
    message = json.dumps(healthcheck, default=str) # convert a JSON object to a string

    # send the message
    # always inform Monitoring for logging no matter if successful or not
    channel.basic_publish(exchange=exchangename, routing_key="healthcheck.info", body=message)
        # By default, the message is "transient" within the broker;
        #  i.e., if the monitoring is offline or the broker cannot match the routing key for the message, the message is lost.
        # If need durability of a message, need to declare the queue in the sender (see sample code below).

    if "status" in healthcheck: # if some error happened in order creation
        # inform Error handler
        channel.queue_declare(queue='errorhandler', durable=True) # make sure the queue used by the error handler exist and durable
        channel.queue_bind(exchange=exchangename, queue='errorhandler', routing_key='healthcheck.error') # make sure the queue is bound to the exchange
        channel.basic_publish(exchange=exchangename, routing_key="healthcheck.error", body=message,
            properties=pika.BasicProperties(delivery_mode = 2) # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange)
        )
        # print("Order status ({:d}) sent to error handler.".format(order["status"]))
    else: 
        # inform Shipping and exit, leaving it to order_reply to handle replies
        # Prepare the correlation id and reply_to queue and do some record keeping
        # corrid = str(uuid.uuid4())
        # row = {"order_id": order["order_id"], "correlation_id": corrid}
        # csvheaders = ["order_id", "correlation_id", "status"]
        # with open("corrids.csv", "a+", newline='') as corrid_file: # 'with' statement in python auto-closes the file when the block of code finishes, even if some exception happens in the middle
        #     csvwriter = csv.DictWriter(corrid_file, csvheaders)
        #     csvwriter.writerow(row)
        replyqueuename = "ping.reply"
        # prepare the channel and send a message to Shipping
        channel.queue_declare(queue='ping', durable=True) # make sure the queue used by Shipping exist and durable
        channel.queue_bind(exchange=exchangename, queue='ping', routing_key='ping.healthcheck') # make sure the queue is bound to the exchange
        channel.basic_publish(exchange=exchangename, routing_key="ping.healthcheck", body=message,
            properties=pika.BasicProperties(delivery_mode = 2, # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange, which are ensured by the previous two api calls)
                reply_to=replyqueuename, # set the reply queue which will be used as the routing key for reply messages
                # correlation_id=corrid # set the correlation id for easier matching of replies
            )
        )
        print("Healthcheck request sent to ping.")
    # close the connection to the broker
    connection.close()

# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is " + os.path.basename(__file__) + ": checking your health...")
    healthcheck = create_healthcheck("sample_healthcheck.txt")
    send_healthcheck(healthcheck)
