from django.db import models

# Create your models here.



class Admin(models.Model):
   admin_id = models.AutoField(primary_key=True , default=1)
   staff_id = models.CharField(max_length=255)
   admin_password = models.CharField(max_length=255)

class User(models.Model):
      user_id = models.AutoField(primary_key=True)
      full_name = models.CharField(max_length=150, unique=True)
      student_id = models.CharField(max_length=50, unique=True)
      password = models.CharField(max_length=255)
      

class UserItemReservation(models.Model):
     reserve_id = models.AutoField(primary_key=True)
     user_id = models.ForeignKey(User , on_delete=models.CASCADE)
     item_id = models.ForeignKey('Item' , on_delete=models.CASCADE)
     deadline_time = models.DateField()

class RequestItem(models.Model):
      request_id = models.AutoField(primary_key=True)
      user_id = models.ForeignKey(User , on_delete=models.CASCADE)
      item_name = models.CharField(max_length=100)
      item_amount = models.IntegerField()
      time_requested = models.TextField(null=True, blank=True)
      request_date = models.DateField()
      status = models.CharField(max_length=20, default='Pending')
      admin_id = models.ForeignKey(Admin , on_delete=models.CASCADE , default=1)


   

class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=100 , default="")
    item_amount = models.IntegerField()
    admin_id = models.ForeignKey(Admin , on_delete=models.CASCADE)
    

    def __str__(self):
     return f"{self.item_name} ({self.item_amount})"