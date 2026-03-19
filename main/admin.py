from django.contrib import admin
from .models import (
    Profile, SkillCategory, Skill, Project, ProjectImage, Experience,
    Education, Certificate, Achievement, OpenSource, ContactMessage
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'title', 'email']


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 3


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'order']
    inlines = [SkillInline]


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 3
    fields = ['image', 'order']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'featured', 'order', 'start_date']
    list_editable = ['featured', 'order']
    inlines = [ProjectImageInline]


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['role', 'company', 'exp_type', 'duration', 'order']
    list_editable = ['order']


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['degree', 'institution', 'duration', 'order']
    list_editable = ['order']


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['name', 'platform', 'date', 'order']
    list_editable = ['order']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'order']
    list_editable = ['order']


@admin.register(OpenSource)
class OpenSourceAdmin(admin.ModelAdmin):
    list_display = ['repo_name', 'prs_merged', 'stars', 'order']
    list_editable = ['order']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at']
    readonly_fields = ['name', 'email', 'message', 'created_at']