from django.db import models
from django.conf import settings  # to reference the AUTH_USER_MODEL


class TestInfo(models.Model):
    group = models.CharField(max_length=50, blank=True)
    test_code = models.CharField(max_length=50, unique=True)
    test_name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50, blank=True)
    normal_range = models.TextField(blank=True)
    description = models.TextField(blank=True)

    # Example cost field:
    test_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
           ordering = ['id']  # or any other field you want to order by

    def __str__(self):
        return f"{self.test_name} ({self.test_code})"
    


class FavoriteTestGroup(models.Model):
    """
    Allows each user to create multiple "favorite test groups."
    E.g., "My Routine Panel," "Pediatrics Panel," etc.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorite_test_groups'
    )
    group_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    # Many-to-many relationship to the LabTest model
    tests = models.ManyToManyField(TestInfo, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'group_name')  
        # ensures a user doesn't create multiple favorite groups with exactly the same name
        ordering = ['group_name']

    def __str__(self):
        return f"{self.group_name} ({self.user.username})"
