from django.contrib import admin
from .models import Entry, Tag, Author

# Register your models here.
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Entry)
