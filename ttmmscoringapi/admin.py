from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(AdminUser)
admin.site.register(Startup)
admin.site.register(PortalControl)
admin.site.register(Funding2)
class ChoiceInLine(admin.TabularInline):
    model = Choice
    
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [(None, {'fields': ['question_text']})]
    inlines = [ChoiceInLine]
 
 
admin.site.register(Question, QuestionAdmin)
