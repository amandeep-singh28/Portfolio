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
            # Save to DB
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message
            )

            try:
                # 🔥 Explicit email (no confusion)
                target_email = os.environ.get(
                    'CONTACT_EMAIL',
                    settings.EMAIL_HOST_USER
                )

                send_mail(
                    subject=f"New Portfolio Message from {name}",
                    message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[target_email],
                    fail_silently=False,
                )

                return JsonResponse({
                    'status': 'success',
                    'message': 'Message sent successfully!'
                })

            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': str(e)
                })

        return JsonResponse({
            'status': 'error',
            'message': 'All fields are required'
        })

    return JsonResponse({'status': 'error'}, status=400)