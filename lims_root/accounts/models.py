from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

SCHOOL_CHOICES = (
    ('CS', 'Computer Science'),
    ('CE', 'Communication Engineering'),
    ('OE', 'OptoElectronic Engineering'),
    ('SE', 'Big Data and Software Engineering'),
    ('AUTO', 'Automation'),
)


class AccountManager(BaseUserManager):

    def create_user(self, email, campus_id, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not campus_id:
            raise ValueError('Users must have a campus ID')

        user = self.model(
            email=self.normalize_email(email),
            campus_id=campus_id,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, campus_id, password=None):
        user = self.create_user(email, campus_id, password)
        user.is_staff = True
        user.is_admin = True
        user.is_verified = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(max_length=60, unique=True)
    campus_id = models.CharField(max_length=30, unique=True)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=50, unique=False)
    school = models.CharField(max_length=4, choices=SCHOOL_CHOICES)
    borrow_limit = models.IntegerField(default=2)

    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'campus_id'
    REQUIRED_FIELDS = ['email']

    objects = AccountManager()

    def __str__(self):
        return self.campus_id

    # Does the user have a specific permission?
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does the user have permissions to view the app "app_label"?
    def has_module_perms(self, app_label):
        return True
