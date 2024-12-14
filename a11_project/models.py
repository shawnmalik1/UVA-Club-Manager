from django.forms import models
from django.db import models
from django.contrib.auth.models import User




class CheckIn(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1) #fixed
    def __str__(self):

        return self.user.username

class Event(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=200)
    date = models.DateField()  # Make sure 'date' is a DateField
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    members = models.ManyToManyField(User, related_name='events', blank=True)
    member_requests = models.ManyToManyField(User, related_name='requested_events', blank=True)
    document = models.FileField()


    def __str__(self):
        return self.title

class Club(models.Model):
    id = models.BigAutoField(primary_key=True)  # Explicitly using BigAutoField
    name = models.CharField(max_length=255)
    description = models.TextField()
    points = models.IntegerField(default=0)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='clubs', default=1)

    def __str__(self):
        return self.name

    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_pma_administrator = models.BooleanField(default=False)
    points = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.user.username} Profile"
    
class Suggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    suggestion_text = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Suggestion by {self.user.username} at {self.submitted_at}"

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    keywords = models.CharField(max_length=500)
    file = models.FileField(upload_to='projects/')
    timestamp = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, related_name='uploaded_files', on_delete=models.CASCADE, null=True, blank=True)


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='projects/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    timestamp = models.DateTimeField(auto_now_add=True)

#This was meant for the live chat feature
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username}: {self.content[:20]}"

class Budget(models.Model):
    total_budget = models.DecimalField(max_digits=7, decimal_places=2, default=500.00)

    def __str__(self):
        return f"Total Budget: {self.total_budget}"
    
    @classmethod
    def get_instance(cls):
        obj, created = cls.objects.get_or_create(id=1)
        return obj
    
class Expenditure(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Expenditure by {self.user.username} - {self.amount}"