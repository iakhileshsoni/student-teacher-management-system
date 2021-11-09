from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, User, UserManager, Group
from django.contrib.auth.models import PermissionsMixin
from django.db.models.fields import BooleanField
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(UserManager):
    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """
        # if not email:
        #     raise ValueError('The given email must be set')
        # email = self.normalize_email(email)s
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        # group, created = Group.objects.get_or_create(name='Superuser')
        # extra_fields.setdefault('role_id', group.id)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class UserPermissionMixin(PermissionsMixin):
    is_superuser = models.BooleanField(_('superuser status'),
                                       default=False,
                                       help_text=_(
                                           'Designates that this user has all permissions without '
                                           'explicitly assigning them.'
                                       ),
                                       )

    groups = None
    user_permissions = None
    is_staff = False

    class Meta:
        abstract = True

    def get_group_permissions(self, obj=None):
        pass
    def get_all_permissions(self, obj=None):
        pass


class Subject(models.Model):
    subject = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.subject


class Users(AbstractBaseUser, PermissionsMixin):

    is_student = models.BooleanField(default=True, null=True)
    first_name = models.CharField(_('first name'), max_length=50, blank=True, null=True)
    username = models.CharField(
            _('username'),
            max_length=150,
            help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
            null=True,
            blank=True,
            unique=True
    )

    is_staff = models.BooleanField(_('teacher'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = 'user'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


class Teacher(models.Model):
    teacher = models.OneToOneField(Users, on_delete=models.CASCADE)
    subject = models.ManyToManyField(Subject)

    def __str__(self):
        return self.teacher.username


class Student(models.Model):
    student = models.OneToOneField(Users,on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.student.username