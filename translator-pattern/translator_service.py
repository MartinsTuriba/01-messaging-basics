import pika
import json
import xml.etree.ElementTree as ET

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='original_queue')
channel.queue_declare(queue='translated_queue')  # Declare the new queue

def callback(ch, method, properties, body):
    try:
        json_message = json.loads(body)

        # Translate to XML
        root = ET.Element("person")
        name = ET.SubElement(root, "name")
        name.text = json_message["first_name"]+" "+json_message["last_name"]
        age = ET.SubElement(root, "age")
        age.text = str(json_message["age"])
        xml_message = ET.tostring(root).decode() # Decode from bytes to string

        channel.basic_publish(exchange='', routing_key='translated_queue', body=xml_message)
        print(f" [x] Translated and sent XML message: {xml_message}")
        ch.basic_ack(delivery_tag=method.delivery_tag) # Acknowledge message

    except json.JSONDecodeError:
        print(" [x] Received invalid JSON message")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False) # Nack message
    except Exception as e: # Handle exceptions
        print(f" [x] Error during translation: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False) # Nack message



channel.basic_consume(queue='original_queue', on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()