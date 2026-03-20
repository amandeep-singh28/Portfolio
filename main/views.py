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
from django.views.decorators.csrf import csrf_exempt


def index(request):
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

@csrf_exempt
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        if name and email and message:
            try:
                # 1. Save to DB
                ContactMessage.objects.create(
                    name=name,
                    email=email,
                    message=message
                )

                # 2. Extract explicit target email
                target_email = os.environ.get(
                    'CONTACT_EMAIL',
                    settings.EMAIL_HOST_USER
                )
                if not target_email:
                    target_email = 'amandeepsingh892333@gmail.com'

                # 3. Bypass Render SMTP Block using FormSubmit
                import requests
                response = requests.post(
                    f"https://formsubmit.co/ajax/{target_email}",
                    data={
                        "_subject": f"New Portfolio Message from {name}",
                        "name": name,
                        "email": email,
                        "message": message,
                    },
                    headers={
                        'Accept': 'application/json'
                    },
                    timeout=10 # Prevents Gunicorn from timing out and crashing!
                )

                if response.status_code != 200:
                    raise Exception(f"FormSubmit failed with status {response.status_code}: {response.text}")

                return JsonResponse({
                    'status': 'success',
                    'message': 'Message sent successfully!'
                })

            except requests.exceptions.Timeout:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Server Error: The email service timed out. Please try again.'
                })
            except Exception as e:
                # This will catch Database errors and FormSubmit connection errors
                return JsonResponse({
                    'status': 'error',
                    'message': f"Server Error: {str(e)}"
                })

        return JsonResponse({
            'status': 'error',
            'message': 'All fields are required'
        })

    return JsonResponse({'status': 'error'}, status=400)