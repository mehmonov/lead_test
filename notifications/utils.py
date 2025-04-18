from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import Group, User

@shared_task
def send_prospect_email_task(lead_id, first_name, email):
    """Mijozga elektron pochta yuborish vazifasi"""
    send_mail(
        subject='Thank you for your application',
        message=(
            f"Hi {first_name},\n\n"
            "We have received your lead submission. Our attorney will contact you soon.\n\n"
            "Best regards,\nCompany Team"
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    return f"Email sent to prospect {email}"

@shared_task
def send_attorney_email_task(lead_id, first_name, last_name, email, submitted_at):
    """Attorney guruhidagi barcha foydalanuvchilarga elektron pochta yuborish vazifasi"""
    # Attorney guruhidagi barcha foydalanuvchilarni topish
    try:
        attorney_group = Group.objects.get(name='attorney')
        attorney_users = User.objects.filter(groups=attorney_group)
        attorney_emails = [user.email for user in attorney_users if user.email]

        if not attorney_emails:
            return "No attorney emails found to notify"

        # Barcha attorney foydalanuvchilarga elektron pochta yuborish
        send_mail(
            subject='New Lead Submitted',
            message=(
                f"A new lead has been submitted:\n\n"
                f"Name: {first_name} {last_name}\n"
                f"Email: {email}\n"
                f"Submitted At: {submitted_at}\n"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=attorney_emails,
            fail_silently=False,
        )
        return f"Email sent to {len(attorney_emails)} attorneys"
    except Group.DoesNotExist:
        return "Attorney group does not exist"
