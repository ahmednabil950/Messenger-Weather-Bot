from django.contrib import admin
from .models import RoomModel

# Register your models here.

admin.site.register(
        RoomModel,
        list_display=["id", "title", "staff_only"],
        list_display_links=["id", "title"],
    )