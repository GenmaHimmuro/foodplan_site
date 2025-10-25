from django.db import migrations


PRICES = {
    'breakfast': {1: 100, 3: 200, 6: 300, 12: 400},
    'lunch':     {1: 300, 3: 600, 6: 900, 12: 1200},
    'dinner':    {1: 200, 3: 400, 6: 600, 12: 800},
    'dessert':   {1: 100, 3: 200, 6: 300, 12: 400},
}


def seed_pricerules(apps, schema_editor):
    PriceRule = apps.get_model('subscription', 'PriceRule')
    for dish_type, durations in PRICES.items():
        for duration, price in durations.items():
            PriceRule.objects.get_or_create(
                dish_type=dish_type,
                duration=duration,
                defaults={'price': price},
            )


def unseed_pricerules(apps, schema_editor):
    PriceRule = apps.get_model('subscription', 'PriceRule')
    filters = []
    for dish_type, durations in PRICES.items():
        for duration in durations.keys():
            filters.append({'dish_type': dish_type, 'duration': duration})
    for f in filters:
        PriceRule.objects.filter(**f).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_pricerules, unseed_pricerules),
    ]

