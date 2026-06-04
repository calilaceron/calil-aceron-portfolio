from django.db import models


class Skill(models.Model):
    LANGUAGES = 'Languages'
    FRAMEWORKS = 'Frameworks & Tools'
    CONCEPTS = 'Concepts'
    SOFT_SKILLS = 'Soft Skills'
    CATEGORY_CHOICES = [
        (LANGUAGES, 'Languages'),
        (FRAMEWORKS, 'Frameworks & Tools'),
        (CONCEPTS, 'Concepts'),
        (SOFT_SKILLS, 'Soft Skills'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['category', 'order', 'name']

    def __str__(self):
        return f'{self.category} — {self.name}'


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tech_stack = models.JSONField(default=list)
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class Publication(models.Model):
    title       = models.CharField(max_length=300)
    role        = models.CharField(max_length=200)
    journal     = models.CharField(max_length=200)
    metrics     = models.CharField(max_length=100, blank=True)
    year        = models.PositiveIntegerField()
    description = models.JSONField(
        default=list,
        help_text='JSON array of bullet-point strings, e.g. ["First point.", "Second."]',
    )
    link        = models.URLField(blank=True)
    order       = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-year', 'title']

    def __str__(self):
        return self.title
