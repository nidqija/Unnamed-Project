from django.db import models

# Create your models here.



class Admin(models.Model):
   admin_id = models.AutoField(primary_key=True , default=1)
   admin_name = models.CharField(max_length=255)
   admin_email = models.EmailField(unique=True)
   admin_password = models.CharField(max_length=255)




class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=100 , default="")
    item_amount = models.IntegerField()
    admin_id = models.ForeignKey(Admin , on_delete=models.CASCADE)
    

    def __str__(self):
     return f"{self.item_name} ({self.item_amount})"