# Generated by Django 3.2 on 2022-03-17 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='message',
            new_name='comment',
        ),
    ]
