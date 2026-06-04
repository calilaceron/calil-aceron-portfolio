from django.db import migrations

BULLETS = [
    "Co-authored a published study on chord-enabled keyboard acceptance conducted through "
    "Mapua University's Research Learning and Immersion Program (ILRAD, 2023).",
    "Applied a Random Forest Classifier and Neural Network ensemble on 9,900 data points; "
    "identified usage behavior as the most influential adoption factor among ten latent variables.",
    "Contributed across all major research phases: conceptualization, methodology design, "
    "data collection and analysis.",
]


def seed(apps, schema_editor):
    Publication = apps.get_model('core', 'Publication')
    Publication.objects.create(
        title=(
            'Evaluation of preceding variables affecting behavioral use and acceptance '
            'of chord-enabled keyboard among students'
        ),
        role='Research Author — Scopus-Indexed Publication (2023)',
        journal='Computers in Human Behavior Reports, Elsevier-ScienceDirect',
        metrics='Impact Factor: 4.9 | CiteScore: 7.8',
        year=2024,
        description=BULLETS,
        link='https://doi.org/10.1016/j.chbr.2024.100482',
        order=1,
    )


def unseed(apps, schema_editor):
    apps.get_model('core', 'Publication').objects.filter(order=1).delete()


class Migration(migrations.Migration):
    dependencies = [('core', '0002_publication')]
    operations   = [migrations.RunPython(seed, unseed)]
