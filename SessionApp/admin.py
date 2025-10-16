from django.contrib import admin
from SessionApp.models import Session

# Customize the admin site headers
admin.site.site_header = "Session Management"
admin.site.site_title = "Session Admin Portal"
admin.site.index_title = "Welcome to the Session Admin Portal"


@admin.register(Session)
class AdminPerso(admin.ModelAdmin):
    list_display = ("title", "topic", "session_day", "start_time", "end_time", "keywords", "submission_date", "paper")
    ordering = ("start_time",)
    list_filter = ("topic", "end_time")
    search_fields = ("title",)
    fieldsets = (
        ("Information générale", {
            "fields": ("session_id", "title", "topic", "keywords")
        }),
        ("Logistics", {
            "fields": ("start_time", "end_time", "session_day")
        }),
    )
    readonly_fields = ("session_id", "session_day", "start_time", "end_time", "paper")
    date_hierarchy = "start_time"

    def duration(self, obj):
        if obj.start_time and obj.end_time:
            delta = obj.end_time - obj.start_time
            return delta.days
        return "N/A"

    duration.short_description = "Duration (days)"
