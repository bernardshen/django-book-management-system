from django.contrib import admin
from .models import Books, Authors, Publishers, Categories, Ratings, Readers, Borrows, Borrow_histry

# Register your models here.
admin.site.register(Books)

admin.site.register(Authors)

admin.site.register(Publishers)

admin.site.register(Ratings)

admin.site.register(Readers)

admin.site.register(Categories)

admin.site.register(Borrows)

admin.site.register(Borrow_histry)