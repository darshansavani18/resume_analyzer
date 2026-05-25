from django.db import models

class Resume(models.Model):
    file = models.FileField(upload_to='resumes/')
    extracted_text = models.TextField(blank=True, null=True)
    field_scores = models.JSONField(blank=True, null=True, default=dict)  # Store scores for all fields
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name