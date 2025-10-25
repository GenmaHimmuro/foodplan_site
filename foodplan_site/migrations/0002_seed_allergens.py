from django.db import migrations


ALLERGENS = [
    ('seafood', 'Рыба и морепродукты'),
    ('meat', 'Мясо'),
    ('grains', 'Зерновые'),
    ('bee_products', 'Продукты пчеловодства'),
    ('nuts', 'Орехи и бобовые'),
    ('milk', 'Молочные продукты'),
]


def seed_allergens(apps, schema_editor):
    Allergen = apps.get_model('foodplan_site', 'Allergen')
    for code, _ in ALLERGENS:
        Allergen.objects.get_or_create(code=code)


def unseed_allergens(apps, schema_editor):
    Allergen = apps.get_model('foodplan_site', 'Allergen')
    codes = [c for c, _ in ALLERGENS]
    Allergen.objects.filter(code__in=codes).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('foodplan_site', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_allergens, unseed_allergens),
    ]

