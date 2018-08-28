from django.contrib import admin

from .models import Catalog, Author

admin.site.register(Catalog)
admin.site.register(Author)
