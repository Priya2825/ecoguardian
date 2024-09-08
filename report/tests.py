from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from report.models import Report, ReportStatus
from report.forms import ReportForm
from django.contrib.messages import get_messages
from django.core import mail


class SubmitReportTest(TestCase):
    def setUp(self):
        self.report = Report.objects.create(
            report_type='Pet Violence',
            description='This is a test report.',
            location='Test Location',
            contact_email='test@example.com',
            contact_phone='1234567890'
        )
        
        self.report_status = ReportStatus.objects.create(
            report=self.report,
            is_completed=False
        )
        
    def test_report_creation(self):
        self.assertEqual(self.report.report_type, 'Pet Violence')
        self.assertEqual(self.report.description, 'This is a test report.')
        self.assertEqual(self.report.location, 'Test Location')
        self.assertEqual(self.report.contact_email, 'test@example.com')
        self.assertEqual(self.report.contact_phone, '1234567890')
        
    def test_submit_report_view(self):
        response = self.client.post(reverse('submit-report'), {
            'report_type': 'Pet Violence',
            'description': 'This is a test report.',
            'location': 'Test Location',
            'contact_email': 'test@example.com',
            'contact_phone': '1234567890'
        }, follow=True)
        report = Report.objects.last()
        self.assertEqual(report.report_type, 'Pet Violence')
        self.assertEqual(report.description, 'This is a test report.')
        
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'EcoGuardian Report Submitted')
        self.assertIn('test@example.com', mail.outbox[0].to)
        self.assertRedirects(response, reverse('report-thank-you'))

class ReportListViewTest(TestCase):
    def setUp(self):
        self.report1 = Report.objects.create(
            report_type='Pet Violence',
            description='This is a test report.',
            location='Test Location',
            contact_email='test@example.com',
            contact_phone='1234567890'
        )
        self.report2 = Report.objects.create(
            report_type='Animal Abuse',
            description='This is another test report.',
            location='Test Location 2',
            contact_email='test2@example.com',
            contact_phone='0987654321'
        )
        
        self.report_status1 = ReportStatus.objects.create(
            report=self.report1,
            is_completed=False
        )
        self.report_status2 = ReportStatus.objects.create(
            report=self.report2,
            is_completed=True
        )
        
    def test_reports_status_list_view(self):
        response = self.client.get(reverse('report-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ReportStatus.objects.count(), 2)
        
        
class ReportActionTest(TestCase):
    def setUp(self):
        self.report = Report.objects.create(
            report_type='Pet Violence',
            description='This is a test report.',
            location='Test Location',
            contact_email='test@example.com',
            contact_phone='1234567890'
        )
        self.report_status = ReportStatus.objects.create(
            report=self.report,
            is_completed=False
        )
        
    def test_report_completed_status(self):
        response = self.client.get(reverse('report-completed', args=[self.report_status.id]))
        self.report_status.refresh_from_db()
        self.assertTrue(self.report_status.is_completed)
        
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'EcoGuardian Report Completed')
        self.assertIn(self.report.contact_email, mail.outbox[0].to)
        self.assertRedirects(response, reverse('report-list'))
        