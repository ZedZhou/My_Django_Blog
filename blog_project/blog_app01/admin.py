from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Article,ArticleAdmin)
admin.site.register(Tag)
admin.site.register(Ad)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Links)