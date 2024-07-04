from django.contrib import admin
from .models import Verifier, Post, User, Seller

admin.site.register(Verifier)
admin.site.register(Post)
admin.site.register(User)
admin.site.register(Seller)