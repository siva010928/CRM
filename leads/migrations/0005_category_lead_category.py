# Generated by Django 4.1 on 2022-08-29 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0004_lead_organization_alter_lead_agent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leads.userprofile')),
            ],
        ),
        migrations.AddField(
            model_name='lead',
            name='Category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='leads.category'),
        ),
    ]