from django.db import migrations

PROJECTS = [
    {
        "title": "MerchMob",
        "description": "An Android merchandising app that allows users to sell and buy products, built for CSCI 181.04: Special Topics in Android Development.",
        "tech_stack": ["Java", "Android Studio", "Android SDK"],
        "github_url": "https://github.com/calilaceron/MerchMob",
        "live_url": "",
        "order": 1,
    },
    {
        "title": "Common Grounds",
        "description": "A full-featured web platform built with Django for community networking, events, and shared spaces.",
        "tech_stack": ["Python", "Django", "SQLite"],
        "github_url": "https://github.com/calilaceron/commongrounds",
        "live_url": "http://165.245.191.223/",
        "order": 2,
    },
    {
        "title": "Learn 2 Dev",
        "description": "A collaborative web application developed for Learn 2 Dev Group 3 with interactive user workflows.",
        "tech_stack": ["React", "Next.js", "JavaScript", "Vercel"],
        "github_url": "https://github.com/calilaceron/learn2dev26-project-group3",
        "live_url": "https://learn2dev26-project-group3.vercel.app",
        "order": 3,
    },
    {
        "title": "Calil Aceron Portfolio",
        "description": "Personal developer portfolio built with Django, dynamic React frontend, Tailwind CSS, and content managed through Django Admin.",
        "tech_stack": ["Django", "Python", "React", "PostgreSQL", "Tailwind CSS"],
        "github_url": "https://github.com/calilaceron/calil-aceron-portfolio",
        "live_url": "https://calil-aceron.up.railway.app/",
        "order": 4,
    },
    {
        "title": "Academic Climb",
        "description": "A Java application designed to help students track and progress through academic milestones and goals.",
        "tech_stack": ["Java", "OOP"],
        "github_url": "https://github.com/calilaceron/Academic-Climb",
        "live_url": "",
        "order": 5,
    },
    {
        "title": "Modern Landing Page",
        "description": "A responsive, modern product landing page featuring clean semantics and mobile-first responsive design.",
        "tech_stack": ["HTML5", "CSS3", "Responsive Design"],
        "github_url": "https://github.com/calilaceron/landing-page",
        "live_url": "https://calilaceron.github.io/landing-page/index.html#",
        "order": 6,
    },
    {
        "title": "Coffee Machine Simulator",
        "description": "An interactive coffee machine simulation program in Python managing resources, coin processing, and drink brewing.",
        "tech_stack": ["Python", "OOP"],
        "github_url": "https://github.com/calilaceron/CoffeeMachine",
        "live_url": "",
        "order": 7,
    },
]


def seed(apps, schema_editor):
    Project = apps.get_model("core", "Project")
    for item in PROJECTS:
        Project.objects.update_or_create(
            title=item["title"],
            defaults=item,
        )


def unseed(apps, schema_editor):
    Project = apps.get_model("core", "Project")
    titles = [item["title"] for item in PROJECTS]
    Project.objects.filter(title__in=titles).delete()


class Migration(migrations.Migration):
    dependencies = [("core", "0003_seed_publication")]
    operations = [migrations.RunPython(seed, unseed)]
