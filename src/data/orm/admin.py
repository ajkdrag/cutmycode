from django.contrib import admin
from src.data.orm.models import Snippet, Comment

admin.site.register(Snippet)
admin.site.register(Comment)
