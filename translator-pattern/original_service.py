import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='original_queue')

message = {"name": "Alice", "age": 30}
channel.basic_publish(exchange='', routing_key='original_queue', body=json.dumps(message))

print(" [x] Sent JSON message")
connection.close()