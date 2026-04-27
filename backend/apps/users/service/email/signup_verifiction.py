from celery import shared_task
from django.core.mail import EmailMultiAlternatives



@shared_task
def send_verifiction_link(gmail,uid,token):
    link = f"http://localhost:8000/api/auth/verify-email/{uid}/{token}/"

    html = f"""
    <h2>Verify your email</h2>
    <p>Click below:</p>
    <a href="{link}">Verify Email</a>
    """

    msg = EmailMultiAlternatives(
        "Verify your email",
        "Click link to verify",
        "noreply@yourapp.com",
        [gmail]
    )
    msg.attach_alternative(html, "text/html")
    msg.send()