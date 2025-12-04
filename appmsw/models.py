from django.db import models
from django.contrib.auth.models import User
#from django.utils.translation import ugettext_lazy as _  replace to gettext_lazy
#https://stackoverflow.com/questions/70656495/importerror-cannot-import-name-ugettext-lazy
from django.utils.translation import gettext_lazy as _

categorys = [
    ("systems", "Systems Parameters Integrations"),
    ("app", "Application Parameters"),
    ("sidemenu", "Side Menu"),
    ("topmenu", "Top Menu"),
    ("prj", "Project"),
]

class Param(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=30, choices=categorys, default='app')
    desc = models.CharField(max_length=1000, default = '', blank=True, null=True)
    option = models.CharField(max_length=1000, default='', blank=True, null=True)
    json = models.TextField(max_length=75000, default='{}', blank=True, null=True)
    value = models.TextField(max_length=32000, default='', blank=True, null=True)
    creation_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             blank=True, null=True)
    public=models.BooleanField(default=True)
    enabled=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name},{self.category},{self.desc}, {self.json}"
 
    def __repr__(self):
        return f"{self.name}, {self.category},{self.desc}"

class DbConnection(models.Model):
    """Модель для хранения подключений к различным базам данных"""
    DATABASE_TYPES = [
        ('postgresql', 'PostgreSQL'),
        ('oracle', 'Oracle'),
        ('iris', 'IRIS'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Название подключения')
    database_type = models.CharField(max_length=20, choices=DATABASE_TYPES, verbose_name='Тип базы данных')
    connection_string = models.CharField(max_length=500, verbose_name='Строка подключения JDBC')
    username = models.CharField(max_length=100, verbose_name='Имя пользователя')
    password = models.CharField(max_length=200, verbose_name='Пароль', blank=True)
    description = models.TextField(max_length=1000, blank=True, verbose_name='Описание')
    is_active = models.BooleanField(default=True, verbose_name='Активно')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Пользователь')
    
    class Meta:
        verbose_name = 'Подключение к БД'
        verbose_name_plural = 'Подключения к БД'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.get_database_type_display()})"
    
    def __repr__(self):
        return f"{self.name}, {self.database_type}"

class Comment(models.Model):
   text = models.TextField(max_length=2000)
   creation_date = models.DateTimeField(auto_now=True)
   author = models.ForeignKey(to=User, on_delete=models.CASCADE)
   param = models.ForeignKey(to=Param, on_delete=models.CASCADE, related_name='comments')
   img = models.ImageField(upload_to="images", null=True, blank=True, verbose_name='Image')
   file = models.FileField(upload_to="files", null=True, blank=True, verbose_name='File')

   def __str__(self):
        return f"{self.text}, {self.author}"


class SysOption(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=30, choices=categorys, default='app', blank=True, null=True)
    desc = models.CharField(max_length=1000, default='', blank=True, null=True)
    option = models.CharField(max_length=1000, default='', blank=True, null=True)
    json = models.TextField(max_length=75000, default='{}', blank=True, null=True)
    value = models.TextField(max_length=32000, default='', blank=True, null=True)
    creation_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             blank=True, null=True)
    public=models.BooleanField(default=True)
    enabled=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name},{self.category},{self.desc}, {self.json}"

    def __repr__(self):
        return f"{self.name}, {self.category},{self.desc}"