import os
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    Profile, SkillCategory, Project, Experience,
    Education, Certificate, Achievement, OpenSource, ContactMessage
)


# 🔥 AUTO SETUP (TEMPORARY)
def setup_data():
    # Create admin
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@gmail.com', 'admin123')

    # Create profile (only if empty)
    if not Profile.objects.exists():
        Profile.objects.create(
            name="Amandeep Singh",
            title="Aspiring Data Scientist",
            bio="Passionate about data, ML, and building impactful projects.",
            email="amandeep87557@gmail.com",
            phone="8923337768",
            location="Punjab, India",
            cgpa="8.1"
        )


def index(request):
    # setup_data()   # 🔥 IMPORTANT (temporary)

    profile = Profile.objects.first()
    skill_categories = SkillCategory.objects.prefetch_related('skills').all()
    projects = Project.objects.all()
    experiences = Experience.objects.all()
    educations = Education.objects.all()
    certificates = Certificate.objects.all()
    achievements = Achievement.objects.all()
    open_source = OpenSource.objects.all()

    context = {
        'profile': profile,
        'skill_categories': skill_categories,
        'projects': projects,
        'experiences': experiences,
        'educations': educations,
        'certificates': certificates,
        'achievements': achievements,
        'open_source': open_source,
    }

    return render(request, 'main/index.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        if name and email and message:
            # 1. Save it to Database (Admin panel)
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message
            )

            # 2. Send Email Notification
            try:
                subject = f"New Portfolio Message from {name}"
                body = f"You received a new message from your portfolio website:\n\nName: {name}\nEmail: {email}\n\nMessage:\n{message}"
                
                # Send from the EMAIL_HOST_USER to the EMAIL_HOST_USER
                send_mail(
                    subject,
                    body,
                    settings.EMAIL_HOST_USER, 
                    [os.environ.get('CONTACT_EMAIL', settings.EMAIL_HOST_USER)],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Failed to send email: {e}")

        return JsonResponse({'status': 'success', 'message': 'Message sent!'})

    return JsonResponse({'status': 'error'}, status=400)