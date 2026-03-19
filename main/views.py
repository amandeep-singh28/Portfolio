from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    Profile, SkillCategory, Project, Experience,
    Education, Certificate, Achievement, OpenSource, ContactMessage
)


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


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        if name and email and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message
            )

        # You can configure Django email settings and enable this
        # send_mail(
        #     subject=f'Portfolio Contact: {name}',
        #     message=f'From: {email}\n\n{message}',
        #     from_email=settings.DEFAULT_FROM_EMAIL,
        #     recipient_list=['amandeep87557@gmail.com'],
        # )

        return JsonResponse({'status': 'success', 'message': 'Message sent!'})
    return JsonResponse({'status': 'error'}, status=400)
