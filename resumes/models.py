from django.db import models

class Resume(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    experience = models.IntegerField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    companies_worked = models.TextField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    Languages = models.TextField(blank=True, null=True) 
    file = models.FileField(upload_to='resumes/')
    updated_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name if self.name else "Unnamed"

