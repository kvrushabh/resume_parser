from django.shortcuts import render, redirect
from .models import Resume
from .forms import ResumeUploadForm
from .utils import parse_resume

def upload_resume(request):
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            resume_obj = form.save(commit=False)
            resume_obj.save()

            # Parse the resume using Pyresparser
            parsed_data = parse_resume(resume_obj.file.path)

            # Save parsed data to the model
            resume_obj.name = parsed_data.get("Name", "")
            resume_obj.email = parsed_data.get("Email", "")
            resume_obj.phone = parsed_data.get("Phone", "")
            resume_obj.skills = ", ".join(parsed_data.get("Skills", []))  # Safely handle skills
            resume_obj.education = ", ".join(parsed_data.get("Education", []))  # Safely handle education
            resume_obj.experience = parsed_data.get("Experience", 0)  # Default experience to 0 if not present

            # Handle the case where Companies Worked might be None or not a list
            companies_worked = parsed_data.get("Companies Worked", [])
            if isinstance(companies_worked, list):  # Only join if it's a list
                resume_obj.companies_worked = ", ".join(companies_worked)
            else:
                resume_obj.companies_worked = ""

            resume_obj.location = parsed_data.get("Location", "")
            resume_obj.save()

            return redirect('resume_list')
    else:
        form = ResumeUploadForm()
    return render(request, 'resumes/upload.html', {'form': form})



def resume_list(request):
    resumes = Resume.objects.all()

    # Dynamic filtering
    experience = request.GET.get('experience')
    skills = request.GET.get('skills')
    education = request.GET.get('education')
    certifications = request.GET.get('certifications')
    location = request.GET.get('location')

    if experience:
        resumes = resumes.filter(experience__gte=int(experience))
    if skills:
        skills_list = skills.split(',')
        for skill in skills_list:
            resumes = resumes.filter(skills__icontains=skill.strip())
    if education:
        resumes = resumes.filter(education__icontains=education)
    if certifications:
        certifications_list = certifications.split(',')
        for cert in certifications_list:
            resumes = resumes.filter(certifications__icontains=cert.strip())
    if location:
        resumes = resumes.filter(location__icontains=location)

    return render(request, 'resumes/list.html', {'resumes': resumes})
