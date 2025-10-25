from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0003_subscription_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='persons',
            field=models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество персон'),
        ),
    ]

