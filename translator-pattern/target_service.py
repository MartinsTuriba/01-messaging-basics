import pika
import xml.etree.ElementTree as ET

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='translated_queue')

def callback(ch, method, properties, body):
    try:
        root = ET.fromstring(body)
        name = root.find("name").text
        age = root.find("age").text
        print(f" [x] Received XML message: Name: {name}, Age: {age}")
        ch.basic_ack(delivery_tag=method.delivery_tag) # Acknowledge message
    except ET.ParseError:
        print(" [x] Received invalid XML message")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False) # Nack message
    except Exception as e: # Handle exceptions
        print(f" [x] Error processing XML: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False) # Nack message

channel.basic_consume(queue='translated_queue', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()