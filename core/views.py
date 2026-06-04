from django.shortcuts import render
from django.http import JsonResponse
from .models import Skill, Project, Publication


def index(request):
    return render(request, 'core/index.html')


def skills_api(request):
    grouped = {}
    for skill in Skill.objects.all():
        grouped.setdefault(skill.category, []).append(skill.name)
    return JsonResponse(grouped)


def projects_api(request):
    projects = list(Project.objects.values(
        'title', 'description', 'tech_stack', 'github_url', 'live_url'
    ))
    return JsonResponse(projects, safe=False)


def publications_api(request):
    pubs = list(Publication.objects.values(
        'title', 'role', 'journal', 'metrics', 'year', 'description', 'link'
    ))
    return JsonResponse(pubs, safe=False)
