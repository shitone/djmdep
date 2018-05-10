from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


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
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=64, unique=True, db_index=True)
    truename = models.CharField(max_length=64)
    department = models.IntegerField()
    phone = models.CharField(max_length=20)
    areacode = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['truename', 'department', 'phone']

    class Meta:
        db_table = "users"

    def get_short_name(self):
        return self.truename

    def get_full_name(self):
        return self.truename

    def __str__(self):
        return self.username

    def verify_password(self, password):
        return self.password == password

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    province = models.CharField(max_length=16)
    role = models.IntegerField()

    class Meta:
        db_table = "departments"