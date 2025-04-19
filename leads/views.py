from rest_framework import viewsets

from notifications.utils import send_attorney_email_task, send_prospect_email_task

from .models import Lead
from .serializers import LeadSerializer


class LeadViewSet(viewsets.ModelViewSet):

    queryset = Lead.objects.all().order_by("-submitted_at")
    serializer_class = LeadSerializer

    def perform_create(self, serializer):
        lead = serializer.save()
        self.send_lead_notifications(lead)

    def send_lead_notifications(self, lead):
        send_prospect_email_task.delay(lead.id, lead.first_name, lead.email)

        send_attorney_email_task.delay(
            lead.id,
            lead.first_name,
            lead.last_name,
            lead.email,
            lead.submitted_at.strftime("%Y-%m-%d %H:%M"),
        )
