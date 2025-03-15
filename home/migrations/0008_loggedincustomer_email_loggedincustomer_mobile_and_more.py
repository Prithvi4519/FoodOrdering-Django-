# Generated by Django 4.1.5 on 2025-02-27 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_loggedincustomer'),
    ]

    operations = [
        migrations.AddField(
            model_name='loggedincustomer',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
        migrations.AddField(
            model_name='loggedincustomer',
            name='mobile',
            field=models.CharField(default=0, max_length=15),
        ),
        migrations.AddField(
            model_name='loggedincustomer',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
    ]
