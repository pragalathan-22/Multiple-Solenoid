

from django.db import models

class LockCommand(models.Model):
    port = models.IntegerField()
    password = models.CharField(max_length=100)
    intime = models.DateTimeField(auto_now_add=True)
    opentime = models.DateTimeField(null=True, blank=True)
    outtime = models.DateTimeField(null=True, blank=True)
    out_opened = models.BooleanField(default=False)

    def __str__(self):
        return f"Port {self.port} | Started: {self.intime} | Closed: {self.outtime}"
