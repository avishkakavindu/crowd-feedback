# Generated by Django 4.2.4 on 2023-08-29 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_feedback_is_feedback_positive_alter_feedback_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='current_crowd',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='shop',
            name='max_crowd',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
