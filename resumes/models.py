from django.db import models

class Resume(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    experience = models.IntegerField(blank=True, null=True)  # Total years of experience
    skills = models.TextField(blank=True, null=True)  # Comma-separated list of skills
    education = models.TextField(blank=True, null=True)  # Highest education degree
    job_title = models.CharField(max_length=255, blank=True, null=True)  # Last job title
    companies_worked = models.TextField(blank=True, null=True)  # Companies worked at (comma-separated)
    certifications = models.TextField(blank=True, null=True)  # Certifications (comma-separated)
    location = models.CharField(max_length=255, blank=True, null=True)  # Location (city, country)
    Languages = models.TextField(blank=True, null=True)  # Languages (comma-separated)
    file = models.FileField(upload_to='resumes/')  # Resume file

    def __str__(self):
        return self.name if self.name else "Unnamed"

