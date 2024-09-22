from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class CustomUser(AbstractUser):
    user_type_data=((1,"HOD"), (2, "Trainer"), (3, "Customer"))
    user_type=models.CharField(default=1, choices=user_type_data, max_length=50)

class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Trainer(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender=models.CharField(max_length=255)
    phoneno=models.CharField(max_length=255)
    profile_pic=models.FileField()
    address=models.TextField()
    price=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Customer(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender=models.CharField(max_length=255)
    phoneno=models.CharField(max_length=255)
    profile_pic=models.FileField()
    address=models.TextField()
    height=models.FloatField()
    weight=models.FloatField()
    age=models.IntegerField()
    bicepsize=models.FloatField()
    chestsize=models.FloatField()
    legsize=models.FloatField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class CustomerDue(models.Model):
    id=models.AutoField(primary_key=True)
    trainer_id=models.ForeignKey(Trainer, on_delete=models.CASCADE, default=1)
    customer_id=models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    session_start_date=models.DateField()
    session_end_date=models.DateField()
    amount=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Event(models.Model):
    id=models.AutoField(primary_key=True)
    event_name=models.CharField(max_length=255)
    event_date=models.DateField()
    event_description=models.TextField()
    amount=models.CharField(max_length=255)
    total_participation=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class EventParticipation(models.Model):
    id=models.AutoField(primary_key=True)
    event_id=models.ForeignKey(Event, on_delete=models.CASCADE, default=1)
    participator=models.CharField(max_length=255)
    amount=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class CustomerLeave(models.Model):
    id=models.AutoField(primary_key=True)
    customer_id=models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    trainer_id=models.ForeignKey(Trainer, on_delete=models.CASCADE, default=1)
    start_date=models.DateField()
    end_date=models.DateField()
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Messages(models.Model):
    id=models.AutoField(primary_key=True)
    end_date=models.DateField()
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type==2:
            Trainer.objects.create(admin=instance,address="",profile_pic="",gender="", price="", phoneno="")
        if instance.user_type==3:
            Customer.objects.create(admin=instance,address="",profile_pic="",gender="", height=0.0, weight=0.0, age=0, phoneno="", bicepsize=0.0, chestsize=0.0, legsize=0.0)

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    if instance.user_type==2:
        instance.trainer.save()
    if instance.user_type==3:
        instance.customer.save()
