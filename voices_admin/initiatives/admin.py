import re

from django.conf import settings
from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django import forms

from .models import Initiative, User

a = re.compile(r"[\'\[\]\"]+")

UPLOAD_URL = "http://89.223.126.166:8000/" if not settings.DEBUG else "localhost:8000"

from django.contrib.admin import SimpleListFilter

# import pymongo

# connect_string = 'mongodb://localhost:27017' 

# my_client = pymongo.MongoClient(connect_string)


class CountryFilter(SimpleListFilter):
    title = "Типы"
    parameter_name = "types"

    def lookups(self, request, model_admin):
        return [("citizen", "От жителей"), ("government", "От властей")]

    def queryset(self, request, queryset):
        if self.value() == "citizen":
            return queryset.filter(category__in=(Initiative.CitizenCategory.EVENT, Initiative.CitizenCategory.PROBLEM))
        if self.value() == "government":
            return queryset.filter(
                category__in=(
                    Initiative.Category.SURVEY,
                    Initiative.Category.PROJECT,
                    Initiative.Category.BUILDING,
                )
            )
# @admin.register(Foo)
# class FooAdmin(admin.ModelAdmin):
#     form = CustomFooForm
#     add_form = CustomAddFooForm # It is not a native django field. I created this field and use it in get_form method.

#     def get_form(self, request, obj=None, **kwargs):
#         """
#         Use special form during foo creation
#         """
#         defaults = {}
#         if obj is None:
#             defaults['form'] = self.add_form
#         defaults.update(kwargs)
#         return super().get_form(request, obj, **defaults)

@admin.register(User)
class UserAdminView(admin.ModelAdmin):
    list_display = ("image_tag", "first_name", "last_name", "city", "deleted_at")
    fields = ("first_name", "last_name", "city", "role", "image_url", "district", "email")
    list_per_page = 20

    def get_queryset(self, request: WSGIRequest):
        city = request.user.city
        qs: QuerySet = super(UserAdminView, self).get_queryset(request)
        return qs.filter(city=city).filter(deleted_at__isnull=True)

    def save_model(self, request, obj: User, form, change):
        super().save_model(request, obj, form, change)
        if not obj.image_url.url.startswith('http'):
            obj.image_url = UPLOAD_URL + obj.image_url.url.removeprefix("/")

        obj.save()

    def delete_queryset(self, request, queryset):
        queryset.update(deleted_at=timezone.now())

    def image_tag(self, obj: User):
        return format_html(f'<img src="{obj.image_url}" style="max-width:200px; max-height:200px"/>')


@admin.register(Initiative)
class InitiativeAdminView(admin.ModelAdmin):
    list_display = ("image_tag", "title", "created_at", "approved", "user", 
                    # "survey",
                    )
    fields = (
        "title",
        "city",
        "main_text",
        "images",
        "status",
        "from_date",
        "to_date",
        "ar_model",
        "event_direction",
        "user",
        "approved",
        "category",
        "address",
    )
    list_filter = ("status", "approved", CountryFilter)
    actions = ["approve_queryset"]
    list_per_page = 20

    def get_queryset(self, request: WSGIRequest):
        city = request.user.city
        qs: QuerySet = super(InitiativeAdminView, self).get_queryset(request)
        return qs.filter(city=city).filter(deleted_at__isnull=True)

    def delete_queryset(self, request, queryset):
        queryset.update(deleted_at=timezone.now())

    def approve_queryset(self, request, queryset):
        queryset.update(approved=True)

    approve_queryset.short_description = "Одобрить инициативы"

    def save_model(self, request, obj: Initiative, form, change):
        if not obj.images:
            obj.images = [obj.image_url] if obj.image_url else []

        if not obj.image_url.url.startswith('http'):
            obj.image_url = UPLOAD_URL + obj.image_url.url.removeprefix("/")
        super().save_model(request, obj, form, change)

    def image_tag(self, obj: Initiative):
        url = ""
        if obj.images:
            url = obj.images[0]
        return format_html(f'<img src="{url}" style="max-width:200px; max-height:200px"/>')

    image_tag.short_description = "Изображение"
    
    # def survey(self, obj: Initiative):
    #     result = my_client.voices.surveys.find_one({'_id': str(obj.id)})
    #     if result:
    #         return str(result)
