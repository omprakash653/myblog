from django.db import models

# Create your models here.
class Contact(models.Model):
    sno = models.AutoField(primary_key=True) #primary key optional write or not
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=14)
    email = models.CharField(max_length=80)
    content = models.TextField()
    timeStamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'message from ' + self.name

