# from django.db import models
# from django.utils import timezone

# class LockCommand(models.Model):
#     port = models.IntegerField(choices=[(1, 'Port 1'), (2, 'Port 2')])
#     password = models.CharField(max_length=20)
#     confirm_password = models.CharField(max_length=20)
#     confirmed = models.BooleanField(default=False)
#     created_at = models.DateTimeField(default=timezone.now)

#     def command_string(self):
#         return f"open{self.port}" if self.confirmed else ""

#     def __str__(self):
#         return f"Lock {self.port} - {'Confirmed' if self.confirmed else 'Pending'}"


# models.py
from django.db import models
from django.utils import timezone

class LockCommand(models.Model):
    port = models.CharField(max_length=5)
    password = models.CharField(max_length=50)
    confirm_password = models.CharField(max_length=50)
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def command_string(self):
        return f"open{self.port}"
