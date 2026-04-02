from django.db import models
from django.contrib.auth.models import User

# Disease Model
class Disease(models.Model):
    name = models.CharField(max_length=100)
    symptoms = models.TextField()
    description = models.TextField()
    precaution = models.TextField()

    def __str__(self):
        return self.name


# Patient History Model
class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symptoms = models.TextField()
    prediction = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.prediction}"
