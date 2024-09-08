from django.contrib import admin
from .models import Report, ReportStatus

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'location', 'reported_at', 'contact_email')
    list_filter = ('report_type', 'reported_at')
    search_fields = ('location', 'description', 'contact_email')

    # Optionally, you can customize the form layout in the admin interface:
    fieldsets = (
        (None, {
            'fields': ('report_type', 'description', 'location')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'contact_phone'),
        }),
        ('Reporting Details', {
            'fields': ('reported_at',),
        }),
    )
    readonly_fields = ('reported_at',)

admin.site.register(ReportStatus)