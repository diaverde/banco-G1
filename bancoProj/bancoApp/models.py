from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Debe tener 'username'")

        user = self.model(email = username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            email = username,
            password = password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class Customer(AbstractBaseUser, PermissionsMixin):
    id = models.BigIntegerField(primary_key=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    isAdmin = models.BooleanField(default=False)

    def save(self, **kwargs):
        some_salt = 'mMABCD12345'
        #print(self.password)
        self.password = make_password(self.password, some_salt)
        #print(self.password)
        super().save(**kwargs)

    objects: UserManager()
    USERNAME_FIELD = 'email'

"""
class Customer(models.Model):
    id = models.BigIntegerField(primary_key=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=50)
    isAdmin = models.BooleanField(default=False)
"""
class Account(models.Model):
    number = models.AutoField(primary_key=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    lastChangeDate = models.DateTimeField()
    isActive = models.BooleanField(default=True)
    user = models.ForeignKey(Customer, related_name='account', on_delete=models.CASCADE)