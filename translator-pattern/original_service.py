import pika
import json
import random
from datetime import datetime, timedelta

# Sample data for random generation
first_names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Erik', 'Fiona', 'George', 'Hannah']
last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
cities = ['New York', 'London', 'Tokyo', 'Paris', 'Berlin', 'Sydney', 'Toronto', 'Singapore']
interests = ['Reading', 'Gaming', 'Cooking', 'Photography', 'Traveling', 'Music', 'Sports', 'Art']

def generate_random_message():
    # Generate a random person
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    age = random.randint(18, 80)
    
    # Generate random registration date within last year
    days_ago = random.randint(0, 365)
    registration_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
    
    # Generate random additional fields
    message = {
        "user_id": f"USER_{random.randint(1000, 9999)}",
        "first_name": first_name,
        "last_name": last_name,
        "age": age,
        "email": f"{first_name.lower()}.{last_name.lower()}@example.com",
        "city": random.choice(cities),
        "interests": random.sample(interests, random.randint(1, 4)),
        "active_status": random.choice([True, False]),
        "registration_date": registration_date,
        "login_count": random.randint(1, 100),
        "premium_member": random.random() < 0.3  # 30% chance of being premium
    }
    
    return message

# Set up RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Declare the queue
channel.queue_declare(queue='original_queue')

# Generate and send multiple messages
num_messages = 5  # Change this to send more or fewer messages
for i in range(num_messages):
    message = generate_random_message()
    channel.basic_publish(
        exchange='',
        routing_key='original_queue',
        body=json.dumps(message),
        properties=pika.BasicProperties(
            delivery_mode=2,  # Make messages persistent
            content_type='application/json'
        )
    )
    print(f" [x] Sent message {i+1}: {json.dumps(message, indent=2)}")

print(f"\nSent {num_messages} messages successfully")
connection.close()