from django.contrib import admin
from django.utils.html import format_html
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'state', 'submitted_at', 'resume_link')
    list_filter = ('state', 'submitted_at')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('-submitted_at',)
    date_hierarchy = 'submitted_at'
    readonly_fields = ('submitted_at',)

    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Application Details', {
            'fields': ('resume', 'state', 'submitted_at')
        }),
    )

    actions = ['mark_as_reached_out']

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Name'

    def resume_link(self, obj):
        if obj.resume:
            return format_html('<a href="{}" target="_blank">View Resume</a>', obj.resume.url)
        return '-'
    resume_link.short_description = 'Resume'

    def mark_as_reached_out(self, request, queryset):
        updated = queryset.update(state=Lead.REACHED_OUT)
        self.message_user(
            request,
            f"{updated} {'lead was' if updated == 1 else 'leads were'} marked as reached out."
        )
    mark_as_reached_out.short_description = "Mark selected leads as reached out"
