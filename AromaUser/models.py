from django.db import models
from django.utils import timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

class AromaUserManager(BaseUserManager):

    def create_user(self, email, password, nickname, **extra_fields):
        """
        Creates and saves a User with the given email
        and password.
        """
        now=timezone.now()
        if not email:
            msg = 'Users must have an email address'
            raise ValueError(msg)
        user = self.model(
        email=AromaUserManager.normalize_email(email),
        nickname=nickname,
        is_staff=False, is_active=True, is_superuser=False,
        **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
          
    def create_superuser(self, email, password, nickname):
        """
        Creates and saves a superuser with the given email,
        favorite topping and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            nickname=nickname,
            )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class AromaUser(AbstractBaseUser, PermissionsMixin):
    """ Inherits from both the AbstractBaseUser and
    PermissionMixin.
    """
    email = models.EmailField(
        verbose_name='email',
        max_length=60,
        unique=True,
        db_index=True,
    )
    nickname = models.CharField(
        verbose_name='nickname',
        max_length=20,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', ]

    objects = AromaUserManager()
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    objects = AromaUserManager()
    def get_full_name(self):
        # The user is identified by their email
        return self.email
    
    def get_short_name(self):
        return self.nickname
    
    def __str__(self):
        return self.email
