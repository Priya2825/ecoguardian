from django.urls import path
from report.views import submit_report, report_thank_you, report_list, report_notcompleted, report_completed

urlpatterns = [
    path('submit/', submit_report, name='submit-report'),
    path('thank-you/', report_thank_you, name='report-thank-you'),
    path('report-list/', report_list, name='report-list'),
    path('<int:rep_id>/completed/', report_completed, name='report-completed'),
    path('<int:rep_id>/not-completed/', report_notcompleted, name='report-notcompleted'),

]