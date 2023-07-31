from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

User = settings.AUTH_USER_MODEL


#Custom Manager del usuario
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Introduce una direccion de correo electrónico')
        if not password:
            raise ValueError('Introduce una contraseña')
        
        email = self.normalize_email(email)
        user = self.model(email=email,username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username,password=None):        
        user = self.create_user(email, username, password)
        user.admin = True
        user.save(using=self._db)
        return user

#USUARIO
class User(AbstractBaseUser, PermissionsMixin):

    user_id = models.AutoField(primary_key=True)
    email = models.EmailField(
        verbose_name='email address', 
        max_length=30,
        unique=True
    )
    username = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        #¿Tiene el usuario un permiso especifico?
        #Por defecto: si, siempre
        return True
    
    def has_module_perms(self, app_label):
        #Tiene el usuario permiso para ver la app 'app_label
        #por defecto: si, siempre
        return True
    
    @property
    def is_admin(self):
        return self.admin
    
    objects = UserManager()

###ALOJAMIENTO
class Stay(models.Model):

    stay_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    url = models.TextField()
    location = models.TextField(default=None)
    polarity = models.FloatField(null=True, blank=True, default=None)

    #Cada usuario puede acceder a todos los alojamientos disponibles
    #user = models.ManyToManyField(User,blank=True)

    def __str__(self):
        return self.name
    

#REVIEW
class Review(models.Model):

    id_review = models.CharField(max_length=20, primary_key=True) 
    costumer_name =  models.CharField(max_length=40) 
    nationality = models.CharField(max_length=60)                
    comment = models.TextField()
    room_type = models.CharField(max_length=70)
    number_nights = models.CharField(max_length=50)
    date_review = models.CharField(max_length=40)
    date_entry = models.CharField(max_length=40)
    client_type = models.CharField(max_length=50)
    polarity = models.FloatField(null=True, blank=True, default=None)
    stay_id = models.ForeignKey('Stay', on_delete= models.CASCADE)

    def __str__(self):
        return self.id_review


#PALABRA CLAVE
class Keyword(models.Model):

    keyword_id = models.AutoField(primary_key=True)
    word = models.CharField(max_length=20, unique = True)
    polarity = models.FloatField()
    frecuency = models.IntegerField()
    id_review = models.ForeignKey('Review', on_delete= models.CASCADE)
    
    def __str__(self):
        return self.word








    
    
         
    
    