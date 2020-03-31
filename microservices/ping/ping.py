
#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import aiohttp
import asyncio
import time

# Using AMPQ
import json
import sys
import os
import random

# Communication patterns:
# Use a message-broker with 'direct' exchange to enable interaction
import pika

hostname = "localhost" # default hostname
port = 5672 # default port`

# connect to the broker and set up a communication channel in the connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port, virtual_host='watchdog'))
    # Note: various network firewalls, filters, gateways (e.g., SMU VPN on wifi), may hinder the connections;
    # If "pika.exceptions.AMQPConnectionError" happens, may try again after disconnecting the wifi and/or disabling firewalls
channel = connection.channel()
# set up the exchange if the exchange doesn't exist
exchangename="healthcheck_direct"
channel.exchange_declare(exchange=exchangename, exchange_type='direct')

async def main(urls):
    # {
    #     "endpoints" : [
    #         {
    #             "endpoint" : "http://yahoo.com",
    #             "status" : "healthy",
    #             "timestamp" : <>
    #         }
    #     ]
    # }
    results = []
    '''ClientSession is the heart and the main entry point for all client API operations.
    The session contains a cookie storage and connection pool, 
    thus cookies and connections are shared between HTTP requests sent by the same session.
    '''
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5), raise_for_status=True) as session:
        for url in urls:
            info = {}
            info["endpoint"] = str(url)
            # Able to connect to url
            try:
                async with session.get(url) as resp:
                    # If no error status code
                    if not resp.status >= 400:
                        # results.append(True)
                        info["status"] = "healthy"
            # Unable to connect to url
            except Exception as e:
                # results.append(False)
                print(type(e))
                info["status"] = "unhealthy"
            
            #add timestamp
            info["timestamp"] = int(time.time())

            results.append(info)
        return results

def receiveHealthcheck():
    # prepare a queue for receiving messages
    channelqueue = channel.queue_declare(queue="ping", durable=True) # 'durable' makes the queue survive broker restarts so that the messages in it survive broker restarts too
    queue_name = channelqueue.method.queue
    channel.queue_bind(exchange=exchangename, queue=queue_name, routing_key='ping.healthcheck') # bind the queue to the exchange via the key

    # set up a consumer and start to wait for coming messages
    channel.basic_qos(prefetch_count=1) # The "Quality of Service" setting makes the broker distribute only one message to a consumer if the consumer is available (i.e., having finished processing and acknowledged all previous messages that it receives)
    channel.basic_consume(queue=queue_name, on_message_callback=callback)
    channel.start_consuming() # an implicit loop waiting to receive messages; it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("Received a request by " + __file__)
    result = processRequest(json.loads(body))
    
    # json.dump(result, sys.stdout, default=str) # convert the JSON object to a string and print out on screen
    print('\n\n') # print a new line feed to the previous json dump

    # prepare the reply message and send it out
    replymessage = json.dumps(result, default=str) # convert the JSON object to a string
    replyqueuename=properties.reply_to
    # A general note about AMQP queues: If a queue or an exchange doesn't exist before a message is sent,
    # - the broker by default silently drops the message;
    # - So, if really need a 'durable' message that can survive broker restarts, need to
    #  + declare the exchange before sending a message, and
    #  + declare the 'durable' queue and bind it to the exchange before sending a message, and
    #  + send the message with a persistent mode (delivery_mode=2).
    channel.queue_declare(queue=properties.reply_to, durable=True) # make sure the queue used for "reply_to" is durable for reply messages
    channel.queue_bind(exchange=exchangename, queue=replyqueuename, routing_key=replyqueuename) # make sure the reply_to queue is bound to the exchange
    # send msg
    channel.basic_publish(exchange=exchangename,
            routing_key=replyqueuename, # use the reply queue set in the request message as the routing key for reply messages
            body=replymessage, 
            properties=pika.BasicProperties(delivery_mode = 2, # make message persistent (stored to disk, not just memory) within the matching queues; default is 1 (only store in memory)
                # correlation_id = properties.correlation_id, # use the correlation id set in the request message
                content_type='application/json'
            )
    )
    print('Response sent to reply queue!')
    channel.basic_ack(delivery_tag=method.delivery_tag) # acknowledge to the broker that the processing of the request message is completed

def processRequest(healthcheck):
    print("Processing ping request...")
    urls = healthcheck['urls']

    s = time.perf_counter()
    ping_results = asyncio.run(main(urls))
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
    
    processed_result = {'endpoints': ping_results}
    return processed_result

def send_error(resultmessage):
    # send the message to the eror handler
    channel.queue_declare(queue='errorhandler', durable=True) # make sure the queue used by the error handler exist and durable
    channel.queue_bind(exchange=exchangename, queue='errorhandler', routing_key='healthcheck.error') # make sure the queue is bound to the exchange
    channel.basic_publish(exchange=exchangename, routing_key="healthcheck.error", body=resultmessage,
        properties=pika.BasicProperties(delivery_mode = 2) # make message persistent within the matching queues until it is received by some receiver (the matching queues have to exist and be durable and bound to the exchange)
    )

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("This is " + os.path.basename(__file__) + ": Listening for healthcheck request...")
    receiveHealthcheck()