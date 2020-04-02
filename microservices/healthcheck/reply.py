import json
import pika
import os
import requests as r


# Set environment variables ; will be stored in .env file

# Extract values from environment variables
broker_hostname = os.environ.get('BROKER_HOSTNAME')
broker_port = os.environ.get('BROKER_PORT')
dh_uri = os.environ.get('DH_URI')


# Initiate connection to message broker
connection = pika.BlockingConnection(pika.ConnectionParameters(host=broker_hostname, port=broker_port, heartbeat=0, virtual_host='watchdog', credentials=pika.PlainCredentials('admin', 'password')))

try:
    channel = connection.channel()
except Exception as e:
    print("An error occured when establishing connection to message broker")
    raise e

# Set up exchange name if doesn't exist
exchange_name = "healthcheck_direct"
channel.exchange_declare(exchange=exchange_name, exchange_type='direct')


def receiveReport():

    # Set up queue for receiving messages
    queue_name = 'ping.reply'
    channelqueue = channel.queue_declare(queue=queue_name, durable=True)
    channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=queue_name)

    # Set up queue for sending messages to notification
    notify_queue = channel.queue_declare(queue='notifications', durable=True)
    channel.queue_bind(exchange=exchange_name, queue='notifications', routing_key='healthcheck.notify')

    # Configure queue and begin event loop for consuming messages
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue_name, on_message_callback=processReport)
    channel.start_consuming()


def processReport(channel, method, properties, body):

    print("Received a report from ping service...")

    report = json.loads(body)['endpoints']

    # print(report)

    alerts = []

    # Load previous report and cross check
    with open('./current_status.txt', 'r') as json_file:
        previous_report = json.load(json_file)

    for report_row in report:
        endpoint = report_row['endpoint']
        # Check if previous report was different from new report
        if previous_report[endpoint] != 'null' and previous_report[endpoint] != report_row['status']:
            alerts.append(report_row)

    # Get contact points for changed endpoints
    if alerts:
        get_contact_route = '/endpoint/contact/get'
        endpoint_index = dict()
        for row in alerts:
            endpoint_index[row['endpoint']] = row
        print("Retrieving contacts from database...")
        response = r.get(f"{dh_uri}{get_contact_route}", json={'endpoint': list(endpoint_index.keys())})

        try:
            response.raise_for_status()
        except Exception as e:
            print("Error occured when adding retrieving contacts")
            raise e

        # response = {
        #     "endpoint": <>,
        #     "chat_id": []
        # }

        notification = []
        for contact_row in response['result']:
            notification.append({'endpoint': contact_row['endpoint'], 'timestamp': endpoint_index[contact_row['endpoint']]['timestamp'], 'status': endpoint_index[contact_row['endpoint']]['status'], 'chat_id': contact_row['chat_id']})

        # Inform user 
        print("Sending alerts to notification service...")
        channel.basic_publish(exchange=exchange_name, routing_key='healthcheck.notify', body=json.dumps({"events": notification}, default=str),
                            properties=pika.BasicProperties(
                                delivery_mode=2,
                                content_type='application/json'
                            ))

        # Add endpoint events
        add_event_route = '/endpoint/event/new'
        print("Sending new events information...")
        response = r.post(f"{dh_uri}{add_event_route}", json={'events': alerts})

        try:
            response.raise_for_status()
        except Exception as e:
            print("Error occured when adding new events")
            raise e

        # print(response.json())

    # Send request to notification endpoint

    # {
    #     "events" : [
    #         {'endpoint': <>,
    #         'status': <>,
    #         'timestamp': <>}
    #     ]
    # }

    # print(report)

    # Update endpoint status
    update_status_route = '/endpoint/status'
    print("Updating endpoint status in database...")
    response = r.patch(f"{dh_uri}{update_status_route}", json={'report': report})

    try:
        response.raise_for_status()
    except Exception as e:
        print("Error occured when updating endpoint status")
        raise e

    print("Report processing complete!")
    channel.basic_ack(delivery_tag=method.delivery_tag)



if __name__ == '__main__':
    print('Listening for reports...')
    receiveReport()