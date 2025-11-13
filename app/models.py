from django.db import models
import os

# Create your models here.

class StudentModel(models.Model):
    firstname =  models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    rollid = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    dept = models.CharField(max_length=100)
    sem = models.CharField(max_length=100)
    contact = models.IntegerField()
    address = models.CharField(max_length=100)
    dateofbirth = models.DateField()
    profile = models.FileField(upload_to=os.path.join('static', 'Student'),default='No Profile')
    desc = models.CharField(max_length=100,default='No Description')
    status = models.CharField(max_length=100, default='Approved')
    s1 = models.CharField(max_length=100,null=True)
    s1 = models.CharField(max_length=100,null=True)
    s1 = models.CharField(max_length=100,null=True)
    s3 = models.CharField(max_length=100,null=True)
    s4 = models.CharField(max_length=100,null=True)
    s5 = models.CharField(max_length=100,null=True)
    otp =  models.IntegerField(null=True)

    def __str__(self):
        return self.firstname + ' ' + self.lastname

    class Meta:
        db_table = "StudentModel"


class FacultyModel(models.Model):
    firstname =  models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    empid = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    dept = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    contact = models.IntegerField()
    address = models.CharField(max_length=100)
    profile = models.FileField(upload_to=os.path.join('static', 'Faculty'),default='No Profile')
    desc = models.CharField(max_length=100,default='No Description')
    status = models.CharField(max_length=100, default='Approved')
    otp =  models.IntegerField(null=True)
    
    def __str__(self):
        return self.firstname + ' ' + self.lastname

    class Meta:
        db_table = "FacultyModel"


class WorkShopModel(models.Model):
    workshopname = models.CharField(max_length=100)
    workshopdate = models.DateTimeField()
    workshopimage = models.FileField(upload_to=os.path.join('static', 'Workshop'))
    workshopfiles = models.FileField(upload_to=os.path.join('static', 'WorkshopFiles'))
    dept = models.CharField(max_length=100)
    sem = models.CharField(max_length=100)

    def __str__(self):
        return self.workshopname
    
    class Meta:
        db_table = "WorkshopModel"


class AttendanceModel(models.Model):
    firstname =  models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    date = models.DateField(max_length=100)
    rollid = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    dept = models.CharField(max_length=100)
    sem = models.CharField(max_length=100)
    contact = models.IntegerField()
    subject = models.CharField(max_length=100)
    attendance = models.CharField(max_length=100, default='Absent')
    ffname = models.CharField(max_length=100)
    flname = models.CharField(max_length=100)

    def __str__(self):
        return self.firstname+ ' ' +self.lastname
    
    class Meta:
        db_table = "AttendanceModel"






class StudentMarksModel(models.Model):
    firstname =  models.CharField(max_length=100,null=True)
    lastname = models.CharField(max_length=100,null=True)
    email = models.EmailField(max_length=100)
    date = models.DateField(max_length=100)
    rollid = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    dept = models.CharField(max_length=100)
    sem = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    test1 = models.IntegerField()
    test2 = models.IntegerField()
    mid = models.IntegerField()
    finalsem = models.IntegerField()
    total = models.IntegerField(null=True)
    percentage = models.IntegerField(null=True)

    def __str__(self):
        return self.email
    class Meta:
        db_table = "StudentMarksModel"

