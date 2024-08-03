
from django.shortcuts import render
from django.http import JsonResponse
from .models import Email
import joblib
from kafka import send_email_to_kafka

model = joblib.load('classifier/email_classifier_model.pkl')

def classify_email(request):
    if request.method == 'POST':
        subject = request.POST.get('subject', '')
        body = request.POST.get('body', '')
        email_text = f"{subject} {body}"
        prediction = model.predict([email_text])[0]
        is_spam = bool(prediction)
        email = Email.objects.create(subject=subject, body=body, is_spam=is_spam)
        return JsonResponse({'is_spam': is_spam})
    return render(request, 'classifier/classify_email.html')

def send_email(request):
    subject = request.GET.get('subject', '')
    body = request.GET.get('body', '')

    send_email_to_kafka.delay(subject, body)  # Use Celery task

    return JsonResponse({'status': 'Email sent to Kafka'})

# Create your views here.

  