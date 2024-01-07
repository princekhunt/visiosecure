from django.db import models

# Create your models here.

class Unlockers(models.Model):
    name = models.CharField(max_length=100, default="Unknown")
    photo_id = models.CharField(max_length=100, default="Unknown")
    image = models.ImageField(upload_to="unlockers", default="unlockers/default.png")

    def __str__(self):
        return self.name
    
class TAccessCodes(models.Model):
    #link jobs
    access_code = models.CharField(max_length=100, default="Unknown")
    jobid = models.IntegerField(default=0)
    name = models.CharField(max_length=100, default="Unknown")
    active = models.BooleanField(default=False)
    success = models.IntegerField(default=-1)


    def __str__(self):
        return self.access_code


class jobs(models.Model):
    status = models.BooleanField(default=False)
    jobid = models.IntegerField(default=0)
    access_code = models.CharField(max_length=100, default="Unknown")
    job = models.IntegerField(default=-1)

    def __str__(self):
        return str(self.jobid)
    
class RandomFacts(models.Model):
    fact = models.CharField(max_length=100, default="Unknown")

    def __str__(self):
        return self.fact
    
class TRegistration(models.Model):
    name = models.CharField(max_length=100, default="Unknown")
    photo_id = models.CharField(max_length=100, default="Unknown")
    image = models.TextField(default="Unknown")

    def __str__(self):
        return self.name
    
class All_logs(models.Model):
    name = models.CharField(max_length=100, default="Unknown")
    success = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=100, default="Unknown")
    image = models.TextField(default="Unknown")

    def __str__(self):
        return self.name
    
class access_code(models.Model):
    code = models.CharField(max_length=100, default="Unknown")
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.code