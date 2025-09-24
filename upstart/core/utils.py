import uuid
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

def send_verification_email(user):
    token = str(uuid.uuid4())
    user.email_token = token
    user.save()

    verification_link = reverse('verify_email', args=[token])
    full_verification_link = f"{settings.SITE_URL}{verification_link}"

    send_mail(
        'Verify Your Email Address',
        f'Please click the following link to verify your email address: {full_verification_link}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
