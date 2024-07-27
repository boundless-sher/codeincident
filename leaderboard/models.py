from django.db import models

# Create your models here.
class Leaderboard(models.Model):
    handle = models.CharField(max_length=100)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
      return f'{self.handle} - {self.score}'
    
    class Meta:
        ordering = ['-score', 'created_at']