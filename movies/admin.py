from django.contrib import admin

from .models import *

admin.site.register(Movie)
admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Rating)
