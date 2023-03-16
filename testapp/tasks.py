from celery import Celery, shared_task
from time import sleep
from django.core.mail import send_mail

# app = Celery('testapp', broker='pyamqp://guest@localhost//')
app = Celery('testapp', broker='redis://redis:6379')


@shared_task
def sleepy(duration):
    sleepy(duration)
    return None


@app.task
def add(x, y):
    return x + y


@shared_task
def send_mail_task():
    send_mail(
        'celery message', 'hello how are you', 'najamsakardu@gmail.com', ['aikramtufail@gmail.com'],
        fail_silently=False)
    return 'Done'
