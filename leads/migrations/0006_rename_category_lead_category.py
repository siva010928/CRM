# Generated by Django 4.1 on 2022-08-29 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0005_category_lead_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lead',
            old_name='Category',
            new_name='category',
        ),
    ]
