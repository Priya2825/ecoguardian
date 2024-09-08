from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Report, ReportStatus
from .forms import ReportForm  # Assuming you have a form for the report submission
from django.core.mail import send_mail

def submit_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            form.save()  # Save the report to the database
            ReportStatus.objects.create(report=report)
            send_mail(
                "EcoGuardian Report Submitted",
                f"Thank you for reporting about the incident. We will soon look into this. You will get an confimration email in next 24 hours",
                "ecoguardian@gmail.com",
                [report.contact_email],
                fail_silently=False,
        )
            return redirect('report-thank-you')  # Redirect to thank you page
    else:
        form = ReportForm()
    
    context = {
        'form': form,
    }
    return render(request, 'submit_report.html', context)

def report_thank_you(request):
    return render(request, 'thank_you.html')


def report_list(request):
    reports = ReportStatus.objects.all()
    context = {
        'reports' : reports,
    }
    return render(request, 'manage_reports.html', context)

def report_completed(request, rep_id):
    report = ReportStatus.objects.get(id=rep_id)
    report.is_completed = True
    report.save()
    send_mail(
                "EcoGuardian Report Completed",
                f"Your reported incident has been checked and resolved.",
                "ecoguardian@gmail.com",
                [report.report.contact_email],
                fail_silently=False,
        )
    return redirect('report-list')

def report_notcompleted(request, rep_id):
    report = ReportStatus.objects.get(id=rep_id)
    report.is_completed = False
    report.save()
    send_mail(
                "EcoGuardian Report Pending",
                f"Your reported incident is taking longer than expect to resolved. You might receive another email once it is resolved. Thank you",
                "ecoguardian@gmail.com",
                [report.report.contact_email],
                fail_silently=False,
        )
    return redirect('report-list')