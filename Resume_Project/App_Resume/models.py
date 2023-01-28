from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class StudentForm(models.Model):
    # user = models.ForeignKey(User,models.CASCADE)
    file = models.FileField() # for creating file input  

# class Meta:  
#     db_table = "student"