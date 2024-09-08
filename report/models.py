from django.db import models

class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('Pet Violence', 'Pet Violence'),
        ('Environmental Violence', 'Environmental Violence'),
    ]
    
    report_type = models.CharField(max_length=50, choices=REPORT_TYPE_CHOICES)
    description = models.TextField()
    location = models.CharField(max_length=255)
    reported_at = models.DateTimeField(auto_now_add=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_report_type_display()} - {self.location}"

class ReportStatus(models.Model):
    report = models.OneToOneField(Report, on_delete=models.CASCADE, related_name='status')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Status for {self.report.report_type} is {self.is_completed}"