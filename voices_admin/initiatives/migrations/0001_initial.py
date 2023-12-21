# Generated by Django 4.2.5 on 2023-10-31 15:57

import datetime
from django.db import migrations, models
import django.db.models.deletion
from uuid_extensions.uuid7 import uuid7


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.UUIDField(default=uuid7, primary_key=True, serialize=False)),
                ("first_name", models.CharField(blank=True, default="Анонимный", max_length=50, null=True)),
                ("last_name", models.CharField(blank=True, default="Пользователь", max_length=50, null=True)),
                ("email", models.CharField(max_length=254, unique=True)),
                (
                    "role",
                    models.CharField(
                        choices=[("citizen", "Citizen"), ("government", "Government")], default="citizen", max_length=10
                    ),
                ),
                (
                    "image_url",
                    models.ImageField(
                        blank=True,
                        default="https://voices-city.ru/api/storage/064e74c0198f7159800002e35c77df4a.jpg",
                        max_length=2000,
                        null=True,
                        upload_to="",
                    ),
                ),
                (
                    "hashed_password",
                    models.CharField(
                        default="$2b$12$QIRcIh4tcbmYNwlqDIbuNOEFbuUDAdEOape/8bT9mSqm0rew6ZZxi", max_length=128
                    ),
                ),
                (
                    "city",
                    models.CharField(
                        blank=True,
                        choices=[("Ярославль", "Yaroslavl"), ("Ростов", "Rostov"), ("Тутаев", "Tutaev")],
                        default=None,
                        max_length=9,
                    ),
                ),
                ("district", models.CharField(blank=True, max_length=50, null=True)),
                ("birthdate", models.DateField(null=True)),
                ("deleted_at", models.DateTimeField(verbose_name="Время удаления")),
            ],
            options={
                "verbose_name": "пользователь",
                "verbose_name_plural": "пользователи",
                "db_table": "users",
            },
        ),
        migrations.CreateModel(
            name="Initiative",
            fields=[
                ("id", models.UUIDField(default=uuid7, primary_key=True, serialize=False)),
                (
                    "city",
                    models.CharField(
                        choices=[("Ярославль", "Yaroslavl"), ("Ростов", "Rostov"), ("Тутаев", "Tutaev")],
                        max_length=35,
                        verbose_name="Город",
                    ),
                ),
                ("main_text", models.TextField()),
                ("title", models.TextField(verbose_name="Заголовок")),
                ("images", models.JSONField(blank=True, null=True)),
                ("image_url", models.ImageField(blank=True, max_length=2000, null=True, upload_to="")),
                ("likes_count", models.IntegerField(default=0)),
                ("comments_count", models.IntegerField(default=0)),
                ("reposts_count", models.IntegerField(default=0)),
                (
                    "status",
                    models.CharField(
                        choices=[("active", "Active"), ("solved", "Solved")],
                        default="active",
                        max_length=6,
                        verbose_name="Статус",
                    ),
                ),
                ("to_date", models.DateField(blank=True, null=True)),
                ("from_date", models.DateField(blank=True, null=True)),
                ("ar_model", models.CharField(blank=True, max_length=2000, null=True)),
                ("event_direction", models.CharField(blank=True, max_length=100, null=True)),
                ("tags", models.JSONField(null=True)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("PROBLEM", "Problem"),
                            ("EVENT", "Event"),
                            ("DECIDE_TOGETHER", "Decide Together"),
                            ("SURVEY", "Survey"),
                            ("PROJECT", "Project"),
                            ("BUILDING", "Building"),
                        ],
                        default="PROBLEM",
                        max_length=15,
                        verbose_name="Категория",
                    ),
                ),
                ("created_at", models.DateTimeField(default=datetime.datetime.now, verbose_name="Время создания")),
                ("updated_at", models.DateTimeField()),
                ("deleted_at", models.DateTimeField(verbose_name="Время удаления")),
                ("approved", models.BooleanField(blank=True, null=True, verbose_name="Одобрена")),
                (
                    "user",
                    models.ForeignKey(
                        db_column="user_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="initiatives.user",
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "инициатива",
                "verbose_name_plural": "инициативы",
                "db_table": "initiatives",
                "ordering": ["-deleted_at"],
            },
        ),
    ]
