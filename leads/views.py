from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Lead
from .serializers import LeadSerializer
from notifications.utils import send_lead_notification

class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        lead = serializer.save()
        send_lead_notification(lead)

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def reach_out(self, request, pk=None):
        lead = self.get_object()
        lead.state = Lead.REACHED_OUT
        lead.save()
        return Response({'status': 'Lead marked as reached out'})
