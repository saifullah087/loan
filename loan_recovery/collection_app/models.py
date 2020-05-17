from django.db import models
from django.forms import ModelForm

# Create your models here.

class Students(models.Model):
    student_number = models.IntegerField(primary_key=True)
    f_name = models.CharField(max_length=20, blank=True, null=True)
    l_name = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    address = models.CharField(max_length=144, blank=True, null=True)
    county = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=45, blank=True, null=True)
    email = models.CharField(max_length=45, blank=True, null=True)
    gpa = models.IntegerField(blank=True, null=True)
    #course_code = models.ForeignKey(Courses, models.DO_NOTHING, db_column='course_code', blank=True, null=True)
    #college = models.ForeignKey(Colleges, models.DO_NOTHING, blank=True, null=True)
    passwords = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        db_table = 'students'


class Article(models.Model):
    title =models.CharField(max_length=100)
    author=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    date =models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ArticleS'

class Blog(models.Model):
    title =models.CharField(max_length=100)
    author=models.CharField(max_length=100)

    class Meta:
        db_table = 'Blog'