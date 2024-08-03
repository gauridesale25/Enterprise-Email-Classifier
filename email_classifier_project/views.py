# email_classifier_project/views.py

from django.http import HttpResponse
from my_app.tasks import add

def home(request):
    return HttpResponse("Welcome to the Email Classifier Home Page")
# views.py

def my_view(request):
    result = add.delay(4, 4)
    return HttpResponse(f'Task result: {result.id}')
