from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0004_subscription_persons'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscription',
            name='description',
        ),
    ]

