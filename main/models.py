from django.db import models


class Profile(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    bio = models.TextField()
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    resume = models.FileField(upload_to='resume/', blank=True)
    profile_photo = models.ImageField(upload_to='photos/', blank=True)
    cgpa = models.CharField(max_length=10, blank=True)
    career_goal = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Profile"


class SkillCategory(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10, blank=True)  # emoji
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']


class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tech_stack = models.CharField(max_length=500)  # comma-separated
    github_link = models.URLField(blank=True)
    live_link = models.URLField(blank=True)
    image = models.ImageField(upload_to='projects/', blank=True)
    start_date = models.CharField(max_length=50, blank=True)
    end_date = models.CharField(max_length=50, blank=True)
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    def tech_list(self):
        return [t.strip() for t in self.tech_stack.split(',')]

    def all_images(self):
        imgs = list(self.extra_images.all())
        if self.image:
            class MainImg:
                def __init__(self, url): self.url = url
            imgs.insert(0, type('Img', (), {'image': type('F', (), {'url': self.image.url})()})())
        return imgs

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='extra_images')
    image = models.ImageField(upload_to='projects/')
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.project.title} — image {self.order}"

    class Meta:
        ordering = ['order']


class Experience(models.Model):
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    duration = models.CharField(max_length=100)
    exp_type = models.CharField(max_length=50, choices=[
        ('Internship', 'Internship'),
        ('Freelance', 'Freelance'),
        ('Part-time', 'Part-time'),
        ('Full-time', 'Full-time'),
        ('Summer Training', 'Summer Training'),
    ])
    tech_stack = models.CharField(max_length=300, blank=True)
    responsibilities = models.TextField()
    order = models.IntegerField(default=0)

    def responsibilities_list(self):
        return [r.strip() for r in self.responsibilities.split('\n') if r.strip()]

    def __str__(self):
        return f"{self.role} @ {self.company}"

    class Meta:
        ordering = ['order']


class Education(models.Model):
    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=200)
    location = models.CharField(max_length=100, blank=True)
    duration = models.CharField(max_length=100)
    score = models.CharField(max_length=50, blank=True)
    score_label = models.CharField(max_length=20, default='CGPA')
    relevant_courses = models.CharField(max_length=500, blank=True)
    order = models.IntegerField(default=0)

    def courses_list(self):
        return [c.strip() for c in self.relevant_courses.split(',') if c.strip()]

    def __str__(self):
        return f"{self.degree} — {self.institution}"

    class Meta:
        ordering = ['order']


class Certificate(models.Model):
    name = models.CharField(max_length=200)
    platform = models.CharField(max_length=100)
    date = models.CharField(max_length=50)
    domain = models.CharField(max_length=100, blank=True)
    link = models.URLField(blank=True)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']


class Achievement(models.Model):
    title = models.CharField(max_length=300)
    date = models.CharField(max_length=50, blank=True)
    icon = models.CharField(max_length=10, default='🏆')
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']


class OpenSource(models.Model):
    repo_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    link = models.URLField(blank=True)
    prs_merged = models.IntegerField(default=0)
    stars = models.IntegerField(default=0)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.repo_name

    class Meta:
        ordering = ['order']


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.email}"

    class Meta:
        ordering = ['-created_at']