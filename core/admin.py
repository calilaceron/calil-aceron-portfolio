from django.contrib import admin
from django.db import models as dj_models
from django.db.models import Max
from django.db.models.functions import Coalesce

from adminsortable2.admin import SortableAdminMixin

from .models import Skill, Project, Publication


@admin.register(Skill)
class SkillAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['name', 'category', 'order']
    list_display_links = ['name']
    list_filter = ['category']
    search_fields = ['name']
    ordering = ['order', 'name']
    list_per_page = 100

    def get_max_order(self, request, obj=None):
        qs = Skill.objects.all()
        if obj is not None and obj.category:
            qs = qs.filter(category=obj.category)
        return qs.aggregate(
            max_order=Coalesce(Max('order', output_field=dj_models.IntegerField()), 0)
        )['max_order']


@admin.register(Project)
class ProjectAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['title', 'order']
    list_display_links = ['title']
    search_fields = ['title']
    ordering = ['order', 'title']
    list_per_page = 100


@admin.register(Publication)
class PublicationAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display       = ['title', 'year', 'journal', 'order']
    list_display_links = ['title']
    search_fields      = ['title', 'journal']
    ordering           = ['order', 'title']
    list_per_page      = 100
