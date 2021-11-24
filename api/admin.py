from django.contrib import admin

from .models import *


@admin.display(description='Email')
def email(obj):
    return obj.user.email

@admin.display(description='Number')
def number(obj):
    return obj.candidate.number

@admin.display(description='Name')
def name(obj):
    return obj.candidate.name

class VoteAdmin(admin.ModelAdmin):
    list_display = (email, number, name, "session")
    list_filter = ("candidate__name", "session")
    
admin.site.register(Vote, VoteAdmin)
admin.site.register((Candidate, Detail))
