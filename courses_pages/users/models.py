
# Django
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# This is for our token authentication
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver 
from rest_framework.authtoken.models import Token

#models



class MyUserManager(BaseUserManager):
    def create_user(self,email, first_name, last_name, born_date, password=None):
        """
            Creates and saves an user with the given email and password.
        """

        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
        if not born_date:
            raise ValueError('Users must have a date of birth')


        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            born_date=born_date,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name, last_name, born_date, password):
        """
            creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            first_name=first_name,
            last_name=last_name,
            born_date=born_date,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Role(models.Model):
    roleid = models.AutoField(primary_key=True, db_column='roleid')
    name = models.CharField(max_length=100, db_column='name')

    class Meta:
        db_table = 'public"."roles'
    
    def __str__(self):
        return self.name

class Country(models.Model):
    country_code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Phone(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='phones')
    number = models.CharField(max_length=15)
    class Meta:
        db_table = 'public"."phones'

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    born_date = models.DateField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Many-to-many linking User and Role through UserRole
    # Many-to-many linking User and Role through UserRole
    roles = models.ManyToManyField(
        Role,
        through='UserRole',
        related_name='users'
    )

    country = models.ForeignKey(Country, on_delete=models.PROTECT, related_name='user',blank=True, null=True, verbose_name='pais de residencia')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'born_date']

    objects = MyUserManager()

    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
  
    class Meta:
        db_table = 'public"."users'



class UserRole(models.Model):
    # Link to custom User model via AUTH_USER_MODEL so Django recognizes the FK
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_roles',
        on_delete=models.CASCADE,
        db_column='userid',
    )
    role = models.ForeignKey(
        Role,
        related_name='role_users',
        on_delete=models.CASCADE,
        db_column='roleid'
    )

    class Meta:
        db_table = 'public"."user_roles'
        unique_together = ('user', 'role')

    def __str__(self):
        return f"{self.user.email} → {self.role.name}"
        
        
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False,**kwargs):
    """
        The token authentication works by exchanging email and password 
        for a token that will be used in all subsequent requests so to identify 
        the user on the server side.
    """

    #if User object it's create, insert and save in the data base, we gona generate a token
    if created:  
        Token.objects.create(user=instance)