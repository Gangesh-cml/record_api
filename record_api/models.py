from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model

class record(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def clean(self):
        # Ensure title is not empty
        if not self.title:
            raise ValidationError("Title cannot be empty.")

        # Ensure title is unique for each user
        existing_records_with_title = record.objects.filter(user=self.user, title=self.title)
        if self.pk:  # Skip this check for new records (during creation).
            existing_records_with_title = existing_records_with_title.exclude(pk=self.pk)

        if existing_records_with_title.exists():
            raise ValidationError("Title must be unique for each user.")
