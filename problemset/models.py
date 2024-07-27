from django.db import models

# Create your models here.
class Problem(models.Model):
    title = models.CharField(max_length=100)
    statement = models.TextField()
    sample_input = models.TextField()
    sample_output = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    correct_output = models.TextField()

    def __str__(self):
        return self.title


class UserProblem(models.Model):
    user = models.TextField()
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user_output = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.user + ' - ' + self.problem.title

    def save(self, *args, **kwargs):
        if self.user_output == self.problem.correct_output:
            self.is_correct = True
        super(UserProblem, self).save(*args, **kwargs)
