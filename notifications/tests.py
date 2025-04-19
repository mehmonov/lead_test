from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase

from notifications.utils import send_attorney_email_task, send_prospect_email_task

User = get_user_model()


class NotificationTaskTests(TestCase):
    def setUp(self):
        self.lead_id = 1
        self.first_name = "Ali"
        self.last_name = "Valiyev"
        self.email = "ali@example.com"
        self.submitted_at = "2025-04-18 12:00:00"

    @patch("notifications.utils.send_mail")
    def test_send_prospect_email_task_success(self, mock_send_mail):
        result = send_prospect_email_task(
            lead_id=self.lead_id, first_name=self.first_name, email=self.email
        )
        mock_send_mail.assert_called_once()
        self.assertIn("Email sent to prospect", result)

    @patch("notifications.utils.send_mail")
    def test_send_attorney_email_task_success(self, mock_send_mail):
        group = Group.objects.create(name="attorney")
        user1 = User.objects.create_user(
            username="att1", email="att1@example.com", password="pass"
        )
        user2 = User.objects.create_user(
            username="att2", email="att2@example.com", password="pass"
        )
        user1.groups.add(group)
        user2.groups.add(group)

        result = send_attorney_email_task(
            lead_id=self.lead_id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            submitted_at=self.submitted_at,
        )
        mock_send_mail.assert_called_once()
        self.assertIn("Email sent to 2 attorneys", result)

    def test_send_attorney_email_task_group_not_exist(self):
        result = send_attorney_email_task(
            lead_id=self.lead_id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            submitted_at=self.submitted_at,
        )
        self.assertEqual(result, "Attorney group does not exist")

    def test_send_attorney_email_task_no_attorney_emails(self):
        group = Group.objects.create(name="attorney")
        user = User.objects.create_user(username="att", email="", password="pass")
        user.groups.add(group)

        result = send_attorney_email_task(
            lead_id=self.lead_id,
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            submitted_at=self.submitted_at,
        )
        self.assertEqual(result, "No attorney emails found to notify")
