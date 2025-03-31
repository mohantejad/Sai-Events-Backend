import os
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.core.validators import EmailValidator, RegexValidator



class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required to create account")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


pp_fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "profile_pictures"))

class CustomAbstractUser(AbstractBaseUser, PermissionsMixin):
    PHONE_REGEX = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(
        _("email address"), 
        blank=False, 
        unique=True,
        validators=[EmailValidator(message="Enter a valid email address.")],
    )
    phone_number = models.CharField(
        _('phone number'),
        max_length=15,
        unique=True,
        blank=True,
        null=True,
        validators=[PHONE_REGEX]
    )
    profile_picture = models.ImageField(
        _('profile_image'),
        storage=pp_fs,
        blank=True,
        null=True
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class AddressTypeChoices(models.TextChoices):
    HOME = "Home", "Home"
    WORK = "Work", "Work"
    RENTAL = "Rental", "Rental"
    OTHER = "Other", "Other"


class Address(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='addresses'
    )
    address_type = models.CharField(
        _("address type"),
        max_length=10,
        choices=AddressTypeChoices.choices,
        default=AddressTypeChoices.HOME
    )
    street = models.CharField(_("street address"), max_length=255)
    city = models.CharField(_("city"), max_length=100)
    state = models.CharField(_("state"), max_length=100)
    country = models.CharField(_("country"), max_length=100)
    postal_code = models.CharField(_("postal code"), max_length=20)
    is_primary = models.BooleanField(_("primary address"), default=False)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country}"


class User(CustomAbstractUser):
    class Meta(CustomAbstractUser.Meta):
        swappable = "AUTH_USER_MODEL"

