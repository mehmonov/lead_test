from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Lead


class LeadSubmissionTests(APITestCase):
    def setUp(self):
        self.url = reverse("lead-list")
        self.valid_payload = {
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com",
            "resume": SimpleUploadedFile(
                "cv.pdf", b"dummy-data", content_type="application/pdf"
            ),
        }

    def test_create_lead_successfully(self):
        response = self.client.post(self.url, self.valid_payload, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Lead.objects.filter(email="alice@example.com").exists())

    def test_create_lead_invalid_email(self):
        payload = self.valid_payload.copy()
        payload["email"] = "invalid-email"
        response = self.client.post(self.url, payload, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_lead_duplicate_email(self):
        Lead.objects.create(
            first_name="Test",
            last_name="User",
            email="alice@example.com",
            resume=self.valid_payload["resume"],
        )
        response = self.client.post(self.url, self.valid_payload, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_lead_invalid_resume_type(self):
        payload = self.valid_payload.copy()
        payload["resume"] = SimpleUploadedFile(
            "text.txt", b"invalid-content", content_type="text/plain"
        )
        response = self.client.post(self.url, payload, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
