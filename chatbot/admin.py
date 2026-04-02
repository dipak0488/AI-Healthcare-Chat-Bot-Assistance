from django.contrib import admin
from .models import Disease, History

# Disease Admin
@admin.register(Disease)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ('name','symptoms','precaution')

    # bulk add diseases button
    actions = ['add_default_diseases']

    def add_default_diseases(self, request, queryset):
        Disease.objects.create(name="Flu", symptoms="fever,cough,headache", description="Flu is a viral infection that affects respiratory system", precaution="Take rest and warm fluids")
        Disease.objects.create(name="Cold", symptoms="cold,cough,sneezing", description="Common cold is a viral infection of nose and throat", precaution="Drink warm water and take rest")
        Disease.objects.create(name="Malaria", symptoms="fever,chills,sweating", description="Malaria is caused by mosquito bite and leads to high fever", precaution="Consult doctor immediately")
        Disease.objects.create(name="Typhoid", symptoms="fever,weakness,stomach pain", description="Typhoid is bacterial infection causing fever and weakness", precaution="Take proper medication")
        self.message_user(request, "Default diseases added successfully")

    add_default_diseases.short_description = "Add default diseases (one click)"


# ⭐ Patient History Admin
@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('user','symptoms','prediction','date')
    list_filter = ('date',)
    search_fields = ('user__username','symptoms','prediction')
