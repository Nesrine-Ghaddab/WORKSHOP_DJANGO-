from django.contrib import admin
from .models import conference, submission

admin.site.site_header = "Conference Management"
admin.site.site_title = "Conference Admin Portal"
admin.site.index_title = "Welcome to the Conference Admin Portal"

class SubmissionInline(admin.StackedInline):
    model = submission
    extra = 1
    readonly_fields = ("submission_id", "submission_date")
    show_change_link = True


@admin.register(conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ("title", "theme", "location", "start_date", "end_date", "duration")
    search_fields = ("title", "keywords")
    ordering = ("start_date",)
    list_filter = ("theme", "location", "end_date")
    fieldsets = (
        ("Informations générales", {
            "fields": ("conference_id", "title", "theme", "description")
        }),
        ("Logistique", {
            "fields": ("location", "start_date", "end_date")
        }),
    )
    readonly_fields = ("conference_id",)
    date_hierarchy = "start_date"
    inlines = [SubmissionInline]

    def duration(self, obj):
        """Calcule la durée de la conférence en jours."""
        if obj.start_date and obj.end_date:
            return (obj.end_date - obj.start_date).days
        return "N/A"
    duration.short_description = "Duration (days)"


@admin.action(description="marquer comme payé")
def mark_as_payed(modeladmin,req,queryset):
    queryset.update(payed=True)

@admin.action
def mark_as_accepted(m,req,q):
    q.update(status="accepted")

@admin.register(submission)
class SubmissionAdmin(admin.ModelAdmin):
    actions=[mark_as_payed]
    actions=[mark_as_accepted]
    
    # a. Colonnes : title, status, user, conference, submission_date, payed, short_abstract
    list_display = ("title", "status", "user_id", "conference", "submission_date", "payed", "short_abstract")

    # d. Filtres
    list_filter = ("status", "payed", "conference", "submission_date")

    # e. Recherche
    search_fields = ("title", "keywords", "user__username")

    # f. Champs modifiables directement
    list_editable = ("status", "payed")

    # g. Organisation du formulaire
    fieldsets = (
        ("Infos générales", {
            "fields": ("submission_id", "title", "abstract", "keywords")
        }),
        ("Fichier et conférence", {
            "fields": ("paper", "conference")
        }),
        ("Suivi", {
            "fields": ("status", "payed", "submission_date", "user_id")
        }),
    )

    # h. Champs en lecture seule
    readonly_fields = ("submission_id", "submission_date")

    ordering = ("submission_date",)
    date_hierarchy = "submission_date"

    
    def short_abstract(self, obj):
        if obj.abstract:
            return (obj.abstract[:50] + "…") if len(obj.abstract) > 50 else obj.abstract
        return "—"
    short_abstract.short_description = "Résumé court"
    


    


