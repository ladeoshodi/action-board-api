from django.contrib import admin
from .models import Tag

# Register your models here.


class TagAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)


admin.site.register(Tag, TagAdmin)
