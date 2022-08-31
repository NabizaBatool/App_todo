from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from todoSite import settings

@shared_task(bind=True)
def sendmail_func(self , mail_subject , message , to_email ):
    send_mail(
            subject=mail_subject ,
            message=message,
            from_email=settings.EMAIL_HOST_USER ,
            recipient_list=[to_email],
            fail_silently=True ,
        )
    return 'Done'

