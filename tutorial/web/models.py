from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.core.validators import EmailValidator

class LogMessage(models.Model):
    message = models.CharField(max_length=300)
    log_date = models.DateTimeField("date logged")

    def __str__(self):
        """Returns a string representation of a message."""
        date = timezone.localtime(self.log_date)
        return f"'{self.message}' logged on {date.strftime('%A, %d %B, %Y at %X')}"

class WebUserManager(UserManager):
    def _create_user(self, username, webid, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        webid = self.model.normalize_username(id)
        user = self.model(username=username, webid=webid, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, webid, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, webid, email, password, **extra_fields)

    def create_superuser(self, username, webid, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, webid, email, password, **extra_fields)


class WebUser(AbstractBaseUser, PermissionsMixin):

    objects = WebUserManager()

    username = models.CharField(
        verbose_name='username',
        max_length=25,
        unique=True,
        help_text=_('25文字以下で'),
        error_messages={
            'unique': 'すでに同じユーザーがいます'
        }
    )

    webid = models.CharField(
        verbose_name='userid',
        max_length=25,
        unique=False,
        help_text=_('25文字以下で'),
        error_messages={
            'unique': 'すでに同じidがいます'
        }
    )

    email: str = models.EmailField(
        verbose_name='email',
        max_length=25,
        unique=True,
        help_text=_('25文字以下'),
        validators=[EmailValidator()],
        error_messages={
            'unique': 'exist same user',
        },
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    deleted: int = models.BooleanField(verbose_name='削除フラグ', default=0, blank=False, null=False)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['webid','email']

    class Meta:
        verbose_name = _('webuser')
        verbose_name_plural = _('webusers')
        db_table = 'webuser'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)