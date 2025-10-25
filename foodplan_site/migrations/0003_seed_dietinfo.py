from django.db import migrations


def seed_dietinfo(apps, schema_editor):
    DietInfo = apps.get_model('foodplan_site', 'DietInfo')
    items = [
        ('classic', 'Классическое меню', ''),
        ('low_carb', 'Низкоуглеводное меню', ''),
        ('vegetarian', 'Вегетарианское меню', ''),
        ('keto', 'Кето меню', ''),
    ]
    for code, title, description in items:
        DietInfo.objects.get_or_create(code=code, defaults={'title': title, 'description': description})


def unseed_dietinfo(apps, schema_editor):
    DietInfo = apps.get_model('foodplan_site', 'DietInfo')
    DietInfo.objects.filter(code__in=['classic', 'low_carb', 'vegetarian', 'keto']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('foodplan_site', '0002_dietinfo'),
    ]

    operations = [
        migrations.RunPython(seed_dietinfo, unseed_dietinfo),
    ]

