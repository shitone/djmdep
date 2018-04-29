from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=64, unique=True, db_index=True)
    truename = models.CharField(max_length=64)
    department = models.IntegerField()
    phone = models.CharField(max_length=20)
    areacode = models.IntegerField()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['truename', 'department', 'phone']

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username

    def verify_password(self, password):
        return self.password == password


class UserManager(BaseUserManager):
    def create_user(self, username, password, truename, department, phone, areacode):
        user = self.model(
            username=username,
            password=password,
            truename=truename,
            department=department,
            phone=phone,
            areacode=areacode,
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, truename, department, phone, areacode):
        user = self.model(
            username=username,
            password=password,
            truename=truename,
            department=department,
            phone=phone,
            areacode=areacode,
        )
        user.save(using=self._db)
        return user


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    province = models.CharField(max_length=16)
    role = models.IntegerField()

    class Meta:
        db_table = "departments"