from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db import models
from users.managers import UserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _


class UserRoles:
    ADMIN = "admin"
    USER = "user"


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=12)
    email = models.EmailField(
        max_length=100,
        unique=True
    )
    role = models.CharField(
        max_length=7,
        choices=[
            (UserRoles.ADMIN, UserRoles.ADMIN),
            (UserRoles.USER,UserRoles.USER),
        ],
        default=UserRoles.USER
    )
    is_active = models.BooleanField(
        verbose_name="Аккаунт активен",
        help_text="Укажите, активен ли аккаунт",
        default=True
    )
    image = models.ImageField(upload_to='images/', null=True)
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', "role"]

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    # также для работы модели пользователя должен быть переопределен
    # менеджер объектов
    objects = UserManager()

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN  #

    @property
    def is_user(self):
        return self.role == UserRoles.USER