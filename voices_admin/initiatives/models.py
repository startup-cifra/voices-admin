from datetime import datetime
from functools import lru_cache

from django.db import models
from passlib.context import CryptContext
from uuid_extensions import uuid7

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


class City(models.TextChoices):
    YAROSLAVL = "Ярославль", _("Ярославль")
    ROSTOV = "Ростов", _("Ростов")
    TUTAEV = "Тутаев", _("Тутаев")

    @classmethod
    @lru_cache
    def all(cls):
        return [e.value for e in cls]


class DjangoUser(AbstractUser):
    city = models.CharField(max_length=9, choices=City.choices, default=None, blank=True)

    class Meta:
        db_table = "auth_user"


class User(models.Model):
    class Role(models.TextChoices):
        CITIZEN = "citizen", _("Житель")
        GOVERNMENT = "government", _("Правительство")

    id = models.UUIDField(primary_key=True, default=uuid7)
    first_name = models.CharField(max_length=50, null=True, default="Анонимный", blank=True)
    last_name = models.CharField(max_length=50, null=True, default="Пользователь", blank=True)
    email = models.CharField(max_length=254, unique=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CITIZEN)
    image_url = models.ImageField(
        max_length=2000,
        null=True,
        default="https://my-city.pro/api/storage/064e74c0198f7159800002e35c77df4a.jpg",
        blank=True,
    )
    hashed_password = models.CharField(max_length=128, default=get_password_hash("string"))

    city = models.CharField(max_length=9, choices=City.choices, default=None, blank=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    birthdate = models.DateField(null=True)
    deleted_at = models.DateTimeField(verbose_name="Время удаления")

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "users"
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


class Initiative(models.Model):
    class CitizenCategory(models.TextChoices):
        PROBLEM = "PROBLEM", _("Правительство")
        EVENT = "EVENT", _("Правительство")

    class Category(models.TextChoices):
        PROBLEM = "PROBLEM", _("Новость")
        EVENT = "EVENT", _("Событие")
        SURVEY = "SURVEY", _("Опрос")
        PROJECT = "PROJECT", _("Проект")
        BUILDING = "BUILDING", _("Строительство")

    class Status(models.TextChoices):
        ACTIVE = "active", _("Активно")
        SOLVED = "solved", _("Решено")

    class TagsCategory(models.TextChoices):
        PROBLEM = "PROBLEM", _("Новость")
        EVENT = "EVENT", _("Событие")
        SURVEY = "SURVEY", _("Опрос")
        PROJECT = "PROJECT", _("Проект")
        BUILDING = "BUILDING", _("Строительство")

    class EventType(models.TextChoices):
        ECOLOGY = "Экология", _("Экология")
        EDUCATION_AND_SCIENCE = "Образование и наука", _("Образование и наука")
        SPORTS = "Спорт", _("Спорт")
        TOURISM = "Туризм", _("Туризм")
        HEALTH_AND_MEDICINE = "Здоровье и медицина", _("Здоровье и медицина")
        PUBLIC_ORDER = "Общественный порядок", _("Общественный порядок")
        CHARITY = "Благотворительность", _("Благотворительность")
        TRANSPORT = "Транспорт", _("Транспорт")
        CULTURE_AND_ART = "Культура и искусство ", _("Культура и искусство")
        ENTERTAINMENT = "Развлечения", _("Развлечения")
        INNOVATION = "Инновации", _("Инновации")
        ENTREPRENEURSHIP = "Предпринимательство", _("Предпринимательство")

    id = models.UUIDField(primary_key=True, default=uuid7)
    city = models.CharField(max_length=35, choices=City.choices, verbose_name="Город")
    main_text = models.TextField(verbose_name="Текст")
    title = models.TextField(verbose_name="Заголовок")
    images = models.JSONField(null=True, blank=True, verbose_name="Изображения")
    image_url = models.ImageField(
        max_length=2000,
        null=True,
        blank=True,
    )
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    reposts_count = models.IntegerField(default=0)
    status = models.CharField(max_length=6, choices=Status.choices, default=Status.ACTIVE, verbose_name="Статус")
    to_date = models.DateField(null=True, blank=True, verbose_name="Дата начала")
    from_date = models.DateField(null=True, blank=True, verbose_name="Дата окончания")
    ar_model = models.FileField(max_length=2000, null=True, blank=True, verbose_name="AR-модель (3D-модель)")
    event_direction = models.CharField(
        max_length=100, null=True, blank=True, verbose_name="Направление мероприятия", choices=EventType.choices
    )
    tags = models.JSONField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id", verbose_name="Пользователь")
    category = models.CharField(
        max_length=15, choices=Category.choices, default=Category.PROBLEM, verbose_name="Категория"
    )
    created_at = models.DateTimeField(verbose_name="Время создания", default=datetime.now)
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField(verbose_name="Время удаления")
    approved = models.BooleanField(null=True, blank=True, verbose_name="Одобрена")
    address = models.CharField(max_length=100, null=True, blank=True, verbose_name="Адрес строительства")

    def __str__(self):
        return self.title

    class Meta:
        db_table = "initiatives"
        verbose_name = "инициатива"
        verbose_name_plural = "инициативы"
        ordering = ["-deleted_at"]
