from django.db import models
from django.contrib.auth.models import User
from .utils import generate_ref_code

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recommended_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rec_to", blank=True, null=True) #CASCADE is not ideal
    code = models.CharField(max_length=12, blank=True)
    is_blood_bank = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} : {self.code}"

    def get_recommended_profile(self):
        pass

    def save(self, *args, **kwargs):
        if self.code == "":
            code = generate_ref_code()
            self.code = code
        super().save(*args, **kwargs)

GENDER_CHOICES = (
         
        ("Male","Male"),("Female","Female"),("Other","Other")
    
    )



class Reciver(models.Model):
  
  number = models.CharField(max_length=10,null=True,default="")
  gender = models.CharField(max_length=20, choices=GENDER_CHOICES,null=True,default="")
  age = models.IntegerField(null=True,default="") 
  bldgrp = models.CharField(max_length=4,null=True,default="")
  address = models.CharField(max_length=100,null=True,default="")
  user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)

class extendeduser(models.Model):
  
  number = models.CharField(max_length=10,null=True,default="")
  gender = models.CharField(max_length=20, choices=GENDER_CHOICES,null=True,default="")
  age = models.IntegerField(null=True,default="") 
  bldgrp = models.CharField(max_length=4,null=True,default="")
  address = models.CharField(max_length=100,null=True,default="")
  user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.user.first_name}"