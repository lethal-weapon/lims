from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

SCHOOL_CHOICES = (
    ('CS', 'Computer Science'),
    ('CE', 'Communication Engineering'),
    ('OE', 'OptoElectronic Engineering'),
    ('SE', 'Big Data and Software Engineering'),
    ('AUTO', 'Automation'),
    ('TBD', 'Unknown'),
)

ROLE_CHOICES = (
    ('VIS', 'Visitor'),
    ('STU', 'Student'),
    ('TEA', 'Teacher'),
    ('STA', 'Staff'),
    ('ADM', 'Administrator'),
    ('SUP', 'Superuser'),
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
        user.role = 'SUP'
        user.is_verified = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(max_length=60, unique=True)
    campus_id = models.CharField(max_length=30, unique=True)
    last_login = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=50, unique=False, blank=True, null=True)
    school = models.CharField(max_length=4, choices=SCHOOL_CHOICES, blank=True, null=True)
    limit = models.IntegerField(default=1, verbose_name='Facility Borrow Limit')

    role = models.CharField(max_length=3, choices=ROLE_CHOICES, default='VIS')
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'campus_id'
    REQUIRED_FIELDS = ['email']

    objects = AccountManager()

    def __str__(self):
        return self.campus_id

    # Returns True if the user has the named permission.
    # If obj is provided, the permission needs to be
    # checked against a specific object instance.
    # app.view/add/change/delete_model
    def has_perm(self, perm, obj=None):
        if self.role == 'SUP':
            return True

        elif self.role == 'ADM':
            if perm == 'accounts.delete_account':
                return False
            return True

        elif self.role == 'STA':
            return True

        return False

    # Returns True if the user has permission to
    # access models in the given app.
    def has_module_perms(self, app_label):
        if app_label == 'accounts':
            return self.role == 'ADM' or self.role == 'SUP'

        if app_label == 'bulletin' or \
            app_label == 'inventory' or \
            app_label == 'applications':
            return self.is_staff

        return False

    # Returns True if the user is allowed
    # to have access to the admin site.
    @property
    def is_staff(self):
        return self.role == 'STA' or \
               self.role == 'ADM' or \
               self.role == 'SUP'
