from django.db import models


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
      return_date = models.DateField(null=True, blank=True)
      actual_return_date = models.DateField(null=True, blank=True)

class RequestVenue(models.Model):
      request_id = models.AutoField(primary_key=True)
      user_id = models.ForeignKey(User , on_delete=models.CASCADE)
      venue_name = models.CharField(max_length=100)
      time_requested = models.TextField(null=True, blank=True)
      request_date = models.DateField()
      status = models.CharField(max_length=20, default='Pending')
      admin_id = models.ForeignKey(Admin , on_delete=models.CASCADE , default=1)
      return_date = models.DateField(null=True, blank=True)
      actual_return_date = models.DateField(null=True, blank=True)



class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_name = models.CharField(max_length=100 , default="")
    item_amount = models.IntegerField()
    admin_id = models.ForeignKey(Admin , on_delete=models.CASCADE)
    

    def __str__(self):
     return f"{self.item_name} ({self.item_amount})"

class Lab(models.Model):
    lab_id = models.AutoField(primary_key=True)
    lab_name = models.CharField(max_length=100, default="")
    location = models.CharField(max_length=255, blank=True, null=True)
    capacity = models.IntegerField(default=1)
    admin_id = models.ForeignKey(Admin, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.lab_name} ({self.location})"

class Material(models.Model):
    material_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    isbn = models.CharField(max_length=50, blank=True, null=True)
    admin_id = models.ForeignKey(Admin, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.author or 'Unknown'}"

class Bookmark(models.Model):
    bookmark_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    material_id = models.ForeignKey(Material, on_delete=models.CASCADE)
    date_bookmarked = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user_id', 'material_id')
    
    def __str__(self):
        return f"{self.user_id.full_name} bookmarked {self.material_id.title}"

class Fine(models.Model):
    fine_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    request_item = models.ForeignKey(RequestItem, on_delete=models.CASCADE, null=True, blank=True)
    request_venue = models.ForeignKey(RequestVenue, on_delete=models.CASCADE, null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fine_reason = models.CharField(max_length=255, default='Overdue return')
    issue_date = models.DateField(auto_now_add=True)
    paid_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, default='Unpaid')
    
    def __str__(self):
        item_type = "Item" if self.request_item else "Venue"
        return f"Fine for {self.user_id.full_name} - {item_type} - ${self.fine_amount}"