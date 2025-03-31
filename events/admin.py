from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "city", "mode", 'date')
    list_filter = ("category", "city", "mode", 'date')
    search_fields = ("title", "description", "city", "category")
    ordering = ("date",) 
    date_hierarchy = "date" 

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        obj.save()

