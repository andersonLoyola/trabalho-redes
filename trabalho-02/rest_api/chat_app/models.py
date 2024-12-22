from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class AccountsConnection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connections')
    connection_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Connection {self.connection_id} for {self.user.username}"