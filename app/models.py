# In your Django app's models.py file

from django.db import models

class WheelSpecification(models.Model):
    
    form_number = models.CharField(max_length=255, unique=True, db_index=True)
    submitted_by = models.CharField(max_length=255)
    submitted_date = models.DateField()

    # The 'fields' object from the JSON is stored in a single JSONField.
    fields = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        String representation of the model, useful for the Django admin interface.
        """
        return f"Wheel Spec Form: {self.form_number}"

    class Meta:
        # Optional: Defines metadata for the model.
        verbose_name = "Wheel Specification"
        verbose_name_plural = "Wheel Specifications"
        ordering = ['-submitted_date'] # Orders records by submission date by default.

