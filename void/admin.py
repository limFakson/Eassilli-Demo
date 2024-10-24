from django.contrib import admin
from .models import Lecturer, PastQues, GenPastQues, Document

# Register your models here.
admin.site.register(Lecturer)
admin.site.register(PastQues)
admin.site.register(Document)
admin.site.register(GenPastQues)
