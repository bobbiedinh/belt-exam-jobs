# Generated by Django 2.2 on 2020-02-21 20:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobsapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='employee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='jobsapp.User'),
        ),
    ]