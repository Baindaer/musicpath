from django.contrib import admin

from .models import Catalog, Author, Session

admin.site.register(Catalog)
admin.site.register(Author)
admin.site.register(Session)
