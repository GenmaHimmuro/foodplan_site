from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodplan_site', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DietInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(choices=[('classic', 'Классическое'), ('low_carb', 'Низкоуглеводное'), ('vegetarian', 'Вегетарианское'), ('keto', 'Кето')], max_length=50, unique=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name': 'Тип меню (описание)',
                'verbose_name_plural': 'Типы меню (описания)',
            },
        ),
    ]

