from django.db import models
from django.contrib.auth.models import User

import uuid
class Vendor(models.Model):
    name=models.CharField(max_length=50)
    contact_details= models.TextField()
    address= models.TextField() 
    vendor_code= models.UUIDField(default=uuid.uuid4, editable=False)
    on_time_delivery_rate= models.FloatField(null=True,blank=True)
    quality_rating_avg= models.FloatField(null=True,blank=True)
    average_response_time= models.FloatField(null=True,blank=True)
    fulfillment_rate = models.FloatField(null=True,blank=True)


    def  __str__(self):
        return self.name 
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vendor = models.OneToOneField(Vendor, on_delete=models.CASCADE)    



  
STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    )
class PurchaseOrder(models.Model):
    po_number= models.UUIDField(default=uuid.uuid4, editable=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField( auto_now_add=True)
    delivery_date=models.DateTimeField( blank=True,null=True)
    items=models.JSONField()
    quantity=models.IntegerField(blank=True,null=True)
    status=models.CharField(choices=STATUS_CHOICES,default='pending', max_length=50)
    quality_rating=models.FloatField(blank=True,null=True)
    issue_date=models.DateTimeField(blank=True,null=True)
    acknowledgment_date=models.DateTimeField(blank=True,null=True)


    
class HistoryPerfomence(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)
    on_time_delivery_rate = models.FloatField(null=True,blank=True)
    quality_rating_avg = models.FloatField(null=True,blank=True)
    average_response_time=models.DurationField(null=True,blank=True)
    fulfillment_rate = models.FloatField(null=True,blank=True)

    

    
    

    

    
