from django.db import models


class AllSessions(models.Model):
    session_id = models.CharField(max_length=5)
    session_name = models.TextField(null=True,default=None)
    session_year = models.IntegerField(null=True,default=None)
    session_sequence = models.IntegerField(null=True,default=None)

    class Meta:
        ordering = ["session_year","session_sequence"]
