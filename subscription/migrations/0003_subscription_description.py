from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0002_seed_pricerules'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
    ]

