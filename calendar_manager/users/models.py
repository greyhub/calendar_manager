from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from slugify import slugify


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', User.Role.MEMBER)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', User.Role.SYSTEM_ADMIN)

        if extra_fields.get('role') < User.Role.SYSTEM_ADMIN:
            raise ValueError('System admin must have role=10.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser):
    class Role(models.IntegerChoices):
        MEMBER = 0
        MANAGER = 5
        SYSTEM_ADMIN = 11
    
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(max_length=120, unique=True)
    #avatars
    lastname = models.CharField(max_length=30)
    middlename = models.CharField(max_length=30, blank=True)
    firstname = models.CharField(max_length=30)
    email = models.EmailField(blank=True)
    role = models.IntegerField(choices=Role.choices, default=Role.MEMBER)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateField(default=timezone.now)
    updated_at = models.DateField(auto_now=True)


    objects = UserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
    
    @staticmethod
    def check_username_exist(username):
        return User.objects.filter(username=username).exists()
    
    @staticmethod
    def check_email_exist(email):
        return User.objects.filter(email=email).exists()

    @staticmethod
    def make_username(firstname, middlename, lastname):
        firstname = slugify(firstname)
        middlename_letters = [slugify(letter)[0] for letter in middlename.split()]
        lastname_letter = slugify(lastname)[0]
        base_username = firstname + str(lastname_letter) + str(''.join(middlename_letters))
        
        if not User.check_username_exist(base_username):
            return base_username
        
        number = 1
        while True:
            username = base_username + str(number)
            if not User.check_username_exist(username):
                return username
            number += 1

    def get_name(self):
        return self.lastname + ' ' + self.firstname

    def get_full_name(self):
        return self.lastname + ' ' + self.middlename + ' ' + self.firstname

    def get_role(self):
        if self.role == self.Role.MEMBER:
            return 'Employee'
        elif self.role == self.Role.MANAGER:
            return 'Manager'
        else:
            return 'Admin'
        