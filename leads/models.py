from django.db import models
from django.utils import timezone


class Lead(models.Model):
    PENDING = "PENDING"
    REACHED_OUT = "REACHED_OUT"

    STATE_CHOICES = [
        (PENDING, "Pending"),
        (REACHED_OUT, "Reached Out"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    resume = models.FileField(upload_to="resumes/")
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default=PENDING)
    submitted_at = models.DateTimeField(default=timezone.now)

    class Meta:
        permissions = [
            (
                "can_change_status_to_reached_out",
                "Can change lead status to reached_out",
            ),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
