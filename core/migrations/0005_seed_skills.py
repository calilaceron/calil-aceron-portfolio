from django.db import migrations

SKILLS = [
    # Languages
    {"name": "Python", "category": "Languages", "order": 1},
    {"name": "Java", "category": "Languages", "order": 2},
    {"name": "JavaScript", "category": "Languages", "order": 3},
    {"name": "SQL", "category": "Languages", "order": 4},
    {"name": "HTML5 / CSS3", "category": "Languages", "order": 5},
    {"name": "C / C++", "category": "Languages", "order": 6},

    # Frameworks & Tools
    {"name": "Django", "category": "Frameworks & Tools", "order": 1},
    {"name": "React", "category": "Frameworks & Tools", "order": 2},
    {"name": "Next.js", "category": "Frameworks & Tools", "order": 3},
    {"name": "Android Studio & SDK", "category": "Frameworks & Tools", "order": 4},
    {"name": "Git & GitHub", "category": "Frameworks & Tools", "order": 5},
    {"name": "PostgreSQL", "category": "Frameworks & Tools", "order": 6},
    {"name": "SQLite", "category": "Frameworks & Tools", "order": 7},
    {"name": "Tailwind CSS", "category": "Frameworks & Tools", "order": 8},
    {"name": "Vercel & Railway", "category": "Frameworks & Tools", "order": 9},

    # Concepts
    {"name": "Object-Oriented Programming (OOP)", "category": "Concepts", "order": 1},
    {"name": "Enterprise Systems", "category": "Concepts", "order": 2},
    {"name": "RESTful APIs", "category": "Concepts", "order": 3},
    {"name": "Machine Learning & Neural Networks", "category": "Concepts", "order": 4},
    {"name": "Data Analysis & Statistics", "category": "Concepts", "order": 5},
    {"name": "Responsive Web Design", "category": "Concepts", "order": 6},

    # Soft Skills
    {"name": "Research & Methodology", "category": "Soft Skills", "order": 1},
    {"name": "Technical Documentation", "category": "Soft Skills", "order": 2},
    {"name": "Problem Solving", "category": "Soft Skills", "order": 3},
    {"name": "Team Collaboration", "category": "Soft Skills", "order": 4},
    {"name": "Project Management", "category": "Soft Skills", "order": 5},
]


def seed(apps, schema_editor):
    Skill = apps.get_model("core", "Skill")
    for item in SKILLS:
        Skill.objects.update_or_create(
            name=item["name"],
            category=item["category"],
            defaults={"order": item["order"]},
        )


def unseed(apps, schema_editor):
    Skill = apps.get_model("core", "Skill")
    names = [item["name"] for item in SKILLS]
    Skill.objects.filter(name__in=names).delete()


class Migration(migrations.Migration):
    dependencies = [("core", "0004_seed_projects")]
    operations = [migrations.RunPython(seed, unseed)]
