# classifier/tasks.py
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='localhost:9092')
# Produce some messages
producer.send('my-topic', b'some_message')
# Flush the producer
producer.flush()

from celery import shared_task
from kafka import KafkaProducer, KafkaConsumer
import json
import joblib

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

model = joblib.load('classifier/email_classifier_model.pkl')

@shared_task
def send_email_to_kafka(subject, body):
    email_data = {'subject': subject, 'body': body}
    producer.send('raw-emails', email_data)
    producer.flush()

@shared_task
def consume_emails_from_kafka():
    consumer = KafkaConsumer(
        'raw-emails',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )
    
    producer = KafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    for message in consumer:
        email_data = message.value
        text = email_data['subject'] + ' ' + email_data['body']
        email_data['is_spam'] = model.predict([text])[0]
        producer.send('classified-emails', email_data)
        producer.flush()
        


@shared_task
def add(x, y):
    return x + y
